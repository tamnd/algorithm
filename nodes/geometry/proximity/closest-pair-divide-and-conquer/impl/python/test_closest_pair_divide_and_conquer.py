# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/closest-pair-divide-and-conquer/. The authors are listed in prov/N8YEH7.jsonl.

import itertools
import random
from fractions import Fraction

from closest_pair_divide_and_conquer import closest_pair_divide_and_conquer, dist2, strip_checks


def brute(points):
    if len(points) < 2:
        return None
    return min(dist2(p, q) for p, q in itertools.combinations(points, 2))


def check(points) -> None:
    got = closest_pair_divide_and_conquer(points)
    want = brute(points)
    if want is None:
        assert got is None
        return
    d2, p, q = got
    assert d2 == want
    assert dist2(p, q) == d2
    # p and q are two different items of the list (equal values only if duplicated).
    assert p in points and q in points
    if p == q:
        assert points.count(p) >= 2


def test_example() -> None:
    pts = [(0, 0), (1, 9), (3, 6), (4, 2), (5, 3), (7, 0), (8, 8), (9, 5)]
    d2, p, q = closest_pair_divide_and_conquer(pts)
    assert d2 == 2 and {p, q} == {(4, 2), (5, 3)}


def test_small_sizes() -> None:
    assert closest_pair_divide_and_conquer([]) is None
    assert closest_pair_divide_and_conquer([(3, 4)]) is None
    assert closest_pair_divide_and_conquer([(0, 0), (3, 4)]) == (25, (0, 0), (3, 4))
    check([(0, 0), (5, 5), (1, 1)])


def test_duplicates() -> None:
    pts = [(1, 1), (7, 3), (2, 9), (7, 3), (0, 5)]
    assert closest_pair_divide_and_conquer(pts)[0] == 0
    assert closest_pair_divide_and_conquer([(4, 4)] * 6)[0] == 0


def test_collinear_and_same_x() -> None:
    check([(0, y) for y in (0, 10, 3, 7, 20, 21, 40)])
    check([(x, 0) for x in (5, 1, 9, 13, 2, 30)])
    check([(x, 2 * x + 1) for x in range(0, 50, 7)])
    # Many points share the split x-coordinate.
    check([(5, y) for y in range(0, 30, 3)] + [(4, 1), (6, 100)])


def test_float_root_pitfall() -> None:
    # sqrt(10**16 + 1) == sqrt(10**16) in doubles, but the exact answer is the pair at 10**16.
    a, b, c = (0, 0), (10**8, 1), (-(10**8), 0)
    d2, p, q = closest_pair_divide_and_conquer([a, b, c])
    assert d2 == 10**16 and {p, q} == {a, c}


def test_fractions() -> None:
    pts = [(Fraction(1, 3), Fraction(0)), (Fraction(2, 3), Fraction(1, 7)), (Fraction(5), Fraction(5)), (Fraction(1, 2), Fraction(1, 9))]
    check(pts)


def test_random_against_all_pairs() -> None:
    rng = random.Random(1975)
    for _ in range(700):
        n = rng.randint(0, 40)
        r = rng.choice([1, 3, 10, 1000])  # small grids force ties, duplicates and collinear points
        pts = [(rng.randint(-r, r), rng.randint(-r, r)) for _ in range(n)]
        check(pts)


def test_packing_bound_seven() -> None:
    rng = random.Random(33)
    worst = 0
    for _ in range(300):
        n = rng.randint(2, 60)
        r = rng.choice([2, 4, 20])
        pts = list({(rng.randint(-r, r), rng.randint(-r, r)) for _ in range(n)})
        worst = max(worst, strip_checks(pts))
    assert worst <= 7
    # A dense grid makes the strip as full as it gets.
    grid = [(x, y) for x in range(8) for y in range(8)]
    assert strip_checks(grid) <= 7
