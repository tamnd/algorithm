# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/priority-search-tree-query/. The authors are listed in prov/ZHWQH0.jsonl.

import random
from fractions import Fraction

from priority_search_tree_query import PrioritySearchTree


def scan(points, x1, x2, y0):
    return sorted(p for p in points if x1 <= p[0] <= x2 and p[1] <= y0)


EXAMPLE = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2), (3, 8), (6, 6)]


def test_worked_example():
    t = PrioritySearchTree(EXAMPLE)
    st = {}
    got = t.query(3, 7, 6, st)
    assert got == [(5, 4), (7, 2), (6, 6)]
    assert st["subtrees"] == 2
    assert st["subtree_visits"] == 4
    assert st["path_nodes"] == 5


def test_empty_and_single():
    assert PrioritySearchTree().query(0, 9, 9) == []
    t = PrioritySearchTree([(3, 3)])
    assert t.query(3, 3, 3) == [(3, 3)]
    assert t.query(3, 3, 2) == []
    assert t.query(4, 2, 9) == []
    assert t.query(0, 2, 9) == []


def test_duplicates_and_boundary():
    pts = [(2, 5), (2, 5), (2, 5), (1, 5), (3, 5), (2, 4)]
    t = PrioritySearchTree(pts)
    assert sorted(t.query(2, 2, 5)) == [(2, 4), (2, 5), (2, 5), (2, 5)]
    assert t.query(2, 2, 4) == [(2, 4)]
    assert sorted(t.query(1, 3, 5)) == sorted(pts)
    assert t.query(1, 3, 3) == []


def test_fractions():
    pts = [(Fraction(i, 3), Fraction((5 * i) % 11, 4)) for i in range(25)]
    t = PrioritySearchTree(pts)
    q = (Fraction(1, 2), Fraction(6), Fraction(3, 2))
    assert sorted(t.query(*q)) == scan(pts, *q)


def test_random_against_scan():
    rng = random.Random(1080)
    for trial in range(800):
        n = rng.randint(0, 35)
        c = rng.choice([2, 8, 40])
        pts = [(rng.randint(0, c), rng.randint(0, c)) for _ in range(n)]
        t = PrioritySearchTree(pts)
        for _ in range(4):
            x1, x2 = rng.randint(-1, c + 1), rng.randint(-1, c + 1)
            y0 = rng.randint(-1, c + 1)
            assert sorted(t.query(x1, x2, y0)) == scan(pts, x1, x2, y0)


def test_output_sensitive_bounds():
    rng = random.Random(12)
    n = 4000
    pts = [(rng.randint(0, 10 ** 5), rng.randint(0, 10 ** 5)) for _ in range(n)]
    t = PrioritySearchTree(pts)
    height = (n - 1).bit_length()
    for _ in range(300):
        x1, x2 = sorted(rng.randint(0, 10 ** 5) for _ in range(2))
        y0 = rng.randint(0, 2 * 10 ** 4)
        st = {}
        got = t.query(x1, x2, y0, st)
        assert sorted(got) == scan(pts, x1, x2, y0)
        assert st["path_nodes"] <= 2 * height + 1
        assert st["subtrees"] <= 2 * height
        assert st["subtree_visits"] <= st["subtrees"] + 2 * len(got)
