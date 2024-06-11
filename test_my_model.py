# you can test the fine_tuning model with this script
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.metrics import classification_report

# 加载微调后的BERT模型和tokenizer
model_path = r'F:\TrainClassfier\my_classifier_model'  # 替换为你的模型路径
tokenizer = BertTokenizer.from_pretrained(r"F:\TrainClassfier\bert-base-cased")
model = BertForSequenceClassification.from_pretrained(model_path)
model.eval()  # 设置模型为评估模式
torch.manual_seed(42)
torch.cuda.manual_seed(42)


# 读取测试集并准备输入数据
def prepare_input_data(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    return inputs


# 读取测试集文件
with open(r'F:\TrainClassfier\src\test_shuffle1.txt', 'r', encoding='utf-8') as file:
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

# 使用模型进行预测
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

# 计算指标
labels = torch.tensor(labels)
predictions = torch.tensor(predictions)
report = classification_report(labels, predictions, target_names=['Class 0', 'Class 1'])
print(report)

# 提取正确率、召回率和F1分数
lines = report.split('\n')
for line in lines:
    if 'accuracy' in line:
        accuracy = line.split(' ')[3]
    elif 'recall' in line:
        recall = line.split(' ')[3]

print(f"Accuracy: {accuracy}")
print(f"Recall: {recall}")
# print(f"F1 Score: {f1_score}")
