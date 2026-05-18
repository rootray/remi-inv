from fastapi import FastAPI

from backend.api.users import router as users_router
from backend.auth.login import router as login_router
from backend.auth.register import router as register_router

app = FastAPI(title="DRIP Investing API")

app.include_router(register_router)
app.include_router(login_router)
app.include_router(users_router)

# db-session: provides get_db() dependency — imported by all route handlers
# db-models: User, AlpacaCredential, Rule, ReinvestmentLog — imported by all components that touch the DB
# auth-register:    POST /auth/register
# auth-login:       POST /auth/login
# auth-middleware:  get_current_user — Depends() used by all protected routes
# api-users:        GET /users/me, PUT /users/me/credentials, GET /users/me/credentials
