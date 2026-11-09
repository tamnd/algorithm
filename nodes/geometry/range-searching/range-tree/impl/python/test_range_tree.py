# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/range-tree/. The authors are listed in prov/XGPFAM.jsonl.

import random
from fractions import Fraction

from range_tree import RangeTree


def scan(points, lo, hi):
    return sorted(p for p in points if all(lo[j] <= p[j] <= hi[j] for j in range(len(lo))))


EXAMPLE = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2), (3, 8), (6, 6)]


def test_worked_example():
    t = RangeTree(EXAMPLE)
    assert t.check_invariant()
    stats = {}
    assert sorted(t.report((3, 2), (7, 6), stats)) == [(5, 4), (6, 6), (7, 2)]
    assert stats["canonical"] == 3
    assert t.count((3, 2), (7, 6)) == 3
    assert t.top.canonical(1, 6) == [9, 5, 6]
    # n log n style space: 8 points on 4 levels of the x-tree, plus the x-array itself.
    assert t.size() == 8 + 8 * 4


def test_empty_and_single():
    t = RangeTree()
    assert len(t) == 0 and t.check_invariant()
    assert t.report((0, 0), (5, 5)) == [] and t.count((0, 0), (5, 5)) == 0
    t = RangeTree([(1, 2)])
    assert t.report((1, 2), (1, 2)) == [(1, 2)]
    assert t.count((0, 3), (5, 5)) == 0
    assert t.report((2, 0), (1, 5)) == []


def test_boundary_and_duplicates():
    pts = [(1, 1), (1, 1), (1, 2), (2, 1), (3, 3), (3, 3)]
    t = RangeTree(pts)
    assert t.check_invariant()
    assert sorted(t.report((1, 1), (1, 2))) == [(1, 1), (1, 1), (1, 2)]
    assert t.count((3, 3), (3, 3)) == 2
    assert t.count((2, 2), (2, 2)) == 0


def test_one_and_three_dimensions():
    t = RangeTree([(5,), (1,), (5,), (3,)])
    assert sorted(t.report((2,), (5,))) == [(3,), (5,), (5,)]
    pts = [(i % 3, i % 5, i % 7) for i in range(40)]
    t = RangeTree(pts)
    assert t.check_invariant()
    assert sorted(t.report((0, 1, 2), (1, 3, 5))) == scan(pts, (0, 1, 2), (1, 3, 5))


def test_fractions():
    pts = [(Fraction(i, 4), Fraction(i * i % 13, 3)) for i in range(25)]
    t = RangeTree(pts)
    lo, hi = (Fraction(1, 2), Fraction(1)), (Fraction(4), Fraction(3))
    assert sorted(t.report(lo, hi)) == scan(pts, lo, hi)


def test_random_against_scan():
    rng = random.Random(1979)
    for trial in range(600):
        d = rng.choice([1, 2, 2, 3])
        n = rng.randint(0, 30)
        c = rng.choice([2, 6, 30])
        pts = [tuple(rng.randint(0, c) for _ in range(d)) for _ in range(n)]
        t = RangeTree(pts, d)
        if trial % 10 == 0:
            assert t.check_invariant()
        for _ in range(4):
            lo = tuple(rng.randint(-1, c + 1) for _ in range(d))
            hi = tuple(rng.randint(-1, c + 1) for _ in range(d))
            want = scan(pts, lo, hi)
            stats = {}
            assert sorted(t.report(lo, hi, stats)) == want
            assert t.count(lo, hi) == len(want)


def test_canonical_nodes_logarithmic():
    rng = random.Random(5)
    n = 2000
    pts = [(rng.randint(0, 10 ** 6), rng.randint(0, 10 ** 6)) for _ in range(n)]
    t = RangeTree(pts)
    depth = (n - 1).bit_length()
    for _ in range(200):
        x1, x2 = sorted(rng.randint(0, 10 ** 6) for _ in range(2))
        y1, y2 = sorted(rng.randint(0, 10 ** 6) for _ in range(2))
        stats = {}
        got = t.count((x1, y1), (x2, y2), stats)
        assert got == len(scan(pts, (x1, y1), (x2, y2)))
        assert stats["canonical"] <= 2 * depth
