import random

# 设定随机种子，确保每次运行的结果一致（可选）
random.seed(45)

# 初始化训练集和测试集
train_lines = []
test_lines = []

# 打开文件并读取所有行
with open(r'F:\TrainClassfier\datasets\train.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 确保数据集行数足够
if len(lines) < 10:
    raise ValueError("数据集行数必须至少为10行")

# 遍历数据集，每十行抽取一行作为测试集
for i in range(0, len(lines), 10):
    # 随机选择一行作为测试集
    test_index = random.randint(0, 9)
    test_line = lines[i + test_index]

    # 将其他行添加到训练集
    train_lines.extend(lines[i:i + 10])
    train_lines.pop(test_index)

    # 将选中的测试行添加到测试集
    test_lines.append(test_line)

# 将训练集和测试集写入不同的文件
with open('train10.txt', 'w', encoding='utf-8') as train_file:
    train_file.writelines(train_lines)

with open('test10.txt', 'w', encoding='utf-8') as test_file:
    test_file.writelines(test_lines)

file.close()
print("数据集已分割完成")
train_file.close()
test_file.close()
print("训练集已写入 train.txt")
print("测试集已写入 test.txt")
