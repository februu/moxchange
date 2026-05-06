import csv
from typing import Iterator
from decimal import Decimal
from moxchange.types import Kline


class CSVFeed:
    """Data feed that reads Kline data from a CSV file."""

    def __init__(self, file_path: str, has_header: bool = True):
        self._file_path = file_path
        self._file = open(file_path, "r", newline="")
        self._reader = csv.reader(self._file)
        if has_header:
            next(self._reader)

    def __iter__(self) -> Iterator[Kline]:
        return self

    def __next__(self) -> Kline:
        try:
            row = next(self._reader)
            return self._process_row(row)
        except StopIteration:
            self._file.close()
            raise

    def _process_row(self, row: list[str]) -> Kline:
        timestamp, _open, high, low, close = row[:5]
        volume = Decimal(row[5]) if len(row) > 5 else None
        return Kline(
            timestamp=timestamp,
            open=Decimal(_open),
            high=Decimal(high),
            low=Decimal(low),
            close=Decimal(close),
            volume=volume,
        )
