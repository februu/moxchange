from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Kline:
    """Represents a single candlestick. Neither timestamp nor volume should be used for any calculations."""

    timestamp: str | None
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: float | None
