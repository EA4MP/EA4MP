import json
import chardet


def metadata_to_json(metadata_text):
    """
    将元数据文本转换为JSON格式的数据

    参数:
    metadata_text (str): 元数据文本字符串，每行为一个键值对

    返回:
    str: 转换后的JSON格式的数据字符串
    """
    # 将字符串按行拆分，并去除空行
    metadata_lines = [line.strip() for line in metadata_text.strip().split("\n")]

    # 创建空字典来存储元数据
    metadata = {}

    # 初始化键和值
    key = None
    value = ""

    # 遍历每一行元数据，解析并添加到字典中
    for line in metadata_lines:
        # 检查当前行是否以空格开头
        if line.startswith(" "):
            # 如果以空格开头，则将其添加到值后面
            value += " " + line.strip()
        else:
            # 如果不以空格开头，则解析键值对并添加到字典中
            if key is not None:
                metadata[key] = value.strip()
                # 检查是否为Description键，如果是，则将后续内容添加到值后面
                if key == "Description":
                    value += " " + line.strip()
            # 解析新的键值对
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
            else:
                # 如果该行没有冒号，则跳过
                continue

    # 处理最后一个键值对
    if key is not None:
        metadata[key] = value.strip()

    # 将元数据转换为JSON格式
    json_data = json.dumps(metadata, indent=4)

    return json_data


# 读取pkg_info文件中的内容，并将内容存到变量metadata_text中
with open("PKG-INFO", "r", encoding="utf-8") as f:
    metadata_text = f.read()
# detected_encoding = chardet.detect(metadata_text)['encoding']
# print(detected_encoding)
json_data = metadata_to_json(metadata_text)
# json_file = json.loads(json_data)

try:
    json_file = json.loads(json_data)
    if "Metadata-Version" in json_file:
        print(json_file["Metadata-Version"])
    else:
        print("no Metadata-Version")
except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format {e}")
