# PKI-2FA-Microservice-With-Docker

Enterpise-grade authentication microservice with PKI and TOTP.

## Requirements
- Docker & Docker Compose
- Python 3.11+ (for local scripts)

## Setup
1. Clone repository
2. `docker-compose up -d --build`

## Endpoints
- `POST /decrypt-seed`
- `GET /generate-2fa`
- `POST /verify-2fa`

## Cron
Logs 2FA codes to `/cron/last_code.txt` every minute.
