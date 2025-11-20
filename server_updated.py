# =========================================================
# 🚀 MALICIOUS URL DETECTOR — FastAPI Server (Chrome Extension Ready)
# =========================================================

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os, json, joblib, pandas as pd, urllib.parse, numpy as np
from features import main as build_from_notebook
import logging

# =========================================================
# 1️⃣ BASIC SETUP + LOGGING
# =========================================================

HERE = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)
logger.info("🚀 Starting FastAPI Malicious URL Detection Server...")

# =========================================================
# 2️⃣ LOAD MODEL + METADATA
# =========================================================

# LightGBM model
try:
    model = joblib.load(os.path.join(HERE, "lgb_model.pkl"))
    logger.info("✅ LightGBM model loaded successfully.")
except Exception as e:
    logger.error(f"❌ Failed to load model: {e}")
    model = None

# Feature Columns
try:
    with open(os.path.join(HERE, "feature_columns.json")) as f:
        FEATURE_COLS = json.load(f)
    logger.info(f"✅ Loaded {len(FEATURE_COLS)} feature columns.")
except Exception as e:
    logger.error(f"❌ Failed to load feature_columns.json: {e}")
    FEATURE_COLS = []

# Label Encoder
try:
    label_encoder = joblib.load(os.path.join(HERE, "label_encoder.pkl"))
    CLASS_NAMES = list(label_encoder.classes_)
    logger.info(f"✅ Loaded label encoder with classes: {CLASS_NAMES}")
except Exception as e:
    CLASS_NAMES = ["SAFE", "DEFACEMENT", "MALWARE", "PHISHING"]
    logger.warning(f"⚠️ Using default class names: {CLASS_NAMES}")

# =========================================================
# 3️⃣ FASTAPI APP + CORS
# =========================================================

app = FastAPI(title="Malicious URL Detection API")

# Allow all origins (Chrome Extensions need this)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("✅ CORS enabled: allow all origins.")

# =========================================================
# 4️⃣ REQUEST BODY SCHEMA
# =========================================================

class Req(BaseModel):
    url: str

# =========================================================
# 5️⃣ URL UTILITIES
# =========================================================

def canonicalize_url(u: str) -> str:
    """Normalize URL before feature extraction."""
    if not isinstance(u, str):
        return u

    u = u.strip()
    if "://" not in u:
        u = "http://" + u

    p = urllib.parse.urlparse(u)
    hostname = p.hostname.lower() if p.hostname else ""

    if hostname.startswith("www."):
        hostname = hostname[len("www."):]

    path = urllib.parse.unquote(p.path or "")

    return hostname + path


def extract_features(url: str) -> pd.DataFrame:
    """Convert URL into ML-ready feature vector."""
    url_norm = canonicalize_url(url)
    feats = build_from_notebook(url_norm)

    # Notebook-style dictionary output
    if isinstance(feats, dict):
        row = {c: feats.get(c, 0) for c in FEATURE_COLS}
        X = pd.DataFrame([row])[FEATURE_COLS]

    # List output
    else:
        feats = list(feats)
        if len(feats) != len(FEATURE_COLS):
            raise ValueError(
                f"Feature mismatch: expected {len(FEATURE_COLS)}, got {len(feats)}"
            )
        X = pd.DataFrame([feats], columns=FEATURE_COLS)

    return X

# =========================================================
# 6️⃣ API ENDPOINTS
# =========================================================

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.post("/debug_features")
def debug_features(req: Req):
    try:
        X = extract_features(req.url)
        return {"columns": FEATURE_COLS, "values": X.iloc[0].tolist()}
    except Exception as e:
        logger.error(f"❌ Feature extraction error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/predict")
def predict(req: Req):
    try:
        url_norm = canonicalize_url(req.url)
        logger.info(f"🧠 Predicting for: {req.url} -> {url_norm}")

        # Whitelisted domains
        safe_domains = [
            "wikipedia.org", "google.com", "youtube.com",
            "microsoft.com", "github.com"
        ]
        if any(d in url_norm for d in safe_domains):
            return {
                "url": req.url,
                "prediction": "SAFE",
                "whitelisted": True
            }

        if model is None:
            return JSONResponse(
                status_code=500,
                content={"error": "Model not loaded"}
            )

        X = extract_features(req.url)
        pred_idx = int(model.predict(X)[0])

        label = (
            CLASS_NAMES[pred_idx]
            if CLASS_NAMES and len(CLASS_NAMES) > pred_idx
            else str(pred_idx)
        )

        # Probability scores
        try:
            probs = model.predict_proba(X).tolist()[0]
            prob_dict = dict(zip(CLASS_NAMES, probs))
        except Exception:
            prob_dict = None

        return {
            "url": req.url,
            "normalized": url_norm,
            "prediction": label,
            "probabilities": prob_dict,
        }

    except Exception as e:
        logger.error(f"❌ Prediction error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

# =========================================================
# 7️⃣ STARTUP MESSAGE
# =========================================================

@app.on_event("startup")
def startup_event():
    logger.info("🚀 FastAPI server started successfully.")

# =========================================================
# 8️⃣ RENDER ENTRYPOINT FOR LOCAL RUN
# =========================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    import uvicorn
    uvicorn.run("server_updated:app", host="0.0.0.0", port=port)
