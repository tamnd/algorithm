# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kd-tree-range-search/. The authors are listed in prov/XJ7XNM.jsonl.

import math
import random
from fractions import Fraction

from kd_tree_range_search import KDTree


def scan(points, x1, x2, y1, y2):
    return sorted(p for p in points if x1 <= p[0] <= x2 and y1 <= p[1] <= y2)


EXAMPLE = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2), (3, 8), (6, 6)]


def test_worked_example():
    t = KDTree(EXAMPLE)
    assert t.check_invariant()
    stats = {}
    got = t.query(3, 7, 2, 6, stats)
    assert sorted(got) == [(5, 4), (6, 6), (7, 2)]
    assert stats["search_nodes"] == 6
    assert stats["reported_nodes"] == 3


def test_empty_and_single():
    t = KDTree()
    assert len(t) == 0 and t.check_invariant()
    assert t.query(0, 10, 0, 10) == []
    t = KDTree([(4, 4)])
    assert t.query(4, 4, 4, 4) == [(4, 4)]
    assert t.query(0, 3, 0, 10) == []
    assert t.query(5, 1, 0, 10) == []


def test_boundary_and_duplicates():
    pts = [(1, 1), (1, 1), (1, 2), (2, 1), (3, 3), (3, 3), (3, 3)]
    t = KDTree(pts)
    assert t.check_invariant()
    assert sorted(t.query(1, 1, 1, 2)) == [(1, 1), (1, 1), (1, 2)]
    assert sorted(t.query(3, 3, 3, 3)) == [(3, 3)] * 3
    assert t.query(2, 2, 2, 2) == []


def test_all_on_one_vertical_line():
    pts = [(5, y) for y in range(200)]
    t = KDTree(pts)
    assert t.check_invariant()
    assert sorted(t.query(5, 5, 10, 19)) == [(5, y) for y in range(10, 20)]


def test_fractions():
    pts = [(Fraction(i, 3), Fraction(7 * i % 11, 2)) for i in range(30)]
    t = KDTree(pts)
    q = (Fraction(1), Fraction(5), Fraction(1, 2), Fraction(3))
    assert sorted(t.query(*q)) == scan(pts, *q)


def test_random_against_scan():
    rng = random.Random(1985)
    for trial in range(600):
        n = rng.randint(0, 40)
        c = rng.choice([3, 10, 50])
        pts = [(rng.randint(0, c), rng.randint(0, c)) for _ in range(n)]
        t = KDTree(pts)
        assert t.check_invariant()
        for _ in range(4):
            x1, x2 = rng.randint(-1, c + 1), rng.randint(-1, c + 1)
            y1, y2 = rng.randint(-1, c + 1), rng.randint(-1, c + 1)
            assert sorted(t.query(x1, x2, y1, y2)) == scan(pts, x1, x2, y1, y2)


def test_search_nodes_grow_like_square_root():
    rng = random.Random(42)
    for n in (256, 1024, 4096):
        pts = [(rng.randint(0, n), rng.randint(0, n)) for _ in range(n)]
        t = KDTree(pts)
        for _ in range(60):
            a = rng.randint(0, n)
            b = rng.randint(a, n)
            if rng.random() < 0.5:
                q = (a, b, a, a + rng.randint(0, 3))
            else:
                q = (a, b, 0, n)
            stats = {}
            got = t.query(*q, stats)
            assert sorted(got) == scan(pts, *q)
            assert stats["search_nodes"] <= 10 * math.isqrt(n) + 10
            assert stats["reported_nodes"] <= 2 * len(got)
