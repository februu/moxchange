from moxchange.types import Account

from .events import AddAccountEvent, EventBus, KlineEvent
from .feeds.data_feed import DataFeed


class Simulator:
    """Simulates a trading environment."""

    def __init__(self, event_bus: EventBus, feed: DataFeed):
        self.event_bus = event_bus
        self.event_bus.subscribe(AddAccountEvent, self._add_account)
        self.feed = feed
        self.accounts : dict[str, Account] = {}

    def step(self):
        """Advances the simulation by one step, processing the next Kline."""
        candle = next(self.feed)
        self.event_bus.publish(KlineEvent(kline=candle))

    def reset(self):
        """Resets the simulation to its initial state."""
        self.feed.reset()
        self.accounts.clear()

    def _add_account(self, event: AddAccountEvent):
        """Adds an account to the simulation."""
        self.accounts[event.account.id] = event.account