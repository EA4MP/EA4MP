# you can test the fine_tuning model with this script
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.metrics import classification_report

# load fine_tuning BERT model and tokenizer
model_path = r'...\my_classifier_model'  # your bert model path
tokenizer = BertTokenizer.from_pretrained(r"\bert-base-cased") # load config file
model = BertForSequenceClassification.from_pretrained(model_path)
model.eval() 
torch.manual_seed(42)
torch.cuda.manual_seed(42)  # random seed


# read data
def prepare_input_data(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    return inputs


# test file path 
with open(r'...\test_shuffle1.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# get data and label
# divided
texts = []
labels = []
for line in lines:
    parts = line.strip().split(',label: ')
    texts.append(parts[0])
    labels.append(int(parts[1]))
count_all = 0

# predict
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

# calculate
labels = torch.tensor(labels)
predictions = torch.tensor(predictions)
report = classification_report(labels, predictions, target_names=['Class 0', 'Class 1'])
print(report)

lines = report.split('\n')
for line in lines:
    if 'accuracy' in line:
        accuracy = line.split(' ')[3]
    elif 'recall' in line:
        recall = line.split(' ')[3]

print(f"Accuracy: {accuracy}")
print(f"Recall: {recall}")
# print(f"F1 Score: {f1_score}")
