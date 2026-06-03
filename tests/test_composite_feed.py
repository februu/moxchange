import pytest
from moxchange.feeds.mock_feed import MockFeed
from moxchange.feeds import RoundRobinFeed, SequentialFeed


def make_feed(n: int, starting_price: float = 100.0, seed: int = 42) -> MockFeed:
    return MockFeed(amount_of_klines=n, starting_price=starting_price, seed=seed)


class TestRoundRobinFeed:
    def test_interleaves_two_feeds(self):
        a = make_feed(3, seed=1)
        b = make_feed(3, seed=2)
        klines_a = list(make_feed(3, seed=1))
        klines_b = list(make_feed(3, seed=2))

        result = list(RoundRobinFeed(a, b))

        assert len(result) == 6
        assert result[0] == klines_a[0]
        assert result[1] == klines_b[0]
        assert result[2] == klines_a[1]
        assert result[3] == klines_b[1]
        assert result[4] == klines_a[2]
        assert result[5] == klines_b[2]

    def test_total_klines_equals_sum_of_feeds(self):
        result = list(RoundRobinFeed(make_feed(4, seed=1), make_feed(6, seed=2)))
        assert len(result) == 10

    def test_unequal_feeds_exhausts_both(self):
        short = make_feed(2, seed=1)
        long_ = make_feed(5, seed=2)
        result = list(RoundRobinFeed(short, long_))
        assert len(result) == 7

    def test_single_feed_passes_through(self):
        feed = make_feed(4, seed=10)
        expected = list(make_feed(4, seed=10))
        result = list(RoundRobinFeed(feed))
        assert result == expected

    def test_empty_feed_skipped(self):
        empty = make_feed(0, seed=1)
        full = make_feed(3, seed=2)
        result = list(RoundRobinFeed(empty, full))
        assert len(result) == 3

    def test_raises_stop_iteration_when_exhausted(self):
        rr = RoundRobinFeed(make_feed(1, seed=1))
        next(rr)
        with pytest.raises(StopIteration):
            next(rr)

    def test_reset_replays_same_sequence(self):
        rr = RoundRobinFeed(make_feed(3, seed=1), make_feed(3, seed=2))
        first = list(rr)
        rr.reset()
        second = list(rr)
        assert first == second

    def test_three_feeds_interleaved(self):
        a = make_feed(2, seed=1)
        b = make_feed(2, seed=2)
        c = make_feed(2, seed=3)
        result = list(RoundRobinFeed(a, b, c))
        assert len(result) == 6


class TestSequentialFeed:
    def test_yields_all_klines_in_order(self):
        a = make_feed(3, seed=1)
        b = make_feed(3, seed=2)
        expected_a = list(make_feed(3, seed=1))
        expected_b = list(make_feed(3, seed=2))

        result = list(SequentialFeed(a, b))

        assert result == expected_a + expected_b

    def test_total_klines_equals_sum_of_feeds(self):
        result = list(SequentialFeed(make_feed(4, seed=1), make_feed(6, seed=2)))
        assert len(result) == 10

    def test_single_feed_passes_through(self):
        feed = make_feed(4, seed=10)
        expected = list(make_feed(4, seed=10))
        result = list(SequentialFeed(feed))
        assert result == expected

    def test_empty_feed_skipped(self):
        empty = make_feed(0, seed=1)
        full = make_feed(3, seed=2)
        result = list(SequentialFeed(empty, full))
        assert len(result) == 3

    def test_raises_stop_iteration_when_exhausted(self):
        seq = SequentialFeed(make_feed(1, seed=1))
        next(seq)
        with pytest.raises(StopIteration):
            next(seq)

    def test_three_feeds_sequential(self):
        a = make_feed(2, seed=1)
        b = make_feed(2, seed=2)
        c = make_feed(2, seed=3)
        expected = (
            list(make_feed(2, seed=1))
            + list(make_feed(2, seed=2))
            + list(make_feed(2, seed=3))
        )
        result = list(SequentialFeed(a, b, c))
        assert result == expected
