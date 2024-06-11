import os
import re
pattern = r'\/.*\.py'

def process_files(file1_path, file2_path):
    # 1. 读取并处理1.txt文件
    processed_lines = []
    with open(file1_path, 'r') as f1:
        lines = f1.readlines()
        for line in lines:
            line = line.strip()
            if line and not line.endswith(":"):
                line = line.replace(".........DataSet.dcp_malSample", "")
                processed_line = re.sub(pattern, "", line)
                processed_lines.append(processed_line)
        data = "".join(processed_lines)
    # print("data:", data)
    # 2. 读取2.txt文件，将数组元素以逗号分隔并合并为单行字符串
    with open(file2_path, 'r') as f2:
        array_data = f2.read()
        vector_str = "".join(array_data.split())
        # print("vector_str:", vector_str)
    # 3. 将处理后的两段字符串拼接在一起，确保在同一行
    combined_data = "[CLS]" + data + "[SEP]" + " ," + vector_str
    # print("combined_data:", combined_data)

    return combined_data


folder_path = r"/home/banxiangao/Desktop/DataSet/dcp_malSample"
for file_name in os.listdir(folder_path):
    if os.path.isdir(os.path.join(folder_path, file_name)):
        print(f"start to ex pac {file_name} info!")
        seq_file_path = os.path.join(folder_path, file_name, "dfs_out.txt")
        vec_file_path = os.path.join(folder_path, file_name, "feature_vec.txt")
        combined_data = process_files(seq_file_path, vec_file_path)
        with open('all_info_data_set.txt', 'a', encoding="utf-8") as output_file:
            output_file.write(combined_data)
            output_file.write("\n")
        with open(os.path.join(folder_path, file_name, "con_info.txt"), "w", encoding="utf-8") as file:
            file.write(combined_data)

        print("success wirte the info you want!")

#
# file1_path = "dfs_out.txt"
# file2_path = "feature_vec.txt"
#
# combined_data = process_files(file1_path, file2_path)
# # print(combined_data)
# print("success wirte the info you want!")
