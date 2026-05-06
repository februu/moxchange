from ..feeds.data_feed import DataFeed


class Simulator:
    """Simulates a trading environment."""

    def __init__(self, feed: DataFeed):
        self.feed = feed

    def step(self):
        """Advances the simulation by one step, processing the next Kline."""
        candle = next(self.feed)
        print(f"Simulated candle: {candle}")
