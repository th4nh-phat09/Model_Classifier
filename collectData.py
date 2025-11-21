from datasets import load_dataset
import pandas as pd

# 1) Load dataset từ HuggingFace
ds = load_dataset("jinaai/triviaqa-span-annotated", split="test")

# 2) Lấy câu hỏi (cột: "query")
questions = ds["query"]  

# 3) Lấy 1.000 câu đầu
questions_1k = questions[:1000]

# 4) Tạo dataframe
df = pd.DataFrame({
    "text": questions_1k,
    "label": ["general"] * len(questions_1k)
})

# 5) Lưu CSV
df.to_csv("general_1000.csv", index=False)

print("Done! File saved: general_1000.csv")
