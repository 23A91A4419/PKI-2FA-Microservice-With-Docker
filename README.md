# PKI-2FA Microservice

This project implements a PKI-based Two-Factor Authentication system using:
- RSA encryption/decryption  
- Seed decryption using private key  
- TOTP generation using the decrypted seed  
- FastAPI microservice with 3 working endpoints  

---

## 🚀 API Endpoints

---

### 1️⃣ POST /decrypt-seed  
Decrypts the encrypted seed and stores the hex seed in `data/seed.txt`.

**Response:**
```json
{
  "status": "ok"
}


{
  "code": "123456",
  "valid_for": 30
}

{
  "code": "123456"
}

{ "valid": true }

{ "valid": false }
