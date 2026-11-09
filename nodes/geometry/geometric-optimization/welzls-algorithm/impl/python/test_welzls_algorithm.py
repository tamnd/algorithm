# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/welzls-algorithm/. The authors are listed in prov/BA4QGE.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from welzls_algorithm import contains, disk_from, minidisk


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def brute(points):
    """Smallest disk by trying every point, pair and non-collinear triple."""
    pts = sorted(set(points))
    if not pts:
        return None
    cands = [disk_from([p]) for p in pts]
    cands += [disk_from(list(c)) for c in combinations(pts, 2)]
    cands += [disk_from(list(c)) for c in combinations(pts, 3) if orient(*c) != 0]
    best = None
    for d in cands:
        if all(contains(d, p) for p in pts) and (best is None or d[2] < best[2]):
            best = d
    return best


def in_hull(c, pts):
    """True when c lies in the convex hull of pts (exact, by pairs and triples)."""
    for p in pts:
        if p == c:
            return True
    for p, q in combinations(pts, 2):
        if orient(p, q, c) == 0 and min(p[0], q[0]) <= c[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= c[1] <= max(p[1], q[1]):
            return True
    for p, q, r in combinations(pts, 3):
        a, b, d = orient(p, q, c), orient(q, r, c), orient(r, p, c)
        if (a >= 0 and b >= 0 and d >= 0) or (a <= 0 and b <= 0 and d <= 0):
            if orient(p, q, r) != 0:
                return True
    return False


def certified(points, disk):
    """A disk is the smallest one iff it holds all points and its center is in the hull of the points on its circle."""
    cx, cy, r2 = disk
    if not all(contains(disk, p) for p in points):
        return False
    on = sorted({p for p in points if (p[0] - cx) ** 2 + (p[1] - cy) ** 2 == r2})
    return in_hull((cx, cy), on)


def test_empty_and_single():
    assert minidisk([]) is None
    assert minidisk([(3, 4)]) == (3, 4, 0)
    assert minidisk([(3, 4)] * 5) == (3, 4, 0)


def test_example_of_the_page():
    pts = [(0, 0), (6, 0), (2, 4), (3, 1), (5, 3), (1, 2)]
    assert minidisk(pts, random.Random(1)) == (3, 1, 10)


def test_collinear_and_duplicates():
    pts = [(0, 0), (2, 2), (1, 1), (5, 5), (5, 5), (3, 3)]
    assert minidisk(pts, random.Random(2)) == (Fraction(5, 2), Fraction(5, 2), Fraction(25, 2))
    pts = [(0, 0), (4, 0)] * 4
    assert minidisk(pts, random.Random(3)) == (2, 0, 4)


def test_cocircular():
    pts = [(5, 0), (0, 5), (-5, 0), (0, -5), (3, 4), (-4, 3), (4, -3), (-3, -4)]
    for seed in range(20):
        assert minidisk(pts, random.Random(seed)) == (0, 0, 25)


def test_random_small_against_brute_force():
    rng = random.Random(12345)
    for _ in range(800):
        n = rng.randint(1, 9)
        k = rng.choice([2, 4, 10])
        pts = [(rng.randint(-k, k), rng.randint(-k, k)) for _ in range(n)]
        if rng.random() < 0.2:
            pts += [rng.choice(pts) for _ in range(3)]
        want = brute(pts)
        for mtf in (True, False):
            assert minidisk(pts, random.Random(rng.random()), mtf) == want


def test_random_collinear():
    rng = random.Random(7)
    for _ in range(200):
        a, b = rng.randint(-3, 3), rng.randint(-3, 3)
        pts = [(t * a, t * b + 1) for t in (rng.randint(-6, 6) for _ in range(rng.randint(1, 7)))]
        assert minidisk(pts, random.Random(rng.random())) == brute(pts)


def test_large_certified():
    rng = random.Random(99)
    for _ in range(60):
        n = rng.randint(50, 300)
        pts = [(rng.randint(-1000, 1000), rng.randint(-1000, 1000)) for _ in range(n)]
        d = minidisk(pts, random.Random(rng.random()))
        assert certified(pts, d)
        assert minidisk(pts, random.Random(5), mtf=False) == d


def test_fraction_input():
    pts = [(Fraction(1, 3), Fraction(0)), (Fraction(-1, 3), Fraction(0)), (Fraction(0), Fraction(1, 7))]
    assert minidisk(pts, random.Random(0)) == brute(pts)
