import json
from collections import Counter
import re
# -*- coding:utf-8 -*-

import os

# ��ȡ����������ͬʱ���ֵĴ���
def get_adjacent_character_pairs(text):
    # ʹ��������ʽ��ȡ�����ַ�����ȥ���ո�
    chinese_characters = re.findall(r'[\u4e00-\u9fa5]', text.replace(' ', ''))
    # �������������ֵ��б�
    pairs = [chinese_characters[i] + ' ' + chinese_characters[i+1] for i in range(len(chinese_characters) - 1)]
    return pairs

# ��ȡ���ı��ļ���GBK���룩
def read_text_file(filename):
    data = []
    with open(filename, 'r', encoding='gbk') as file:
        for line in file:
            # ����ÿ�е�JSON����
            entry = json.loads(line)
            data.append(entry)
    return data

# ��ȡ�ı��е�����������ͬʱ���ֵĴ���
def get_adjacent_character_pairs_from_text(data):
    pairs_count = Counter()
    for entry in data:
        # ��ȡ���������
        title = entry.get('title', '')
        html = entry.get('html', '')
        # ��ϱ��������
        text = title + ' ' + html
        # ��ȡ����������ͬʱ���ֵĴ���
        pairs = get_adjacent_character_pairs(text)
        # ͳ�ƴ���
        pairs_count.update(pairs)
    return pairs_count

# ��ȡƴ��-���ֶ��ձ�
def read_pinyin_table(filename):
    pinyin_dict = {}
    with open(filename, 'r', encoding='gbk') as file:
        for line in file:
            line = line.strip()
            if line:
                pinyin, characters = line.split(' ', 1)
                pinyin_dict[pinyin] = characters.split()
    return pinyin_dict

# ��ͳ�ƽ�����������ֵ�ƴ������
def group_by_character_pinyin(pairs_count, pinyin_dict):
    grouped_result = {}
    for pair, count in pairs_count.items():
        first_char, second_char = pair.split()
        first_pinyin = find_pinyin(first_char, pinyin_dict)
        second_pinyin = find_pinyin(second_char, pinyin_dict)
        if first_pinyin and second_pinyin:
            pinyin_key = first_pinyin + ' ' + second_pinyin
            if pinyin_key not in grouped_result:
                grouped_result[pinyin_key] = {"words": [], "counts": []}
            grouped_result[pinyin_key]["words"].append(pair)
            grouped_result[pinyin_key]["counts"].append(count)
    return grouped_result

# ���ݺ��ֲ���ƴ��
def find_pinyin(character, pinyin_dict):
    for pinyin, characters in pinyin_dict.items():
        if character in characters:
            return pinyin
    return None

# ָ���洢�����JSON�ļ���
output_json_file = '2_word.txt'

# ָ������txt�ļ����ļ���·��
folder_path = './training_set'

# ��ȡ�ļ���������txt�ļ���·��
txt_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.txt')]

# ��������txt�ļ���ͳ������������ͬʱ���ֵĴ���
total_pairs_count = Counter()
for txt_file in txt_files:
    data = read_text_file(txt_file)
    pairs_count = get_adjacent_character_pairs_from_text(data)
    total_pairs_count.update(pairs_count)

# ��ȡƴ��-���ֶ��ձ�
pinyin_table_file = 'pinyin_table.txt'
pinyin_dict = read_pinyin_table(pinyin_table_file)

# ��ͳ�ƽ�����������ֵ�ƴ������
grouped_result = group_by_character_pinyin(total_pairs_count, pinyin_dict)

# ������洢ΪJSON��ʹ��UTF-8���룩
with open(output_json_file, 'w', encoding='utf-8') as file:
    json.dump(grouped_result, file, ensure_ascii=False, indent=4)
print("success!")
