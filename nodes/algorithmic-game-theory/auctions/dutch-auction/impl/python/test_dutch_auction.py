# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dutch-auction/. The authors are listed in prov/6N55V9.jsonl.

import math
import random
from fractions import Fraction

import pytest

from dutch_auction import dutch_auction


def first_price(bids, reserve):
    """Reference first-price rule: highest bid at least the reserve, smallest index on ties."""
    eligible = [i for i in range(len(bids)) if bids[i] >= reserve]
    if not eligible:
        return None, 0
    best = max(bids[i] for i in eligible)
    return min(i for i in eligible if bids[i] == best), best


def round_to_clock(s, top, delta):
    """The largest clock level top - k delta (k >= 0) that is at most s."""
    if s >= top:
        return top
    return top - math.ceil((top - s) / delta) * delta


def test_example() -> None:
    # Values (10, 7, 3), equilibrium-like stops (6, 4, 2), clock from 12 down by 1.
    assert dutch_auction([6, 4, 2], 12, 1) == (0, 6)
    assert dutch_auction([Fraction(13, 2), 4, 2], 12, 1) == (0, 6)
    assert dutch_auction([6, 4, 2], 12, 1, reserve=7) == (None, 0)
    assert dutch_auction([6, 6, 2], 12, 1) == (0, 6)
    assert dutch_auction([2, 6, 6], 12, 1) == (1, 6)


def test_edges() -> None:
    assert dutch_auction([], 10, 1) == (None, 0)
    assert dutch_auction([20, 3], 10, 1) == (0, 10)
    assert dutch_auction([3, 20], 10, 1) == (1, 10)
    assert dutch_auction([0], 10, 1) == (0, 0)
    assert dutch_auction([Fraction(1, 2)], 10, 1, reserve=1) == (None, 0)
    with pytest.raises(ValueError):
        dutch_auction([1], 10, 0)


def test_equals_first_price_on_rounded_bids() -> None:
    rng = random.Random(1)
    for _ in range(2000):
        n = rng.randrange(0, 6)
        delta = Fraction(rng.randrange(1, 5), 2)
        top = Fraction(rng.randrange(8, 16))
        reserve = Fraction(rng.randrange(0, 4))
        stops = [Fraction(rng.randrange(0, 40), 3) for _ in range(n)]
        rounded = [round_to_clock(s, top, delta) for s in stops]
        assert dutch_auction(stops, top, delta, reserve) == first_price(rounded, reserve)


def test_equals_first_price_on_clock_bids() -> None:
    rng = random.Random(2)
    for _ in range(1000):
        bids = [Fraction(rng.randrange(0, 21), 4) for _ in range(rng.randrange(1, 6))]
        assert dutch_auction(bids, 5, Fraction(1, 4)) == first_price(bids, 0)


def test_price_is_within_delta_of_highest_stop() -> None:
    rng = random.Random(3)
    for _ in range(1000):
        stops = [Fraction(rng.randrange(0, 100), 9) for _ in range(rng.randrange(1, 6))]
        w, p = dutch_auction(stops, 12, Fraction(1, 3))
        assert max(stops) - Fraction(1, 3) < p <= max(stops)
        assert stops[w] >= p


def test_revenue_uniform() -> None:
    # Equilibrium stops (n - 1) v / n with uniform values; the price is within
    # delta = 0.01 below the first-price price, whose mean is (n - 1)/(n + 1).
    rng = random.Random(4)
    for n in (2, 3):
        trials, total = 5000, 0.0
        for _ in range(trials):
            stops = [(n - 1) * rng.random() / n for _ in range(n)]
            _, p = dutch_auction(stops, 1.0, 0.01)
            total += p
        # Hoeffding with 5000 prices in [0, 1]: deviation above 0.03 has probability below 0.001.
        assert abs(total / trials - (n - 1) / (n + 1)) < 0.03 + 0.01
