# DRIP Investing — Progress Map

**Platform:** Web (Next.js frontend + FastAPI backend)
**Tech Stack:** Python 3.12, FastAPI, Celery, Redis, PostgreSQL, Next.js (React), Alpaca API
**GitHub:** [TBD — repo not yet created]
**Orchestration File:** backend/main.py
**Last Updated:** 2026-05-18

---

## Phases

### Phase 1 — Foundation
- [ ] Component: db-session — Database connection pool and session factory
- [ ] Component: db-models — SQLAlchemy ORM models (User, AlpacaCredential, Rule, ReinvestmentLog)
- [ ] Component: auth-register — User sign-up, password hashing, account creation
- [ ] Component: auth-login — Login, JWT token issuance
- [ ] Component: auth-middleware — JWT validation on protected routes
- [ ] Component: api-users — REST endpoints for user profile and Alpaca credentials

### Phase 2 — Alpaca Integration
- [ ] Component: alpaca-client — Authenticated Alpaca SDK instance per user
- [ ] Component: alpaca-portfolio — Fetch holdings and positions from Alpaca
- [ ] Component: alpaca-dividends — Detect dividend activity from Alpaca account history
- [ ] Component: alpaca-orders — Place and track reinvestment buy orders

### Phase 3 — DRIP Automation
- [ ] Component: rules-engine — Evaluate user rules for reinvestment decisions
- [ ] Component: drip-scheduler — Celery periodic task: poll dividends, trigger reinvestment
- [ ] Component: api-portfolio — REST endpoints for holdings, dividend history, reinvestment log
- [ ] Component: api-rules — REST endpoints for CRUD on user reinvestment rules

### Phase 4 — Frontend
- [ ] Component: frontend-api-client — Typed fetch wrapper for backend API calls
- [ ] Component: frontend-auth — Sign-up and login pages
- [ ] Component: frontend-dashboard — Portfolio overview, dividend history, reinvestment log
- [ ] Component: frontend-rules — Rules management UI

---

## Known Issues / Blockers
- GitHub repo not yet created (Step 5 pending user approval)

## Completed Phases
(none yet)
