# DRIP Investing — Progress Map

**Platform:** Web (Next.js frontend + FastAPI backend)
**Tech Stack:** Python 3.12, FastAPI, Celery, Redis, PostgreSQL, Next.js (React), Alpaca API
**GitHub:** https://github.com/rootray/remi-inv
**Orchestration File:** backend/main.py
**Last Updated:** 2026-05-18 (Phase 4 — all phases complete)

---

## Phases

### Phase 1 — Foundation
- [x] Component: db-session — Database connection pool and session factory
- [x] Component: db-models — SQLAlchemy ORM models (User, AlpacaCredential, Rule, ReinvestmentLog)
- [x] Component: auth-register — User sign-up, password hashing, account creation
- [x] Component: auth-login — Login, JWT token issuance
- [x] Component: auth-middleware — JWT validation on protected routes
- [x] Component: api-users — REST endpoints for user profile and Alpaca credentials

### Phase 2 — Alpaca Integration
- [x] Component: crypto — Shared Fernet encrypt/decrypt helpers (extracted from api-users)
- [x] Component: alpaca-client — Authenticated Alpaca SDK instance per user
- [x] Component: alpaca-portfolio — Fetch holdings and positions from Alpaca
- [x] Component: alpaca-dividends — Detect dividend activity from Alpaca account history
- [x] Component: alpaca-orders — Place and track reinvestment buy orders

### Phase 3 — DRIP Automation
- [x] Component: rules-engine — Evaluate user rules for reinvestment decisions
- [x] Component: drip-scheduler — Celery periodic task: poll dividends, trigger reinvestment
- [x] Component: api-portfolio — REST endpoints for holdings, dividend history, reinvestment log
- [x] Component: api-rules — REST endpoints for CRUD on user reinvestment rules

### Phase 4 — Frontend
- [x] Component: frontend-api-client — Typed fetch wrapper for backend API calls
- [x] Component: frontend-auth — Sign-up and login pages
- [x] Component: frontend-dashboard — Portfolio overview, dividend history, reinvestment log
- [x] Component: frontend-rules — Rules management UI

---

## Known Issues / Blockers
- GitHub repo not yet created (Step 5 pending user approval)

## Completed Phases
(none yet)
