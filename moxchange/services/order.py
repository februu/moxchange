import uuid
from collections import defaultdict

from moxchange.events import EventBus
from moxchange.services import AccountService
from moxchange.types import Asset, Kline, Order


class OrderService:

    def __init__(self, event_bus: EventBus, account_service: AccountService) -> None:
        self._bus = event_bus
        self.account_service = account_service
        self.open_orders: dict[Asset, dict[uuid.UUID, Order]] = defaultdict(dict)

    def place_order(self, order: Order) -> None:
        self.open_orders[order.asset][order.id] = order

    def cancel_order(self, order_id: uuid.UUID, asset: Asset) -> None:
        if order_id in self.open_orders[asset]:
            del self.open_orders[asset][order_id]

    def get_open_orders_for_asset(self, asset: Asset) -> list[Order]:
        return list(self.open_orders[asset].values())

    def get_open_orders_for_account(self, account_id: uuid.UUID) -> list[Order]:
        account = self.account_service.get_account(account_id)
        if not account:
            return []
        return [
            order
            for orders in self.open_orders.values()
            for order in orders.values()
            if order.account_id == account_id
        ]

    def clear_open_orders(self) -> None:
        self.open_orders.clear()

    def match_orders(self, kline : Kline) -> list[Order]:
        ...
    