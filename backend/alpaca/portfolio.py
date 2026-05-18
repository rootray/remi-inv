from alpaca.trading.client import TradingClient
from alpaca.trading.models import Position


def get_positions(client: TradingClient) -> list[Position]:
    return client.get_all_positions()
