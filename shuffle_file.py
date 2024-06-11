import random


def shuffle_lines(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 打乱行
    random.shuffle(lines)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)


# 使用函数
shuffle_lines(r'F:\TrainClassfier\src\test5.txt', r'F:\TrainClassfier\src\test5_shuffle.txt')
