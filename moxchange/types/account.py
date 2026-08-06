import uuid
from collections import defaultdict
from decimal import Decimal

from moxchange.types import Position


class Account:
    def __init__(self, id: uuid.UUID, custom_name: str = ""):
        self.id = id
        self.custom_name = custom_name
        self.balance : Decimal = Decimal("0.0")
        self.positions : dict[str, Position] = defaultdict()


    def __repr__(self):
        return f"Account(id={self.id}, custom_name={self.custom_name}, balance={self.balance})"