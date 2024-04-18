import json
from collections import Counter
import re
import os

# ��ȡ���ı��ļ���GBK���룩
def read_text_file(filename):
    data = []
    with open(filename, 'r', encoding='gbk') as file:
        for line in file:
            # ����ÿ�е�JSON����
            entry = json.loads(line)
            data.append(entry)
    return data

# ��ȡ�ı��еĵ������ֳ��ֵĴ���
def get_character_count_from_text(data):
    character_count = Counter()
    for entry in data:
        # ��ȡ���������
        title = entry.get('title', '')
        html = entry.get('html', '')
        # ��ϱ��������
        text = title + ' ' + html
        # ʹ��������ʽ��ȡ�����ַ�
        chinese_characters = re.findall(r'[\u4e00-\u9fa5]', text)
        # ͳ�Ƶ������ֳ��ֵĴ���
        character_count.update(chinese_characters)
    return character_count

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

# ����������ͳ�ƽ����ƴ������
def group_by_character_pinyin(character_count, pinyin_dict):
    grouped_result = {}
    for character, count in character_count.items():
        pinyin = find_pinyin(character, pinyin_dict)
        if pinyin:
            if pinyin not in grouped_result:
                grouped_result[pinyin] = {"words": [], "counts": []}
            grouped_result[pinyin]["words"].append(character)
            grouped_result[pinyin]["counts"].append(count)
    return grouped_result

# ���ݺ��ֲ���ƴ��
def find_pinyin(character, pinyin_dict):
    for pinyin, characters in pinyin_dict.items():
        if character in characters:
            return pinyin
    return None

# ָ���洢�����JSON�ļ���
output_json_file = '1_word.txt'

# ָ������txt�ļ����ļ���·��
folder_path = './training_set'

# ��ȡ�ļ���������txt�ļ���·��
txt_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.txt')]

# ��������txt�ļ���ͳ�Ƶ������ֳ��ֵĴ���
total_character_count = Counter()
for txt_file in txt_files:
    data = read_text_file(txt_file)
    character_count = get_character_count_from_text(data)
    total_character_count.update(character_count)

# ��ȡƴ��-���ֶ��ձ�
pinyin_table_file = 'pinyin_table.txt'
pinyin_dict = read_pinyin_table(pinyin_table_file)

# ����������ͳ�ƽ����ƴ������
grouped_result = group_by_character_pinyin(total_character_count, pinyin_dict)

# ������洢ΪJSON��ʹ��UTF-8���룩
with open(output_json_file, 'w', encoding='utf-8') as file:
    json.dump(grouped_result, file, ensure_ascii=False, indent=4)
 
print("success!")