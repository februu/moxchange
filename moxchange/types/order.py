import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from .asset import Asset
from .kline import Kline


@dataclass(frozen=True)
class Order:
    """Immutable representation of a single order."""

    id: uuid.UUID
    account_id: uuid.UUID
    asset: Asset
    quantity: Decimal
    timestamp: datetime

    def try_fill(self, kline: Kline) -> tuple[Decimal | None, Order]:
        """Attempts to fill this order against `kline`.

        Returns (fill_price, order_to_keep_in_the_book). `order_to_keep_in_the_book`
        is normally `self`, but an order may replace itself with a different Order
        (e.g. a triggered StopLimitOrder becoming a LimitOrder) instead of filling outright.
        """
        raise NotImplementedError

    def is_buy(self) -> bool:
        """Returns True if this is a buy order, False if it's a sell order."""
        return self.quantity > 0

@dataclass(frozen=True)
class MarketOrder(Order):
    """Market order, executed at the current market price."""

    def try_fill(self, kline: Kline) -> tuple[Decimal | None, Order]:
        return kline.open, self

@dataclass(frozen=True)
class LimitOrder(Order):
    """Limit order, executed at a specified price or better."""

    limit_price: Decimal

    def try_fill(self, kline: Kline) -> tuple[Decimal | None, Order]:
        if self.is_buy():
            if kline.low > self.limit_price:
                return None, self
        else:
            if kline.high < self.limit_price:
                return None, self
        return self.limit_price, self

@dataclass(frozen=True)
class StopMarketOrder(Order):
    """Stop market order, executed when the market price reaches a specified stop price."""

    stop_price: Decimal

    def try_fill(self, kline: Kline) -> tuple[Decimal | None, Order]:
        if self.is_buy():
            if kline.high < self.stop_price:
                return None, self
        else:
            if kline.low > self.stop_price:
                return None, self
        return self.stop_price, self

@dataclass(frozen=True)
class StopLimitOrder(Order):
    """Stop limit order: becomes a LimitOrder once the stop price is reached."""

    stop_price: Decimal
    limit_price: Decimal

    def is_stop_triggered(self, kline: Kline) -> bool:
        if self.is_buy():
            return kline.high >= self.stop_price
        return kline.low <= self.stop_price

    def try_fill(self, kline: Kline) -> tuple[Decimal | None, Order]:
        if not self.is_stop_triggered(kline):
            return None, self

        armed = LimitOrder(
            id=self.id,
            account_id=self.account_id,
            asset=self.asset,
            quantity=self.quantity,
            timestamp=self.timestamp,
            limit_price=self.limit_price,
        )
        return armed.try_fill(kline)
