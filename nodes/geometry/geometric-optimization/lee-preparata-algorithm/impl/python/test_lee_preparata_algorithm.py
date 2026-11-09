# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lee-preparata-algorithm/. The authors are listed in prov/A26CZG.jsonl.

"""Tests against an independent reference: Dijkstra on the visibility graph of s, t and the
polygon vertices, where visibility is decided exactly with Fractions. Lengths are compared
with a relative tolerance of 1e-9, because they are sums of square roots."""

import heapq
import random
from fractions import Fraction
from math import gcd, hypot, isclose

import pytest

from lee_preparata_algorithm import orient, path_length, shortest_path, triangulate

WALLS = [(0, 0), (4, 0), (4, 4), (5, 4), (5, 0), (12, 0), (12, 6), (9, 6), (9, 2), (8, 2), (8, 6), (0, 6)]
SPIRAL = [(0, 0), (10, 0), (10, 10), (2, 10), (2, 4), (6, 4), (6, 6), (4, 6), (4, 8), (8, 8), (8, 2), (0, 2)]
COMB = [(0, 0), (7, 0), (7, 4), (6, 4), (6, 1), (5, 1), (5, 4), (4, 4), (4, 1), (3, 1), (3, 4), (2, 4), (2, 1), (1, 1), (1, 4), (0, 4)]


def on_segment(a, b, p):
    return orient(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def inside_closed(poly, p):
    n = len(poly)
    odd = False
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if on_segment(a, b, p):
            return True
        if (a[1] > p[1]) != (b[1] > p[1]):
            x = a[0] + Fraction(p[1] - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if x > p[0]:
                odd = not odd
    return odd


def visible(poly, p, q):
    """The closed segment pq lies in the closed polygon: cut pq where it meets the boundary and test the midpoints."""
    if p == q:
        return inside_closed(poly, p)
    dx, dy = q[0] - p[0], q[1] - p[1]
    norm = dx * dx + dy * dy
    cuts = {Fraction(0), Fraction(1)}
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        for v in (a, b):
            if on_segment(p, q, v):
                cuts.add(Fraction((v[0] - p[0]) * dx + (v[1] - p[1]) * dy, norm))
        den = dx * (b[1] - a[1]) - dy * (b[0] - a[0])
        if den:
            tp = Fraction((a[0] - p[0]) * (b[1] - a[1]) - (a[1] - p[1]) * (b[0] - a[0]), den)
            te = Fraction((a[0] - p[0]) * dy - (a[1] - p[1]) * dx, den)
            if 0 <= tp <= 1 and 0 <= te <= 1:
                cuts.add(tp)
    cuts = sorted(cuts)
    return all(inside_closed(poly, (p[0] + (u + w) / 2 * dx, p[1] + (u + w) / 2 * dy)) for u, w in zip(cuts, cuts[1:]))


def reference_length(poly, s, t):
    nodes = [s, t] + [v for v in poly if v != s and v != t]
    best = [float("inf")] * len(nodes)
    best[0] = 0.0
    heap = [(0.0, 0)]
    seen = set()
    while heap:
        d, i = heapq.heappop(heap)
        if i in seen:
            continue
        seen.add(i)
        if i == 1:
            return d
        for j, w in enumerate(nodes):
            if j not in seen and visible(poly, nodes[i], w):
                nd = d + hypot(w[0] - nodes[i][0], w[1] - nodes[i][1])
                if nd < best[j]:
                    best[j] = nd
                    heapq.heappush(heap, (nd, j))
    raise AssertionError("t is not reachable")


def check(poly, s, t, tris=None):
    path = shortest_path(poly, s, t, tris)
    assert path[0] == s and path[-1] == t
    index = {v: i for i, v in enumerate(poly)}
    n = len(poly)
    for a, b, c in zip(path, path[1:], path[2:]):
        assert b in index, (poly, s, t, path)
        i = index[b]
        assert orient(poly[i - 1], b, poly[(i + 1) % n]) < 0  # a reflex vertex
        assert orient(a, b, c) != 0  # a real bend
    for a, b in zip(path, path[1:]):
        assert a != b and visible(poly, a, b), (poly, s, t, path)
    assert isclose(path_length(path), reference_length(poly, s, t), rel_tol=1e-9, abs_tol=1e-9)
    return path


def simple(poly):
    n = len(poly)
    if n < 3 or len(set(poly)) != n:
        return False
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        for j in range(i + 1, n):
            c, d = poly[j], poly[(j + 1) % n]
            if j == i + 1 or (i == 0 and j == n - 1):
                # adjacent edges meet only at their shared vertex
                shared, x, y = (b, a, d) if j == i + 1 else (a, b, c)
                if orient(shared, x, y) == 0 and (x[0] - shared[0]) * (y[0] - shared[0]) + (x[1] - shared[1]) * (y[1] - shared[1]) > 0:
                    return False
            elif segments_meet(a, b, c, d):
                return False
    return True


def segments_meet(a, b, c, d):
    o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
    if o1 * o2 < 0 and o3 * o4 < 0:
        return True
    return on_segment(a, b, c) or on_segment(a, b, d) or on_segment(c, d, a) or on_segment(c, d, b)


def random_polygon(rng, n, size):
    """Random lattice points, untangled by reversing the chain between two crossing edges."""
    for _ in range(100):
        pts = list({(rng.randint(0, size), rng.randint(0, size)) for _ in range(n)})
        rng.shuffle(pts)
        m = len(pts)
        for _ in range(300):
            cross = next(
                ((i, j) for i in range(m) for j in range(i + 2, m) if not (i == 0 and j == m - 1) and segments_meet(pts[i], pts[i + 1], pts[j], pts[(j + 1) % m])),
                None,
            )
            if cross is None:
                break
            i, j = cross
            pts[i + 1:j + 1] = pts[i + 1:j + 1][::-1]
        if m >= 3 and simple(pts):
            twice = sum(pts[i][0] * pts[(i + 1) % m][1] - pts[(i + 1) % m][0] * pts[i][1] for i in range(m))
            if twice != 0:
                return pts if twice > 0 else pts[::-1]
    raise AssertionError("no polygon")


def with_straight_vertices(rng, poly):
    out = []
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        out.append(a)
        g = gcd(abs(b[0] - a[0]), abs(b[1] - a[1]))
        for k in range(1, g):
            if rng.random() < 0.25:
                out.append((a[0] + k * (b[0] - a[0]) // g, a[1] + k * (b[1] - a[1]) // g))
    return out


def lattice_point(rng, poly):
    r = rng.random()
    if r < 0.15:
        return rng.choice(poly)
    if r < 0.3:
        i = rng.randrange(len(poly))
        a, b = poly[i], poly[(i + 1) % len(poly)]
        g = gcd(abs(b[0] - a[0]), abs(b[1] - a[1]))
        k = rng.randint(0, g)
        return (a[0] + k * (b[0] - a[0]) // g, a[1] + k * (b[1] - a[1]) // g)
    xs, ys = [p[0] for p in poly], [p[1] for p in poly]
    while True:
        p = (rng.randint(min(xs), max(xs)), rng.randint(min(ys), max(ys)))
        if inside_closed(poly, p):
            return p


def test_page_example():
    assert shortest_path(WALLS, (1, 1), (11, 5)) == [(1, 1), (4, 4), (5, 4), (8, 2), (9, 2), (11, 5)]
    check(WALLS, (1, 1), (11, 5))
    assert isclose(path_length(shortest_path(WALLS, (1, 1), (11, 5))), 2 + 3 * 2 ** 0.5 + 2 * 13 ** 0.5)


def test_triangulation_is_valid():
    rng = random.Random(1)
    for poly in [WALLS, SPIRAL, COMB] + [random_polygon(rng, 10, 12) for _ in range(10)]:
        tris = triangulate(poly)
        assert len(tris) == len(poly) - 2
        twice = sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))
        assert sum(orient(poly[a], poly[b], poly[c]) for a, b, c in tris) == twice
        assert all(orient(poly[a], poly[b], poly[c]) > 0 for a, b, c in tris)


def test_fixed_shapes():
    rng = random.Random(2)
    for poly in (WALLS, SPIRAL, COMB):
        for _ in range(12):
            check(poly, lattice_point(rng, poly), lattice_point(rng, poly))


def test_same_point_and_same_triangle():
    assert shortest_path(WALLS, (2, 2), (2, 2)) == [(2, 2)]
    assert shortest_path(WALLS, (1, 1), (2, 1)) == [(1, 1), (2, 1)]
    check(SPIRAL, (1, 1), (5, 5))


def test_any_triangulation_gives_the_same_path():
    rng = random.Random(3)
    for poly in (WALLS, SPIRAL, COMB):
        n = len(poly)
        for shift in range(0, n, 3):
            rotated = poly[shift:] + poly[:shift]
            tris = [tuple((x + shift) % n for x in tri) for tri in triangulate(rotated)]
            for _ in range(4):
                s, t = lattice_point(rng, poly), lattice_point(rng, poly)
                assert shortest_path(poly, s, t, tris) == shortest_path(poly, s, t)


def test_random_polygons():
    rng = random.Random(4)
    for trial in range(30):
        poly = random_polygon(rng, rng.randint(4, 11), 10)
        if trial % 3 == 0:
            poly = with_straight_vertices(rng, poly)
        for _ in range(3):
            check(poly, lattice_point(rng, poly), lattice_point(rng, poly))


def test_bad_input():
    with pytest.raises(ValueError):
        shortest_path([(0, 0), (0, 4), (4, 0)], (1, 1), (2, 1))  # clockwise
    with pytest.raises(ValueError):
        shortest_path(WALLS, (1, 1), (20, 20))  # t outside
