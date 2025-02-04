FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .

# Install all dependencies including PyTorch and hf_transfer
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir hf_transfer

# Copy the rest of the application
COPY . .

# Pre-download the model during build
RUN python3 -c 'from transformers import pipeline; pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", timeout=300)'

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]