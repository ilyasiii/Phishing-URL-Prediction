from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
from typing import List
import os
import sys

# Add src directory to path so pickled objects can find the features module
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

app = FastAPI(title='Phishing URL Detector')

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class URLRequest(BaseModel):
    urls: List[str]


class PredictionResponse(BaseModel):
    predictions: List[int]
    probabilities: List[float]
    labels: List[str]


# Load artifacts at startup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEATURE_PATH = os.path.join(BASE_DIR, 'models', 'feature_extractor.pkl')
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'xgboost_model.pkl')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

_feat = joblib.load(FEATURE_PATH)
_model = joblib.load(MODEL_PATH)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get('/')
def root():
    return FileResponse(os.path.join(STATIC_DIR, 'index.html'))


@app.post('/predict', response_model=PredictionResponse)
def predict(payload: URLRequest):
    """Predict if URLs are phishing (1) or legitimate (0)."""
    urls = payload.urls
    X = _feat.transform(urls)
    try:
        probs = _model.predict_proba(X)[:, 1]
    except Exception:
        probs = _model.predict_proba(X.toarray())[:, 1]
    preds = (probs >= 0.5).astype(int).tolist()
    labels = ['phishing' if p == 1 else 'legitimate' for p in preds]
    return PredictionResponse(predictions=preds, probabilities=probs.tolist(), labels=labels)

