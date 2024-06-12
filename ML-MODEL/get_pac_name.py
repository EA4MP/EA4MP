import re




def remove_last_version_info(s):

    match = re.search(r'-(\d+\.\d+\.\d+)$', s)
    if match:
        return re.sub(r'-(\d+\.\d+\.\d+)$', '', s)
    return s


print(processed_strings)
