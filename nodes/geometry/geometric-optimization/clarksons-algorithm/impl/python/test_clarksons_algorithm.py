# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clarksons-algorithm/. The authors are listed in prov/JER2FD.jsonl.

"""Tests for Clarkson's algorithm on the smallest enclosing disk, with exact arithmetic."""

import random
from fractions import Fraction
from itertools import combinations

from clarksons_algorithm import DELTA, clarkson, contains, disk_from, iterative, violators


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
    """True when c lies in the convex hull of pts (exact, by points, pairs and triples)."""
    if c in pts:
        return True
    for p, q in combinations(pts, 2):
        if orient(p, q, c) == 0 and min(p[0], q[0]) <= c[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= c[1] <= max(p[1], q[1]):
            return True
    for p, q, r in combinations(pts, 3):
        a, b, d = orient(p, q, c), orient(q, r, c), orient(r, p, c)
        if orient(p, q, r) != 0 and ((a >= 0 and b >= 0 and d >= 0) or (a <= 0 and b <= 0 and d <= 0)):
            return True
    return False


def certified(points, disk):
    """The smallest disk holds all points and has its center in the hull of the points on its circle."""
    cx, cy, r2 = disk
    if not all(contains(disk, p) for p in points):
        return False
    on = sorted({p for p in points if (p[0] - cx) ** 2 + (p[1] - cy) ** 2 == r2})
    return in_hull((cx, cy), on)


def test_empty_single_and_duplicates():
    assert clarkson([]) is None
    assert clarkson([(3, 4)]) == (3, 4, 0)
    assert clarkson([(3, 4)] * 200, random.Random(1)) == (3, 4, 0)
    assert clarkson([(0, 0), (4, 0)] * 100, random.Random(2)) == (2, 0, 4)


def test_lattice_disk():
    pts = [(x, y) for x in range(-10, 11) for y in range(-10, 11) if x * x + y * y <= 100]
    assert len(pts) == 317
    assert clarkson(pts, random.Random(5)) == (0, 0, 100)


def test_page_example():
    pts = [(x, y) for x in range(30) for y in range(10)]
    stats = {}
    disk = clarkson(pts, random.Random(0), stats=stats)
    assert disk == (Fraction(29, 2), Fraction(9, 2), Fraction(461, 2))
    assert stats["phases"] == 3


def test_small_against_brute_force():
    rng = random.Random(11)
    for _ in range(300):
        n = rng.randint(1, 9)
        pts = [(rng.randint(-5, 5), rng.randint(-5, 5)) for _ in range(n)]
        assert clarkson(pts, random.Random(rng.random())) == brute(pts)


def test_iterative_stage_certified():
    """With n above the base size, the reweighting loop runs; the answer is still exact."""
    rng = random.Random(12)
    for _ in range(40):
        n = rng.randint(40, 90)
        pts = [(rng.randint(-6, 6), rng.randint(-6, 6)) for _ in range(n)]
        stats = {}
        disk = iterative(pts, list(range(n)), random.Random(rng.random()), 30, stats)
        assert certified(pts, disk)
        assert stats["rounds"] >= 1


def test_large_certified_and_recursive_stage_runs():
    rng = random.Random(13)
    for trial in range(6):
        n = 400 + 200 * trial
        pts = [(rng.randint(-1000, 1000), rng.randint(-1000, 1000)) for _ in range(n)]
        stats = {}
        disk = clarkson(pts, random.Random(trial), stats=stats)
        assert certified(pts, disk)
        assert stats["phases"] >= 1
        assert stats["phases"] <= 25       # O(DELTA) phases in expectation


def test_collinear_and_cocircular():
    line = [(k, 2 * k) for k in range(-50, 51)]
    assert clarkson(line, random.Random(3)) == (0, 0, 50 * 50 + 100 * 100)
    circle = [(x, y) for x in range(-25, 26) for y in range(-25, 26) if x * x + y * y == 625]
    assert len(circle) == 20
    assert clarkson(circle * 10, random.Random(4)) == (0, 0, 625)


def test_fraction_input():
    pts = [(Fraction(1, 3), Fraction(0)), (Fraction(-2, 7), Fraction(1, 5)), (Fraction(0), Fraction(-3, 2))]
    pts = pts * 50
    assert clarkson(pts, random.Random(6)) == brute(pts)


def test_sampling_lemma_exactly():
    """Over all r-subsets R, the mean number of violators is at most DELTA (n - r) / (r + 1)."""
    rng = random.Random(14)
    for _ in range(3):
        pts = [(rng.randint(-20, 20), rng.randint(-20, 20)) for _ in range(10)]
        n = len(pts)
        for r in range(1, n):
            total = 0
            count = 0
            for sub in combinations(range(n), r):
                rest = [i for i in range(n) if i not in sub]
                total += len(violators(brute([pts[i] for i in sub]), pts, rest))
                count += 1
            assert Fraction(total, count) <= Fraction(DELTA * (n - r), r + 1)


def test_violators_meet_every_basis():
    """If R has violators, they include a point of every basis of the whole set (Lemma 3.1)."""
    rng = random.Random(15)
    for _ in range(5):
        pts = [(rng.randint(-8, 8), rng.randint(-8, 8)) for _ in range(9)]
        n = len(pts)
        best = brute(pts)
        bases = []
        for k in (1, 2, 3):
            for b in combinations(range(n), k):
                if brute([pts[i] for i in b]) == best and not any(set(c) <= set(b) for c in bases):
                    bases.append(b)
        assert bases
        for r in range(1, n):
            for sub in combinations(range(n), r):
                bad = set(violators(brute([pts[i] for i in sub]), pts, range(n)))
                if bad:
                    assert all(bad & set(b) for b in bases)
