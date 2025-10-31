# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

# Install system dependencies including wget for Litestream
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    pkg-config \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf-xlib-2.0-dev \
    postgresql-client \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Litestream
RUN wget https://github.com/benbjohnson/litestream/releases/download/v0.3.13/litestream-v0.3.13-linux-amd64.tar.gz && \
    tar -xzf litestream-v0.3.13-linux-amd64.tar.gz && \
    mv litestream /usr/local/bin/ && \
    rm litestream-v0.3.13-linux-amd64.tar.gz && \
    chmod +x /usr/local/bin/litestream

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy Litestream config
COPY litestream.yml /app/litestream.yml

# Copy and set permissions for startup script
COPY start_with_litestream.sh /app/start_with_litestream.sh
RUN chmod +x /app/start_with_litestream.sh

# Create necessary directories
RUN mkdir -p /app/data

# Expose port
EXPOSE 8080

# Run with Litestream
CMD ["/app/start_with_litestream.sh"]
