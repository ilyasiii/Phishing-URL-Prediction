# Phishing URL Detector (XGBoost)

## Run API

```powershell
./venv/Scripts/activate
pip install -r requirements.txt
uvicorn src.app:app --reload --port 8000
```

## Test with Postman

**POST** `http://127.0.0.1:8000/predict`

**Body (JSON):**
```json
{"urls": ["https://www.google.com", "http://paypa1-secure.com/login"]}
```

**Response:**
```json
{
  "predictions": [0, 1],
  "probabilities": [0.02, 0.98],
  "labels": ["legitimate", "phishing"]
}
```

## Test URLs

**Legitimate:**
- https://www.threads.net
- https://claude.ai
- https://vercel.com

**Phishing (simulated):**
- http://secure-paypa1-login.com/verify
- http://faceb00k-security.net/login.php
- http://g00gle-docs.net/document
