import csv
from typing import Iterator
from decimal import Decimal
from moxchange.types import Kline


class CSVFeed:
    def __init__(self, file_path: str, has_header: bool = True):
        self._file_path = file_path
        self._has_header = has_header

    def __iter__(self) -> Iterator[Kline]:
        with open(self._file_path, "r", newline="") as f:
            reader = csv.reader(f)
            if self._has_header:
                next(reader)
            for row in reader:
                yield self._process_row(row)

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
