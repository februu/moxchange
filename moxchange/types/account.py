import uuid


class Account:
    def __init__(self, custom_name: str = ""):
        self.id = str(uuid.uuid4())
        self.custom_name = custom_name
        self.balance = 0.0
        self.positions = {}


    def __repr__(self):
        return f"Account(id={self.id}, custom_name={self.custom_name}, balance={self.balance})"