# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/point-in-convex-polygon/. The authors are listed in prov/KB6KXW.jsonl.

import random
from fractions import Fraction

import pytest

from point_in_convex_polygon import BOUNDARY, INSIDE, OUTSIDE, point_in_convex_polygon


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def oracle(poly, q):
    """Brute force: test q against every edge (a strictly convex CCW polygon is the
    intersection of the closed half-planes to the left of its edges)."""
    n = len(poly)
    signs = [cross(poly[i], poly[(i + 1) % n], q) for i in range(n)]
    if any(s < 0 for s in signs):
        return OUTSIDE
    if any(s == 0 for s in signs):
        return BOUNDARY
    return INSIDE


def on_boundary(poly, q):
    """Independent boundary test by bounding boxes."""
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if cross(a, b, q) == 0 and min(a[0], b[0]) <= q[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= q[1] <= max(a[1], b[1]):
            return True
    return False


def strict_hull(points):
    """Andrew's monotone chain, dropping collinear points: a strictly convex CCW polygon."""
    pts = sorted(set(points))
    if len(pts) < 3:
        return pts

    def half(seq):
        out = []
        for p in seq:
            while len(out) >= 2 and cross(out[-2], out[-1], p) <= 0:
                out.pop()
            out.append(p)
        return out

    lower = half(pts)
    upper = half(pts[::-1])
    return lower[:-1] + upper[:-1]


def queries(poly):
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    qs = [(x, y) for x in range(min(xs) - 1, max(xs) + 2) for y in range(min(ys) - 1, max(ys) + 2)]
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        for t in (-2, -1, Fraction(1, 2), 2, 3):
            qs.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
    for j in range(2, n - 1):
        a, b = poly[0], poly[j]
        for t in (-1, Fraction(1, 3), 2):
            qs.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
    return qs


def check(poly):
    for q in queries(poly):
        got = point_in_convex_polygon(poly, q)
        want = oracle(poly, q)
        assert got == want, (poly, q, got, want)
        assert (got == BOUNDARY) == on_boundary(poly, q), (poly, q)


def test_example() -> None:
    v = [(2, 0), (5, 1), (6, 4), (4, 6), (1, 5), (0, 2)]
    assert point_in_convex_polygon(v, (3, 3)) == INSIDE
    assert point_in_convex_polygon(v, (5, 5)) == BOUNDARY
    assert point_in_convex_polygon(v, (1, 1)) == BOUNDARY
    assert point_in_convex_polygon(v, (3, 0)) == OUTSIDE
    assert point_in_convex_polygon(v, (7, 4)) == OUTSIDE
    assert point_in_convex_polygon(v, (2, 0)) == BOUNDARY
    assert point_in_convex_polygon(v, (8, 2)) == OUTSIDE  # on the line of edge v0 v1, beyond v1
    assert point_in_convex_polygon(v, (-2, 4)) == OUTSIDE  # on the line of edge v5 v0, beyond v5
    check(v)


def test_triangles_and_vertices() -> None:
    tri = [(0, 0), (4, 0), (0, 4)]
    assert point_in_convex_polygon(tri, (1, 1)) == INSIDE
    assert point_in_convex_polygon(tri, (0, 0)) == BOUNDARY
    assert point_in_convex_polygon(tri, (4, 0)) == BOUNDARY
    assert point_in_convex_polygon(tri, (0, 4)) == BOUNDARY
    assert point_in_convex_polygon(tri, (2, 2)) == BOUNDARY
    assert point_in_convex_polygon(tri, (-1, 0)) == OUTSIDE  # behind v0 on the line of edge v0 v1
    assert point_in_convex_polygon(tri, (0, -1)) == OUTSIDE  # behind v0 on the line of edge v2 v0
    assert point_in_convex_polygon(tri, (-1, -1)) == OUTSIDE
    assert point_in_convex_polygon(tri, (Fraction(1, 3), Fraction(10, 3))) == INSIDE
    assert point_in_convex_polygon(tri, (Fraction(1, 2), Fraction(7, 2))) == BOUNDARY
    check(tri)
    with pytest.raises(ValueError):
        point_in_convex_polygon([(0, 0), (1, 0)], (0, 0))


def test_every_start_vertex() -> None:
    v = [(2, 0), (5, 1), (6, 4), (4, 6), (1, 5), (0, 2)]
    for k in range(len(v)):
        check(v[k:] + v[:k])


def test_random_convex_polygons() -> None:
    rng = random.Random(20261109)
    count = 0
    while count < 600:
        r = rng.choice([2, 3, 5, 8])
        pts = [(rng.randint(-r, r), rng.randint(-r, r)) for _ in range(rng.randint(3, 14))]
        poly = strict_hull(pts)
        if len(poly) < 3:
            continue
        k = rng.randrange(len(poly))
        poly = poly[k:] + poly[:k]
        check(poly)
        count += 1


def test_large_polygon_logarithmic_steps() -> None:
    # vertices on the parabola y = x^2 plus one point closing it: strictly convex, n = 2001
    poly = [(x, x * x) for x in range(-1000, 1001)][::-1]
    poly = strict_hull(poly)
    rng = random.Random(3)
    for _ in range(300):
        q = (rng.randint(-1001, 1001), rng.randint(-1, 1000001))
        assert point_in_convex_polygon(poly, q) == oracle(poly, q)
