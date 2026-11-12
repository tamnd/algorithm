# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-least-connections/. The authors are listed in prov/FXQQ1P.jsonl.

import random
from fractions import Fraction
from math import ceil

import pytest

from weighted_least_connections import (WeightedLeastConnections, lvs_overhead, lvs_wlc_pick,
                                        picks_from_zero, sed_pick, wlc_choose)


def oracle(h, w, up):
    """Reference: exact ratios with Fraction, first index on a tie."""
    cand = [j for j in range(len(h)) if up[j] and w[j] > 0]
    if not cand:
        return None
    return min(cand, key=lambda j: (Fraction(h[j], w[j]), j))


def test_trace_of_the_page() -> None:
    lb = WeightedLeastConnections([3, 2, 1])
    assert [lb.pick() for _ in range(6)] == [0, 1, 2, 0, 1, 0]
    assert lb.a == [3, 2, 1]
    lb.done(0)
    lb.done(0)
    assert lb.a == [1, 2, 1]
    assert [lb.pick(), lb.pick()] == [0, 0]
    assert lb.a == [3, 2, 1]


def test_examples_of_the_page() -> None:
    assert lvs_overhead(2, 100) == 612 and lvs_overhead(3, 0) == 768
    assert lvs_wlc_pick([2, 3], [100, 0], [1, 1]) == 0
    assert wlc_choose([5, 0], [10, 1], [True, True]) == 1
    assert sed_pick([5, 0], [10, 1]) == 0
    p = picks_from_zero([100] + [1] * 9, 10)
    assert p == list(range(10))


def test_zero_weight_down_and_empty() -> None:
    lb = WeightedLeastConnections([0, 2, 0])
    assert [lb.pick() for _ in range(5)] == [1] * 5
    lb.up[1] = False
    assert lb.pick() is None
    assert WeightedLeastConnections([]).pick() is None
    with pytest.raises(ValueError):
        WeightedLeastConnections([1]).done(0)
    with pytest.raises(ValueError):
        WeightedLeastConnections([1, -1])


def test_random_against_fraction_oracle() -> None:
    rng = random.Random(7)
    for _ in range(400):
        n = rng.randint(1, 6)
        w = [rng.randint(0, 5) for _ in range(n)]
        lb = WeightedLeastConnections(w)
        model = [0] * n
        for _ in range(40):
            if rng.random() < 0.15:
                lb.up[rng.randrange(n)] = rng.random() < 0.7
            busy = [j for j in range(n) if model[j] > 0]
            if busy and rng.random() < 0.35:
                j = rng.choice(busy)
                lb.done(j)
                model[j] -= 1
                continue
            want = oracle(model, w, lb.up)
            assert lb.pick() == want
            if want is not None:
                model[want] += 1
            assert lb.a == model


def test_upper_quota_and_lower_bound_without_departures() -> None:
    rng = random.Random(11)
    for _ in range(300):
        n = rng.randint(1, 6)
        w = [rng.randint(1, 9) for _ in range(n)]
        total = sum(w)
        lb = WeightedLeastConnections(w)
        for k in range(1, 60):
            lb.pick()
            for j in range(n):
                assert lb.a[j] <= ceil(Fraction(k * w[j], total))
                assert lb.a[j] >= Fraction(k * w[j], total) - (n - 1)
            if k % total == 0:
                assert lb.a == [w[j] * k // total for j in range(n)]


def test_lvs_rule_matches_fraction_oracle() -> None:
    rng = random.Random(5)
    for _ in range(500):
        n = rng.randint(1, 5)
        act = [rng.randint(0, 20) for _ in range(n)]
        ina = [rng.randint(0, 600) for _ in range(n)]
        w = [rng.randint(0, 4) for _ in range(n)]
        h = [256 * a + i for a, i in zip(act, ina)]
        assert lvs_wlc_pick(act, ina, w) == oracle(h, w, [True] * n)
