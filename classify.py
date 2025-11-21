# classify.py
import sys
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

text = sys.argv[1]  # nhận input từ Node.js

device = "cuda" if torch.cuda.is_available() else "cpu"
model_path = "D:\\train-model-classifier\\bert_classifier"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
model.to(device)
model.eval()

tokens = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128).to(device)
with torch.no_grad():
    logits = model(**tokens).logits
    pred = torch.argmax(logits, dim=-1).item()

label = "general" if pred == 0 else "heritage"
print(label)  # Node.js sẽ đọc output này
