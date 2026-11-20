# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hughes-hartogs-algorithm/. The authors are listed in prov/YMENDP.jsonl.

import itertools
import math
import random
from fractions import Fraction as F

import pytest

from hughes_hartogs_algorithm import bit_power, greedy_from_increments, hughes_hartogs

PAGE_GAINS = [F(20), F(9), F(5), F(3, 2)]


def power_of(gains, bits, gap=1):
    return sum(bit_power(g, b, gap) for g, b in zip(gains, bits))


def brute_ma(gains, target, b_max, gap=1):
    best = None
    for b in itertools.product(range(b_max + 1), repeat=len(gains)):
        if sum(b) == target:
            e = power_of(gains, b, gap)
            if best is None or e < best:
                best = e
    return best


def brute_ra(gains, budget, b_max, gap=1):
    best = (-1, None)
    for b in itertools.product(range(b_max + 1), repeat=len(gains)):
        e = power_of(gains, b, gap)
        if e <= budget and (sum(b) > best[0] or (sum(b) == best[0] and e < best[1])):
            best = (sum(b), e)
    return best


def test_page_example_trace() -> None:
    expected = [
        (1, 0, 0, 0), (2, 0, 0, 0), (2, 1, 0, 0), (3, 1, 0, 0), (3, 1, 1, 0),
        (3, 2, 1, 0), (4, 2, 1, 0), (4, 2, 2, 0), (4, 3, 2, 0), (4, 3, 2, 1),
    ]
    for k, b in enumerate(expected, start=1):
        bits, e = hughes_hartogs(PAGE_GAINS, target_bits=k)
        assert tuple(bits) == b
        assert e == power_of(PAGE_GAINS, b)
    bits, e = hughes_hartogs(PAGE_GAINS, target_bits=8)
    assert e == F(101, 60)
    assert brute_ma(PAGE_GAINS, 8, 8) == F(101, 60)


def test_page_example_rate_adaptive() -> None:
    assert hughes_hartogs(PAGE_GAINS, budget=2) == ([4, 2, 2, 0], F(101, 60))
    assert hughes_hartogs(PAGE_GAINS, budget=F(101, 60)) == ([4, 2, 2, 0], F(101, 60))
    bits, _ = hughes_hartogs(PAGE_GAINS, budget=F(101, 60) - F(1, 1000))
    assert sum(bits) == 7
    assert hughes_hartogs(PAGE_GAINS, budget=0) == ([0, 0, 0, 0], 0)


def test_margin_adaptive_matches_brute_force() -> None:
    rng = random.Random(21)
    for _ in range(150):
        n = rng.randint(1, 4)
        gains = [F(rng.randint(1, 60), rng.randint(1, 6)) for _ in range(n)]
        b_max = rng.randint(1, 6)
        target = rng.randint(0, n * b_max)
        bits, e = hughes_hartogs(gains, target_bits=target, b_max=b_max)
        assert sum(bits) == target and max(bits) <= b_max
        assert e == power_of(gains, bits)
        assert e == brute_ma(gains, target, b_max)


def test_rate_adaptive_matches_brute_force() -> None:
    rng = random.Random(22)
    for _ in range(150):
        n = rng.randint(1, 4)
        gains = [F(rng.randint(1, 60), rng.randint(1, 6)) for _ in range(n)]
        b_max = rng.randint(1, 6)
        gap = F(rng.randint(1, 9))
        budget = F(rng.randint(0, 400), 10)
        bits, e = hughes_hartogs(gains, budget=budget, gap=gap, b_max=b_max)
        assert e <= budget
        assert (sum(bits), e) == brute_ra(gains, budget, b_max, gap)


def test_gap_does_not_change_the_ma_allocation() -> None:
    rng = random.Random(23)
    gains = [rng.uniform(0.5, 40) for _ in range(32)]
    b1, e1 = hughes_hartogs(gains, target_bits=100)
    b7, e7 = hughes_hartogs(gains, target_bits=100, gap=7.0)
    assert b1 == b7
    assert abs(e7 - 7 * e1) < 1e-9 * e7


def water_filling_rate(gains, budget, gap=1.0):
    nu = [gap / g for g in gains]
    lo, hi = 0.0, max(nu) + budget
    for _ in range(200):
        mid = (lo + hi) / 2
        if sum(max(0.0, mid - v) for v in nu) < budget:
            lo = mid
        else:
            hi = mid
    return sum(max(0.0, math.log2(lo / v)) for v in nu)


def test_bound_against_water_filling() -> None:
    rng = random.Random(24)
    for _ in range(100):
        n = rng.randint(1, 64)
        gains = [rng.expovariate(1 / 30) + 0.01 for _ in range(n)]
        budget = rng.uniform(0.1, 50)
        bits, _ = hughes_hartogs(gains, budget=budget, gap=2.0)
        c = water_filling_rate(gains, budget, gap=2.0)
        assert c - n < sum(bits) <= c + 1e-9
    gains = [20, 9, 5, 1.5]
    assert abs(water_filling_rate(gains, 2) - 8.791781) < 1e-6


def test_greedy_needs_increasing_increments() -> None:
    bits, total = greedy_from_increments([[4, 1], [3, 3]], 2)
    assert bits == [0, 2] and total == 6
    assert min(4 + 1, 3 + 3, 4 + 3) == 5
    rng = random.Random(25)
    for _ in range(100):
        n = rng.randint(1, 4)
        tables = [sorted(rng.randint(1, 20) for _ in range(4)) for _ in range(n)]
        target = rng.randint(0, 4 * n)
        _, total = greedy_from_increments(tables, target)
        best = min(
            sum(sum(t[:k]) for t, k in zip(tables, ks))
            for ks in itertools.product(range(5), repeat=n)
            if sum(ks) == target
        )
        assert total == best


def test_caps_and_bad_input() -> None:
    assert hughes_hartogs([1, 100], target_bits=5, b_max=3)[0] == [2, 3]
    assert hughes_hartogs([1, 100], budget=10**9, b_max=3)[0] == [3, 3]
    assert hughes_hartogs([1, 100], budget=10**9, b_max=0)[0] == [0, 0]
    with pytest.raises(ValueError):
        hughes_hartogs([1, 2], target_bits=7, b_max=3)
    with pytest.raises(ValueError):
        hughes_hartogs([1, 2])
    with pytest.raises(ValueError):
        hughes_hartogs([1, 2], target_bits=1, budget=1)
    with pytest.raises(ValueError):
        hughes_hartogs([1, 0], target_bits=1)
    with pytest.raises(ValueError):
        hughes_hartogs([], budget=1)
