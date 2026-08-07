import uuid
from datetime import datetime
from decimal import Decimal

from moxchange.events import EventBus
from moxchange.types import Account, Asset, Kline


class AccountService:
    """Keeps track of accounts."""

    def __init__(self, event_bus: EventBus) -> None:
        self._bus = event_bus
        self._accounts: dict[uuid.UUID, Account] = {}

    def add_account(self, name: str) -> Account:
        account = Account(id=uuid.uuid4(), custom_name=name)
        self._accounts[account.id] = account
        return account

    def get_account(self, account_id: uuid.UUID) -> Account | None:
        return self._accounts.get(account_id)

    def clear(self) -> None:
        self._accounts.clear()

    def update_positions(self, kline : Kline) -> None:
        ...

    def apply_fill(
        self, account_id: uuid.UUID, asset: Asset, quantity: Decimal, price: Decimal, timestamp: datetime
    ) -> None:
        """Nets a fill into the account's position for `asset`. Returns None if the account doesn't exist."""
        account = self._accounts[account_id]
        position = account.get_or_create_position(asset)
        transaction = position.apply_transaction(quantity, price, timestamp)
        account.add_transaction(transaction)