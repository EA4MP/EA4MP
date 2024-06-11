from transformers import BertForSequenceClassification, BertTokenizer
from torch.utils.data import TensorDataset, DataLoader
import torch
from transformers import BertTokenizer



device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)


model = BertForSequenceClassification.from_pretrained(r"F:\TrainClassfier\bert-base-cased", num_labels=2)
model.to(device)  
tokenizer = BertTokenizer.from_pretrained(r"F:\TrainClassfier\bert-base-cased")

data_path = r'train.txt'
def preprocess_data(data_path):
    inputs = []
    labels = []
    with open(data_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(',label:')
            text = parts[0].strip() 
            label = int(parts[1].strip())  
            inputs.append(text)
            labels.append(label)

    return inputs, labels


inputs, labels = preprocess_data(data_path)

inputs = tokenizer(inputs, padding=True, truncation=True, max_length=512, return_tensors='pt')

input_ids = inputs['input_ids'].to(device)
attention_mask = inputs['attention_mask'].to(device)
labels = torch.tensor(labels).to(device)

dataset = TensorDataset(input_ids, attention_mask, labels)

dataloader = DataLoader(dataset, batch_size=8, shuffle=True)

optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)

model.train()
total_steps = len(dataloader) * 8  
for epoch in range(8):
    print(f"Epoch {epoch + 1}/{8}")
    for batch_index, batch in enumerate(dataloader):
        input_ids, attention_mask, labels = batch

        input_ids = input_ids.to(device)
        attention_mask = attention_mask.to(device)
        labels = labels.to(device)

        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (batch_index + 1) % 100 == 0:
            print(f"Batch {batch_index + 1}/{len(dataloader)} - Loss: {loss.item()}")

model.save_pretrained(r"./my_classifier_model")
