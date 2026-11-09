# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partition-tree/. The authors are listed in prov/CNGG0W.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from partition_tree import (CROSSED, INSIDE, OUTSIDE, PartitionTree, classify, convex_hull,
                            crosses, extreme, hull_chains, line_through, triangle_constraints,
                            value)


def scan(points, constraints):
    return sorted(p for p in points if all(value(h, p) <= 0 for h in constraints))


EXAMPLE = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2), (3, 8), (6, 6)]


def classes(t, v=0):
    return [sorted(t.pts[i] for i in t.perm[t.lo[w]:t.hi[w]]) for w in t.children[v]]


def test_worked_example():
    t = PartitionTree(EXAMPLE, r=4, leaf_size=2, seed=0)
    t.check_invariant()
    assert classes(t) == [[(2, 3), (5, 4)], [(7, 2), (8, 1)], [(6, 6), (9, 6)], [(3, 8), (4, 7)]]
    lines = [line_through(a, b) for a, b in itertools.combinations(sorted(EXAMPLE), 2)]
    numbers = [t.crossing_numbers(h)[0] for h in lines]
    assert max(numbers) == 2 and [numbers.count(c) for c in (0, 1, 2)] == [3, 3, 22]
    # x - y >= 1: one cell inside, one outside, two crossed
    h = (-1, 1, -1)
    assert [classify(t.cell[w], [h]) for w in t.children[0]] == [CROSSED, INSIDE, CROSSED, OUTSIDE]
    stats = {}
    count, out = t.query([h], stats=stats)
    assert count == 4 and sorted(out) == [(5, 4), (7, 2), (8, 1), (9, 6)]
    assert stats["visits"] == 5
    assert sorted(t.triangle((3, 1), (9, 5), (3, 7))) == [(5, 4), (6, 6)]
    box = [(-1, 0, -3), (1, 0, 7), (0, -1, -2), (0, 1, 6)]
    assert sorted(t.report(box)) == [(5, 4), (6, 6), (7, 2)]


def test_best_pairing_is_unique():
    lines = [line_through(a, b) for a, b in itertools.combinations(sorted(EXAMPLE), 2)]

    def pairings(s):
        if not s:
            yield []
            return
        for i in range(1, len(s)):
            for rest in pairings(s[1:i] + s[i + 1:]):
                yield [(s[0], s[i])] + rest

    worst = [max(sum(crosses(h, convex_hull(list(c))) for c in pr) for h in lines)
             for pr in pairings(sorted(EXAMPLE))]
    assert len(worst) == 105 and [worst.count(c) for c in (2, 3, 4)] == [1, 33, 71]
    xs = sorted(EXAMPLE)
    strips = [xs[i:i + 2] for i in range(0, 8, 2)]
    assert max(sum(crosses(h, convex_hull(c)) for c in strips) for h in lines) == 4


def test_empty_and_single():
    t = PartitionTree([])
    t.check_invariant()
    assert t.count([(1, 0, 5)]) == 0 and t.report([]) == []
    t = PartitionTree([(3, 3)])
    t.check_invariant()
    assert t.halfplane(1, 0, 3) == [(3, 3)]  # on the boundary line x = 3
    assert t.halfplane(1, 0, 2) == []
    assert t.triangle((3, 3), (5, 3), (3, 5)) == [(3, 3)]  # at a vertex
    assert t.triangle((4, 4), (6, 4), (4, 6)) == []


def test_duplicates_and_boundary():
    pts = [(2, 2)] * 7 + [(0, 0), (4, 0), (0, 4), (2, 0), (1, 1)]
    for seed in range(3):
        t = PartitionTree(pts, r=3, leaf_size=1, seed=seed)
        t.check_invariant()
        tri = triangle_constraints((0, 0), (4, 0), (0, 4))
        assert sorted(t.report(tri)) == sorted(pts)  # every point is in the closed triangle
        assert t.count(triangle_constraints((0, 0), (2, 2), (2, 0))) == 10
        assert t.count([(1, 1, 3)]) == 3  # x + y <= 3 misses the seven copies of (2, 2)
        assert t.count([(1, 1, 4)]) == 12


def test_all_points_equal_or_collinear():
    t = PartitionTree([(5, 5)] * 20, r=4, leaf_size=2, seed=1)
    t.check_invariant()
    assert t.count([(1, 0, 5)]) == 20 and t.count([(1, 0, 4)]) == 0
    line = [(i, 2 * i) for i in range(30)]
    t = PartitionTree(line, r=4, leaf_size=3, seed=2)
    t.check_invariant()
    assert sorted(t.report([(-2, 1, 0), (2, -1, 0), (1, 0, 10)])) == line[:11]


def test_degenerate_triangle_rejected():
    with pytest.raises(ValueError):
        triangle_constraints((0, 0), (1, 1), (2, 2))
    with pytest.raises(ValueError):
        PartitionTree([(0, 0)], r=1)


def test_against_linear_scan():
    for seed in (1, 2, 3, 4, 5):
        rng = random.Random(seed)
        n = rng.choice([2, 9, 40, 150])
        pts = [(rng.randrange(12), rng.randrange(12)) for _ in range(n)]
        t = PartitionTree(pts, r=rng.choice([2, 3, 4, 8]), leaf_size=rng.choice([1, 2, 5]), seed=seed)
        t.check_invariant()
        for _ in range(60):
            if rng.random() < 0.5:
                a, b, c = _point(rng), _point(rng), _point(rng)
                while orient_zero(a, b, c):
                    c = _point(rng)
                cons = triangle_constraints(a, b, c)
            else:
                cons = [(rng.randrange(-3, 4), rng.randrange(-3, 4), rng.randrange(-20, 30))
                        for _ in range(rng.randrange(1, 4))]
            count, out = t.query(cons)
            assert sorted(out) == scan(pts, cons)
            assert count == len(out) == t.count(cons)


def orient_zero(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) == 0


def _point(rng):
    return (rng.randrange(12), rng.randrange(12))


def test_against_linear_scan_triangles_with_points_as_vertices():
    rng = random.Random(11)
    pts = [_point(rng) for _ in range(120)]
    t = PartitionTree(pts, r=6, leaf_size=4, seed=11)
    for _ in range(200):
        a, b, c = rng.sample(pts, 3)
        if orient_zero(a, b, c):
            continue
        cons = triangle_constraints(a, b, c)
        assert sorted(t.report(cons)) == scan(pts, cons)


def test_fractions():
    rng = random.Random(21)
    pts = [(Fraction(rng.randrange(40), 3), Fraction(rng.randrange(40), 7)) for _ in range(80)]
    t = PartitionTree(pts, r=5, leaf_size=3, seed=21)
    t.check_invariant()
    for _ in range(50):
        cons = [(Fraction(rng.randrange(-5, 6), 2), Fraction(rng.randrange(-5, 6), 3),
                 Fraction(rng.randrange(-30, 30), 5))]
        assert sorted(t.report(cons)) == scan(pts, cons)


def test_sublinear_visits():
    rng = random.Random(7)
    pts = [(rng.randrange(10 ** 6), rng.randrange(10 ** 6)) for _ in range(2000)]
    t = PartitionTree(pts, r=16, leaf_size=8, seed=1)
    total = 0
    for _ in range(20):
        a, b = rng.sample(pts, 2)
        stats = {}
        t.query([line_through(a, b)], report=False, stats=stats)
        total += stats["visits"]
    assert total / 20 < 2000 / 4


def test_extreme_matches_brute_force():
    rng = random.Random(31)
    for _ in range(300):
        pts = [(rng.randrange(-6, 7), rng.randrange(-6, 7)) for _ in range(rng.randrange(1, 15))]
        if rng.random() < 0.2:
            pts = [(3, rng.randrange(9)) for _ in pts]  # all on a vertical line
        cell = hull_chains(pts)
        for _ in range(10):
            a, b = rng.randrange(-4, 5), rng.randrange(-4, 5)
            assert extreme(cell, a, b) == max(a * x + b * y for x, y in pts)


def test_small_fan_out_and_odd_sizes():
    for r in (2, 3):
        for n in range(1, 12):
            rng = random.Random(100 * r + n)
            pts = [_point(rng) for _ in range(n)]
            t = PartitionTree(pts, r=r, leaf_size=1, seed=n)
            t.check_invariant()
            assert t.count([(1, 0, 6)]) == sum(1 for p in pts if p[0] <= 6)
