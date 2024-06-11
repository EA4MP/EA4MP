import os


def remove_duplicates(file_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 使用集合去除重复行，同时保持原来的顺序
    unique_lines = []
    seen_lines = set()

    for line in lines:
        if line not in seen_lines:
            unique_lines.append(line)
            seen_lines.add(line)

    # 写入去除重复行后的内容到文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(unique_lines)


pac_path = r'F:\weekly_update\dcp_24_04_18'
try:
    for file_name in os.listdir(pac_path):
        file_path_1 = os.path.join(pac_path, file_name, "dfs_out.txt")
        file_path_2 = os.path.join(pac_path, file_name, "bfs_out.txt")
        if os.path.exists(file_path_1):
            remove_duplicates(file_path_1)
            print(f"{file_name} dfs done!")
        if os.path.exists(file_path_2):
            remove_duplicates(file_path_2)
            print(f"{file_name} bfs done!")
except Exception as e:
    print(file_name + e)


