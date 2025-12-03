# Phishing URL Detector (XGBoost)

A machine learning system that detects phishing URLs using XGBoost with advanced feature engineering (lexical analysis, TF-IDF, and character n-grams).

## 🚀 Quick Start (Local Development)

### 1. Download Model Artifacts

The trained models are hosted on [GitHub Releases](https://github.com/ilyasiii/Phishing-URL-Prediction/releases/tag/phishing).

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Download models
python scripts\download_model.py `
  --model-url "https://github.com/ilyasiii/Phishing-URL-Prediction/releases/download/phishing/xgboost_model.pkl" `
  --feature-url "https://github.com/ilyasiii/Phishing-URL-Prediction/releases/download/phishing/feature_extractor.pkl" `
  --out-dir models
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run the API

```powershell
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser at `http://localhost:8000` to use the web interface.

## 🧪 Test the API

### Using curl (PowerShell)

```powershell
curl -X POST http://127.0.0.1:8000/predict `
  -H "Content-Type: application/json" `
  -d '{"urls": ["https://www.google.com", "http://paypa1-secure.com/login"]}'
```

### Using Postman

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

## 🌐 Deployment on PythonAnywhere (100% Free)

Deploy your phishing URL detector on PythonAnywhere with no credit card required!

### Quick Start

1. **Create free account** at [PythonAnywhere.com](https://www.pythonanywhere.com)

2. **Open Bash console** and clone your repo:
   ```bash
   git clone https://github.com/ilyasiii/Phishing-URL-Prediction.git
   cd Phishing-URL-Prediction
   ```

3. **Create virtual environment**:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 phishing-env
   pip install -r requirements.txt
   ```

4. **Download models**:
   ```bash
   python scripts/download_model.py \
     --model-url "https://github.com/ilyasiii/Phishing-URL-Prediction/releases/download/phishing/xgboost_model.pkl" \
     --feature-url "https://github.com/ilyasiii/Phishing-URL-Prediction/releases/download/phishing/feature_extractor.pkl" \
     --out-dir models
   ```

5. **Configure Web App**:
   - Go to **Web** tab → **Add a new web app**
   - Choose **Manual configuration** → **Python 3.10**
   - Edit WSGI file (see `PYTHONANYWHERE.md` for complete config)
   - Set virtualenv path: `/home/yourusername/.virtualenvs/phishing-env`
   - Add static files mapping: URL: `/static/` → Directory: `/home/yourusername/Phishing-URL-Prediction/static/`

6. **Reload and access** at `http://yourusername.pythonanywhere.com`

📖 **Full deployment guide**: See [PYTHONANYWHERE.md](PYTHONANYWHERE.md) for detailed step-by-step instructions.

### Why PythonAnywhere?
- ✅ **100% Free** - No credit card required
- ✅ **Always-on** - No cold starts
- ✅ **HTTPS included** - Secure by default
- ✅ **Easy setup** - Web-based configuration
- ✅ **512 MB storage** - Enough for this project

## 📦 Project Structure

```
.
├── src/
│   ├── app.py              # FastAPI application
│   └── features.py         # Feature extraction pipeline
├── static/
│   ├── index.html          # Web UI
│   ├── style.css           # Styling
│   └── script.js           # Frontend logic
├── scripts/
│   └── download_model.py   # Model download helper
├── models/                 # Model artifacts (not in Git)
│   ├── xgboost_model.pkl
│   └── feature_extractor.pkl
├── Dockerfile              # Docker configuration
├── render.yaml             # Render blueprint
├── vercel.json             # Vercel configuration
├── requirements.txt        # Python dependencies
└── README.md

```

## 🧬 Features

- **Lexical Analysis**: URL length, special characters, entropy, etc.
- **TF-IDF Vectorization**: Captures patterns in URL paths and query strings
- **Character N-grams**: Domain-level pattern recognition
- **XGBoost Classifier**: High-performance gradient boosting
- **Interactive UI**: Real-time predictions with history tracking

## 🧪 Test URLs

**Legitimate:**
- https://www.threads.net
- https://claude.ai
- https://vercel.com
- https://github.com

**Phishing (simulated patterns):**
- http://secure-paypa1-login.com/verify
- http://faceb00k-security.net/login.php
- http://g00gle-docs.net/document
- http://amaz0n-account.xyz/signin

## 🔒 Security Notes

- Model files are hosted on GitHub Releases (public)
- For production, use private storage (S3/GCS) with presigned URLs
- Add SHA256 checksum verification for model integrity
- Implement rate limiting on the `/predict` endpoint
- Use HTTPS in production

## 📝 License

MIT
