import asyncio
import os
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from celery import Celery
from sqlalchemy import select

from backend.alpaca.client import get_trading_client
from backend.alpaca.dividends import get_recent_dividends
from backend.alpaca.orders import place_fractional_buy
from backend.db.models import AlpacaCredential, ReinvestmentLog, ReinvestmentStatus, Rule, User
from backend.db.session import AsyncSessionLocal
from backend.rules.engine import evaluate

app = Celery("drip", broker=os.environ.get("REDIS_URL", "redis://localhost:6379/0"))

app.conf.beat_schedule = {
    "poll-dividends": {
        "task": "backend.jobs.drip_scheduler.poll_dividends",
        "schedule": 3600.0,  # hourly
    },
}


@app.task(name="backend.jobs.drip_scheduler.poll_dividends")
def poll_dividends() -> None:
    asyncio.run(_poll_all_users())


async def _poll_all_users() -> None:
    async with AsyncSessionLocal() as db:
        user_ids = list(await db.scalars(select(AlpacaCredential.user_id)))
    for user_id in user_ids:
        try:
            await _process_user(user_id)
        except Exception:
            pass  # isolate per-user failures


async def _process_user(user_id: int) -> None:
    async with AsyncSessionLocal() as db:
        user = await db.get(User, user_id)
        if user is None or not user.is_active:
            return

        client = await get_trading_client(user, db)
        since = datetime.now(timezone.utc) - timedelta(hours=25)
        dividends = get_recent_dividends(client, since)

        rules = list(await db.scalars(
            select(Rule).where(Rule.user_id == user_id, Rule.is_active.is_(True))
        ))

        for div in dividends:
            amount = Decimal(str(div.net_amount))

            # Skip dividends already logged (deduplication by symbol + amount)
            already_logged = await db.scalar(
                select(ReinvestmentLog).where(
                    ReinvestmentLog.user_id == user.id,
                    ReinvestmentLog.source_symbol == div.symbol,
                    ReinvestmentLog.dividend_amount == amount,
                )
            )
            if already_logged:
                continue

            target_symbol, should_reinvest = evaluate(rules, div.symbol, amount)

            log = ReinvestmentLog(
                user_id=user.id,
                source_symbol=div.symbol,
                target_symbol=target_symbol,
                dividend_amount=amount,
                status=ReinvestmentStatus.pending,
            )

            if should_reinvest:
                try:
                    order = place_fractional_buy(client, target_symbol, amount)
                    log.alpaca_order_id = str(order.id)
                    log.status = ReinvestmentStatus.filled
                except Exception as exc:
                    log.status = ReinvestmentStatus.failed
                    log.error_message = str(exc)[:500]
            else:
                log.status = ReinvestmentStatus.failed
                log.error_message = "No matching active rule"

            db.add(log)

        await db.commit()
