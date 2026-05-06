from typing import Iterator, Protocol
from moxchange.types import Kline


class DataFeed(Protocol):
    """Protocol for data feeds that provide Kline data."""

    def __next__(self) -> Kline: ...
    def __iter__(self) -> Iterator[Kline]: ...
