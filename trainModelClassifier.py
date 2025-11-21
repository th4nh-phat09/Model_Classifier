import pandas as pd
from transformers import AutoTokenizer
from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoModelForSequenceClassification
from torch.optim import AdamW
from torch import nn

# Load CSV
df = pd.read_csv("D:\\train-model-classifier\\questions.csv")

# Map label sang số (0=general, 1=heritage)
label2id = {"general": 0, "heritage": 1}
df['label_id'] = df['label'].map(label2id)

print("Sample data:")
print(df.head())

tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
tokens = tokenizer(
    df['text'].tolist(),
    padding=True,
    truncation=True,
    max_length=128,
    return_tensors="pt"
)

# Tạo class Dataset PyTorch
class QuestionDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels
    def __len__(self):
        return len(self.labels)
    def __getitem__(self, idx):
        # trả về dictionary input_ids, attention_mask, etc + label
        return {key: val[idx] for key, val in self.encodings.items()}, self.labels[idx]



train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['label_id'])

# Tokenize riêng train/test
train_tokens = tokenizer(train_df['text'].tolist(), padding=True, truncation=True, max_length=128, return_tensors="pt")
test_tokens = tokenizer(test_df['text'].tolist(), padding=True, truncation=True, max_length=128, return_tensors="pt")

train_dataset = QuestionDataset(train_tokens, torch.tensor(list(train_df['label_id'])))
test_dataset = QuestionDataset(test_tokens, torch.tensor(list(test_df['label_id'])))

# DataLoader để train
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)

# BERT multilingual cho 2 label
model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-multilingual-cased",
    num_labels=2
)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Optimizer + Loss
optimizer = AdamW(model.parameters(), lr=5e-5)
loss_fn = nn.CrossEntropyLoss()

# Training Loop
epochs = 3

for epoch in range(epochs):
    model.train()
    total_loss = 0
    for batch in train_loader:
        inputs, labels = batch
        inputs = {k: v.to(device) for k, v in inputs.items()}
        labels = labels.to(device)

        optimizer.zero_grad()
        outputs = model(**inputs)
        loss = loss_fn(outputs.logits, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
    print(f"Epoch {epoch+1}/{epochs}, Avg Loss: {total_loss/len(train_loader):.4f}")

# 9️⃣ Test trên test set
model.eval()
correct, total = 0, 0
for batch in test_loader:
    inputs, labels = batch
    inputs = {k:v.to(device) for k,v in inputs.items()}
    labels = labels.to(device)
    with torch.no_grad():
        logits = model(**inputs).logits
        preds = torch.argmax(logits, dim=-1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)
print(f"Test accuracy: {correct/total*100:.2f}%")

# Lưu model
model.save_pretrained("bert_classifier")
tokenizer.save_pretrained("bert_classifier")
print("Model saved to 'bert_classifier/'")
