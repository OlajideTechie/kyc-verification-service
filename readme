# KYC Passport Verification Service

A minimal backend service that simulates a real-world KYC passport verification flow using a third-party verification provider.

This project was inspired by a stalled KYC onboarding experience, where a passport verification remained “under review” for days with no feedback. The goal is to explore how better system design, state management, and feedback loops can improve trust and user experience during identity verification.

---

## 📜 License References

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
| POST | `/api/verifications/` | Submit passport for verification |
| GET | `/api/verifications/{id}/` | Get verification status |
| POST | `/api/verifications/{id}/retry/` | Retry failed verification |

---

## 🚀 Running Locally

```bash
# Set up virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  

# or 
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

