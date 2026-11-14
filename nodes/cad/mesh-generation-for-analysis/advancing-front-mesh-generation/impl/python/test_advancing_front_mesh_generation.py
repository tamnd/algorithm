# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/advancing-front-mesh-generation/. The authors are listed in prov/NKGVJD.jsonl.

import random
from collections import Counter
from fractions import Fraction as F

import pytest

from advancing_front_mesh_generation import advancing_front, min_angle_degrees
from mg1geom import orient2d, twice_area


def convex_hull(points):
    """Counterclockwise convex hull by the monotone chain, collinear points dropped."""
    pts = sorted(set(points))

    def half(seq):
        h = []
        for p in seq:
            while len(h) >= 2 and orient2d(h[-2], h[-1], p) <= 0:
                h.pop()
            h.append(p)
        return h

    return half(pts)[:-1] + half(list(reversed(pts)))[:-1]


def shoelace_exact(poly):
    """Twice the area by the shoelace formula, written out with Fractions (the oracle)."""
    n = len(poly)
    return sum(F(poly[i][0]) * F(poly[(i + 1) % n][1]) - F(poly[(i + 1) % n][0]) * F(poly[i][1]) for i in range(n))


def on_segment(p, a, b):
    return orient2d(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def interiors_disjoint(t, s):
    """Two counterclockwise triangles have disjoint interiors iff an edge of one separates them."""
    for p, q in ((t, s), (s, t)):
        for k in range(3):
            a, b = p[k], p[(k + 1) % 3]
            if all(orient2d(a, b, v) <= 0 for v in q):
                return True
    return False


def check_mesh(poly, tris, convex):
    poly = [(F(x), F(y)) for x, y in poly]
    n = len(poly)
    # every triangle is counterclockwise
    assert all(orient2d(*t) > 0 for t in tris)
    # every vertex is inside the closed polygon
    if convex:
        for t in tris:
            for v in t:
                assert all(orient2d(poly[i], poly[(i + 1) % n], v) >= 0 for i in range(n))
    # exact area sum
    assert sum(orient2d(*t) for t in tris) == shoelace_exact(poly)
    # conformity: each directed edge once; an edge without its twin lies on the boundary
    directed = Counter((t[k], t[(k + 1) % 3]) for t in tris for k in range(3))
    assert max(directed.values()) == 1
    for (a, b) in directed:
        if (b, a) not in directed:
            assert any(on_segment(a, poly[i], poly[(i + 1) % n]) and on_segment(b, poly[i], poly[(i + 1) % n]) for i in range(n))
    # no vertex lies inside another triangle or in the middle of its edge
    verts = {v for t in tris for v in t}
    for t in tris:
        for v in verts:
            if v not in t:
                assert not (orient2d(t[0], t[1], v) >= 0 and orient2d(t[1], t[2], v) >= 0 and orient2d(t[2], t[0], v) >= 0)


def test_example_of_the_page() -> None:
    tris, verts = advancing_front([(0, 0), (4, 0), (4, 4), (0, 4)], 2)
    assert len(tris) == 8 and len(verts) == 9
    assert tris[0] == ((0, 0), (2, 0), (0, 2))
    assert tris[4] == ((0, 2), (2, 0), (2, 2))
    assert (F(2), F(2)) in verts
    assert all(orient2d(*t) == 4 for t in tris)
    check_mesh([(0, 0), (4, 0), (4, 4), (0, 4)], tris, True)
    assert abs(min_angle_degrees(tris) - 45.0) < 1e-9


def test_random_convex_polygons() -> None:
    rng = random.Random(1)
    for _ in range(10):
        poly = convex_hull([(rng.randint(0, 40), rng.randint(0, 40)) for _ in range(12)])
        h = rng.randint(5, 10)
        tris, verts = advancing_front(poly, h)
        check_mesh(poly, tris, True)
        # Euler: V - E + F = 1 for a triangulated disk
        edges = {frozenset((t[k], t[(k + 1) % 3])) for t in tris for k in range(3)}
        assert len(verts) - len(edges) + len(tris) == 1
        assert len(tris) <= 2 * len(verts) - 5


def test_interiors_pairwise_disjoint() -> None:
    rng = random.Random(3)
    for _ in range(3):
        poly = convex_hull([(rng.randint(0, 30), rng.randint(0, 30)) for _ in range(10)])
        tris, _ = advancing_front(poly, 7)
        for i in range(len(tris)):
            for j in range(i + 1, len(tris)):
                assert interiors_disjoint(tris[i], tris[j])


def test_nonconvex_polygon_and_rational_size() -> None:
    poly = [(0, 0), (8, 0), (8, 3), (3, 3), (3, 8), (0, 8)]
    tris, _ = advancing_front(poly, F(3, 2))
    check_mesh(poly, tris, False)
    comb = [(0, 0), (9, 0), (9, 4), (7, 4), (7, 1), (6, 1), (6, 4), (3, 4), (3, 1), (2, 1), (2, 4), (0, 4)]
    tris, _ = advancing_front(comb, 2)
    check_mesh(comb, tris, False)


def test_quality_is_only_measured() -> None:
    rng = random.Random(1)
    poly = convex_hull([(rng.randint(0, 40), rng.randint(0, 40)) for _ in range(12)])
    tris, _ = advancing_front(poly, 4)
    check_mesh(poly, tris, True)
    assert 0 < min_angle_degrees(tris) < 10  # valid, but with a small angle


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        advancing_front([(0, 0), (0, 4), (4, 0)], 1)  # clockwise
    with pytest.raises(ValueError):
        advancing_front([(0, 0), (4, 0), (0, 4)], 0)
