def compare_files(file1_path, file2_path):
    # �򿪲���ȡ�ļ�����
    with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='gbk') as file2:
        lines_file1 = file1.readlines()
        lines_file2 = file2.readlines()

    # ͳ���ļ�����
    num_lines = min(len(lines_file1), len(lines_file2))

    # ��ʼ��������
    total_line_matches = 0
    total_char_matches = 0

    # �Ƚ�ÿһ��
    for line1, line2 in zip(lines_file1, lines_file2):
        line1 = line1.strip()  # �Ƴ���ĩβ�Ļ��з��Ϳհ��ַ�
        line2 = line2.strip()

        # ���������ƶ�
        if line1 == line2:
            total_line_matches += 1

        # �����ַ����ƶ�
        char_matches = sum(a == b for a, b in zip(line1, line2))
        total_char_matches += char_matches

    # �������
    line_accuracy = total_line_matches / num_lines if num_lines > 0 else 0
    char_accuracy = total_char_matches / sum(len(line) for line in lines_file1)

    return line_accuracy, char_accuracy

if __name__ == "__main__":
    file1_path = "../data/std_output.txt"
    file2_path = "../data/output.txt"

    line_accuracy, char_accuracy = compare_files(file1_path, file2_path)

    print("Line Accuracy: {:.2f}%".format(line_accuracy * 100))
    print("Character Accuracy: {:.2f}%".format(char_accuracy * 100))
