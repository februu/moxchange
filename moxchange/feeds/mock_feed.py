import random
from collections.abc import Iterator
from decimal import Decimal

from moxchange.types import Asset, Kline


class MockFeed:
    """Data feed that generates realistic-looking random Kline data for testing."""

    def __init__(
        self,
        symbol: str,
        amount_of_klines: int = 100,
        starting_price: float = 100.0,
        volatility: float = 0.015,
        drift: float = 0.0001,
        volume_range: tuple[float, float] = (100.0, 1000.0),
        seed: int = 42,
    ):
        self._symbol = symbol
        self._seed = seed
        self._generator = random.Random(seed)
        self._amount_of_klines = amount_of_klines
        self._volatility = volatility
        self._drift = drift
        self._volume_range = volume_range
        self._current_index = 0
        self._starting_price = starting_price
        self._last_close = starting_price

    def __iter__(self) -> Iterator[Kline]:
        return self

    def __next__(self) -> Kline:
        if self._current_index >= self._amount_of_klines:
            raise StopIteration

        open_price = self._last_close

        ticks = [open_price]
        for _ in range(10):
            move = ticks[-1] * self._generator.gauss(self._drift, self._volatility)
            ticks.append(ticks[-1] + move)

        close_price = ticks[-1]
        high_price = max(ticks)
        low_price = min(ticks)

        self._last_close = close_price
        self._current_index += 1

        return Kline(
            asset=Asset(self._symbol),
            open=Decimal(str(round(open_price, 8))),
            high=Decimal(str(round(high_price, 8))),
            low=Decimal(str(round(low_price, 8))),
            close=Decimal(str(round(close_price, 8))),
            data={
                "volume": Decimal(
                    str(
                        round(
                            self._generator.uniform(*self._volume_range),
                            2,
                        )
                    )
                )
            },
        )

    def reset(self):
        """Reset the feed to the initial state."""
        self._generator = random.Random(self._seed)
        self._current_index = 0
        self._last_close = self._starting_price
