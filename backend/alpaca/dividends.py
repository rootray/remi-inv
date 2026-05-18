from datetime import datetime

from alpaca.trading.client import TradingClient
from alpaca.trading.enums import ActivityType
from alpaca.trading.requests import GetAccountActivitiesRequest


def get_recent_dividends(client: TradingClient, since: datetime) -> list:
    request = GetAccountActivitiesRequest(
        activity_types=[ActivityType.DIV],
        after=since,
    )
    return client.get_account_activities(activity_filter=request)
