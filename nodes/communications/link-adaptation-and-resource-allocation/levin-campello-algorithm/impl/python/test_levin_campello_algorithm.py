# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/levin-campello-algorithm/. The authors are listed in prov/XEKW7B.jsonl.

import heapq
import itertools
import math
import random
from fractions import Fraction as F

import pytest

from levin_campello_algorithm import levin_campello

PAGE_GAINS = [F(20), F(9), F(5), F(3, 2)]


def power_of(gains, bits, gap=1):
    return sum(gap * (2**b - 1) / g for g, b in zip(gains, bits))


def greedy(gains, target, gap=1, b_max=None):
    """Plain greedy loading, ties to the lowest index; the reference optimum."""
    bits = [0] * len(gains)
    heap = [(gap / g, i) for i, g in enumerate(gains)]
    heapq.heapify(heap)
    for _ in range(target):
        _, i = heapq.heappop(heap)
        bits[i] += 1
        if b_max is None or bits[i] < b_max:
            heapq.heappush(heap, (gap * 2 ** bits[i] / gains[i], i))
    return bits


def brute(gains, b_max, gap, target=None, budget=None):
    best = None
    for b in itertools.product(range(b_max + 1), repeat=len(gains)):
        e = power_of(gains, b, gap)
        if target is not None and sum(b) == target:
            key = (0, e)
        elif budget is not None and e <= budget:
            key = (-sum(b), e)
        else:
            continue
        if best is None or key < best:
            best = key
    return best


def test_page_example_ma() -> None:
    bits, e, swaps = levin_campello(PAGE_GAINS, [2, 2, 2, 2], target_bits=8)
    assert bits == [4, 2, 2, 0] and e == F(101, 60) and swaps == 2


def test_page_example_ra() -> None:
    assert levin_campello(PAGE_GAINS, [3, 2, 1, 0], budget=2) == ([4, 2, 2, 0], F(101, 60), 0)
    assert levin_campello(PAGE_GAINS, [2, 2, 2, 2], budget=2) == ([4, 2, 2, 0], F(101, 60), 2)
    assert levin_campello(PAGE_GAINS, [6, 6, 6, 6], budget=2)[:2] == ([4, 2, 2, 0], F(101, 60))


def test_ma_matches_brute_force_from_any_start() -> None:
    rng = random.Random(31)
    for _ in range(120):
        n = rng.randint(1, 4)
        gains = [F(rng.randint(1, 60), rng.randint(1, 6)) for _ in range(n)]
        b_max = rng.randint(1, 6)
        target = rng.randint(0, n * b_max)
        start = [rng.randint(0, b_max) for _ in range(n)]
        bits, e, _ = levin_campello(gains, start, target_bits=target, b_max=b_max)
        assert sum(bits) == target and min(bits) >= 0 and max(bits) <= b_max
        assert e == power_of(gains, bits)
        assert (0, e) == brute(gains, b_max, 1, target=target)


def test_ra_matches_brute_force_from_any_start() -> None:
    rng = random.Random(32)
    for _ in range(120):
        n = rng.randint(1, 4)
        gains = [F(rng.randint(1, 60), rng.randint(1, 6)) for _ in range(n)]
        b_max = rng.randint(1, 6)
        gap = F(rng.randint(1, 9))
        budget = F(rng.randint(0, 400), 10)
        start = [rng.randint(0, b_max) for _ in range(n)]
        bits, e, _ = levin_campello(gains, start, budget=budget, gap=gap, b_max=b_max)
        assert e == power_of(gains, bits, gap) and e <= budget
        assert (-sum(bits), e) == brute(gains, b_max, gap, budget=budget)


def test_swaps_are_half_the_distance_to_the_optimum() -> None:
    rng = random.Random(33)
    for _ in range(200):
        n = rng.randint(2, 40)
        gains = [rng.uniform(0.1, 100) for _ in range(n)]
        start = [rng.randint(0, 8) for _ in range(n)]
        target = sum(start)
        best = greedy(gains, target)
        bits, e, swaps = levin_campello(gains, start, target_bits=target)
        assert bits == best
        assert 2 * swaps == sum(abs(a - b) for a, b in zip(start, best))
        assert abs(e - power_of(gains, best)) < 1e-9 * (1 + e)


def test_ties_never_need_more_swaps() -> None:
    rng = random.Random(34)
    for _ in range(200):
        n = rng.randint(2, 6)
        gains = [F(rng.choice([1, 2, 4, 8])) for _ in range(n)]
        start = [rng.randint(0, 5) for _ in range(n)]
        best = greedy(gains, sum(start))
        bits, e, swaps = levin_campello(gains, start, target_bits=sum(start))
        assert e == power_of(gains, best)
        assert 2 * swaps <= sum(abs(a - b) for a, b in zip(start, best))


def test_start_near_water_filling() -> None:
    rng = random.Random(35)
    n, budget, gap = 256, 300.0, 10 ** (9.8 / 10)
    gains = [rng.expovariate(1 / 1000) + 1 for _ in range(n)]
    nu = [gap / g for g in gains]
    lo, hi = 0.0, max(nu) + budget
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if sum(max(0.0, mid - v) for v in nu) < budget else (lo, mid)
    start = [max(0, math.floor(math.log2(lo / v))) if lo > v else 0 for v in nu]
    bits, e, swaps = levin_campello(gains, start, budget=budget, gap=gap)
    ref = greedy(gains, sum(bits), gap)
    assert abs(e - power_of(gains, ref, gap)) < 1e-9 * e
    assert e <= budget
    assert power_of(gains, greedy(gains, sum(bits) + 1, gap), gap) > budget
    assert sum(bits) - sum(start) < n


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        levin_campello([1, 2], [0, 0])
    with pytest.raises(ValueError):
        levin_campello([1, 2], [0], target_bits=1)
    with pytest.raises(ValueError):
        levin_campello([1, 0], [0, 0], target_bits=1)
    with pytest.raises(ValueError):
        levin_campello([1, 2], [0, 5], target_bits=1, b_max=3)
    with pytest.raises(ValueError):
        levin_campello([1, 2], [0, 0], target_bits=7, b_max=3)
    with pytest.raises(ValueError):
        levin_campello([1, 2], [0, 0], budget=-1)
    assert levin_campello([1, 2], [3, 3], target_bits=0) == ([0, 0], 0, 0)
