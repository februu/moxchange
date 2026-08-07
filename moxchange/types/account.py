import uuid
from collections import defaultdict
from decimal import Decimal

from .asset import Asset
from .position import Position
from .transaction import Transaction


class Account:
    def __init__(self, id: uuid.UUID, custom_name: str = ""):
        self.id = id
        self.custom_name = custom_name
        self.balance : Decimal = Decimal("0.0")
        self._positions : dict[Asset, Position] = defaultdict()
        self.transactions : list[Transaction] = []


    def __repr__(self):
        return f"Account(id={self.id}, custom_name={self.custom_name}, balance={self.balance})"

    def get_or_create_position(self, asset: Asset) -> Position:
        if asset not in self._positions:
            self._positions[asset] = Position(asset=asset)
        return self._positions[asset]

    def add_transaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)