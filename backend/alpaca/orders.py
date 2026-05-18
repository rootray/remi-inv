from decimal import Decimal

from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.models import Order
from alpaca.trading.requests import MarketOrderRequest


def place_fractional_buy(client: TradingClient, symbol: str, notional: Decimal) -> Order:
    request = MarketOrderRequest(
        symbol=symbol,
        notional=float(notional),
        side=OrderSide.BUY,
        time_in_force=TimeInForce.DAY,
    )
    return client.submit_order(order_data=request)
