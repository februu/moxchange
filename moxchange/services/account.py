import uuid

from moxchange.events import EventBus
from moxchange.types import Account


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