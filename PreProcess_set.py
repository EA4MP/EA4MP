import torch
def preprocess_data(data_path):
    inputs = []
    labels = []

    # 读取数据文件
    with open(data_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            # 分割文本和标签
            parts = line.strip().split(',label:')
            text = parts[0].strip()  # 获取文本部分
            label = int(parts[1].strip())  # 获取标签部分
            inputs.append(text)
            labels.append(label)



    return inputs, labels

# 数据文件路径
data_path = r'F:\TrainClassfier\datasets\train.txt'

# 预处理数据
inputs, labels = preprocess_data(data_path)

print("Inputs:", inputs)
print("Labels:", labels)
