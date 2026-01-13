# Stage 1: Builder
FROM python:3.11-slim as builder
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app

# Set Timezone to UTC
ENV TZ=UTC
RUN apt-get update && apt-get install -y cron tzdata dos2unix && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*

# Copy dependencies from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY app ./app
COPY scripts ./scripts
COPY cron ./cron

# Setup cron job
# Copy the cron file to /etc/cron.d/
COPY cron/2fa-cron /etc/cron.d/2fa-cron
# Give execution rights on the cron job (must be 0644)
RUN dos2unix /etc/cron.d/2fa-cron && \
    chmod 0644 /etc/cron.d/2fa-cron && \
    crontab /etc/cron.d/2fa-cron

# Create volume mount points directory
RUN mkdir -p /data /cron

# Expose port
EXPOSE 8080

# Start cron daemon and FastAPI app
# cron runs in background, uvicorn runs in foreground
CMD ["sh", "-c", "cron && uvicorn app.main:app --host 0.0.0.0 --port 8080"]
