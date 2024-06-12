import numpy as np
import torch
import pickle
from transformers import BertForSequenceClassification, BertTokenizer
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

with open('naive_bayes_model.pkl', 'rb') as f:
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

adaboost = AdaBoostClassifier(n_estimators=50, algorithm='SAMME')
adaboost.fit(X_train, y_train)

predictions = adaboost.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
report = classification_report(y_test, predictions)

print("accuary:", accuracy)
print("report：\n", report)

with open('adaboost_ensemble_model.pkl', 'wb') as f:
    pickle.dump(adaboost, f)

print("save finish")
