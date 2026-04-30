from typing import Iterator, Protocol
from moxchange.types import Kline


class DataFeed(Protocol):
    def __iter__(self) -> Iterator[Kline]: ...
