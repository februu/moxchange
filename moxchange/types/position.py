from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from .transaction import Transaction


def _sign(value: Decimal) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


@dataclass
class Position:
    """Net exposure to a symbol, built up by netting a sequence of trades."""

    symbol: str
    quantity: Decimal = Decimal(0)      # signed: positive for long, negative for short
    entry_price: Decimal = Decimal(0)
    leverage: Decimal = Decimal(1)

    @property
    def is_open(self) -> bool:
        return self.quantity != 0

    def unrealized_pnl(self, mark_price: Decimal) -> Decimal:
        return (mark_price - self.entry_price) * self.quantity

    def margin_used(self) -> Decimal:
        return abs(self.quantity) * self.entry_price / self.leverage

    def apply_transaction(self, quantity: Decimal, price: Decimal, timestamp: datetime) -> Transaction:
        """Nets a fill into this position, updating quantity/entry_price in place.

        `quantity` is signed: positive buys, negative sells. Returns the resulting
        Transaction record
        """
        if quantity == 0:
            raise ValueError("transaction quantity must not be zero")

        realized_pnl = Decimal(0)

        if self.quantity == 0 or _sign(self.quantity) == _sign(quantity):
            # opening or adding to the position: roll into a weighted-average entry price
            new_quantity = self.quantity + quantity
            self.entry_price = (
                self.entry_price * self.quantity + price * quantity
            ) / new_quantity
            self.quantity = new_quantity
        else:
            # reducing, closing, or flipping through zero
            closing_amount = min(abs(quantity), abs(self.quantity))
            realized_pnl = (price - self.entry_price) * closing_amount * _sign(self.quantity)

            new_quantity = self.quantity + quantity
            if new_quantity == 0:
                self.entry_price = Decimal(0)
            elif _sign(new_quantity) != _sign(self.quantity):
                # flipped: the remainder beyond what closed the old side opens fresh
                self.entry_price = price
            self.quantity = new_quantity

        return Transaction(
            symbol=self.symbol,
            quantity=quantity,
            price=price,
            timestamp=timestamp,
            realized_pnl=realized_pnl,
        )
