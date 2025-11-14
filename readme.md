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
│── features.py                     # Feature extraction logic
│── server-updated.py               # Model inference API
│── lgb_model.pkl                   # Trained LightGBM model
│── malicious-tfidf-updated.ipynb   # Training & experimentation notebook
│── feature_meta.json               # Metadata used during inference
│── feature_columns.json            # Final feature list used for training
│── requirements.txt                # Python dependencies
│── chrome-extension/               # Browser extension source code
│── README.md
```

---

## 🚀 Project Overview

Malicious URLs remain a common attack vector for phishing, malware delivery, and social engineering.  
This project detects malicious URLs using:

### ✔ Lexical Features  
- URL length  
- Digit, symbol, and dot counts  
- Suspicious keyword presence  
- Entropy  
- TLD and domain patterns  

### ✔ NLP / TF-IDF Vectorization  
- Character-level TF-IDF  
- N-gram token patterns  

### ✔ ML Algorithm  
LightGBM is used for high accuracy, fast prediction time, and strong performance on sparse vector data.

---

## 🔧 Setup & Execution (Windows / macOS / Linux)

### **1️⃣ Create & Activate Virtual Environment**

### 🪟 Windows
```bash
python -m venv venv
venv\Scripts\activate.bat
```

### 🍎 macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

### 🐧 Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### **2️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

---

### **3️⃣ Start the Server (Uvicorn)**
```bash
uvicorn server-updated:app --host 127.0.0.1 --port 8010 --reload
```

The API runs at:
```
http://127.0.0.1:8010
```

---

### **4️⃣ Stop the Server**
Press:
```
CTRL + C
```

---

## ▶️ API Endpoint Usage

### **POST /predict**
Send a JSON body containing a URL:

```bash
curl -X POST http://127.0.0.1:8010/predict \
     -H "Content-Type: application/json" \
     -d '{"url": "http://example-login-free.ru"}'
```

### Example Response:
```json
{
  "url": "http://example-login-free.ru",
  "prediction": "malicious",
  "score": 0.9874
}
```

---

## 🧩 Chrome Extension

The `chrome-extension/` folder contains a working Chrome extension that communicates with your backend API.

### Install Steps:
1. Open `chrome://extensions/`  
2. Enable **Developer Mode**  
3. Click **Load unpacked**  
4. Select the `chrome-extension/` folder  

---

## 📊 Model Training

Training is documented in:

```
malicious-tfidf-updated.ipynb
```

Includes:

- Dataset preprocessing  
- TF-IDF vectorization  
- Feature engineering  
- LightGBM model training  
- Evaluation metrics  
- Feature importance analysis  

---

## 🛠 Feature Engineering

Implemented in `features.py`:

- URL lexical features  
- Special character ratios  
- Entropy calculation  
- Suspicious keyword detection  
- TF-IDF embedding integration  
- Normalization & vector assembly  

---

## 📦 Key Files

| File | Description |
|------|-------------|
| `lgb_model.pkl` | Final trained LightGBM model |
| `feature_columns.json` | Ordered list of input features |
| `feature_meta.json` | Metadata for TF-IDF & preprocessing |
| `server-updated.py` | FastAPI/Uvicorn server for predictions |
| `features.py` | Feature extraction functions |
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

## 📈 Sample Model Performance

| Metric | Score |
|--------|--------|
| Accuracy | 95–98% |
| Precision | 94% |
| Recall | 96% |
| F1 Score | 95% |

---

## 🛡️ Use Cases

- Browser security plugins  
- Enterprise filtering  
- Email threat scanning  
- Phishing URL detection  
- Threat intelligence enrichment  

---

## 📌 Future Improvements

- Add WHOIS/domain age features  
- Dockerized deployment  
- Deep learning (CNN/LSTM hybrid)  
- Add Firefox/Edge version of extension  
- Larger & real-world datasets  

---

## 📝 License
This project is open-source. Add MIT/Apache License if required.

