# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kd-tree-nearest-neighbor-search/. The authors are listed in prov/GXNZ91.jsonl.

import random
from fractions import Fraction

from kd_tree_nearest_neighbor_search import build, dist2, nearest


def brute(points, q):
    return min(dist2(p, q) for p in points)


def check(points, q) -> None:
    got = nearest(build(points), q)
    if not points:
        assert got is None
        return
    d2, p = got
    assert d2 == brute(points, q)
    assert p in points and dist2(p, q) == d2


def test_example() -> None:
    pts = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
    root = build(pts)
    assert root.point == (7, 2)
    stats = [0]
    assert nearest(root, (3, 6), stats) == (2, (4, 7))
    assert stats[0] == 3  # (7,2), (5,4), (4,7); the subtrees of (2,3) and (9,6) are pruned


def test_empty_and_single() -> None:
    assert nearest(build([]), (0, 0)) is None
    assert nearest(build([(3, 4)]), (0, 0)) == (25, (3, 4))


def test_duplicates_collinear_and_query_on_points() -> None:
    check([(1, 1)] * 5 + [(2, 2)], (2, 2))
    check([(x, 0) for x in range(10)], (4, 3))
    check([(0, y) for y in range(0, 50, 5)], (0, 12))
    pts = [(x, y) for x in range(5) for y in range(5)]
    for q in pts:
        assert nearest(build(pts), q)[0] == 0


def test_float_root_pitfall() -> None:
    # sqrt(10**16 + 1) and sqrt(10**16) are the same double; the exact answer is (-10**8, 0).
    pts = [(10**8, 1), (-(10**8), 0)]
    assert nearest(build(pts), (0, 0)) == (10**16, (-(10**8), 0))


def test_fractions_and_three_dimensions() -> None:
    check([(Fraction(1, 3), Fraction(2, 7)), (Fraction(1, 2), Fraction(0)), (Fraction(3), Fraction(-1, 5))], (Fraction(2, 5), Fraction(1, 9)))
    rng = random.Random(3)
    for _ in range(100):
        pts = [tuple(rng.randint(-5, 5) for _ in range(3)) for _ in range(rng.randint(1, 30))]
        check(pts, tuple(rng.randint(-6, 6) for _ in range(3)))


def test_random_against_brute_force() -> None:
    rng = random.Random(1977)
    for _ in range(800):
        n = rng.randint(0, 50)
        r = rng.choice([1, 3, 10, 1000])
        pts = [(rng.randint(-r, r), rng.randint(-r, r)) for _ in range(n)]
        check(pts, (rng.randint(-r - 2, r + 2), rng.randint(-r - 2, r + 2)))


def test_few_visits_on_spread_points() -> None:
    rng = random.Random(8)
    pts = [(rng.randint(0, 10**6), rng.randint(0, 10**6)) for _ in range(4096)]
    root = build(pts)
    stats = [0]
    for _ in range(300):
        nearest(root, (rng.randint(0, 10**6), rng.randint(0, 10**6)), stats)
    assert stats[0] / 300 < 100


def test_worst_case_points_on_a_circle() -> None:
    # All lattice points on x^2 + y^2 = 5525^2 are at the same distance from the center,
    # so pruning only ever skips empty subtrees and the query visits every node.
    r = 5525
    pts = []
    for x in range(-r, r + 1):
        y2 = r * r - x * x
        y = int(y2**0.5)
        while y * y > y2:
            y -= 1
        while (y + 1) * (y + 1) <= y2:
            y += 1
        if y * y == y2:
            pts.append((x, y))
            if y:
                pts.append((x, -y))
    root = build(pts)
    stats = [0]
    assert nearest(root, (0, 0), stats)[0] == r * r
    assert stats[0] == len(pts)
