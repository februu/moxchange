from dataclasses import dataclass, field
from decimal import Decimal


@dataclass(frozen=True)
class Kline:
    """Represents a single candlestick."""

    symbol: str
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    data: dict = field(default_factory=dict, compare=False)

    def __post_init__(self):
        """Validates that OHLC values are positive and logically consistent."""
        if not all(v > 0 for v in (self.open, self.high, self.low, self.close)):
            raise ValueError(
                f"OHLC values must be positive: open={self.open} high={self.high} low={self.low} close={self.close}"
            )
        if self.high < self.low:
            raise ValueError(f"High must be >= low: high={self.high} low={self.low}")
        if not (self.low <= self.open <= self.high):
            raise ValueError(
                f"Open must be between low and high: open={self.open} high={self.high} low={self.low}"
            )
        if not (self.low <= self.close <= self.high):
            raise ValueError(
                f"Close must be between low and high: close={self.close} high={self.high} low={self.low}"
            )

    def is_bullish(self) -> bool:
        """Returns True if the candlestick is bullish (close > open)."""
        return self.close > self.open

    def is_bearish(self) -> bool:
        """Returns True if the candlestick is bearish (close < open)."""
        return self.close < self.open

    def contains(self, price: Decimal) -> bool:
        """Returns True if the given price is within the high and low of the candlestick."""
        return self.low <= price <= self.high
