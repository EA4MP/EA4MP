# 本部分用来验证包名相似度
import pandas as pd
import os

def damerau_levenshtein_distance(s1, s2):
    """
    计算两个字符串之间的Damerau-Levenshtein距离
    """
    len_s1, len_s2 = len(s1), len(s2)
    d = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]

    for i in range(len_s1 + 1):
        d[i][0] = i
    for j in range(len_s2 + 1):
        d[0][j] = j

    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            d[i][j] = min(
                d[i - 1][j] + 1,  # deletion
                d[i][j - 1] + 1,  # insertion
                d[i - 1][j - 1] + cost,  # substitution
            )
            if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
                d[i][j] = min(d[i][j], d[i - 2][j - 2] + cost)  # transposition

    return d[len_s1][len_s2]


def similarity_score(s1, s2):
    """
    计算两个字符串之间的相似度分数
    """
    distance = damerau_levenshtein_distance(s1, s2)
    max_length = max(len(s1), len(s2))
    similarity = 1 - distance / max_length
    return similarity


def calculate_similarity(popular_packages, target_package):
    max_similarity = 0
    for package in popular_packages:
        similarity = similarity_score(package, target_package)
        max_similarity = max(max_similarity, similarity)

    print(max_similarity)
    if max_similarity < 0.1:
        return 0
    elif max_similarity < 0.2:
        return 1
    # Add more conditions as needed
    elif max_similarity < 0.3:
        return 2
    elif max_similarity < 0.4:
        return 3
    elif max_similarity < 0.5:
        return 4
    elif max_similarity < 0.6:
        return 5
    elif max_similarity < 0.7:
        return 6
    elif max_similarity < 0.8:
        return 7
    elif max_similarity < 0.9:
        return 8
    else:
        return 9


