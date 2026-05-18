from alpaca.trading.client import TradingClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.crypto import decrypt
from backend.db.models import AlpacaCredential, User


async def get_trading_client(user: User, db: AsyncSession) -> TradingClient:
    credential = await db.scalar(
        select(AlpacaCredential).where(AlpacaCredential.user_id == user.id)
    )
    if credential is None:
        raise ValueError(f"No Alpaca credentials stored for user {user.id}")

    api_key = decrypt(credential.encrypted_api_key)
    secret_key = decrypt(credential.encrypted_secret_key)
    paper = "paper-api.alpaca.markets" in credential.base_url

    return TradingClient(api_key=api_key, secret_key=secret_key, paper=paper)
