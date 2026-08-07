import uuid
from datetime import datetime
from decimal import Decimal

from moxchange.events import EventBus
from moxchange.services import AccountService, OrderService
from moxchange.types import (
    Account,
    Asset,
    Kline,
    LimitOrder,
    MarketOrder,
    StopLimitOrder,
    StopMarketOrder,
)

BTC = Asset("BTC")
ETH = Asset("ETH")
NOW = datetime(2024, 1, 1)


def make_services() -> tuple[EventBus, AccountService, OrderService]:
    bus = EventBus()
    account_service = AccountService(bus)
    order_service = OrderService(bus, account_service)
    return bus, account_service, order_service


def make_kline(open, high, low, close, asset: Asset = BTC) -> Kline:
    return Kline(
        asset=asset,
        open=Decimal(str(open)),
        high=Decimal(str(high)),
        low=Decimal(str(low)),
        close=Decimal(str(close)),
    )


def make_market_order(account: Account, quantity=1, asset: Asset = BTC) -> MarketOrder:
    return MarketOrder(
        id=uuid.uuid4(), account_id=account.id, asset=asset, quantity=Decimal(quantity), timestamp=NOW
    )


def make_limit_order(account: Account, quantity=1, limit_price=100, asset: Asset = BTC) -> LimitOrder:
    return LimitOrder(
        id=uuid.uuid4(), account_id=account.id, asset=asset, quantity=Decimal(quantity), timestamp=NOW,
        limit_price=Decimal(str(limit_price)),
    )


def make_stop_market_order(account: Account, quantity=1, stop_price=100, asset: Asset = BTC) -> StopMarketOrder:
    return StopMarketOrder(
        id=uuid.uuid4(), account_id=account.id, asset=asset, quantity=Decimal(quantity), timestamp=NOW,
        stop_price=Decimal(str(stop_price)),
    )


def make_stop_limit_order(
    account: Account, quantity=1, stop_price=100, limit_price=105, asset: Asset = BTC
) -> StopLimitOrder:
    return StopLimitOrder(
        id=uuid.uuid4(), account_id=account.id, asset=asset, quantity=Decimal(quantity), timestamp=NOW,
        stop_price=Decimal(str(stop_price)), limit_price=Decimal(str(limit_price)),
    )


class TestPlaceCancelQuery:
    def test_place_order_adds_to_open_orders(self):
        _, account_service, order_service = make_services()
        account = account_service.add_account("alice")
        order = make_market_order(account)

        order_service.place_order(order)

        assert order_service.get_open_orders_for_asset(BTC) == [order]

    def test_cancel_order_removes_it(self):
        _, account_service, order_service = make_services()
        account = account_service.add_account("alice")
        order = make_limit_order(account)
        order_service.place_order(order)

        order_service.cancel_order(order.id, BTC)

        assert order_service.get_open_orders_for_asset(BTC) == []

    def test_cancel_unknown_order_is_a_noop(self):
        _, account_service, order_service = make_services()
        order_service.cancel_order(uuid.uuid4(), BTC)
        assert order_service.get_open_orders_for_asset(BTC) == []

    def test_get_open_orders_for_account_filters_by_account(self):
        _, account_service, order_service = make_services()
        alice = account_service.add_account("alice")
        bob = account_service.add_account("bob")
        alice_order = make_market_order(alice)
        bob_order = make_market_order(bob)
        order_service.place_order(alice_order)
        order_service.place_order(bob_order)

        assert order_service.get_open_orders_for_account(alice.id) == [alice_order]

    def test_get_open_orders_for_unknown_account_returns_empty(self):
        _, account_service, order_service = make_services()
        account = account_service.add_account("alice")
        order_service.place_order(make_market_order(account))

        assert order_service.get_open_orders_for_account(uuid.uuid4()) == []

    def test_clear_open_orders_empties_everything(self):
        _, account_service, order_service = make_services()
        account = account_service.add_account("alice")
        order_service.place_order(make_market_order(account, asset=BTC))
        order_service.place_order(make_market_order(account, asset=ETH))

        order_service.clear_open_orders()

        assert order_service.get_open_orders_for_asset(BTC) == []
        assert order_service.get_open_orders_for_asset(ETH) == []


class TestExecuteOrdersMarket:
    def test_fills_immediately_and_updates_position(self):
        _, account_service, order_service = make_services()
        account = account_service.add_account("alice")
        order = make_market_order(account, quantity=2)
        order_service.place_order(order)

        order_service.execute_orders(make_kline(open=100, high=105, low=95, close=102))

        assert order_service.get_open_orders_for_asset(BTC) == []
        position = account.get_or_create_position(BTC)
        assert position.quantity == Decimal(2)
        assert position.entry_price == Decimal(100)
        assert len(account.transactions) == 1
        assert account.transactions[0].price == Decimal(100)


class TestExecuteOrdersLimit:
    def test_stays_open_until_price_reaches_limit(self):
        _, account_service, order_service = make_services()
        account = account_service.add_account("alice")
        order = make_limit_order(account, quantity=1, limit_price=90)
        order_service.place_order(order)

        order_service.execute_orders(make_kline(open=100, high=105, low=95, close=101))
        assert order_service.get_open_orders_for_asset(BTC) == [order]

        order_service.execute_orders(make_kline(open=95, high=96, low=88, close=91))
        assert order_service.get_open_orders_for_asset(BTC) == []
        assert account.transactions[0].price == Decimal(90)

    def test_fills_at_limit_price_not_the_better_gapped_open(self):
        _, account_service, order_service = make_services()
        account = account_service.add_account("alice")
        order = make_limit_order(account, quantity=1, limit_price=90)
        order_service.place_order(order)

        order_service.execute_orders(make_kline(open=60, high=65, low=55, close=62))

        assert account.transactions[0].price == Decimal(90)


class TestExecuteOrdersStopMarket:
    def test_stays_open_until_stop_is_reached(self):
        _, account_service, order_service = make_services()
        account = account_service.add_account("alice")
        order = make_stop_market_order(account, quantity=-1, stop_price=90)
        order_service.place_order(order)

        order_service.execute_orders(make_kline(open=100, high=105, low=95, close=101))
        assert order_service.get_open_orders_for_asset(BTC) == [order]

        order_service.execute_orders(make_kline(open=95, high=96, low=88, close=91))
        assert order_service.get_open_orders_for_asset(BTC) == []
        assert account.transactions[0].price == Decimal(90)

    def test_fills_at_stop_price_not_the_worse_gapped_open(self):
        _, account_service, order_service = make_services()
        account = account_service.add_account("alice")
        order = make_stop_market_order(account, quantity=-1, stop_price=90)
        order_service.place_order(order)

        order_service.execute_orders(make_kline(open=60, high=65, low=55, close=62))

        assert account.transactions[0].price == Decimal(90)


class TestExecuteOrdersStopLimit:
    def test_arms_on_one_bar_and_fills_on_a_later_bar(self):
        _, account_service, order_service = make_services()
        account = account_service.add_account("dave")
        order = make_stop_limit_order(account, quantity=1, stop_price=110, limit_price=112)
        order_service.place_order(order)

        # Bar 1: spikes through the stop but stays above the limit -- arms, does not fill.
        order_service.execute_orders(make_kline(open=114, high=115, low=113, close=114))
        remaining = order_service.get_open_orders_for_asset(BTC)
        assert len(remaining) == 1
        assert type(remaining[0]) is LimitOrder
        assert account.transactions == []

        # Bar 2: price retreats well below the original stop, but is within the armed limit.
        order_service.execute_orders(make_kline(open=106, high=108, low=105, close=106))
        assert order_service.get_open_orders_for_asset(BTC) == []
        assert account.transactions[0].price == Decimal(112)

    def test_fills_within_the_same_bar_when_both_conditions_are_met(self):
        _, account_service, order_service = make_services()
        account = account_service.add_account("dave")
        order = make_stop_limit_order(account, quantity=1, stop_price=110, limit_price=112)
        order_service.place_order(order)

        order_service.execute_orders(make_kline(open=104, high=111, low=100, close=105))

        assert order_service.get_open_orders_for_asset(BTC) == []
        assert account.transactions[0].price == Decimal(112)

    def test_stays_open_when_stop_never_triggers(self):
        _, account_service, order_service = make_services()
        account = account_service.add_account("dave")
        order = make_stop_limit_order(account, quantity=1, stop_price=110, limit_price=112)
        order_service.place_order(order)

        order_service.execute_orders(make_kline(open=100, high=105, low=95, close=101))
        order_service.execute_orders(make_kline(open=101, high=106, low=98, close=103))

        assert order_service.get_open_orders_for_asset(BTC) == [order]
        assert account.transactions == []

    def test_armed_order_never_fills_if_price_runs_away(self):
        _, account_service, order_service = make_services()
        account = account_service.add_account("dave")
        order = make_stop_limit_order(account, quantity=1, stop_price=110, limit_price=112)
        order_service.place_order(order)

        # Arms, but price keeps rising past the limit and never comes back.
        order_service.execute_orders(make_kline(open=114, high=115, low=113, close=114))
        order_service.execute_orders(make_kline(open=120, high=125, low=118, close=122))

        remaining = order_service.get_open_orders_for_asset(BTC)
        assert len(remaining) == 1
        assert type(remaining[0]) is LimitOrder
        assert account.transactions == []


class TestExecuteOrdersAssetIsolation:
    def test_only_touches_orders_for_the_klines_asset(self):
        _, account_service, order_service = make_services()
        account = account_service.add_account("alice")
        eth_order = make_limit_order(account, quantity=1, limit_price=100, asset=ETH)
        order_service.place_order(eth_order)
        order_service.place_order(make_market_order(account, asset=BTC))

        order_service.execute_orders(make_kline(open=50, high=55, low=45, close=52, asset=BTC))

        assert order_service.get_open_orders_for_asset(ETH) == [eth_order]
        assert order_service.get_open_orders_for_asset(BTC) == []
