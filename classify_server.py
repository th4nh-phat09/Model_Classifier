import sys
import json
from transformers import pipeline

# Load model một lần duy nhất khi khởi động
print("Loading model...", file=sys.stderr)
classifier = pipeline("text-classification", model="bert_classifier")
print("Model loaded!", file=sys.stderr)

# Map label ID về tên thực
label_map = {
    "LABEL_0": "general",
    "LABEL_1": "heritage"
}

# Đọc input liên tục từ stdin
for line in sys.stdin:
    try:
        text = line.strip()
        if not text:
            continue
        
        result = classifier(text)[0]
        label = result['label']
        
        # Convert LABEL_0/LABEL_1 về general/heritage
        label = label_map.get(label, label)
        
        print(json.dumps({"label": label}))
        sys.stdout.flush()
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.stdout.flush()
