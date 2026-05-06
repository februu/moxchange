from dataclasses import dataclass
from enum import Enum
from collections import defaultdict
from typing import Callable

from moxchange.types import Kline


class EventType(Enum):
    """Defines the types of events that can occur in the simulation."""

    CANDLE = "CANDLE"


@dataclass
class Event:
    """Represents a single event."""

    type: EventType
    payload: Kline


class EventBus:
    """Manages and dispatches events."""

    def __init__(self):
        self._subscribers: dict[EventType, list[Callable]] = defaultdict(list)

    def subscribe(self, event_type: EventType, handler: Callable):
        self._subscribers[event_type].append(handler)

    def publish(self, event: Event):
        for handler in self._subscribers[event.type]:
            handler(event)
