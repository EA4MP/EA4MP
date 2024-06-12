import numpy as np
import torch
import pickle
from transformers import BertForSequenceClassification, BertTokenizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

with open(r'', 'rb') as f:
    nb_model = pickle.load(f)


tokenizer = BertTokenizer.from_pretrained(r'bert-base-cased')
bert_model = BertForSequenceClassification.from_pretrained(r'')
bert_model.eval()

with open(r'', 'r') as f:
    lines = f.readlines()

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

    nb_pred = nb_model.predict_proba([nb_features[:-1]])[0][1] 

    combined_features = [bert_outputs[1], nb_pred] 
    X_combined.append(combined_features)
    y.append(label)

X_combined = np.array(X_combined)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.2, random_state=42)

def ensemble_predict(X):
    combined_pred = []
    for features in X:
        bert_pred = features[0]
        nb_pred = features[1]
        ensemble_prob = (bert_pred + nb_pred) / 2  
        combined_pred.append(1 if ensemble_prob >= 0.5 else 0)
    return np.array(combined_pred)


predictions = ensemble_predict(X_test)
accuracy = accuracy_score(y_test, predictions)
report = classification_report(y_test, predictions)

print("accuracy:", accuracy)
print("report：\n", report)

ensemble_model = {
    'bert_model': bert_model,
    'nb_model': nb_model,
    'tokenizer': tokenizer,
    'predict_function': ensemble_predict
}

with open('ensemble_model_with_equal_weights.pkl', 'wb') as f:
    pickle.dump(ensemble_model, f)

print("save finish!")
