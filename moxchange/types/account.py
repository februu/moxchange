import uuid
from decimal import Decimal


class Account:
    def __init__(self, id: uuid.UUID, custom_name: str = ""):
        self.id = id
        self.custom_name = custom_name
        self.balance : Decimal = Decimal("0.0")
        self.positions = {}


    def __repr__(self):
        return f"Account(id={self.id}, custom_name={self.custom_name}, balance={self.balance})"