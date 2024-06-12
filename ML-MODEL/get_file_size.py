
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


file_path = ""
# get_file_size(file_path)
print(get_file_size(file_path))
