#!/bin/bash
# Startup script for Render deployment

echo "Downloading model artifacts..."
python scripts/download_model.py \
  --model-url "${MODEL_URL}" \
  --feature-url "${FEATURE_URL}" \
  --out-dir models

if [ $? -eq 0 ]; then
    echo "Models downloaded successfully"
else
    echo "Failed to download models"
    exit 1
fi

echo "Starting FastAPI server..."
exec uvicorn src.app:app --host 0.0.0.0 --port ${PORT:-8000}
