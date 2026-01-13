🔐 PKI-2FA Secure Microservice (Dockerized)
📌 Overview

This project implements a secure, containerized authentication microservice using Public Key Infrastructure (PKI) and Time-based One-Time Password (TOTP) based Two-Factor Authentication (2FA).

The service demonstrates enterprise-grade security practices, combining:

RSA 4096-bit asymmetric cryptography

Secure seed exchange using RSA-OAEP

Commit proof signing using RSA-PSS

TOTP-based 2FA generation and verification

Docker multi-stage builds

Persistent storage using Docker volumes

Automated cron jobs inside a container

🎯 Objectives

Securely receive and decrypt an encrypted seed using RSA

Generate and verify TOTP codes based on the decrypted seed

Persist sensitive data across container restarts

Automate TOTP logging using cron

Provide REST APIs for authentication operations

Package everything into a production-ready Docker container

🧱 Architecture

Language: Python

Framework: FastAPI

Cryptography: RSA (OAEP, PSS), SHA-256

2FA: TOTP (SHA-1, 30s, 6 digits)

Containerization: Docker + Docker Compose

Scheduling: cron (inside container)

Persistence: Docker volumes

🔐 Cryptography Details
RSA Key Pair

Key Size: 4096 bits

Public Exponent: 65537

Format: PEM

Algorithms Used

Seed Decryption: RSA-OAEP (SHA-256, MGF1-SHA256)

Commit Signing: RSA-PSS (SHA-256, max salt length)

Signature Encryption: RSA-OAEP (SHA-256)

🔁 API Endpoints
1️⃣ Decrypt Seed

POST /decrypt-seed

Request

{
  "encrypted_seed": "<base64_string>"
}


Response

{ "status": "ok" }


Stores the decrypted seed at /data/seed.txt.

2️⃣ Generate 2FA Code

GET /generate-2fa

Response

{
  "code": "123456",
  "valid_for": 27
}


Generates a 6-digit TOTP code and returns remaining validity time.

3️⃣ Verify 2FA Code

POST /verify-2fa

Request

{
  "code": "123456"
}


Response

{
  "valid": true
}


Supports ±1 time window tolerance (±30 seconds).

⏱️ Cron Job

Runs every minute

Reads seed from /data/seed.txt

Generates current TOTP code

Logs output to /cron/last_code.txt

Log Format

YYYY-MM-DD HH:MM:SS - 2FA Code: XXXXXX


Timezone: UTC

Line endings enforced using .gitattributes (LF)

🐳 Docker Implementation
Features

Multi-stage Dockerfile (builder + runtime)

Minimal base image (python:3.11-slim)

Cron daemon installed and configured

UTC timezone enforced

Persistent volumes:

/data → decrypted seed

/cron → cron output

Ports

API exposed on port 8080

▶️ Running the Project
Build & Start
docker-compose build
docker-compose up -d

Test APIs

Decrypt Seed

curl -X POST http://localhost:8080/decrypt-seed \
  -H "Content-Type: application/json" \
  -d "{\"encrypted_seed\": \"$(cat encrypted_seed.txt)\"}"


Generate 2FA

curl http://localhost:8080/generate-2fa


Verify 2FA

curl -X POST http://localhost:8080/verify-2fa \
  -H "Content-Type: application/json" \
  -d '{"code":"123456"}'

Check Cron Output
docker exec -it pki-2fa-service sh -c "cat /cron/last_code.txt"

📁 Repository Structure
.
├── app/                  # API source code
├── scripts/              # Utility and proof scripts
├── cron/                 # Cron configuration
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── student_private.pem   # Required (assignment only)
├── student_public.pem
├── instructor_public.pem
├── .gitattributes
├── .gitignore
└── README.md

⚠️ Security Notes

The RSA keys in this repository are ONLY for this assignment

These keys are publicly committed as required

DO NOT reuse these keys for any real system

encrypted_seed.txt and proof files are intentionally not committed

✅ Status

All APIs tested and working

Seed persists across container restarts

Cron job executes correctly

Cryptographic operations match specification

Repository hygiene verified