# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direction-parallel-toolpath/. The authors are listed in prov/ZR545D.jsonl.

import math
import random
from collections import Counter
from fractions import Fraction as F

import pytest

from direction_parallel_toolpath import (
    direction_parallel,
    edges,
    in_region,
    path_segments,
    scanlines,
)

U_SHAPE = [[(0, 0), (10, 0), (10, 8), (7, 8), (7, 4), (3, 4), (3, 8), (0, 8)]]


def dist2(p, a, b):
    """Exact squared distance from p to the segment ab."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    dd = dx * dx + dy * dy
    t = 0 if dd == 0 else ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / dd
    t = min(1, max(0, t))
    qx, qy = a[0] + t * dx - p[0], a[1] + t * dy - p[1]
    return qx * qx + qy * qy


def fdist2(p, a, b):
    ax, ay, bx, by = float(a[0]), float(a[1]), float(b[0]), float(b[1])
    px, py = float(p[0]), float(p[1])
    dx, dy = bx - ax, by - ay
    dd = dx * dx + dy * dy
    t = 0.0 if dd == 0 else min(1.0, max(0.0, ((px - ax) * dx + (py - ay) * dy) / dd))
    qx, qy = ax + t * dx - px, ay + t * dy - py
    return qx * qx + qy * qy


def within(p, segs, r2):
    """Is p within distance sqrt(r2) of a segment? Floats first, exact near the threshold."""
    r2f = float(r2)
    for a, b in segs:
        d = fdist2(p, a, b)
        if d < r2f - 1e-9:
            return True
        if d <= r2f + 1e-9 and dist2(p, a, b) <= r2:
            return True
    return False


def in_dilation(rings, p, r2):
    """Brute force for the cut region C + D_r: p is in C or within r of an edge of C."""
    return in_region(rings, p) or within(p, list(edges(rings)), r2)


def star_with_hole(rng):
    k = rng.randrange(6, 11)
    outer = []
    for i in range(k):
        ang = 2 * math.pi * (i + rng.uniform(-0.2, 0.2)) / k
        rad = rng.uniform(4, 10)
        outer.append((F(round(4 * rad * math.cos(ang)), 4), F(round(4 * rad * math.sin(ang)), 4)))
    ox, oy = F(rng.randrange(-2, 3), 4), F(rng.randrange(-2, 3), 4)
    hole = [(ox - 1, oy - 1), (ox + F(3, 2), oy - F(1, 2)), (ox, oy + F(3, 2))]
    return [outer, hole]


def grid(rings, r, m):
    xs = [p[0] for ring in rings for p in ring]
    ys = [p[1] for ring in rings for p in ring]
    x0, x1, y0, y1 = min(xs) - r, max(xs) + r, min(ys) - r, max(ys) + r
    return [(x0 + (x1 - x0) * F(i, m), y0 + (y1 - y0) * F(j, m)) for i in range(m + 1) for j in range(m + 1)]


def test_u_shape_example():
    strokes = direction_parallel(U_SHAPE, 2)
    assert strokes[0] == [(0, 1), (10, 1), (10, 3), (0, 3), (0, 5), (3, 5), (3, 7), (0, 7)]
    assert strokes[1] == [(7, 5), (10, 5), (10, 7), (7, 7)]
    assert len(strokes) == 3 and len(strokes[2]) == 9
    lengths = [sum(math.dist(a, b) for a, b in zip(st, st[1:])) for st in strokes]
    assert lengths == [32, 8, 44]


def test_rasterized_cut_region_is_the_dilation():
    """Every grid point of C + D_r is within r of the path, and no other point is."""
    rng = random.Random(3)
    cases = [(U_SHAPE, F(1), F(2))]
    for _ in range(12):
        r = F(rng.randrange(4, 9), 4)
        cases.append((star_with_hole(rng), r, r * F(rng.randrange(5, 9), 4)))
    for rings, r, s in cases:
        segs = path_segments(direction_parallel(rings, s))
        for p in grid(rings, r, 28):
            assert in_dilation(rings, p, r * r) == within(p, segs, r * r), (p, r, s)


def test_tool_center_stays_in_region():
    rng = random.Random(7)
    for _ in range(12):
        rings = star_with_hole(rng)
        s = F(rng.randrange(4, 13), 4)
        for a, b in path_segments(direction_parallel(rings, s)):
            for i in range(17):
                t = F(i, 16)
                assert in_region(rings, (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))


def test_each_interval_is_cut_once():
    rng = random.Random(11)
    for _ in range(15):
        rings = star_with_hole(rng)
        s = F(rng.randrange(4, 13), 4)
        lines = scanlines(rings, s)
        want = Counter((y, lo, hi) for y, iv in lines for lo, hi in iv)
        strokes = direction_parallel(rings, s, contour=False)
        got = Counter()
        for a, b in path_segments(strokes):
            if a[1] == b[1]:
                got[(a[1], min(a[0], b[0]), max(a[0], b[0]))] += 1
        assert got == want


def test_without_contour_a_tongue_stays_uncut():
    tongue = [[(0, 0), (4, 0), (4, F(19, 10)), (12, F(19, 10)), (12, F(21, 10)),
               (4, F(21, 10)), (4, 4), (0, 4)]]
    p = (F(25, 2), F(2))
    assert in_dilation(tongue, p, 1)
    assert not within(p, path_segments(direction_parallel(tongue, 2, contour=False)), 1)
    assert within(p, path_segments(direction_parallel(tongue, 2)), 1)


def test_step_over_above_twice_the_radius_leaves_material():
    square = [[(0, 0), (10, 0), (10, 10), (0, 10)]]
    segs = path_segments(direction_parallel(square, 3))
    assert [y for y, _ in scanlines(square, 3)] == [F(3, 2), F(9, 2), F(15, 2)]
    assert in_dilation(square, (5, 3), 1) and not within((5, 3), segs, 1)


def test_bad_input():
    with pytest.raises(ValueError):
        direction_parallel(U_SHAPE, 0)
    with pytest.raises(ValueError):
        direction_parallel([[(0, 0), (1, 0)]], 1)
