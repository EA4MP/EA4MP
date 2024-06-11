import ast


def parse_line(line):
    # 根据逗号和空格分割数据
    parts = line.split(' ,')
    # 第一部分是代码序列，包含CLS和SEP
    code_sequence = parts[0]
    # 第二部分是特征向量
    feature_vector_str = ast.literal_eval(parts[1])
    feature_vector = feature_vector_str[:-1]
    # 第三部分提取最后一个数字作为标签
    label = feature_vector_str[-1]
    # print(feature_vector)
    # print(label)
    # 将特征向量转换为整数列表
    # feature_vector = list(map(int, feature_vector_str.split()[:-1]))
    return code_sequence, feature_vector, label


# line = "[CLS]<builtin>.print <call>.1inch-8.6.setup.run setuptools.setup(.1inch-8.6.setup.run): subprocess.Popen read[SEP] ,[0,6,3,2,2,0,1,1,1,0,0]"
# code_sequence, feature_vector, label = parse_line(line)
# print(code_sequence)
# print(feature_vector)
# print(label)
