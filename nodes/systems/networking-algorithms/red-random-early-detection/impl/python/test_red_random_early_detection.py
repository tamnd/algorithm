# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/red-random-early-detection/. The authors are listed in prov/A9935B.jsonl.

import math
import random
from collections import Counter
from fractions import Fraction

from red_random_early_detection import RED, simulate_red_queue


def test_average_after_a_ramp() -> None:
    # The queue grows by one packet at each arrival, from 1 to 100.
    red = RED(5, 15, 0.02, 0.001, random.Random(0))
    for q in range(1, 101):
        red.update_average(q)
    w = 0.001
    closed = 101 + ((1 - w) ** 101 - 1) / w
    assert math.isclose(red.avg, closed, rel_tol=1e-9)
    assert 4.88 < red.avg < 4.89


def test_thresholds() -> None:
    red = RED(5, 15, 0.1, 0.0, random.Random(1))
    red.avg = 4.999
    assert not any(red.arrival(4) for _ in range(1000))
    red.avg = 15.0
    assert all(red.arrival(20) for _ in range(1000))
    red.avg = 10.0
    assert math.isclose(red.marking_probability(), 0.05)


def test_count_correction_makes_gaps_uniform() -> None:
    # w_q = 0 freezes avg, so p_b = 0.2 * (10 - 5) / 10 = 0.1.
    red = RED(5, 15, 0.2, 0.0, random.Random(7))
    red.avg = 10.0
    gaps: list[int] = []
    g = 0
    for _ in range(50000):
        g += 1
        if red.arrival(1):
            gaps.append(g)
            g = 0
    c = Counter(gaps)
    assert set(c) == set(range(1, 11))  # never a gap above 1/p_b
    n = len(gaps)
    for k in range(1, 11):
        assert abs(c[k] / n - 0.1) < 0.015
    assert abs(sum(gaps) / n - 5.5) < 0.1


def test_gap_law_exact() -> None:
    # Pr[gap = n] = prod_{k<n} (1 - p_a(k-1)) * p_a(n-1) = p_b for n <= 1/p_b.
    for p_b in (Fraction(1, 4), Fraction(1, 10), Fraction(1, 7)):
        alive = Fraction(1)
        for n in range(1, int(1 / p_b) + 1):
            count = n - 1
            p_a = min(Fraction(1), p_b / (1 - count * p_b))
            assert alive * p_a == p_b
            alive *= 1 - p_a
        assert alive == 0


def test_without_correction_gaps_are_geometric() -> None:
    rng = random.Random(7)
    gaps: list[int] = []
    g = 0
    for _ in range(50000):
        g += 1
        if rng.random() < 0.1:
            gaps.append(g)
            g = 0
    long_gaps = sum(1 for x in gaps if x > 10) / len(gaps)
    assert abs(long_gaps - 0.9**10) < 0.03


def test_idle_decay() -> None:
    red = RED(5, 15, 0.1, 0.01, random.Random(2), s=1.0)
    red.avg = 10.0
    red.queue_empty(100.0)
    red.update_average(0, 150.0)
    assert math.isclose(red.avg, 10.0 * 0.99**50)


def test_queue_settles_between_thresholds() -> None:
    rng = random.Random(3)
    arrivals = [2 if rng.random() < 0.05 else 1 for _ in range(20000)]
    red = RED(5, 15, 0.1, 0.002, random.Random(4))
    qs, avgs, early, overflow = simulate_red_queue(red, arrivals, 40)
    tail = avgs[10000:]
    assert 5 < sum(tail) / len(tail) < 15
    assert overflow == 0
    assert early > 0
    assert max(qs) < 40
