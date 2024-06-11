import numpy as np
import torch
import pickle
from transformers import BertForSequenceClassification, BertTokenizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

# 加载Naive Bayes模型
with open(r'F:\TrainClassfier\src\NBProcess\naive_bayes_model.pkl', 'rb') as f:
    nb_model = pickle.load(f)

# 加载微调的BERT模型
tokenizer = BertTokenizer.from_pretrained(r'F:\TrainClassfier\bert-base-cased')
bert_model = BertForSequenceClassification.from_pretrained(r'F:\TrainClassfier\my_classifier11_model')
bert_model.eval()

# 加载数据
with open(r'F:\TrainClassfier\src\NBProcess\all_info_data_set.txt', 'r') as f:
    lines = f.readlines()

# 读取和处理数据
X_combined = []
y = []

for line in lines:
    parts = line.strip().split(' ,')
    text = parts[0]
    nb_features = list(map(int, parts[1].strip('[]').split(',')))
    label = int(parts[-1].strip('[').strip(']').split(',')[-1])
    print(nb_features)
    print(label)

    input_ids = tokenizer(text, return_tensors="pt", padding=True, truncation=True)['input_ids']
    bert_outputs = bert_model(input_ids)['logits'].detach().numpy()[0]

    nb_pred = nb_model.predict_proba([nb_features[:-1]])[0][1]  # 取正类的概率

    combined_features = [bert_outputs[1], nb_pred]  # 取正类的概率或决策函数值
    X_combined.append(combined_features)
    y.append(label)

X_combined = np.array(X_combined)
y = np.array(y)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.2, random_state=42)

# 集成BERT和Naive Bayes模型
def ensemble_predict(X):
    combined_pred = []
    for features in X:
        bert_pred = features[0]
        nb_pred = features[1]
        ensemble_prob = (bert_pred + nb_pred) / 2  # 权重都为1/2
        combined_pred.append(1 if ensemble_prob >= 0.5 else 0)
    return np.array(combined_pred)

# 评估集成模型性能
predictions = ensemble_predict(X_test)
accuracy = accuracy_score(y_test, predictions)
report = classification_report(y_test, predictions)

print("测试集准确率:", accuracy)
print("测试集分类报告：\n", report)

# 保存集成模型和预测函数
ensemble_model = {
    'bert_model': bert_model,
    'nb_model': nb_model,
    'tokenizer': tokenizer,
    'predict_function': ensemble_predict
}

with open('ensemble_model_with_equal_weights.pkl', 'wb') as f:
    pickle.dump(ensemble_model, f)

print("模型已保存。")
