# Dockerfile for FastAPI backend
FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY static/ ./static/

# Environment variables for model URLs (set these in Render dashboard)
ENV MODEL_URL=""
ENV FEATURE_URL=""
ENV PORT=8000

# Download models at container startup
RUN mkdir -p models

# Expose port
EXPOSE 8000

# Start script that downloads models then runs uvicorn
CMD python scripts/download_model.py \
    --model-url "${MODEL_URL}" \
    --feature-url "${FEATURE_URL}" \
    --out-dir models && \
    uvicorn src.app:app --host 0.0.0.0 --port ${PORT}
