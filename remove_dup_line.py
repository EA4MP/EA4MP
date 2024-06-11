import os

# Remove duplicate rows from a collection
def remove_duplicates(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    unique_lines = []
    seen_lines = set()

    for line in lines:
        if line not in seen_lines:
            unique_lines.append(line)
            seen_lines.add(line)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(unique_lines)


pac_path = r''
try:
    for file_name in os.listdir(pac_path):
        file_path_1 = os.path.join(pac_path, file_name, "dfs_out.txt")
        if os.path.exists(file_path_1):
            remove_duplicates(file_path_1)
            print(f"{file_name} dfs done!")
except Exception as e:
    print(file_name + e)


