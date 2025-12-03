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

### Option A: Vercel (Frontend) + Render (Backend)

#### Deploy Backend to Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New +** → **Web Service**
3. Connect your GitHub repository: `ilyasiii/Phishing-URL-Prediction`
4. Configure:
   - **Name**: `phishing-url-api`
   - **Environment**: `Docker`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Dockerfile Path**: `./Dockerfile` (auto-detected)
5. Add Environment Variables:
   - `MODEL_URL` = `https://github.com/ilyasiii/Phishing-URL-Prediction/releases/download/phishing/xgboost_model.pkl`
   - `FEATURE_URL` = `https://github.com/ilyasiii/Phishing-URL-Prediction/releases/download/phishing/feature_extractor.pkl`
   - `PORT` = `8000` (Render sets this automatically)
6. Click **Create Web Service**
7. Copy your API URL (e.g., `https://phishing-url-api.onrender.com`)

#### Deploy Frontend to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/new)
2. Import your GitHub repository: `ilyasiii/Phishing-URL-Prediction`
3. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: `./`
   - **Build Command**: (leave empty)
   - **Output Directory**: `static`
4. **Important**: Update `static/script.js` with your Render API URL:
   ```javascript
   const API_URL = 'https://your-render-app.onrender.com';
   ```
5. Click **Deploy**
6. Your frontend will be live at `https://your-project.vercel.app`

### Option B: Single Server (Render with Static Files)

The FastAPI app already serves the static frontend at `/`. Just deploy the backend to Render (steps above) and access the UI at your Render URL.

### Option C: Fly.io (Alternative)

1. Install [Fly CLI](https://fly.io/docs/hands-on/install-flyctl/)
2. Login: `flyctl auth login`
3. Launch app:
   ```bash
   flyctl launch --name phishing-url-detector
   ```
4. Set secrets:
   ```bash
   flyctl secrets set MODEL_URL="https://github.com/ilyasiii/Phishing-URL-Prediction/releases/download/phishing/xgboost_model.pkl"
   flyctl secrets set FEATURE_URL="https://github.com/ilyasiii/Phishing-URL-Prediction/releases/download/phishing/feature_extractor.pkl"
   ```
5. Deploy: `flyctl deploy`

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
