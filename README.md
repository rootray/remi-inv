# DRIP Investing

> A web application that automatically reinvests dividend payouts into your Alpaca brokerage account, compounding returns without manual intervention.

---

## Prerequisites

- Python 3.12+
- Node.js 20+
- PostgreSQL
- Redis
- An [Alpaca](https://alpaca.markets) brokerage account (paper trading supported)

---

## Installation

```bash
git clone [repo URL]
cd drip-investing

# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

---

## Environment Setup

Copy `.env.example` to `.env` and fill in the required values:

```bash
cp .env.example .env
```

| Variable | Description | Required |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `JWT_SECRET_KEY` | Secret for signing JWT tokens | Yes |
| `JWT_EXPIRE_MINUTES` | Token expiry in minutes (default: 60) | No |
| `REDIS_URL` | Redis connection URL for Celery | Yes |
| `DRIP_POLL_INTERVAL_SECONDS` | How often to check for new dividends (default: 300) | No |
| `ALPACA_BASE_URL` | Alpaca API base URL (use paper URL for dev) | Yes |
| `CREDENTIAL_ENCRYPTION_KEY` | Key for encrypting stored Alpaca API keys | Yes |
| `FRONTEND_URL` | Frontend URL for CORS (default: http://localhost:3000) | Yes |

---

## How to Run

**Backend API:**
```bash
uvicorn backend.main:app --reload
```

**Celery worker + scheduler:**
```bash
celery -A backend.jobs.drip_scheduler worker --loglevel=info
celery -A backend.jobs.drip_scheduler beat --loglevel=info
```

**Frontend:**
```bash
cd frontend && npm run dev
```

---

## Features

### DRIP Automation
Automatically detects dividend payouts on your Alpaca account and places reinvestment buy orders according to your configured rules.

### User Accounts
Sign up, log in, and securely connect your Alpaca API credentials. Keys are encrypted at rest.

### Portfolio Dashboard
View your current holdings, dividend history, and a full log of every reinvestment order placed.

### Rules Engine
Configure how dividends are reinvested:
- Reinvest all dividends immediately
- Reinvest only when the payout exceeds a threshold amount
- Reinvest into a specific stock regardless of which stock paid the dividend

---

## Running Tests

```bash
# Backend
pytest backend/

# Frontend
cd frontend && npm test
```

---

## Known Issues / Limitations

- [TBD as development progresses]
