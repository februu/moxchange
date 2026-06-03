from typing import Iterator
from moxchange.types import Kline
from moxchange.feeds import DataFeed


class RoundRobinFeed:
    """Combines multiple Kline feeds into one via round-robin interleaving."""

    def __init__(self, *feeds: DataFeed):
        self._feeds: list[DataFeed] = list(feeds)  # not modified after init
        self._queue: list[DataFeed] = list(feeds)  # round-robin queue
        self._pos = 0

    def __iter__(self) -> Iterator[Kline]:
        return self

    def __next__(self) -> Kline:
        while self._queue:
            feed = self._queue[self._pos % len(self._queue)]
            try:
                kline = next(feed)
                self._pos += 1
                return kline
            except StopIteration:
                self._queue.remove(feed)
        raise StopIteration

    def reset(self):
        """Reset all feeds and the round-robin queue."""
        for feed in self._feeds:
            feed.reset()
        self._queue = list(self._feeds)
        self._pos = 0
