# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/priority-search-tree/. The authors are listed in prov/2MY7Y5.jsonl.

import random
from fractions import Fraction

from priority_search_tree import PrioritySearchTree


def scan(points, x1, x2, y0):
    return sorted(p for p in points if x1 <= p[0] <= x2 and p[1] <= y0)


def lowest(points, x1, x2):
    c = [p for p in points if x1 <= p[0] <= x2]
    return min(c, key=lambda p: (p[1], p[0])) if c else None


EXAMPLE = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2), (3, 8), (6, 6)]


def test_worked_example():
    t = PrioritySearchTree(EXAMPLE)
    t.check_invariant()
    stored = {v: t.pts[j] for v, j in t.node.items()}
    assert stored == {1: (8, 1), 2: (2, 3), 3: (7, 2), 4: (3, 8),
                      5: (5, 4), 6: (6, 6), 7: (9, 6), 10: (4, 7)}
    assert sorted(t.three_sided(3, 7, 6)) == [(5, 4), (6, 6), (7, 2)]
    assert t.lowest_in_x_range(3, 7) == (7, 2)
    assert t.lowest_in_x_range(9, 9) == (9, 6)


def test_empty_and_single():
    t = PrioritySearchTree()
    t.check_invariant()
    assert t.three_sided(0, 9, 9) == [] and t.lowest_in_x_range(0, 9) is None
    t = PrioritySearchTree([(3, 3)])
    t.check_invariant()
    assert t.three_sided(3, 3, 3) == [(3, 3)]
    assert t.three_sided(3, 3, 2) == []
    assert t.three_sided(4, 2, 9) == []
    assert t.lowest_in_x_range(3, 3) == (3, 3)


def test_duplicates_and_boundary():
    pts = [(2, 5), (2, 5), (2, 5), (1, 5), (3, 5), (2, 4)]
    t = PrioritySearchTree(pts)
    t.check_invariant()
    assert sorted(t.three_sided(2, 2, 5)) == [(2, 4), (2, 5), (2, 5), (2, 5)]
    assert t.three_sided(2, 2, 4) == [(2, 4)]
    assert sorted(t.three_sided(1, 3, 5)) == sorted(pts)


def test_fractions():
    pts = [(Fraction(i, 3), Fraction((5 * i) % 11, 4)) for i in range(25)]
    t = PrioritySearchTree(pts)
    t.check_invariant()
    assert sorted(t.three_sided(Fraction(1, 2), Fraction(6), Fraction(3, 2))) == \
        scan(pts, Fraction(1, 2), Fraction(6), Fraction(3, 2))


def test_random_against_scan():
    rng = random.Random(1985)
    for trial in range(700):
        n = rng.randint(0, 35)
        c = rng.choice([2, 8, 40])
        pts = [(rng.randint(0, c), rng.randint(0, c)) for _ in range(n)]
        t = PrioritySearchTree(pts)
        if trial % 25 == 0:
            t.check_invariant()
        for _ in range(4):
            x1, x2 = rng.randint(-1, c + 1), rng.randint(-1, c + 1)
            y0 = rng.randint(-1, c + 1)
            assert sorted(t.three_sided(x1, x2, y0)) == scan(pts, x1, x2, y0)
            assert t.lowest_in_x_range(x1, x2) == lowest(pts, x1, x2)


def test_output_sensitive_bounds():
    rng = random.Random(10)
    n = 4000
    pts = [(rng.randint(0, 10 ** 5), rng.randint(0, 10 ** 5)) for _ in range(n)]
    t = PrioritySearchTree(pts)
    height = (n - 1).bit_length()
    for _ in range(300):
        x1, x2 = sorted(rng.randint(0, 10 ** 5) for _ in range(2))
        y0 = rng.randint(0, 10 ** 4)
        st = {}
        got = t.three_sided(x1, x2, y0, st)
        assert sorted(got) == scan(pts, x1, x2, y0)
        assert st["calls"] <= 4 * height + 2 * len(got) + 5
        st = {}
        t.lowest_in_x_range(x1, x2, st)
        assert st["calls"] <= 4 * height + 5
