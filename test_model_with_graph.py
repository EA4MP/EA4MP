# same as test_my _moedl.py but will show the ROC figure

import torch
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.metrics import roc_curve, precision_recall_curve, auc, classification_report
import matplotlib.pyplot as plt


model_path = r'...\my_classifier15_model'  # your model path (fine_tuned BERT)
tokenizer = BertTokenizer.from_pretrained(r"\bert-base-cased")
model = BertForSequenceClassification.from_pretrained(model_path)
model.eval() 
torch.manual_seed(5)
torch.cuda.manual_seed(5)



def prepare_input_data(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    return inputs



with open(r'...\test5_shuffle5.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()


texts = []
labels = []
for line in lines:
    parts = line.strip().split(',label: ')
    texts.append(parts[0])
    labels.append(int(parts[1]))
count_all = 0
TP = 0
TN = 0
FP = 0
FN = 0
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
        # sigmoid function to get the prediction
        probs = torch.sigmoid(logits).cpu().numpy()
        probabilities.append(probs[0][1]) 
binary_labels = [1 if label == 1 else 0 for label in labels]


fpr, tpr, thresholds = roc_curve(binary_labels, probabilities)
roc_auc = auc(fpr, tpr)


precision, recall, _ = precision_recall_curve(binary_labels, probabilities)

# ROC-AUC
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f'ROC curve (AUC = {roc_auc:.4f})')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc='lower right')
plt.show()

# P-R
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

# 
ACCURACY = (TP+TN)/(TP+FP+TN+FN)
RECALL = TP/(TP+FN)
F1 = 2*(ACCURACY*RECALL)/(ACCURACY+RECALL)
# 

# 
print(f"Accuracy: {ACCURACY}")
print(f"Recall: {RECALL}")
print(f"F1 Score: {F1}")

