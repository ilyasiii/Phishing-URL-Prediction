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

## 🌐 Deployment

### Recommended: Fly.io (Fast Global Deployment)

Fly.io provides fast deployment with automatic scaling and global edge locations.

#### Prerequisites

Install Fly CLI:
```powershell
# PowerShell (Windows)
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# Or use winget
winget install fly.io.flyctl
```

#### Deploy Steps

1. **Login to Fly.io**
   ```powershell
   flyctl auth login
   ```

2. **Launch the app** (from your project directory)
   ```powershell
   flyctl launch --name phishing-url-detector
   ```
   - When prompted, say **No** to Postgres/Redis
   - Select a region closest to you (e.g., `ord` for Chicago)
   - Say **Yes** to deploy now (or deploy later with `flyctl deploy`)

3. **Set model URLs as secrets**
   ```powershell
   flyctl secrets set MODEL_URL="https://github.com/ilyasiii/Phishing-URL-Prediction/releases/download/phishing/xgboost_model.pkl"
   flyctl secrets set FEATURE_URL="https://github.com/ilyasiii/Phishing-URL-Prediction/releases/download/phishing/feature_extractor.pkl"
   ```

4. **Deploy** (if you skipped deploy in step 2)
   ```powershell
   flyctl deploy
   ```

5. **Open your app**
   ```powershell
   flyctl open
   ```

Your app will be live at: `https://phishing-url-detector.fly.dev`

#### Manage Your App

```powershell
# View logs
flyctl logs

# Check status
flyctl status

# Scale resources (if needed)
flyctl scale memory 1024

# SSH into container
flyctl ssh console
```

### Alternative: Render (Simpler Setup)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New +** → **Web Service**
3. Connect repo: `ilyasiii/Phishing-URL-Prediction`
4. Environment: **Docker**, Branch: **main**
5. Add environment variables:
   - `MODEL_URL` = `https://github.com/ilyasiii/Phishing-URL-Prediction/releases/download/phishing/xgboost_model.pkl`
   - `FEATURE_URL` = `https://github.com/ilyasiii/Phishing-URL-Prediction/releases/download/phishing/feature_extractor.pkl`
6. Deploy (Free tier available)

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
