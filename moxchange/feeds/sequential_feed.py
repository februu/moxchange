from collections.abc import Iterator

from moxchange.feeds import DataFeed
from moxchange.types import Kline


class SequentialFeed:
    """Combines multiple Kline feeds one after another."""

    def __init__(self, *feeds: DataFeed):
        self._feeds = iter(feeds)
        self._current = next(self._feeds, None)

    def __iter__(self) -> Iterator[Kline]:
        return self

    def __next__(self) -> Kline:
        while self._current is not None:
            try:
                return next(self._current)
            except StopIteration:
                self._current = next(self._feeds, None)
        raise StopIteration
