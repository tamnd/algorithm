# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/miss-ratio-curve/. The authors are listed in prov/38ZHAR.jsonl.

import random
from fractions import Fraction

from miss_ratio_curve import (
    fifo_misses,
    lower_convex_hull,
    lru_curve_from_distances,
    lru_misses,
    miss_ratio_curve,
    talus_split,
)

BELADY = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]


def test_lru_curve_is_non_increasing() -> None:
    rng = random.Random(1)
    for _ in range(50):
        trace = [rng.randrange(rng.randint(1, 30)) for _ in range(rng.randint(1, 300))]
        curve = miss_ratio_curve(trace, range(0, 35))
        assert all(a >= b for a, b in zip(curve, curve[1:]))
        assert curve[0] == 1
        assert curve[-1] == Fraction(len(set(trace)), len(trace))


def test_lru_curve_from_reuse_distances_equals_simulation() -> None:
    rng = random.Random(2)
    for _ in range(50):
        trace = [rng.randrange(25) for _ in range(rng.randint(1, 300))]
        assert lru_curve_from_distances(trace, 30) == miss_ratio_curve(trace, range(31))


def test_fifo_curve_can_rise() -> None:
    curve = miss_ratio_curve(BELADY, [3, 4], fifo_misses)
    assert curve == [Fraction(9, 12), Fraction(10, 12)]
    assert miss_ratio_curve(BELADY, [3, 4], lru_misses) == [Fraction(10, 12), Fraction(8, 12)]


def test_loop_has_a_cliff() -> None:
    trace = list(range(8)) * 10
    curve = miss_ratio_curve(trace, range(10))
    assert curve[:8] == [1] * 8
    assert curve[8] == curve[9] == Fraction(8, 80)


def test_convex_hull_lies_below_and_is_convex() -> None:
    rng = random.Random(3)
    for _ in range(30):
        trace = [rng.randrange(20) for _ in range(200)] + list(range(20, 30)) * 5
        pts = [(Fraction(c), m) for c, m in enumerate(miss_ratio_curve(trace, range(32)))]
        hull = lower_convex_hull(pts)
        assert hull[0] == pts[0] and hull[-1] == pts[-1]
        for (x1, y1), (x2, y2), (x3, y3) in zip(hull, hull[1:], hull[2:]):
            assert (y2 - y1) / (x2 - x1) < (y3 - y2) / (x3 - x2)
        for x, y in pts:
            for (x1, y1), (x2, y2) in zip(hull, hull[1:]):
                if x1 <= x <= x2:
                    assert y >= y1 + (y2 - y1) * (x - x1) / (x2 - x1)


def test_talus_split_gives_the_line() -> None:
    alpha, beta, s = Fraction(2), Fraction(10), Fraction(5)
    rho, s1 = talus_split(alpha, beta, s)
    assert s1 / rho == alpha
    assert (s - s1) / (1 - rho) == beta


def test_talus_on_a_loop_reaches_the_hull() -> None:
    # One LRU cache of size 50 on a loop of 100 items misses every time. Split the items:
    # half of them (rho = 1/2) go to a partition of size 0, the other half to one of size 50.
    rng = random.Random(4)
    items = list(range(100))
    trace = items * 40
    rho, s1 = talus_split(Fraction(0), Fraction(100), Fraction(50))
    assert (rho, s1) == (Fraction(1, 2), 0)
    first = set(rng.sample(items, 50))
    a = [x for x in trace if x in first]
    b = [x for x in trace if x not in first]
    total = lru_misses(a, int(s1)) + lru_misses(b, 50 - int(s1))
    assert lru_misses(trace, 50) == len(trace)
    assert Fraction(total, len(trace)) == Fraction(2000 + 50, 4000)
