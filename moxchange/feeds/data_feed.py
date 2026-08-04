from collections.abc import Iterator
from typing import Protocol

from moxchange.types import Kline


class DataFeed(Protocol):
    """Protocol for data feeds that provide Kline data."""

    def __next__(self) -> Kline:
        """Return the next Kline from the feed."""
        ...

    def __iter__(self) -> Iterator[Kline]:
        """Return an iterator over Klines from the feed."""
        ...

    def reset(self) -> None:
        """Reset the feed to the beginning."""
        ...
