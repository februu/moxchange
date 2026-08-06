from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from .asset import Asset


@dataclass(frozen=True)
class Transaction:
    """Immutable record of a single fill against a position."""

    asset: Asset
    quantity: Decimal
    price: Decimal
    timestamp: datetime
    realized_pnl: Decimal = Decimal(0)
