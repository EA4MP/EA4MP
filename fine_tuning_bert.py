from transformers import BertForSequenceClassification, Trainer, TrainingArguments
from torch.utils.data import TensorDataset, DataLoader
import torch
from transformers import BertTokenizer


tokenizer = BertTokenizer.from_pretrained(r"F:\TrainClassfier\bert-base-cased")
model = BertForSequenceClassification.from_pretrained(r"F:\TrainClassfier\bert-base-cased", num_labels=2)

# 设置微调参数
# training_args = TrainingArguments(
#     output_dir="./results",   # 指定微调结果输出路径
#     num_train_epochs=3,       # 设置微调的轮数
#     per_device_train_batch_size=8,  # 指定训练时每个GPU/CPU设备的批大小
#     logging_dir="./logs",     # 指定训练日志输出路径
# )

# 数据文件路径
data_path = r'F:\TrainClassfier\datasets\train.txt'


# 预处理数据
def preprocess_data(data_path):
    inputs = []
    labels = []

    # 读取数据文件
    with open(data_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            # 分割文本和标签
            parts = line.strip().split(',label:')
            text = parts[0].strip()  # 获取文本部分
            label = int(parts[1].strip())  # 获取标签部分
            inputs.append(text)
            labels.append(label)

    return inputs, labels


inputs, labels = preprocess_data(data_path)

# 将输入数据和标签转换为Tensor对象
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

model.save_pretrained(r"./my_classifier_model")
