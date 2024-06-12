import ast


def parse_line(line):

    parts = line.split(' ,')

    code_sequence = parts[0]

    feature_vector_str = ast.literal_eval(parts[1])
    feature_vector = feature_vector_str[:-1]

    label = feature_vector_str[-1]

    return code_sequence, feature_vector, label


# line = "[CLS]<builtin>.print <call>.1inch-8.6.setup.run setuptools.setup(.1inch-8.6.setup.run): subprocess.Popen read[SEP] ,[0,6,3,2,2,0,1,1,1,0,0]"
# code_sequence, feature_vector, label = parse_line(line)
# print(code_sequence)
# print(feature_vector)
# print(label)
