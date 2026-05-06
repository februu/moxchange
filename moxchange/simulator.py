from .events import EventBus, Event, EventType
from .feeds.data_feed import DataFeed


class Simulator:
    """Simulates a trading environment."""

    def __init__(self, event_bus: EventBus, feed: DataFeed):
        self.event_bus = event_bus
        self.feed = feed

    def step(self):
        """Advances the simulation by one step, processing the next Kline."""
        candle = next(self.feed)
        self.event_bus.publish(Event(type=EventType.CANDLE, payload=candle))
