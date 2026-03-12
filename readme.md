# KYC Passport Verification Service

A minimal backend service that simulates a real-world KYC passport verification flow using a third-party verification provider.

This project was inspired by a stalled KYC onboarding experience, where a passport verification remained “under review” for days with no feedback. The goal is to explore how better system design, state management, and feedback loops can improve trust and user experience during identity verification.

---

## 📜 License References

![Interswitch](https://img.shields.io/badge/Interswitch-Passport%20Verification-green?style=for-the-badge&logo=shield)](https://www.interswitchgroup.com)
![Python](https://img.shields.io/badge/Python-3.10-blue)
![Django](https://img.shields.io/badge/Django-5.0-darkgreen)
![DRF](https://img.shields.io/badge/DRF-REST--Framework-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791)

---

## 🎯 Objectives

- Model clear KYC verification states
- Integrate with an external passport verification API
- Avoid “silent failures” during onboarding
- Provide transparency and traceability in verification flows

---

## 🔄 Verification Flow

1. User submits passport details
2. Verification request is sent to provider
3. Status transitions through defined states
4. Final result is returned and persisted

---

## 🧱 Core Status States

- `submitted`
- `processing`
- `verified`
- `failed`
- `requires_action`
- `expired`

---

## 🛠 Tech Stack

- Python
- Django + Django REST Framework
- External Verification API (Interswitch)

---

## 📌 Endpoints

| Method | Endpoint | Description |
|------|---------|-------------|
| POST | `/api/start-verifications` | Submit passport for verification |
| GET | `/api/verifications/{verification_id}` | Get verification status |


### Sample API Response

```json
{
  "status": true,
  "verification_id": "9980983d-c162-4279-bf26-33d6ddceb7f0",
  "result": {
    "success": true,
    "code": "200",
    "message": "request processed successfully",
    "data": {
      "first_name": "jane",
      "last_name": "doe",
      "middle_name": "Osas",
      "dob": "12/02/1980",
      "mobile": "08012345678",
      "passport_number": "B0****000",
      "gender": "Male",
      "issued_at": "ALAUSA, LAGOS",
      "issued_date": "01/06/2020",
      "expiry_date": "01/06/2026",
      "document_type": "Standard Passport"
    }
  }
}

---

## 🚀 Running Locally

```bash
# Set up virtual environment
python -m venv venv

# Activate virtual environment (for mac/linux users)
source venv/bin/activate  

# Activate virtual environment (for windows users) 
env\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run migration
python manage.py migrate

# Start the server
python manage.py runserver
```

### Access Swagger docs at
```http://127.0.0.1:8000/swagger/```

