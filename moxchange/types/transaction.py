from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class Transaction:
    """Immutable record of a single fill against a position."""

    symbol: str
    quantity: Decimal
    price: Decimal
    timestamp: datetime
    realized_pnl: Decimal = Decimal(0)
