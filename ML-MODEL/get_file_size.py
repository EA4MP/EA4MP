# 选取文件的大小作为评价标准之一，依据：恶意包的总是倾向于使用更轻量化的大小来引诱用户下载

# 将包的大小按照以下标准进行区分：
# 0-100KB：0
# 100KB-1MB：1
# 1MB-5MB：2
# 5MB-10MB：3
# 10MB-∞：4
import os


def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size


def get_file_size(file_path):
    """
    获取文件大小
    :param file_path: 文件路径
    :return: 文件大小
    """
    if not os.path.exists(file_path):
        return False
    file_size = get_folder_size(file_path)
    print(file_size/1024)
    if file_size <= 100 * 1024:
        return 1
    elif file_size <= 1024 * 1024:
        return 2
    elif file_size <= 5 * 1024 * 1024:
        return 3
    elif file_size <= 10 * 1024 * 1024:
        return 4
    else:
        return 5


file_path = "F:\javademo1"
# get_file_size(file_path)
print(get_file_size(file_path))
