# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/convex-polygon-point-location/. The authors are listed in prov/QBH461.jsonl.

import math
import random
from math import gcd

import pytest

from convex_polygon_point_location import ConvexPolygonLocator, orient, reference


def hull(points):
    """Andrew's monotone chain, counterclockwise, without collinear points."""
    pts = sorted(set(points))
    if len(pts) < 3:
        return pts
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and orient(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and orient(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def with_collinear(poly, rng):
    """Insert some lattice points that lie inside edges, so consecutive vertices are collinear."""
    out = []
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        out.append(a)
        g = gcd(abs(b[0] - a[0]), abs(b[1] - a[1]))
        for t in range(1, g):
            if rng.random() < 0.5:
                out.append((a[0] + (b[0] - a[0]) * t // g, a[1] + (b[1] - a[1]) * t // g))
    return out


def random_polygon(rng, grid):
    while True:
        pts = [(rng.randint(0, grid), rng.randint(0, grid)) for _ in range(rng.randint(3, 3 * grid))]
        h = hull(pts)
        if len(h) >= 3:
            break
    if rng.random() < 0.5:
        h = with_collinear(h, rng)
    r = rng.randrange(len(h))
    return h[r:] + h[:r]


def test_against_linear_scan():
    rng = random.Random(1978)
    for _ in range(300):
        grid = rng.choice([2, 3, 4, 6, 9])
        poly = random_polygon(rng, grid)
        loc = ConvexPolygonLocator(poly)
        for x in range(-1, grid + 2):
            for y in range(-1, grid + 2):
                assert loc.locate((x, y)) == reference(poly, (x, y)), (poly, (x, y))


def test_points_on_wedge_rays_and_the_center():
    # c = (1, 1) is a lattice point, and the rays from c pass through lattice points
    tri = [(0, 0), (3, 0), (0, 3)]
    loc = ConvexPolygonLocator(tri)
    assert loc.locate((1, 1)) == ("inside", 0)
    for q in [(2, 1), (1, 2), (0, 0), (-1, -1), (3, 0), (5, -1), (2, 2), (0, 1), (-2, 5)]:
        assert loc.locate(q) == reference(tri, q)
    assert loc.locate((-1, -1)) == ("outside", 0)  # beyond vertex 0 on the ray from c
    assert loc.locate((5, -1)) == ("outside", 1)  # beyond vertex 1
    assert loc.locate((2, 2)) == ("outside", 1)  # beyond the edge from (3, 0) to (0, 3)


def test_collinear_vertices_and_vertical_edges():
    square = [(0, 0), (2, 0), (4, 0), (4, 2), (4, 4), (2, 4), (0, 4), (0, 2)]
    loc = ConvexPolygonLocator(square)
    assert loc.locate((4, 1)) == ("edge", 2)
    assert loc.locate((4, 2)) == ("vertex", 3)
    assert loc.locate((0, 3)) == ("edge", 6)
    assert loc.locate((2, 2)) == ("inside", reference(square, (2, 2))[1])
    for x in range(-2, 7):
        for y in range(-2, 7):
            assert loc.locate((x, y)) == reference(square, (x, y))


def test_degenerate_inputs_are_rejected():
    for bad in ([], [(0, 0)], [(0, 0), (1, 1)], [(0, 0), (1, 1), (2, 2)], [(0, 0), (2, 0), (5, 0), (1, 0)]):
        with pytest.raises(ValueError):
            ConvexPolygonLocator(bad)


def test_logarithmic_number_of_tests():
    for n in (3, 4, 7, 8, 64, 1000):
        # a regular-like lattice polygon: the hull of points on a large circle
        pts = [(round(10**6 * math.cos(2 * math.pi * k / n)), round(10**6 * math.sin(2 * math.pi * k / n))) for k in range(n)]
        poly = hull(pts)
        loc = ConvexPolygonLocator(poly)
        rng = random.Random(n)
        for _ in range(200):
            q = (rng.randint(-1_100_000, 1_100_000), rng.randint(-1_100_000, 1_100_000))
            loc.tests = 0
            ans = loc.locate(q)
            assert loc.tests <= math.ceil(math.log2(len(poly)))
            assert ans[0] == reference(poly, q)[0]


def test_answer_kind_does_not_depend_on_the_start_vertex():
    rng = random.Random(5)
    for _ in range(50):
        poly = random_polygon(rng, 6)
        n = len(poly)
        for r in range(n):
            rot = poly[r:] + poly[:r]
            a, b = ConvexPolygonLocator(poly), ConvexPolygonLocator(rot)
            for x in range(-1, 8):
                for y in range(-1, 8):
                    ka, ia = a.locate((x, y))
                    kb, ib = b.locate((x, y))
                    assert ka == kb
                    if ka in ("vertex", "edge"):
                        assert (ia - r) % n == ib


def test_worked_example():
    poly = [(0, 0), (3, 0), (6, 0), (8, 3), (6, 6), (2, 6), (0, 3)]
    loc = ConvexPolygonLocator(poly)
    assert loc.s == (11, 3)
    assert loc.locate((5, 4)) == ("inside", 4)
    assert loc.locate((1, 5)) == ("outside", 5)
    assert loc.locate((3, 1)) == ("inside", 6)
    assert loc.locate((9, 6)) == ("outside", 3)
    assert loc.locate((4, 0)) == ("edge", 1)
    assert loc.locate((0, 3)) == ("vertex", 6)
