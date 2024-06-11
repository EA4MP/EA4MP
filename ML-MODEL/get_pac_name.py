import re

# 示例列表，包含需要处理的字符串
strings = [
    "algoGUI-0.1.0",
    "aliyun-python-sdk-domain-intl-1.0.0",
    "anotherTool-1.2.3",
    "yetAnother-0.0.1-beta",
    "justAName"
]


# 使用正则表达式匹配并去除最后一个版本号
def remove_last_version_info(s):
    # 匹配最后一个连字符及其后面的所有字符
    match = re.search(r'-(\d+\.\d+\.\d+)$', s)
    if match:
        # 使用空字符串替换匹配到的版本号
        return re.sub(r'-(\d+\.\d+\.\d+)$', '', s)
    return s


# 对列表中的每个字符串应用函数
processed_strings = [remove_last_version_info(s) for s in strings]

print(processed_strings)
