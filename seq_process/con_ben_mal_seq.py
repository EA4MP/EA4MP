def merge_text_files(file1_path, file2_path, output_path):
    # 打开第一个文件并读取内容
    with open(file1_path, 'r', encoding='utf-8') as file1:
        file1_content = file1.read()

    # 打开第二个文件并读取内容
    with open(file2_path, 'r', encoding='utf-8') as file2:
        file2_content = file2.read()

    # 将两个文件的内容合并
    merged_content = file1_content + '\n' + file2_content

    # 将合并后的内容写入新文件
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(merged_content)


# 指定两个输入文件和输出文件的路径
file1_path = r'F:\TrainClassfier\datasets\ben\ben_bfs.txt'
file2_path = r'F:\TrainClassfier\datasets\mal\mal_bfs.txt'
output_path = r'F:\TrainClassfier\datasets\train.txt'

# 合并两个文件
merge_text_files(file1_path, file2_path, output_path)

print("文件合并完成。")
