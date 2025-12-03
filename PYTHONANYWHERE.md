# PythonAnywhere Deployment Guide

Complete step-by-step guide to deploy your Phishing URL Detector on PythonAnywhere (100% Free).

## Prerequisites

- A [PythonAnywhere](https://www.pythonanywhere.com) free account
- Your GitHub repository: `https://github.com/ilyasiii/Phishing-URL-Prediction`

---

## Step 1: Create PythonAnywhere Account

1. Go to [PythonAnywhere.com](https://www.pythonanywhere.com)
2. Click **Pricing & signup** → **Create a Beginner account** (Free)
3. Sign up with email (no credit card required)
4. Verify your email

---

## Step 2: Open a Bash Console

1. From your PythonAnywhere dashboard, click **Consoles**
2. Click **Bash** to open a new console
3. Clone your repository:

```bash
git clone https://github.com/ilyasiii/Phishing-URL-Prediction.git
cd Phishing-URL-Prediction
```

---

## Step 3: Create Virtual Environment

```bash
# Create virtual environment with Python 3.10
mkvirtualenv --python=/usr/bin/python3.10 phishing-env

# Activate it (should auto-activate after creation)
workon phishing-env

# Install dependencies
pip install -r requirements.txt
```

**Note**: This may take 5-10 minutes. If you see memory errors, it's normal on free tier - just retry.

---

## Step 4: Download Model Files

```bash
# Make sure you're in the project directory
cd ~/Phishing-URL-Prediction

# Download models
python scripts/download_model.py \
  --model-url "https://github.com/ilyasiii/Phishing-URL-Prediction/releases/download/phishing/xgboost_model.pkl" \
  --feature-url "https://github.com/ilyasiii/Phishing-URL-Prediction/releases/download/phishing/feature_extractor.pkl" \
  --out-dir models

# Verify downloads
ls -lh models/
```

You should see two files: `xgboost_model.pkl` (~265 KB) and `feature_extractor.pkl` (~1.29 MB)

---

## Step 5: Configure Web App

1. Go to **Web** tab in PythonAnywhere dashboard
2. Click **Add a new web app**
3. Choose **Manual configuration** (not Flask/Django)
4. Select **Python 3.10**
5. Click **Next**

---

## Step 6: Configure WSGI File

1. On the Web tab, find **Code** section
2. Click on the WSGI configuration file link (e.g., `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
3. **Delete all existing content** in the file
4. Copy and paste this configuration:

```python
import sys
import os

# IMPORTANT: Replace 'yourusername' with your PythonAnywhere username
project_home = '/home/yourusername/Phishing-URL-Prediction'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variables
os.environ['MODEL_URL'] = 'https://github.com/ilyasiii/Phishing-URL-Prediction/releases/download/phishing/xgboost_model.pkl'
os.environ['FEATURE_URL'] = 'https://github.com/ilyasiii/Phishing-URL-Prediction/releases/download/phishing/feature_extractor.pkl'

# Download models if they don't exist
models_dir = os.path.join(project_home, 'models')
model_path = os.path.join(models_dir, 'xgboost_model.pkl')
feature_path = os.path.join(models_dir, 'feature_extractor.pkl')

if not os.path.exists(model_path) or not os.path.exists(feature_path):
    print("Downloading model files...")
    import subprocess
    subprocess.run([
        sys.executable, 
        os.path.join(project_home, 'scripts', 'download_model.py'),
        '--model-url', os.environ['MODEL_URL'],
        '--feature-url', os.environ['FEATURE_URL'],
        '--out-dir', models_dir
    ])

# Import FastAPI app
from src.app import app
application = app
```

5. **Replace `yourusername`** with your actual PythonAnywhere username (appears in the URL)
6. Click **Save**

---

## Step 7: Set Virtual Environment

1. Still on the **Web** tab, find **Virtualenv** section
2. Enter the path to your virtual environment:
   ```
   /home/yourusername/.virtualenvs/phishing-env
   ```
   (Replace `yourusername` with your username)
3. PythonAnywhere will verify it exists

---

## Step 8: Configure Static Files

1. On the **Web** tab, scroll to **Static files** section
2. Click **Enter URL** and **Enter path**:
   - **URL**: `/static/`
   - **Directory**: `/home/yourusername/Phishing-URL-Prediction/static/`
   
   (Replace `yourusername` with your username)

---

## Step 9: Reload and Test

1. Scroll to the top of the **Web** tab
2. Click the big green **Reload** button
3. Wait 10-20 seconds
4. Click the link at the top: `http://yourusername.pythonanywhere.com`

Your app should now be live! 🎉

---

## Testing Your Deployment

### Test the UI
1. Open `http://yourusername.pythonanywhere.com` in your browser
2. Enter a URL like `https://github.com`
3. Click **Check URL**
4. You should see a prediction result

### Test the API
```bash
curl -X POST http://yourusername.pythonanywhere.com/predict \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://google.com", "http://paypa1-secure.com"]}'
```

Expected response:
```json
{
  "predictions": [0, 1],
  "probabilities": [0.01, 0.99],
  "labels": ["legitimate", "phishing"]
}
```

---

## Troubleshooting

### Issue: 502 Bad Gateway
**Solution**: Check error log on Web tab → Log files → Error log

Common causes:
- Typo in WSGI file path
- Virtual environment path incorrect
- Missing dependencies

### Issue: Models not loading
**Solution**: 
1. Open Bash console
2. Run model download manually:
```bash
cd ~/Phishing-URL-Prediction
workon phishing-env
python scripts/download_model.py \
  --model-url "https://github.com/ilyasiii/Phishing-URL-Prediction/releases/download/phishing/xgboost_model.pkl" \
  --feature-url "https://github.com/ilyasiii/Phishing-URL-Prediction/releases/download/phishing/feature_extractor.pkl" \
  --out-dir models
```

### Issue: Import errors
**Solution**: Verify all dependencies installed
```bash
workon phishing-env
pip install -r requirements.txt
```

### Issue: Static files not loading
**Solution**: Check static files mapping on Web tab matches exactly:
- URL: `/static/`
- Path: `/home/yourusername/Phishing-URL-Prediction/static/`

---

## Updating Your App

When you push changes to GitHub:

```bash
# In PythonAnywhere Bash console
cd ~/Phishing-URL-Prediction
git pull origin main

# If requirements changed
workon phishing-env
pip install -r requirements.txt

# Reload from Web tab
```

Or reload via command line:
```bash
touch /var/www/yourusername_pythonanywhere_com_wsgi.py
```

---

## PythonAnywhere Free Tier Limits

✅ **What's included (FREE)**:
- 1 web app (with your domain: `yourusername.pythonanywhere.com`)
- 512 MB disk space
- Python 3.10 support
- Always-on (no cold starts)
- HTTPS included
- 100 seconds daily CPU time

⚠️ **Limitations**:
- Can only access whitelisted sites (GitHub is whitelisted ✓)
- Web app auto-sleeps after 3 months of inactivity (just reload to restart)
- No SSH access (use web console)

For most projects, the free tier is perfect for demos and portfolios!

---

## Upgrading (Optional)

If you need more resources:
- **Hacker plan**: $5/month (more CPU, multiple apps, longer timeout)
- **Custom domains** supported on paid plans

---

## Next Steps

- ✅ Share your live URL: `http://yourusername.pythonanywhere.com`
- 📊 Monitor usage in PythonAnywhere dashboard
- 🔒 Consider adding authentication for production use
- 📈 Track predictions (add logging/analytics)

---

## Support

- PythonAnywhere Help: https://help.pythonanywhere.com/
- Forums: https://www.pythonanywhere.com/forums/
- GitHub Issues: Open an issue on your repository
