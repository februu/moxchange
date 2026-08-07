from moxchange.services import AccountService, OrderService

from .events import EventBus, KlineEvent
from .feeds.data_feed import DataFeed


class Simulator:
    """Simulates a trading environment."""

    def __init__(self, event_bus: EventBus, feed: DataFeed, account_service: AccountService, order_service: OrderService) -> None:
        self.event_bus = event_bus
        self.feed = feed
        self.account_service = account_service
        self.order_service = order_service

    def step(self):
        """Advances the simulation by one step, processing the next Kline."""
        candle = next(self.feed)
        self.event_bus.publish(KlineEvent(kline=candle))
        self.account_service.update_positions(candle)
        self.order_service.execute_orders(candle)

    def reset(self):
        """Resets the simulation to its initial state."""
        self.feed.reset()
        self.account_service.clear()