import difflib
# def calculate_edit_distance(str1, str2):
#     # 计算1-DL距离
#     d = difflib.ndiff(str1, str2)
#     diff_count = sum(1 for i in d if i[0] != ' ')
#     return diff_count


def calculate_similarity(str1, str2):
    # 计算相似度
    diff_count = calculate_edit_distance(str1, str2)
    similarity = 1 - diff_count / max(len(str1), len(str2))
    return similarity


def calculate_edit_distance(str1, str2):
    m, n = len(str1), len(str2)

    # 初始化二维数组dp
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 初始化边界条件
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # 动态规划求解
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1

    return dp[m][n]


def process_line(line_a, lines_b):
    match_found = False
    for line_b in lines_b:
        line_b = line_b.strip()  # 去除行尾的换行符
        # 计算编辑距离和相似度
        # print(line_a)
        if abs(len(line_b) - len(line_a)) < 5:
            # print(line_b)
            edit_distance = calculate_edit_distance(line_a, line_b)
            similarity = calculate_similarity(line_a, line_b)
            if (edit_distance <= 3 and similarity >= 0.5) or similarity >= 0.7:
                print(f"Match found: {line_a} : {line_b}")
                # match_found = True
                break


with open(r'F:\TrainClassfier\src\pac_name_pypi.csv', 'r') as file_a, \
        open(r'F:\TrainClassfier\src\famous.csv', 'r') as file_b:
    lines_a = file_a.readlines()
    lines_b = file_b.readlines()
    for line_a in lines_a:
        line_a = line_a.strip()  # 去除行尾的换行符
        print(line_a)
        process_line(line_a, lines_b)





