from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn.metrics import classification_report
import pickle


# 加载数据集
def load_data(file_path):
    data = []
    labels = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                vector = list(map(int, line[1:-1].split(', ')))
                data.append(vector[:-1])  # 特征向量
                labels.append(vector[-1])  # 标签
    return np.array(data), np.array(labels)


# 载入数据
benign_data, benign_labels = load_data(r'F:\TrainClassfier\src\NBProcess\Metadata-feature-extraction\ben-feature.txt')
malicious_data, malicious_labels = load_data(r'F:\TrainClassfier\src\NBProcess\Metadata-feature-extraction\mal-feature.txt')

# 合并两个数据集
all_data = np.vstack((benign_data, malicious_data))
all_labels = np.hstack((benign_labels, malicious_labels))

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(all_data, all_labels, test_size=0.2, random_state=42)

# 创建并训练朴素贝叶斯分类器
classifier = GaussianNB()
classifier.fit(X_train, y_train)

with open('naive_bayes_model.pkl', 'wb') as file:
    pickle.dump(classifier, file)

# 在测试集上进行预测
y_pred = classifier.predict(X_test)

# 计算准确率
accuracy = accuracy_score(y_test, y_pred)
print("准确率:", accuracy)
report = classification_report(y_test, y_pred)
print("分类报告：\n", report)
