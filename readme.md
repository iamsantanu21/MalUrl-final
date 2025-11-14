# 🛡️ Malicious URL & Domain Detection (NLP-Based)  
An end-to-end machine learning system for detecting malicious URLs using lexical features, TF-IDF patterns, and gradient boosting classifiers (LightGBM).  
This project includes:

- ✨ **Machine Learning Model** (LightGBM)
- 🧪 **Feature Engineering Pipeline**
- 🔍 **URL Analysis Utilities**
- 🧩 **Browser Extension (Chrome)**
- ⚙️ **Model Serving API**
- 📊 **Notebooks for Training & Experimentation**

---

## 📁 Project Structure

```
MalUrl-final/
│── features.py                 # Feature extraction logic
│── server-updated.py           # Model inference API
│── lgb_model.pkl               # Trained LightGBM model
│── malicious-tfidf-updated.ipynb  # Training & experimentation notebook
│── feature_meta.json           # Metadata used during inference
│── feature_columns.json        # Final feature list used for training
│── requirements.txt            # Python dependencies
│── chrome-extension/           # Browser extension source code
│── README.md
```

---

## 🚀 Project Overview

Malicious URLs are a major vector for phishing, malware distribution, and cyber-attacks.  
This system detects malicious URLs based on:

### ✔ Lexical Features  
- URL length  
- Number of digits  
- Special character count  
- Suspicious keyword presence  
- TLD category  
- Entropy  

### ✔ NLP / TF-IDF Vectorization  
- Character-level TF-IDF  
- N-gram analysis  

### ✔ ML Algorithm  
The final model uses **LightGBM**, selected for high accuracy and fast inference.

---

## 🧰 Installation

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/iamsantanu21/MalUrl-final.git
cd MalUrl-final
```

### 2️⃣ Install dependencies  
```bash
pip install -r requirements.txt
```

---

## ▶️ Running the API Server

The backend server loads the trained model and returns predictions.

Start the server:

```bash
python server-updated.py
```

The API runs at:

```
http://localhost:5000/predict
```

### Example Request  
```bash
curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"url": "http://example-login-free.ru"}'
```

### Example Response  
```json
{
  "url": "http://example-login-free.ru",
  "prediction": "malicious",
  "score": 0.9874
}
```

---

## 🧩 Browser Extension (Chrome)

The extension allows users to test URLs directly in their browser.

### Install Steps:
1. Open `chrome://extensions/`  
2. Enable **Developer Mode**  
3. Click **Load unpacked**  
4. Select the `chrome-extension/` folder  

---

## 📊 Model Training

Model development is documented in:

```
malicious-tfidf-updated.ipynb
```

It covers:

- Preprocessing  
- TF-IDF vectorization  
- Feature engineering  
- LightGBM training  
- Evaluation metrics  

---

## 🛠 Feature Engineering

Core logic implemented in `features.py` includes:

- URL lexical features  
- Character-level patterns  
- Token-based TF-IDF  
- Suspicious keyword detection  
- Normalization  
- Domain/TLD analysis  

---

## 📦 Key Files

| File | Description |
|------|-------------|
| `lgb_model.pkl` | Final trained LightGBM model |
| `feature_columns.json` | List of ML features |
| `feature_meta.json` | Metadata for inference |
| `server-updated.py` | API server for predictions |
| `features.py` | Feature extraction pipeline |
| `malicious-tfidf-updated.ipynb` | Training notebook |

---

## 🧪 Example Python Usage

```python
from features import extract_features
import joblib

model = joblib.load("lgb_model.pkl")

url = "http://verify-account-security-update.ru"

features = extract_features(url)
prediction = model.predict([features])[0]

print("Malicious" if prediction == 1 else "Benign")
```

---

## 📈 Sample Performance

| Metric | Score |
|-------|-------|
| Accuracy | 95–98% |
| Precision | 94% |
| Recall | 96% |
| F1 Score | 95% |

---

## 🛡️ Use Cases

- Browser security plugins  
- Phishing URL blocking  
- Enterprise filtering  
- Email malware detection  
- Threat intelligence systems  

---

## 📌 Future Improvements

- WHOIS-based domain age features  
- Deep learning (CNN/LSTM hybrid model)  
- Dockerized deployment  
- Firefox/Edge extension support  
- Larger dataset for robustness  

---

## 📝 License

This project is open-source (add MIT or Apache license if needed).
