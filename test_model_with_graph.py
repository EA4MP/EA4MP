import torch
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.metrics import roc_curve, precision_recall_curve, auc, classification_report
import matplotlib.pyplot as plt


model_path = r'F:\TrainClassfier\my_classifier15_model'  # 替换为你的模型路径
tokenizer = BertTokenizer.from_pretrained(r"F:\TrainClassfier\bert-base-cased")
model = BertForSequenceClassification.from_pretrained(model_path)
model.eval()  # 设置模型为评估模式
torch.manual_seed(5)
torch.cuda.manual_seed(5)


# 读取测试集并准备输入数据
def prepare_input_data(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    return inputs


# 读取测试集文件
with open(r'F:\TrainClassfier\src\batch5\test5_shuffle5.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 提取文本和标签
texts = []
labels = []
for line in lines:
    # 假设label始终在最后一行且格式为",label: X"
    parts = line.strip().split(',label: ')
    texts.append(parts[0])
    labels.append(int(parts[1]))
count_all = 0
TP = 0
TN = 0
FP = 0
FN = 0
# 使用模型进行预测并获取概率值
probabilities = []
predictions = []
with torch.no_grad():
    for text in texts:
        count_all += 1
        inputs = prepare_input_data(text)
        outputs = model(**inputs)
        logits = outputs.logits
        preds = torch.argmax(logits, dim=-1)
        predictions.append(preds.item())
        print(f"{count_all}:{preds.item()}")
        if preds.item() == 0 and labels[count_all - 1] == 0:
            TN += 1
        if preds.item() == 1 and labels[count_all - 1] == 1:
            TP += 1
        if preds.item() == 0 and labels[count_all - 1] == 1:
            FN += 1
        if preds.item() == 1 and labels[count_all - 1] == 0:
            FP += 1
        # 获取概率值，对于二分类问题，通常使用sigmoid函数
        probs = torch.sigmoid(logits).cpu().numpy()
        probabilities.append(probs[0][1])  # 取正类的概率

# 将标签转换为二进制类标签
binary_labels = [1 if label == 1 else 0 for label in labels]

# 计算ROC-AUC曲线的指标
fpr, tpr, thresholds = roc_curve(binary_labels, probabilities)
roc_auc = auc(fpr, tpr)

# 计算P-R曲线的指标
precision, recall, _ = precision_recall_curve(binary_labels, probabilities)

# 绘制ROC-AUC曲线
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f'ROC curve (AUC = {roc_auc:.4f})')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc='lower right')
plt.show()

# 绘制P-R曲线
plt.figure(figsize=(8, 6))
plt.plot(recall, precision, label='Precision-Recall curve')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.1])
plt.xlim([0.0, 1.0])
plt.title('Precision-Recall Curve')
plt.legend(loc='lower left')
plt.show()
print(TN)
print(TP)
print(FN)
print(FP)

print(count_all)
print(TP+FP+TN+FN)

# 计算评估指标 正确率、召回率、F1分数等
ACCURACY = (TP+TN)/(TP+FP+TN+FN)
RECALL = TP/(TP+FN)
F1 = 2*(ACCURACY*RECALL)/(ACCURACY+RECALL)
# 计算指标

# 提取正确率、召回率和F1分数
print(f"Accuracy: {ACCURACY}")
print(f"Recall: {RECALL}")
print(f"F1 Score: {F1}")

# 雨抱龙吟傲，霞帔凤焰嚣
# 歼敌千里夜，匿迹水云朝
