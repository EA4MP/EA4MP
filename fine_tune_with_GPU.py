from transformers import BertForSequenceClassification, BertTokenizer
from torch.utils.data import TensorDataset, DataLoader
import torch
from transformers import BertTokenizer



# 检查GPU是否可用
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# 加载预训练BERT模型和分词器
model = BertForSequenceClassification.from_pretrained(r"F:\TrainClassfier\bert-base-cased", num_labels=2)
model.to(device)  # 将模型移动到GPU上
tokenizer = BertTokenizer.from_pretrained(r"F:\TrainClassfier\bert-base-cased")

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

# 使用分词器编码输入数据
inputs = tokenizer(inputs, padding=True, truncation=True, max_length=512, return_tensors='pt')

# 将输入数据和标签转换为Tensor对象，并将其移动到GPU上
input_ids = inputs['input_ids'].to(device)
attention_mask = inputs['attention_mask'].to(device)
labels = torch.tensor(labels).to(device)

# 创建TensorDataset对象
dataset = TensorDataset(input_ids, attention_mask, labels)

# 创建DataLoader对象
dataloader = DataLoader(dataset, batch_size=8, shuffle=True)

# 定义优化器，将模型参数也移动到GPU上
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)

# 开始微调
model.train()
total_steps = len(dataloader) * 8  # 计算总的训练步数
for epoch in range(8):
    print(f"Epoch {epoch + 1}/{8}")
    for batch_index, batch in enumerate(dataloader):
        input_ids, attention_mask, labels = batch

        # 将数据移动到GPU上
        input_ids = input_ids.to(device)
        attention_mask = attention_mask.to(device)
        labels = labels.to(device)

        # 前向传播
        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss

        # 反向传播和参数更新
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # 打印训练进度
        if (batch_index + 1) % 100 == 0:
            print(f"Batch {batch_index + 1}/{len(dataloader)} - Loss: {loss.item()}")

# 保存微调后的模型
model.save_pretrained(r"./my_classifier_model")
