# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partition-tree-query/. The authors are listed in prov/T2GH1M.jsonl.

import random
from fractions import Fraction

import pytest

from partition_tree_query import (PartitionTree, extreme, hull_chains, line_through,
                                  partition_tree_query, triangle_constraints, value)


def scan(points, constraints):
    return sorted(p for p in points if all(value(h, p) <= 0 for h in constraints))


def collinear(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) == 0


EXAMPLE = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2), (3, 8), (6, 6)]


def test_worked_example():
    t = PartitionTree(EXAMPLE, r=4, leaf_size=2, seed=0)
    tri = triangle_constraints((1, 0), (10, 0), (10, 9))
    assert tri == [(0, -9, 0), (9, 0, 90), (-9, 9, -9)]
    stats = {}
    count, out = partition_tree_query(t, tri, stats=stats)
    assert count == 4 and out == [(5, 4), (7, 2), (8, 1), (9, 6)]
    assert stats == {"visits": 5, "inside": 1, "outside": 1, "scanned": 4}
    # the bounds of -9x + 9y over the four cells, against c = -9
    assert (-extreme(t.cell[0], 9, -9), extreme(t.cell[0], -9, 9)) == (-63, 45)
    cells = [t.cell[w] for w in t.children[0]]
    assert [(-extreme(c, 9, -9), extreme(c, -9, 9)) for c in cells] == [
        (-9, 9), (-63, -45), (-27, 0), (27, 45)]
    stats = {}
    count, out = partition_tree_query(t, triangle_constraints((3, 1), (9, 5), (3, 7)), stats=stats)
    assert count == 2 and sorted(out) == [(5, 4), (6, 6)]
    assert stats == {"visits": 5, "inside": 0, "outside": 2, "scanned": 4}
    box = [(-1, 0, -3), (1, 0, 7), (0, -1, -2), (0, 1, 6)]  # [3, 7] x [2, 6]
    assert partition_tree_query(t, box, report=False) == 3


def test_empty_and_single():
    t = PartitionTree([])
    assert partition_tree_query(t, [(1, 1, 1)]) == (0, [])
    t = PartitionTree([(4, 4)])
    assert partition_tree_query(t, [(1, 1, 8)]) == (1, [(4, 4)])  # on the line x + y = 8
    assert partition_tree_query(t, [(1, 1, 7)]) == (0, [])
    assert partition_tree_query(t, []) == (1, [(4, 4)])  # no constraint: the whole plane


def test_duplicates_and_boundary():
    pts = [(3, 3)] * 6 + [(0, 0), (6, 0), (0, 6), (3, 0), (0, 3)]
    t = PartitionTree(pts, r=3, leaf_size=2, seed=4)
    tri = triangle_constraints((0, 0), (6, 0), (0, 6))
    assert sorted(partition_tree_query(t, tri)[1]) == sorted(pts)
    assert partition_tree_query(t, [(1, 1, 6)], report=False) == 11
    assert partition_tree_query(t, [(1, 1, 5)], report=False) == 3
    assert partition_tree_query(t, [(-1, 0, -3), (0, -1, -3)], report=False) == 6


def test_degenerate_triangle_rejected():
    with pytest.raises(ValueError):
        triangle_constraints((1, 1), (2, 2), (5, 5))


def test_against_linear_scan():
    for seed in (1, 2, 3, 4, 5, 6):
        rng = random.Random(seed)
        n = rng.choice([1, 2, 7, 30, 120])
        pts = [(rng.randrange(10), rng.randrange(10)) for _ in range(n)]
        t = PartitionTree(pts, r=rng.choice([2, 4, 6]), leaf_size=rng.choice([1, 3]), seed=seed)
        for _ in range(80):
            kind = rng.randrange(3)
            if kind == 0:
                a, b, c = [(rng.randrange(11), rng.randrange(11)) for _ in range(3)]
                if collinear(a, b, c):
                    continue
                cons = triangle_constraints(a, b, c)
            elif kind == 1:
                cons = [(rng.randrange(-3, 4), rng.randrange(-3, 4), rng.randrange(-15, 25))]
            else:
                x1, x2 = sorted((rng.randrange(10), rng.randrange(10)))
                y1, y2 = sorted((rng.randrange(10), rng.randrange(10)))
                cons = [(-1, 0, -x1), (1, 0, x2), (0, -1, -y1), (0, 1, y2)]
            count, out = partition_tree_query(t, cons)
            assert sorted(out) == scan(pts, cons) and count == len(out)
            assert partition_tree_query(t, cons, report=False) == count


def test_fractions():
    rng = random.Random(8)
    pts = [(Fraction(rng.randrange(30), 4), Fraction(rng.randrange(30), 5)) for _ in range(60)]
    t = PartitionTree(pts, r=4, leaf_size=2, seed=8)
    for _ in range(40):
        a, b, c = rng.sample(pts, 3)
        if collinear(a, b, c):
            continue
        cons = triangle_constraints(a, b, c)
        assert sorted(partition_tree_query(t, cons)[1]) == scan(pts, cons)


def test_extreme_matches_brute_force():
    rng = random.Random(9)
    for _ in range(300):
        pts = [(rng.randrange(-5, 6), rng.randrange(-5, 6)) for _ in range(rng.randrange(1, 12))]
        cell = hull_chains(pts)
        for _ in range(8):
            a, b = rng.randrange(-3, 4), rng.randrange(-3, 4)
            assert extreme(cell, a, b) == max(a * x + b * y for x, y in pts)


def test_every_opened_node_is_crossed():
    rng = random.Random(10)
    pts = [(rng.randrange(1000), rng.randrange(1000)) for _ in range(500)]
    t = PartitionTree(pts, r=8, leaf_size=4, seed=10)
    for _ in range(20):
        p, q = rng.sample(pts, 2)
        h = line_through(p, q)
        stats = {}
        partition_tree_query(t, [h], report=False, stats=stats)
        crossed = stats["visits"] - stats["inside"] - stats["outside"]
        opened = [v for v in range(len(t.lo))
                  if min(value(h, x) for x in t.cell[v][0] + t.cell[v][1]) <= 0
                  < max(value(h, x) for x in t.cell[v][0] + t.cell[v][1])]
        assert crossed <= len(opened)
        assert stats["visits"] < len(t.lo)
