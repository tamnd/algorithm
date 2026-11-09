# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/range-tree-query/. The authors are listed in prov/ZMJ28C.jsonl.

import random
from fractions import Fraction

from range_tree_query import RangeTree2D


def scan(points, x1, x2, y1, y2):
    return sorted(p for p in points if x1 <= p[0] <= x2 and y1 <= p[1] <= y2)


EXAMPLE = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2), (3, 8), (6, 6)]


def test_worked_example():
    t = RangeTree2D(EXAMPLE)
    stats = {}
    got = t.report(3, 7, 2, 6, stats)
    assert got == [(5, 4), (6, 6), (7, 2)]
    assert stats["split_depth"] == 0
    assert stats["one_d_queries"] == 2
    assert t.count(3, 7, 2, 6) == 3


def test_empty_and_single():
    t = RangeTree2D()
    assert t.report(0, 9, 0, 9) == [] and t.count(0, 9, 0, 9) == 0
    t = RangeTree2D([(3, 3)])
    assert t.report(3, 3, 3, 3) == [(3, 3)]
    assert t.report(3, 3, 4, 9) == []
    assert t.report(4, 2, 0, 9) == []


def test_split_at_a_leaf_and_duplicates():
    pts = [(1, 5), (2, 5), (2, 5), (2, 7), (3, 1)]
    t = RangeTree2D(pts)
    assert t.report(3, 3, 0, 9) == [(3, 1)]
    assert sorted(t.report(2, 2, 5, 5)) == [(2, 5), (2, 5)]
    assert t.count(2, 2, 5, 7) == 3
    assert t.count(0, 9, 6, 6) == 0


def test_fractions():
    pts = [(Fraction(i, 5), Fraction((3 * i) % 7, 2)) for i in range(30)]
    t = RangeTree2D(pts)
    q = (Fraction(1, 3), Fraction(4), Fraction(1), Fraction(5, 2))
    assert sorted(t.report(*q)) == scan(pts, *q)


def test_random_against_scan():
    rng = random.Random(1980)
    for trial in range(700):
        n = rng.randint(0, 35)
        c = rng.choice([2, 8, 40])
        pts = [(rng.randint(0, c), rng.randint(0, c)) for _ in range(n)]
        t = RangeTree2D(pts)
        for _ in range(4):
            x1, x2 = rng.randint(-1, c + 1), rng.randint(-1, c + 1)
            y1, y2 = rng.randint(-1, c + 1), rng.randint(-1, c + 1)
            want = scan(pts, x1, x2, y1, y2)
            assert sorted(t.report(x1, x2, y1, y2)) == want
            assert t.count(x1, x2, y1, y2) == len(want)


def test_logarithmic_one_d_queries():
    rng = random.Random(11)
    n = 3000
    pts = [(rng.randint(0, 10 ** 5), rng.randint(0, 10 ** 5)) for _ in range(n)]
    t = RangeTree2D(pts)
    height = (n - 1).bit_length()
    for _ in range(300):
        x1, x2 = sorted(rng.randint(0, 10 ** 5) for _ in range(2))
        y1, y2 = sorted(rng.randint(0, 10 ** 5) for _ in range(2))
        stats = {}
        got = t.count(x1, x2, y1, y2, stats)
        assert got == len(scan(pts, x1, x2, y1, y2))
        assert stats["one_d_queries"] <= 2 * height
        assert stats["path_nodes"] <= 2 * height
