# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/english-auction/. The authors are listed in prov/6F235Y.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from english_auction import english_auction, utility


def reference(d, delta, start=0):
    """Closed form: the clock stops at the last grid price the second threshold accepts."""
    eligible = [i for i in range(len(d)) if d[i] >= start]
    if not eligible:
        return None, 0
    if len(eligible) == 1:
        return eligible[0], start
    top = sorted((d[i] for i in eligible), reverse=True)
    g = start + ((top[1] - start) // delta) * delta
    if top[0] >= g + delta:
        return d.index(top[0]), g + delta
    return min(i for i in eligible if d[i] >= g), g


def test_example() -> None:
    assert english_auction([10, 7, 3], 1) == (0, 8)
    assert english_auction([10, 7, 3], Fraction(1, 2)) == (0, Fraction(15, 2))
    assert english_auction([10, 7, 3], 1, start=8) == (0, 8)
    assert english_auction([10, 7, 3], 1, start=11) == (None, 0)


def test_edges() -> None:
    assert english_auction([], 1) == (None, 0)
    assert english_auction([5], 1) == (0, 0)
    assert english_auction([5], 1, start=2) == (0, 2)
    assert english_auction([7, 7, 3], 1) == (0, 7)
    assert english_auction([3, 7, 7], 1) == (1, 7)
    assert english_auction([7, Fraction(15, 2), 3], 1) == (0, 7)
    with pytest.raises(ValueError):
        english_auction([1, 2], 0)


def test_against_closed_form() -> None:
    rng = random.Random(1)
    for _ in range(2000):
        n = rng.randrange(0, 6)
        d = [Fraction(rng.randrange(0, 25), 2) for _ in range(n)]
        delta = Fraction(rng.randrange(1, 7), 2)
        start = Fraction(rng.randrange(0, 6), 2)
        assert english_auction(d, delta, start) == reference(d, delta, start)


def test_close_to_vickrey() -> None:
    rng = random.Random(2)
    for _ in range(1000):
        n = rng.randrange(2, 6)
        v = [Fraction(rng.randrange(0, 100), 7) for _ in range(n)]
        delta = Fraction(rng.randrange(1, 10), 3)
        w, p = english_auction(v, delta)
        second = sorted(v, reverse=True)[1]
        assert abs(p - second) <= delta
        assert v[w] >= max(v) - delta
        assert p <= v[w]


def test_truthful_threshold_is_delta_dominant() -> None:
    delta = 1
    grid = [Fraction(k, 2) for k in range(0, 11)]
    for start in (0, 2):
        for others in itertools.product(grid, repeat=2):
            for i in range(3):
                for value in grid:
                    def u(d):
                        th = list(others[:i]) + [d] + list(others[i:])
                        return utility(value, th, i, delta, start)

                    u_true = u(value)
                    assert u_true >= 0
                    best = max(u(d) for d in grid)
                    assert u_true >= best - delta
                    if i == 2:
                        # with the last index, ties are always lost, and the gain is below delta
                        assert u_true > best - delta or best == u_true


def test_revenue_uniform() -> None:
    # The price is within 0.05 of the second-highest value, whose mean is 1/3.
    # With 5000 trials and prices in [0, 1.05], Hoeffding gives deviation above 0.03
    # with probability at most 2 exp(-2 * 5000 * 0.03^2 / 1.05^2) < 0.001.
    rng = random.Random(3)
    trials = 5000
    total = 0.0
    for _ in range(trials):
        _, p = english_auction([rng.random(), rng.random()], 0.05)
        total += p
    assert abs(total / trials - 1 / 3) < 0.05 + 0.03
