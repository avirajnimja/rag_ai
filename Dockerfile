# Base image with Python and Ollama
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set up Python environment
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download embedding model
RUN ollama pull mxbai-embed-large
RUN ollama pull llama3:8b

# Copy application code
COPY . .

# Create data directory for vectorstore
RUN mkdir -p /app/data

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV OLLAMA_HOST=0.0.0.0



# Start services (Ollama in background, then app)
CMD ollama serve & \
    sleep 10 && \
    python main.py