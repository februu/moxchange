import uuid
from datetime import datetime
from decimal import Decimal

from moxchange.types import (
    Asset,
    Kline,
    LimitOrder,
    MarketOrder,
    StopLimitOrder,
    StopMarketOrder,
)

ASSET = Asset("BTC")
NOW = datetime(2024, 1, 1)


def make_kline(open, high, low, close) -> Kline:
    return Kline(
        asset=ASSET,
        open=Decimal(str(open)),
        high=Decimal(str(high)),
        low=Decimal(str(low)),
        close=Decimal(str(close)),
    )


def make_market_order(quantity=1) -> MarketOrder:
    return MarketOrder(
        id=uuid.uuid4(), account_id=uuid.uuid4(), asset=ASSET, quantity=Decimal(quantity), timestamp=NOW
    )


def make_limit_order(quantity=1, limit_price=100) -> LimitOrder:
    return LimitOrder(
        id=uuid.uuid4(), account_id=uuid.uuid4(), asset=ASSET, quantity=Decimal(quantity), timestamp=NOW,
        limit_price=Decimal(str(limit_price)),
    )


def make_stop_market_order(quantity=1, stop_price=100) -> StopMarketOrder:
    return StopMarketOrder(
        id=uuid.uuid4(), account_id=uuid.uuid4(), asset=ASSET, quantity=Decimal(quantity), timestamp=NOW,
        stop_price=Decimal(str(stop_price)),
    )


def make_stop_limit_order(quantity=1, stop_price=100, limit_price=105) -> StopLimitOrder:
    return StopLimitOrder(
        id=uuid.uuid4(), account_id=uuid.uuid4(), asset=ASSET, quantity=Decimal(quantity), timestamp=NOW,
        stop_price=Decimal(str(stop_price)), limit_price=Decimal(str(limit_price)),
    )


class TestMarketOrder:
    def test_fills_at_open(self):
        order = make_market_order(quantity=1)
        kline = make_kline(open=100, high=110, low=90, close=105)

        price, kept = order.try_fill(kline)

        assert price == Decimal(100)
        assert kept is order

    def test_fills_regardless_of_side(self):
        buy = make_market_order(quantity=1)
        sell = make_market_order(quantity=-1)
        kline = make_kline(open=50, high=60, low=40, close=55)

        assert buy.try_fill(kline)[0] == Decimal(50)
        assert sell.try_fill(kline)[0] == Decimal(50)


class TestLimitOrder:
    def test_buy_fills_when_low_reaches_limit(self):
        order = make_limit_order(quantity=1, limit_price=100)
        kline = make_kline(open=105, high=110, low=100, close=102)

        price, kept = order.try_fill(kline)

        assert price == Decimal(100)
        assert kept is order

    def test_buy_does_not_fill_when_low_stays_above_limit(self):
        order = make_limit_order(quantity=1, limit_price=100)
        kline = make_kline(open=105, high=110, low=101, close=108)

        price, kept = order.try_fill(kline)

        assert price is None
        assert kept is order

    def test_buy_fills_at_exact_limit_even_when_bar_gaps_far_below(self):
        order = make_limit_order(quantity=1, limit_price=100)
        kline = make_kline(open=60, high=65, low=55, close=62)

        price, _ = order.try_fill(kline)

        assert price == Decimal(100)

    def test_sell_fills_when_high_reaches_limit(self):
        order = make_limit_order(quantity=-1, limit_price=100)
        kline = make_kline(open=95, high=100, low=90, close=98)

        price, kept = order.try_fill(kline)

        assert price == Decimal(100)
        assert kept is order

    def test_sell_does_not_fill_when_high_stays_below_limit(self):
        order = make_limit_order(quantity=-1, limit_price=100)
        kline = make_kline(open=90, high=99, low=85, close=92)

        price, _ = order.try_fill(kline)

        assert price is None

    def test_sell_fills_at_exact_limit_even_when_bar_gaps_far_above(self):
        order = make_limit_order(quantity=-1, limit_price=100)
        kline = make_kline(open=150, high=155, low=145, close=148)

        price, _ = order.try_fill(kline)

        assert price == Decimal(100)


class TestStopMarketOrder:
    def test_buy_triggers_when_high_reaches_stop(self):
        order = make_stop_market_order(quantity=1, stop_price=100)
        kline = make_kline(open=95, high=100, low=90, close=98)

        price, kept = order.try_fill(kline)

        assert price == Decimal(100)
        assert kept is order

    def test_buy_does_not_trigger_when_high_stays_below_stop(self):
        order = make_stop_market_order(quantity=1, stop_price=100)
        kline = make_kline(open=90, high=99, low=85, close=92)

        price, _ = order.try_fill(kline)

        assert price is None

    def test_buy_fills_at_exact_stop_even_when_bar_gaps_far_above(self):
        order = make_stop_market_order(quantity=1, stop_price=100)
        kline = make_kline(open=150, high=155, low=145, close=148)

        price, _ = order.try_fill(kline)

        assert price == Decimal(100)

    def test_sell_triggers_when_low_reaches_stop(self):
        order = make_stop_market_order(quantity=-1, stop_price=100)
        kline = make_kline(open=105, high=110, low=100, close=102)

        price, kept = order.try_fill(kline)

        assert price == Decimal(100)
        assert kept is order

    def test_sell_does_not_trigger_when_low_stays_above_stop(self):
        order = make_stop_market_order(quantity=-1, stop_price=100)
        kline = make_kline(open=105, high=110, low=101, close=108)

        price, _ = order.try_fill(kline)

        assert price is None

    def test_sell_fills_at_exact_stop_even_when_bar_gaps_far_below(self):
        order = make_stop_market_order(quantity=-1, stop_price=100)
        kline = make_kline(open=60, high=65, low=55, close=62)

        price, _ = order.try_fill(kline)

        assert price == Decimal(100)


class TestStopLimitOrder:
    def test_is_stop_triggered_buy(self):
        order = make_stop_limit_order(quantity=1, stop_price=100, limit_price=105)

        assert order.is_stop_triggered(make_kline(open=95, high=100, low=90, close=98))
        assert not order.is_stop_triggered(make_kline(open=90, high=99, low=85, close=92))

    def test_is_stop_triggered_sell(self):
        order = make_stop_limit_order(quantity=-1, stop_price=100, limit_price=95)

        assert order.is_stop_triggered(make_kline(open=105, high=110, low=100, close=102))
        assert not order.is_stop_triggered(make_kline(open=105, high=110, low=101, close=108))

    def test_not_triggered_stays_as_itself(self):
        order = make_stop_limit_order(quantity=1, stop_price=100, limit_price=105)
        kline = make_kline(open=90, high=95, low=85, close=92)

        price, kept = order.try_fill(kline)

        assert price is None
        assert kept is order

    def test_triggered_but_limit_not_reached_becomes_limit_order(self):
        order = make_stop_limit_order(quantity=1, stop_price=100, limit_price=102)
        kline = make_kline(open=104, high=110, low=103, close=108)

        price, kept = order.try_fill(kline)

        assert price is None
        assert type(kept) is LimitOrder
        assert kept.id == order.id
        assert kept.account_id == order.account_id
        assert kept.asset == order.asset
        assert kept.quantity == order.quantity
        assert kept.timestamp == order.timestamp
        assert kept.limit_price == order.limit_price

    def test_triggered_and_limit_reached_in_same_bar_fills(self):
        order = make_stop_limit_order(quantity=1, stop_price=100, limit_price=105)
        kline = make_kline(open=98, high=106, low=95, close=101)

        price, kept = order.try_fill(kline)

        assert price == Decimal(105)
        assert type(kept) is LimitOrder

    def test_sell_stop_limit_triggers_and_fills(self):
        order = make_stop_limit_order(quantity=-1, stop_price=100, limit_price=98)
        kline = make_kline(open=102, high=103, low=97, close=99)

        price, kept = order.try_fill(kline)

        assert price == Decimal(98)
        assert type(kept) is LimitOrder
