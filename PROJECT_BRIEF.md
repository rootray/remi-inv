# DRIP Investing — Project Brief

**What it does:** A web application that automates dividend reinvestment (DRIP) for retail investors. Users connect their Alpaca brokerage account, configure reinvestment rules, and the platform automatically detects dividend payouts and places reinvestment buy orders on their behalf — compounding returns without manual intervention.

**Who it is for:** General public — any retail investor with an Alpaca brokerage account.

**Target platform:** Web app (browser-based, no install required).

---

## MVP Features

| Feature | Description |
|---|---|
| DRIP automation | Detect dividend payouts via Alpaca; automatically place reinvestment buy orders |
| User accounts & auth | Sign-up, login, secure per-user Alpaca API key storage |
| Portfolio dashboard | Holdings, dividend history, and full reinvestment activity log |
| Rules engine | User-configurable rules: reinvest all dividends, reinvest above a threshold, target specific stocks |

## Explicit Non-Goals

- No tax reporting — no 1099-DIV generation or tax lot tracking
- No manual trade entry — only DRIP reinvestment orders

---

## Tech Stack

| Layer | Choice | Reason |
|---|---|---|
| Frontend | Next.js (React) | Web-first, fast dashboard builds, SSR capable |
| Backend API | Python + FastAPI | Best Alpaca SDK support, async-ready, clean REST |
| Background jobs | Celery + Redis | Reliable scheduled task execution for automated DRIP |
| Database | PostgreSQL | Relational, battle-tested for financial data |
| Auth | JWT + bcrypt | Simple, stateless, no third-party dependency |
| Brokerage | Alpaca API | Commission-free, paper trading available for dev/test |

---

## Sign-off

Approved by user: 2026-05-18
