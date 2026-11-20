# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vickrey-auction/. The authors are listed in prov/3GCYFC.jsonl.

import itertools
import random
from fractions import Fraction

from vickrey_auction import utility, vickrey_auction


def reference(bids, reserve=0):
    eligible = [i for i in range(len(bids)) if bids[i] >= reserve]
    if not eligible:
        return None, 0
    top = max(bids[i] for i in eligible)
    winner = min(i for i in eligible if bids[i] == top)
    others = [bids[j] for j in range(len(bids)) if j != winner]
    return winner, max([reserve] + others)


def test_example() -> None:
    assert vickrey_auction([10, 7, 3]) == (0, 7)
    assert vickrey_auction([3, 7, 10]) == (2, 7)
    assert vickrey_auction([10, 7, 3], reserve=8) == (0, 8)
    assert vickrey_auction([10, 7, 3], reserve=12) == (None, 0)


def test_edges() -> None:
    assert vickrey_auction([]) == (None, 0)
    assert vickrey_auction([5]) == (0, 0)
    assert vickrey_auction([5], reserve=2) == (0, 2)
    assert vickrey_auction([7, 7, 3]) == (0, 7)
    assert vickrey_auction([3, 7, 7]) == (1, 7)
    assert vickrey_auction([2, 2], reserve=2) == (0, 2)
    assert vickrey_auction([Fraction(1, 3), Fraction(1, 2)]) == (1, Fraction(1, 3))


def test_against_reference() -> None:
    rng = random.Random(1)
    for _ in range(2000):
        n = rng.randrange(0, 7)
        bids = [rng.randrange(0, 6) for _ in range(n)]
        r = rng.randrange(0, 5)
        assert vickrey_auction(bids, r) == reference(bids, r)


def test_truthful_bidding_is_dominant() -> None:
    grid = range(0, 6)
    for reserve in (0, 2):
        for others in itertools.product(grid, repeat=2):
            for i in range(3):
                for value in grid:
                    truthful = list(others[:i]) + [value] + list(others[i:])
                    u_true = utility(value, truthful, i, reserve)
                    assert u_true >= 0
                    for lie in grid:
                        bids = list(others[:i]) + [lie] + list(others[i:])
                        assert u_true >= utility(value, bids, i, reserve)


def test_price_does_not_depend_on_winning_bid() -> None:
    rng = random.Random(2)
    for _ in range(500):
        bids = [rng.randrange(0, 20) for _ in range(4)]
        w, p = vickrey_auction(bids)
        raised = list(bids)
        raised[w] += rng.randrange(0, 10)
        assert vickrey_auction(raised) == (w, p)


def mean_revenue(n, reserve, trials, seed):
    rng = random.Random(seed)
    total = 0.0
    for _ in range(trials):
        _, price = vickrey_auction([rng.random() for _ in range(n)], reserve)
        total += price
    return total / trials


def test_revenue_uniform() -> None:
    # Each price is in [0, 1]. With 20000 trials, Hoeffding gives
    # P(|mean - expectation| > 0.02) <= 2 exp(-16) < 1e-6.
    assert abs(mean_revenue(2, 0, 20000, 3) - 1 / 3) < 0.02
    assert abs(mean_revenue(3, 0, 20000, 4) - 1 / 2) < 0.02
    assert abs(mean_revenue(2, 0.5, 20000, 5) - 5 / 12) < 0.02
    assert abs(mean_revenue(1, 0.5, 20000, 6) - 1 / 4) < 0.02
