# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/first-price-auction/. The authors are listed in prov/VEN1KY.jsonl.

import random
from fractions import Fraction

from first_price_auction import equilibrium_bid, first_price_auction, interim_utility


def reference(bids, reserve=0):
    eligible = [i for i in range(len(bids)) if bids[i] >= reserve]
    if not eligible:
        return None, 0
    top = max(bids[i] for i in eligible)
    return min(i for i in eligible if bids[i] == top), top


def test_example() -> None:
    assert first_price_auction([10, 7, 3]) == (0, 10)
    assert first_price_auction([3, 7, 10]) == (2, 10)
    assert first_price_auction([10, 7, 3], reserve=8) == (0, 10)
    assert first_price_auction([10, 7, 3], reserve=11) == (None, 0)


def test_edges() -> None:
    assert first_price_auction([]) == (None, 0)
    assert first_price_auction([5]) == (0, 5)
    assert first_price_auction([7, 7, 3]) == (0, 7)
    assert first_price_auction([3, 7, 7]) == (1, 7)
    assert first_price_auction([2, 1], reserve=2) == (0, 2)


def test_against_reference() -> None:
    rng = random.Random(1)
    for _ in range(2000):
        bids = [rng.randrange(0, 6) for _ in range(rng.randrange(0, 7))]
        r = rng.randrange(0, 5)
        assert first_price_auction(bids, r) == reference(bids, r)


def test_truthful_bidding_is_not_dominant() -> None:
    # Values 10 and 7: the truthful bid 10 earns 0, the bid 8 earns 2.
    w, p = first_price_auction([10, 7])
    assert 10 - p == 0
    w, p = first_price_auction([8, 7])
    assert w == 0 and 10 - p == 2


def test_equilibrium_values() -> None:
    assert equilibrium_bid(Fraction(1, 2), 2) == Fraction(1, 4)
    assert equilibrium_bid(Fraction(9, 10), 3) == Fraction(3, 5)
    assert equilibrium_bid(Fraction(1), 2, a=2) == Fraction(2, 3)


def test_equilibrium_is_best_response() -> None:
    # Bids above equilibrium_bid(1) win for sure and are worse than bidding
    # equilibrium_bid(1), so every relevant bid is equilibrium_bid(t) for some t.
    grid = [Fraction(k, 60) for k in range(61)]
    for n in (2, 3, 4):
        for a in (1, 2):
            for v in [Fraction(k, 12) for k in range(13)]:
                best = interim_utility(v, v, n, a)
                assert best >= 0
                for t in grid:
                    assert interim_utility(v, t, n, a) <= best
                if 0 < v:
                    near = min(v + Fraction(1, 60), Fraction(1))
                    if near != v:
                        assert interim_utility(v, near, n, a) < best


def test_expected_utility_by_simulation() -> None:
    # Check interim_utility against the auction itself for one deviation.
    rng = random.Random(2)
    n, v, t = 3, Fraction(3, 4), Fraction(1, 2)
    trials, total = 20000, 0.0
    b0 = float(equilibrium_bid(t, n))
    for _ in range(trials):
        bids = [b0] + [float(equilibrium_bid(Fraction(rng.random()), n)) for _ in range(n - 1)]
        w, p = first_price_auction(bids)
        if w == 0:
            total += float(v) - p
    # Utilities are in [0, 1]; Hoeffding gives deviation above 0.02 with probability below 1e-6.
    assert abs(total / trials - float(interim_utility(v, t, n))) < 0.02


def test_revenue_uniform() -> None:
    rng = random.Random(3)
    for n in (2, 3, 5):
        trials, total = 20000, 0.0
        for _ in range(trials):
            values = [rng.random() for _ in range(n)]
            _, p = first_price_auction([(n - 1) * x / n for x in values])
            total += p
        assert abs(total / trials - (n - 1) / (n + 1)) < 0.02
