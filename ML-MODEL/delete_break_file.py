import os
import shutil


def is_file_corrupted(file_path):
    try:
        with open(file_path, 'rb') as f:
            f.read()  # 尝试读取文件内容，如果文件损坏可能会抛出异常
    except Exception as e:
        print(f"File {file_path} is corrupted: {e}")
        return True
    else:
        return False


def delete_corrupted_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if is_file_corrupted(file_path):
                print(f"Deleting corrupted file: {file_path}")
                try:
                    shutil.rmtree(file_path)  # 使用shutil.rmtree删除文件或目录
                except Exception as e:
                    print(f"Error deleting file {file_path}: {e}")


# 使用示例
delete_corrupted_files(r'/home/banxiangao/Desktop/DataSet/dcp_malSample')

