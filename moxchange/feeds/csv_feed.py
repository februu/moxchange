import csv
from typing import Iterator
from decimal import Decimal
from moxchange.types import Kline


class CSVFeed:
    """Data feed that reads Kline data from a CSV file."""

    def __init__(self, file_path: str, has_header: bool = True):
        self._file_path = file_path
        self._file = open(file_path, "r", newline="")
        self._has_header = has_header
        if self._has_header:
            self._reader = csv.DictReader(self._file)
        else:
            self._reader = csv.reader(self._file)

    def __iter__(self) -> Iterator[Kline]:
        return self

    def __next__(self) -> Kline:
        try:
            row = next(self._reader)
            return self._process_row(row)
        except StopIteration:
            self._file.close()
            raise

    def _process_row(self, row) -> Kline:
        if self._has_header:
            additional_data = {
                k: v
                for k, v in row.items()
                if k.lower() not in {"open", "high", "low", "close"}
            }
            return Kline(
                open=Decimal(row["open"]),
                high=Decimal(row["high"]),
                low=Decimal(row["low"]),
                close=Decimal(row["close"]),
                data=additional_data,
            )
        else:
            _open, high, low, close = row[:4]
            return Kline(
                open=Decimal(_open),
                high=Decimal(high),
                low=Decimal(low),
                close=Decimal(close),
            )

    def reset(self):
        """Reset the feed to the beginning of the file."""
        self._file.seek(0)
        if self._has_header:
            self._reader = csv.DictReader(self._file)
        else:
            self._reader = csv.reader(self._file)
