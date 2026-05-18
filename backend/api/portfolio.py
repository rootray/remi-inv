from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.alpaca.client import get_trading_client
from backend.alpaca.dividends import get_recent_dividends
from backend.alpaca.portfolio import get_positions
from backend.auth.middleware import get_current_user
from backend.db.models import ReinvestmentLog, User
from backend.db.session import get_db

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/positions")
async def list_positions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    client = await get_trading_client(current_user, db)
    positions = get_positions(client)
    return [
        {
            "symbol": p.symbol,
            "qty": p.qty,
            "market_value": p.market_value,
            "unrealized_pl": p.unrealized_pl,
            "current_price": p.current_price,
        }
        for p in positions
    ]


@router.get("/dividends")
async def list_dividends(
    since: Optional[datetime] = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    if since is None:
        since = datetime.now(timezone.utc) - timedelta(days=30)
    client = await get_trading_client(current_user, db)
    dividends = get_recent_dividends(client, since)
    return [
        {
            "symbol": d.symbol,
            "net_amount": str(d.net_amount),
            "date": str(d.date),
        }
        for d in dividends
    ]


@router.get("/reinvestment-log")
async def list_reinvestment_log(
    limit: int = Query(default=50, le=200),
    offset: int = Query(default=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    logs = list(await db.scalars(
        select(ReinvestmentLog)
        .where(ReinvestmentLog.user_id == current_user.id)
        .order_by(ReinvestmentLog.executed_at.desc())
        .limit(limit)
        .offset(offset)
    ))
    return [
        {
            "id": log.id,
            "source_symbol": log.source_symbol,
            "target_symbol": log.target_symbol,
            "dividend_amount": str(log.dividend_amount),
            "shares_purchased": str(log.shares_purchased) if log.shares_purchased else None,
            "alpaca_order_id": log.alpaca_order_id,
            "status": log.status.value,
            "error_message": log.error_message,
            "executed_at": log.executed_at.isoformat(),
        }
        for log in logs
    ]
