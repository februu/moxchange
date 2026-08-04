from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, TypeVar

from moxchange.types import Kline


@dataclass(frozen=True)
class KlineEvent:
    """Event representing a Kline (candlestick) data point."""
    kline: Kline

TEvent = TypeVar("TEvent")

class EventBus:
    """Manages and dispatches events."""

    def __init__(self):
        self._subscribers: dict[type, list[Callable[[Any], None]]] = defaultdict(list)

    def subscribe(self, event_type: type[TEvent], handler: Callable[[TEvent], None]) -> None:
        self._subscribers[event_type].append(handler)

    def publish(self, event: object) -> None:
        for handler in self._subscribers[type(event)]:
            handler(event)
