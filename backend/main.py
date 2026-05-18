from fastapi import FastAPI

from backend.api.portfolio import router as portfolio_router
from backend.api.rules import router as rules_router
from backend.api.users import router as users_router
from backend.auth.login import router as login_router
from backend.auth.register import router as register_router

app = FastAPI(title="DRIP Investing API")

app.include_router(register_router)
app.include_router(login_router)
app.include_router(users_router)
app.include_router(portfolio_router)
app.include_router(rules_router)

# db-session:         provides get_db() dependency — imported by all route handlers
# db-models:          User, AlpacaCredential, Rule, ReinvestmentLog — imported by all components that touch the DB
# crypto:             encrypt/decrypt helpers for Alpaca credentials — shared by api-users and alpaca-client
# auth-register:      POST /auth/register
# auth-login:         POST /auth/login
# auth-middleware:    get_current_user — Depends() used by all protected routes
# api-users:          GET /users/me, PUT /users/me/credentials, GET /users/me/credentials
# alpaca-client:      get_trading_client(user, db) — decrypts credentials, returns TradingClient
# alpaca-portfolio:   get_positions(client) — returns list of Position
# alpaca-dividends:   get_recent_dividends(client, since) — returns DIV activities since datetime
# alpaca-orders:      place_fractional_buy(client, symbol, notional) — submits notional market buy
# rules-engine:       evaluate(rules, source_symbol, dividend_amount) — returns (target_symbol, should_reinvest)
# drip-scheduler:     Celery beat task — polls dividends hourly, evaluates rules, places orders
# api-portfolio:      GET /portfolio/positions, /portfolio/dividends, /portfolio/reinvestment-log
# api-rules:          GET/POST /rules, PATCH/DELETE /rules/{id}
