# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/layered-range-tree/. The authors are listed in prov/HMB009.jsonl.

import random
from fractions import Fraction

from layered_range_tree import LayeredRangeTree


def scan(points, x1, x2, y1, y2):
    return sorted(p for p in points if x1 <= p[0] <= x2 and y1 <= p[1] <= y2)


EXAMPLE = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2), (3, 8), (6, 6)]


def test_worked_example():
    t = LayeredRangeTree(EXAMPLE)
    t.check_invariant()
    assert t.left[1] == [0, 0, 0, 1, 2, 2, 2, 3, 4]
    stats = {}
    got = t.report(3, 7, 2, 6, stats)
    assert got == [(5, 4), (6, 6), (7, 2)]
    assert stats["binary_searches"] == 2
    assert stats["canonical"] == 2
    assert t.count(3, 7, 2, 6) == 3


def test_empty_and_single():
    t = LayeredRangeTree()
    t.check_invariant()
    assert t.report(0, 9, 0, 9) == [] and t.count(0, 9, 0, 9) == 0
    t = LayeredRangeTree([(3, 3)])
    t.check_invariant()
    assert t.report(3, 3, 3, 3) == [(3, 3)]
    assert t.report(3, 3, 4, 9) == []
    assert t.report(4, 2, 0, 9) == []
    assert t.count(0, 9, 5, 1) == 0


def test_duplicates_and_boundary():
    pts = [(1, 5), (2, 5), (2, 5), (2, 7), (3, 1), (2, 5)]
    t = LayeredRangeTree(pts)
    t.check_invariant()
    assert t.report(3, 3, 0, 9) == [(3, 1)]
    assert sorted(t.report(2, 2, 5, 5)) == [(2, 5)] * 3
    assert t.count(2, 2, 5, 7) == 4
    assert t.count(0, 9, 6, 6) == 0
    assert t.count(1, 3, 1, 7) == 6


def test_fractions():
    pts = [(Fraction(i, 5), Fraction((3 * i) % 7, 2)) for i in range(30)]
    t = LayeredRangeTree(pts)
    t.check_invariant()
    q = (Fraction(1, 3), Fraction(4), Fraction(1), Fraction(5, 2))
    assert sorted(t.report(*q)) == scan(pts, *q)


def test_random_against_scan():
    rng = random.Random(1986)
    for trial in range(700):
        n = rng.randint(0, 35)
        c = rng.choice([2, 8, 40])
        pts = [(rng.randint(0, c), rng.randint(0, c)) for _ in range(n)]
        t = LayeredRangeTree(pts)
        if trial % 50 == 0:
            t.check_invariant()
        for _ in range(4):
            x1, x2 = rng.randint(-1, c + 1), rng.randint(-1, c + 1)
            y1, y2 = rng.randint(-1, c + 1), rng.randint(-1, c + 1)
            want = scan(pts, x1, x2, y1, y2)
            assert sorted(t.report(x1, x2, y1, y2)) == want
            assert t.count(x1, x2, y1, y2) == len(want)


def test_two_binary_searches_and_logarithmic_path():
    rng = random.Random(5)
    n = 3000
    pts = [(rng.randint(0, 10 ** 5), rng.randint(0, 10 ** 5)) for _ in range(n)]
    t = LayeredRangeTree(pts)
    height = (n - 1).bit_length()
    for _ in range(300):
        x1, x2 = sorted(rng.randint(0, 10 ** 5) for _ in range(2))
        y1, y2 = sorted(rng.randint(0, 10 ** 5) for _ in range(2))
        stats = {}
        got = t.count(x1, x2, y1, y2, stats)
        assert got == len(scan(pts, x1, x2, y1, y2))
        assert stats["binary_searches"] <= 2
        assert stats["path_nodes"] <= 2 * height
        assert stats["canonical"] <= 2 * height
