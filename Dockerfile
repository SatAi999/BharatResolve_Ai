FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for OpenCV, Tesseract OCR, and curl
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create /aikart directory for input/output contract
RUN mkdir -p /aikart

COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY backend/ /app/backend/
COPY aikart/ /app/aikart/

ENV PYTHONPATH=/app/backend

# Default entrypoint for aiKart container execution
CMD ["python", "aikart/run.py"]
