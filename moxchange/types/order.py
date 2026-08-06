import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from .asset import Asset


@dataclass(frozen=True)
class Order:
    """Immutable representation of a single order."""

    id: uuid.UUID
    account_id: uuid.UUID
    asset: Asset
    quantity: Decimal
    timestamp: datetime

@dataclass(frozen=True)
class MarketOrder(Order):
    """Market order, executed at the current market price."""

@dataclass(frozen=True)
class LimitOrder(Order):
    """Limit order, executed at a specified price or better."""

    limit_price: Decimal

@dataclass(frozen=True)
class StopMarketOrder(Order):
    """Stop market order, executed when the market price reaches a specified stop price."""

    stop_price: Decimal

@dataclass(frozen=True)
class StopLimitOrder(Order):
    """Stop limit order, executed when the market price reaches a specified stop price."""

    stop_price: Decimal
    limit_price: Decimal