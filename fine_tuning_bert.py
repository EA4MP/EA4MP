# you can run this script is you dont have a GPU ,but it may very very very slow
# so we recommend using another script : fine_tune_with_GPU.py


from transformers import BertForSequenceClassification, Trainer, TrainingArguments
from torch.utils.data import TensorDataset, DataLoader
import torch
from transformers import BertTokenizer


tokenizer = BertTokenizer.from_pretrained(r"F:\TrainClassfier\bert-base-cased")
model = BertForSequenceClassification.from_pretrained(r"F:\TrainClassfier\bert-base-cased", num_labels=2)


# training_args = TrainingArguments(
#     output_dir="./results",   
#     num_train_epochs=3,       
#     per_device_train_batch_size=8,  
#     logging_dir="./logs",     
# )


data_path = r'...\train.txt'


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
labels = torch.tensor(labels)

datasets = list(zip(inputs['input_ids'], inputs['attention_mask'], labels))
dataloader = DataLoader(datasets, batch_size=8)

optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)

model.train()
for epoch in range(8):
    for batch in dataloader:
        input_ids, attention_mask, labels = batch
        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

model.save_pretrained(r".../my_classifier_model")
