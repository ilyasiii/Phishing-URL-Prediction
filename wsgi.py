"""
WSGI configuration for PythonAnywhere deployment
This file makes the FastAPI app compatible with PythonAnywhere's WSGI setup
"""
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/Phishing-URL-Prediction'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variables for model URLs
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

# Import the FastAPI app
from src.app import app

# PythonAnywhere requires a WSGI application object called 'application'
application = app
