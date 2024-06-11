import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split

def read_and_process_file(file_path):
    """
    从指定文件路径读取数据并处理成numpy数组。
    文件每行是一个样本，特征由逗号分隔，最后一列为标签。
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    data = [list(map(int, line.strip().replace('[', '').replace(']', '').split(', '))) for line in lines]
    return np.array(data)

# 读取数据
benign_file_path = 'benign.txt'  # 替换为良性包数据文件路径
malicious_file_path = 'malicious.txt'  # 替换为恶意包数据文件路径

benign_data = read_and_process_file(benign_file_path)
malicious_data = read_and_process_file(malicious_file_path)

# 合并数据
data = np.vstack((benign_data, malicious_data))
X = data[:, :-1]  # 特征向量
y = data[:, -1]  # 标签

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 训练随机森林模型
rf_clf = RandomForestClassifier(random_state=42)
rf_clf.fit(X_train, y_train)

# 预测
y_pred = rf_clf.predict(X_test)

# 评估模型
print("Accuracy:", accuracy_score(y_test, y_pred))
report = classification_report(y_test, y_pred, output_dict=True)
print("Classification Report (micro avg):\n", report['micro avg'])
