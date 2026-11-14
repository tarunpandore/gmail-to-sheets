# Use lightweight official Python runtime
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies if required
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and default configuration
COPY config.py .
COPY src/ ./src/

# Security: run as non-root user
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/credentials && \
    chown -R appuser:appuser /app

USER appuser

# Disable python stdout buffering and set python path for automation
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app:/app/src"

CMD ["python", "src/main.py"]
