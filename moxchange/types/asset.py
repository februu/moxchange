from dataclasses import dataclass


@dataclass(frozen=True)
class Asset:
    """Immutable representation of a single financial instrument."""
    symbol: str

    def __repr__(self) -> str:
        return self.symbol

    def __str__(self) -> str:
        return self.symbol

    def __hash__(self) -> int:
        return hash(self.symbol)