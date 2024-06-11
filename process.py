# 打开文件
with open(r"filtered_data.txt", "r") as file:
    # 逐行读取文件内容
    lines = file.readlines()

# 创建一个空列表，用于存储符合条件的行
filtered_lines = []

# 遍历每一行内容
for line in lines:
    if line.strip():
        # 将每一行内容按照空格进行分割
        parts = line.strip().split(" / ")
        # 获取第二列数据并转换为浮点数
        value = float(parts[1])
        # 如果第二列数据大于0.75，则将该行添加到筛选列表中
        if not value == 1:
            filtered_lines.append(line)

# 输出符合条件的行
for line in filtered_lines:
    print(line.strip())

with open("filtered_data.txt", "w") as output_file:
    # 将筛选后的结果写入新文件
    for line in filtered_lines:
        output_file.write(line)

print("筛选结果已写入到 filtered_data.txt 文件中。")

