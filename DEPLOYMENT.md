# Deployment Guide

This guide provides step-by-step instructions for deploying the Phishing URL Detector to production.

## 🎯 Deployment Architecture

We recommend **Option A: Render (Backend) + FastAPI serves static frontend** for simplicity, or **Option B: Render (Backend) + Vercel (Frontend)** for separation of concerns.

---

## Option A: Single Server on Render (Recommended for Beginners)

This deploys both the API and frontend on a single Render service.

### Steps

1. **Push your code to GitHub** (already done ✓)

2. **Go to [Render Dashboard](https://dashboard.render.com/)**
   - Sign up/login with GitHub

3. **Create New Web Service**
   - Click **New +** → **Web Service**
   - Select **Build and deploy from a Git repository**
   - Connect your GitHub account and select: `ilyasiii/Phishing-URL-Prediction`

4. **Configure the Service**
   ```
   Name: phishing-url-detector
   Region: Oregon (or closest to you)
   Branch: main
   Root Directory: (leave empty)
   Environment: Docker
   ```

5. **Add Environment Variables**
   Click **Advanced** → **Add Environment Variable**:
   ```
   MODEL_URL = https://github.com/ilyasiii/Phishing-URL-Prediction/releases/download/phishing/xgboost_model.pkl
   FEATURE_URL = https://github.com/ilyasiii/Phishing-URL-Prediction/releases/download/phishing/feature_extractor.pkl
   PORT = 8000
   ```

6. **Deploy**
   - Select **Free** plan
   - Click **Create Web Service**
   - Wait 5-10 minutes for build to complete

7. **Access Your App**
   - Render will provide a URL like: `https://phishing-url-detector.onrender.com`
   - Open it in your browser — the UI will be served at `/`
   - API endpoint: `https://phishing-url-detector.onrender.com/predict`

### ⚠️ Important Notes for Free Tier
- Free instances spin down after 15 minutes of inactivity
- First request after sleep takes ~30 seconds to wake up
- Monthly limit: 750 hours (sufficient for demos)

---

## Option B: Render (Backend) + Vercel (Frontend)

Separate frontend and backend for better scalability.

### Step 1: Deploy Backend to Render

Follow **Option A steps 1-6** above to deploy the FastAPI backend.

After deployment, copy your Render URL (e.g., `https://phishing-url-api.onrender.com`)

### Step 2: Update Frontend API URL

1. Open `static/script.js` in your local repository

2. Replace the API_URL line with your Render backend URL:
   ```javascript
   const API_URL = 'https://phishing-url-api.onrender.com';
   ```

3. Commit and push:
   ```powershell
   git add static/script.js
   git commit -m "Update API URL for production"
   git push origin main
   ```

### Step 3: Deploy Frontend to Vercel

1. **Go to [Vercel Dashboard](https://vercel.com/new)**
   - Sign up/login with GitHub

2. **Import Repository**
   - Click **Add New...** → **Project**
   - Select `ilyasiii/Phishing-URL-Prediction`

3. **Configure Project**
   ```
   Framework Preset: Other
   Root Directory: ./
   Build Command: (leave empty)
   Output Directory: static
   Install Command: (leave empty)
   ```

4. **Deploy**
   - Click **Deploy**
   - Wait 1-2 minutes

5. **Access Your App**
   - Vercel provides a URL like: `https://phishing-url-prediction.vercel.app`
   - The UI will make API calls to your Render backend

### Enable CORS (if needed)

If you get CORS errors, the `src/app.py` already includes CORS middleware. Verify it allows your Vercel domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Option C: Fly.io (Alternative)

Fast global deployment with free tier.

### Prerequisites
```powershell
# Install Fly CLI
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# Login
flyctl auth login
```

### Deploy
```powershell
# Initialize (run in project root)
flyctl launch --name phishing-url-detector --region ord

# Set secrets
flyctl secrets set MODEL_URL="https://github.com/ilyasiii/Phishing-URL-Prediction/releases/download/phishing/xgboost_model.pkl"
flyctl secrets set FEATURE_URL="https://github.com/ilyasiii/Phishing-URL-Prediction/releases/download/phishing/feature_extractor.pkl"

# Deploy
flyctl deploy

# Open in browser
flyctl open
```

---

## 🧪 Testing Your Deployment

### Test the API endpoint
```powershell
curl -X POST https://your-app.onrender.com/predict `
  -H "Content-Type: application/json" `
  -d '{"urls": ["https://google.com", "http://paypa1-secure.com"]}'
```

### Expected Response
```json
{
  "predictions": [0, 1],
  "probabilities": [0.01, 0.99],
  "labels": ["legitimate", "phishing"]
}
```

### Test the UI
1. Open your deployed URL in a browser
2. Enter a URL (e.g., `https://github.com`)
3. Click "Check URL"
4. Should see prediction result within 2-3 seconds

---

## 🔧 Troubleshooting

### Issue: Models fail to download
**Symptoms**: Container crashes on startup, logs show download errors

**Solution**: Verify environment variables are set correctly in Render/Fly dashboard

### Issue: CORS errors in browser console
**Symptoms**: Frontend can't reach backend API

**Solution**: 
1. Check `src/app.py` has CORS middleware enabled
2. For production, update `allow_origins` to include your Vercel domain:
   ```python
   allow_origins=["https://your-app.vercel.app"]
   ```

### Issue: Free tier instance is slow
**Symptoms**: First request takes 30+ seconds

**Reason**: Free tier instances sleep after 15 min inactivity

**Solutions**:
- Upgrade to paid tier ($7/month) for always-on instances
- Use a uptime monitor (UptimeRobot) to ping every 14 minutes
- Accept the cold start delay for demo projects

### Issue: Build fails on Render
**Check**:
1. Dockerfile exists in repository root
2. requirements.txt has all dependencies
3. Build logs for specific error messages

---

## 💰 Cost Estimates

### Free Tier (Recommended for Learning)
- **Render**: 750 hours/month free
- **Vercel**: 100 GB bandwidth/month free
- **Total**: $0/month

### Production (Paid)
- **Render Starter**: $7/month (always-on, 512 MB RAM)
- **Vercel Pro**: $20/month (higher limits, team features)
- **Fly.io**: ~$5/month (shared-cpu-1x, 256 MB RAM)

---

## 🚀 Next Steps

1. ✅ Deploy backend to Render
2. ✅ Test API endpoint with curl/Postman
3. ✅ Deploy frontend (if using Vercel)
4. ✅ Test full workflow in browser
5. 📊 Monitor usage and performance
6. 🔒 Add authentication (optional)
7. 📈 Implement analytics/logging

---

## 📞 Support

- **Issues**: Open a GitHub issue on the repository
- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **Fly.io Docs**: https://fly.io/docs
