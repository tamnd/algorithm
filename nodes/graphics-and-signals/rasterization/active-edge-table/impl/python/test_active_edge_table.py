# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/active-edge-table/. The authors are listed in prov/3J25VA.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from active_edge_table import ActiveEdgeTable, fill_spans

K = 10**6


def edges_of(rings):
    out = []
    for ring in rings:
        for k in range(len(ring)):
            out.append((ring[k], ring[(k + 1) % len(ring)]))
    return out


def brute_crossings(rings, j):
    """All (x, direction) where an edge meets the center line of row j, by the half-open rule, sorted."""
    yc = Fraction(2 * j + 1, 2)
    out = []
    for a, b in edges_of(rings):
        if a[1] == b[1]:
            continue
        lo, hi = min(a[1], b[1]), max(a[1], b[1])
        if lo <= yc < hi:
            x = a[0] + (yc - a[1]) * Fraction(b[0] - a[0]) / (b[1] - a[1])
            out.append((x, 1 if a[1] < b[1] else -1))
    return sorted(out)


def orient(a, b, c):
    v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return (v > 0) - (v < 0)


def on_box(a, b, c):
    return min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= c[1] <= max(a[1], b[1])


def segments_meet(p1, p2, q1, q2):
    d1, d2 = orient(q1, q2, p1), orient(q1, q2, p2)
    d3, d4 = orient(p1, p2, q1), orient(p1, p2, q2)
    if d1 * d2 < 0 and d3 * d4 < 0:
        return True
    return (d1 == 0 and on_box(q1, q2, p1)) or (d2 == 0 and on_box(q1, q2, p2)) or (
        d3 == 0 and on_box(p1, p2, q1)) or (d4 == 0 and on_box(p1, p2, q2))


def winding(rings, px, py):
    w = 0
    for (ax, ay), (bx, by) in edges_of(rings):
        side = (bx - ax) * (py - ay) - (px - ax) * (by - ay)
        if ay <= py:
            if by > py and side > 0:
                w += 1
        elif by <= py and side < 0:
            w -= 1
    return w


def brute_fill(rings, width, height, rule):
    out = set()
    for j in range(height):
        for i in range(width):
            w = winding(rings, Fraction(2 * i + 1, 2) + Fraction(1, K), Fraction(2 * j + 1, 2) + Fraction(1, K * K))
            if (w % 2 == 1) if rule == "evenodd" else (w != 0):
                out.add((i, j))
    return out


def random_ring(rng, n, lo, hi):
    return [(Fraction(rng.randint(4 * lo, 4 * hi), 4), Fraction(rng.randint(4 * lo, 4 * hi), 4)) for _ in range(n)]


def test_page_example():
    # A bow tie: its two long edges cross between rows 1 and 2.
    bow = [(0, 0), (4, 4), (4, 0), (0, 4)]
    aet = ActiveEdgeTable([bow], 4)
    rows, swaps = [], []
    for _ in range(4):
        aet.next_row()
        rows.append(aet.crossings())
        swaps.append(aet.swaps)
    h = Fraction(1, 2)
    assert rows == [
        [(0, -1), (h, 1), (7 * h, 1), (4, -1)],
        [(0, -1), (3 * h, 1), (5 * h, 1), (4, -1)],
        [(0, -1), (3 * h, 1), (5 * h, 1), (4, -1)],
        [(0, -1), (h, 1), (7 * h, 1), (4, -1)],
    ]
    # The re-sort before row 2 swaps the two diagonals, which cross at (2, 2).
    assert swaps == [0, 0, 1, 1]
    assert fill_spans([bow], 4, 4) == [(0, 3, 4), (1, 0, 1), (1, 2, 4), (2, 0, 1), (2, 2, 4), (3, 3, 4)]


def test_crossings_match_brute_force():
    rng = random.Random(1972)
    for trial in range(300):
        height = rng.randint(1, 16)
        rings = [random_ring(rng, rng.randint(3, 9), -2, 18) for _ in range(rng.randint(1, 3))]
        if trial % 3 == 0:
            rings = [[(x, Fraction(2 * int(y) + 1, 2)) for x, y in ring] for ring in rings]
        aet = ActiveEdgeTable(rings, height)
        for _ in range(height):
            j = aet.next_row()
            got = aet.crossings()
            assert [x for x, _ in got] == sorted(x for x, _ in got)
            assert sorted(got) == brute_crossings(rings, j)


def test_swaps_bounded_by_crossing_pairs():
    rng = random.Random(1967)
    for _ in range(200):
        height = rng.randint(1, 16)
        rings = [random_ring(rng, rng.randint(3, 10), -1, 16)]
        aet = ActiveEdgeTable(rings, height)
        for _ in range(height):
            aet.next_row()
        es = [e for e in edges_of(rings) if e[0][1] != e[1][1]]
        pairs = sum(1 for (p1, p2), (q1, q2) in combinations(es, 2) if segments_meet(p1, p2, q1, q2))
        assert aet.swaps <= pairs


def test_convex_polygon_never_swaps():
    hexagon = [(3, 0), (7, 2), (7, 6), (3, 9), (0, 6), (0, 2)]
    aet = ActiveEdgeTable([hexagon], 10)
    for _ in range(10):
        aet.next_row()
        assert len(aet.crossings()) in (0, 2)
    assert aet.swaps == 0


def test_fill_against_brute_force():
    rng = random.Random(2024)
    for _ in range(80):
        width, height = rng.randint(1, 12), rng.randint(1, 12)
        rings = [random_ring(rng, rng.randint(3, 7), -2, 14) for _ in range(rng.randint(1, 2))]
        for rule in ("evenodd", "nonzero"):
            got = {(i, j) for j, lo, hi in fill_spans(rings, width, height, rule) for i in range(lo, hi)}
            assert got == brute_fill(rings, width, height, rule)
