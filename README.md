# Heritage Question Classifier

BERT-based question classifier for Vietnamese heritage chatbot system. Determines if questions are heritage-related or general queries.

## 🚀 Features

- **BERT Model**: Fine-tuned Vietnamese BERT for question classification
- **Binary Classification**: Heritage-related vs General questions
- **REST API**: Express.js server wrapping Python classifier
- **Real-time Inference**: Fast classification for chatbot routing
- **Training Pipeline**: Complete training workflow included

## 🛠️ Tech Stack

### Python (ML)

- **Model**: `vinai/phobert-base` (Vietnamese BERT)
- **Framework**: PyTorch + Transformers
- **Dataset**: Custom CSV with labeled questions

### Node.js (API Server)

- **Runtime**: Node.js
- **Framework**: Express.js
- **IPC**: Child process communication with Python

## 📦 Installation

### Python Dependencies

```bash
# Install Python packages
pip install -r requirements.txt
```

**requirements.txt:**

```
torch>=2.0.0
transformers>=4.30.0
scikit-learn>=1.3.0
pandas>=2.0.0
numpy>=1.24.0
```

### Node.js Dependencies

```bash
# Install Node packages
npm install
```

## 🔧 Training the Model

### 1. Prepare Dataset

Create `questions.csv`:

```csv
question,label
Where is Hue Imperial City located?,heritage
What is the history of Ha Long Bay?,heritage
How do I learn JavaScript?,general
What is the weather today?,general
Tell me about Hoi An Ancient Town,heritage
```

**Labels:**

- `heritage` (1): Questions about Vietnamese heritage sites
- `general` (0): Non-heritage questions

### 2. Train Model

```bash
python trainModelClassifier.py
```

**Training process:**

- Loads `questions.csv`
- Splits train/test (80/20)
- Fine-tunes PhoBERT
- Saves model to `bert_classifier/`
- Outputs accuracy metrics

**Model files generated:**

```
bert_classifier/
├── config.json
├── model.safetensors
├── tokenizer_config.json
├── tokenizer.json
├── special_tokens_map.json
└── vocab.txt
```

## 🏃 Running the Classifier

### Option 1: Standalone Python Server

```bash
python classify_server.py
```

- Reads from stdin
- Outputs JSON to stdout
- Used by Node.js wrapper

### Option 2: Node.js API Server

```bash
# Development
node server.js

# Production with PM2
pm2 start ecosystem.config.js
```

**API Endpoint:**

```http
POST http://localhost:3000/classify
Content-Type: application/json

{
  "text": "Where is the Temple of Literature?"
}
```

**Response:**

```json
{
  "text": "Where is the Temple of Literature?",
  "label": "heritage"
}
```

## 📁 Project Structure

```
train-model-classifier/
├── server.js                    # Express API server
├── classify_server.py           # Python stdin/stdout classifier
├── classify.py                  # Standalone classifier script
├── trainModelClassifier.py      # Training pipeline
├── collectData.py              # Data collection helper
├── questions.csv               # Training dataset
├── requirements.txt            # Python dependencies
├── package.json               # Node dependencies
├── ecosystem.config.js        # PM2 config
└── bert_classifier/           # Trained model (generated)
    ├── config.json
    ├── model.safetensors
    └── ...
```

## 🎯 Model Performance

**Expected Metrics:**

- Accuracy: ~95%
- F1-Score: ~0.94
- Inference Time: <100ms

## 🔄 Integration with RAG System

The classifier is used in the RAG pipeline:

```
User Question
    ↓
Question Classifier (This Service)
    ↓
├─ Heritage → RAG Pipeline
└─ General  → General Response
```

## 🚀 Deployment

### Local Development

```bash
node server.js
```

### Production with PM2

```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

**ecosystem.config.js:**

```javascript
module.exports = {
  apps: [
    {
      name: "heritage-classifier",
      script: "server.js",
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: "1G",
      env: {
        NODE_ENV: "production",
        PORT: 3000,
      },
    },
  ],
};
```

## 🔗 Related Repositories

- **Frontend**: [heritage-naver-fe](../heritage-naver-fe)
- **Backend API**: [heritage-naver-api](../heritage-naver-api)

## 📊 API Usage Example

```javascript
// Node.js example
const response = await fetch("http://localhost:3000/classify", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    text: "Tell me about Vietnamese heritage sites",
  }),
});

const result = await response.json();
console.log(result.label); // "heritage"
```

## 🛠️ Troubleshooting

**Model loading fails:**

- Ensure `bert_classifier/` directory exists
- Run training script first: `python trainModelClassifier.py`

**Python process crashes:**

- Check Python version (3.8+)
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check memory usage (model needs ~500MB RAM)

**Slow inference:**

- Use GPU if available (modify `classify_server.py`)
- Consider model quantization for production

## 📄 License

MIT

## 👥 Contributors

- Nguyen An Thanh Phat (thanphat354@gmail.com)
