# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gc-space-time-tradeoff/. The authors are listed in prov/4J3Z1T.jsonl.

import random
from fractions import Fraction

import pytest

from gc_space_time_tradeoff import copying_cost, mark_sweep_cost, simulate_copying, simulate_mark_sweep


def test_worked_example() -> None:
    # L = 10 live words, unit costs.
    assert copying_cost(40, 10) == 1  # H = 4L: each allocated word costs one copied word
    assert copying_cost(80, 10) == Fraction(1, 3)
    assert copying_cost(160, 10) == Fraction(1, 7)
    assert mark_sweep_cost(40, 10) == Fraction(5, 3)
    assert mark_sweep_cost(80, 10) == Fraction(9, 7)
    assert simulate_copying(40, 10, 3) == 1
    assert simulate_mark_sweep(80, 10, 3) == Fraction(9, 7)


def test_formulas_match_the_simulators() -> None:
    rng = random.Random(1987)
    for _ in range(600):
        L = rng.randint(0, 12)
        cycles = rng.randint(1, 4)
        c, m, s = (Fraction(rng.randint(1, 9), rng.randint(1, 4)) for _ in range(3))
        H = 2 * rng.randint(L + 1, L + 25)
        assert simulate_copying(H, L, cycles, c) == copying_cost(H, L, c)
        H = rng.randint(L + 1, 3 * L + 25)
        assert simulate_mark_sweep(H, L, cycles, m, s) == mark_sweep_cost(H, L, m, s)


def test_both_costs_fall_as_the_heap_grows() -> None:
    for L in range(1, 30):
        prev_c = prev_m = None
        for H in range(2 * L + 2, 2 * L + 200, 2):
            cc, mc = copying_cost(H, L), mark_sweep_cost(H, L, 1, 1)
            if prev_c is not None:
                assert cc < prev_c and mc < prev_m
            assert mc > 1  # the sweep term never goes away: the limit is s = 1
            prev_c, prev_m = cc, mc


def test_ratio_form() -> None:
    # With H = k L, copying costs 2 c / (k - 2) and mark-sweep (m + s k) / (k - 1).
    for L in range(1, 20):
        for k in range(3, 12):
            assert copying_cost(k * L, L, 5) == Fraction(10, k - 2)
            assert mark_sweep_cost(k * L, L, 2, 3) == Fraction(2 + 3 * k, k - 1)


def test_preconditions() -> None:
    with pytest.raises(ValueError):
        copying_cost(20, 10)
    with pytest.raises(ValueError):
        mark_sweep_cost(10, 10)
