# ============================
# Stage 1: Builder
# ============================
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Create a virtual environment and install dependencies
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install -r requirements.txt

# ============================
# Stage 2: Runtime
# ============================
FROM python:3.11-slim

# ---- Timezone + cron + system tools ----
ENV TZ=UTC

# Set working directory
WORKDIR /app

# Install cron + timezone data
RUN apt-get update && \
    apt-get install -y --no-install-recommends cron tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*

# Copy virtualenv from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code (FastAPI app + scripts + keys, etc.)
COPY . /app

# Create volume mount points for /data and /cron
RUN mkdir -p /data /cron && chmod 755 /data /cron \
    && mkdir -p /app/data \
    && ln -s /data /app/data || true

# Expose HTTP port 8080 (as required)
EXPOSE 8080

# Start cron service and FastAPI app
CMD ["/bin/sh", "-c", "cron && uvicorn app.main:app --host 0.0.0.0 --port 8080"]
