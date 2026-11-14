# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimal-delaunay-triangulation/. The authors are listed in prov/CQ85FC.jsonl.

import random
from fractions import Fraction as F

from mg3geom import incircle, orient2d, twice_area
from optimal_delaunay_triangulation import (delaunay, energy, move_vertex, odt_smooth, odt_target,
                                            star_energy, triangle_error)


def random_inner(rng, n, size=8):
    """n distinct points with coordinates on the grid of step 1/4, strictly inside [0, size]^2."""
    pts = set()
    while len(pts) < n:
        pts.add((F(rng.randint(1, 4 * size - 1), 4), F(rng.randint(1, 4 * size - 1), 4)))
    return sorted(pts)


SQUARE = [(F(0), F(0)), (F(8), F(0)), (F(8), F(8)), (F(0), F(8))]


def check_triangulation(points, tris, corners):
    """Exact: counterclockwise triangles, each directed edge once, interior edges
    twice in opposite directions, area sum equal to the polygon, Euler count."""
    seen = set()
    for i, j, k in tris:
        assert orient2d(points[i], points[j], points[k]) > 0
        for e in ((i, j), (j, k), (k, i)):
            assert e not in seen
            seen.add(e)
    assert sum(orient2d(points[i], points[j], points[k]) for i, j, k in tris) == twice_area(corners)
    hull = sum(1 for (i, j) in seen if (j, i) not in seen)
    assert hull == len(corners)
    assert len(tris) == 2 * len(points) - hull - 2


def is_delaunay(points, tris):
    """Global empty circle test, exact, against every point."""
    for i, j, k in tris:
        for p in points:
            if incircle(points[i], points[j], points[k], p) > 0:
                return False
    return True


def test_triangle_error_against_midpoint_rule():
    # the midpoint rule integrates quadratics exactly on a triangle
    rng = random.Random(1)
    f = lambda p: p[0] ** 2 + p[1] ** 2
    for _ in range(200):
        a, b, c = [(F(rng.randint(-20, 20), 3), F(rng.randint(-20, 20), 3)) for _ in range(3)]
        if orient2d(a, b, c) <= 0:
            continue
        area = F(orient2d(a, b, c), 2)
        mids = [((p[0] + q[0]) / 2, (p[1] + q[1]) / 2, (f(p) + f(q)) / 2) for p, q in ((a, b), (b, c), (c, a))]
        oracle = area / 3 * sum(fi - (mx ** 2 + my ** 2) for mx, my, fi in mids)
        assert triangle_error(a, b, c) == oracle


def test_target_is_weighted_mean_of_circumcentres():
    rng = random.Random(2)
    checked = 0
    for _ in range(100):
        corners = SQUARE
        inner = random_inner(rng, 6)
        pts = list(corners) + inner
        tris = delaunay(pts, 4)
        for v in range(4, len(pts)):
            link = []
            for i, j, k in tris:
                if v in (i, j, k):
                    r = (i, j, k).index(v)
                    link.append((pts[(i, j, k)[(r + 1) % 3]], pts[(i, j, k)[(r + 2) % 3]]))
            num_x = num_y = om = F(0)
            for a, b in link:
                x = pts[v]
                area = F(orient2d(x, a, b), 2)
                d = 2 * orient2d(x, a, b)
                sx = x[0] ** 2 + x[1] ** 2
                sa = a[0] ** 2 + a[1] ** 2
                sb = b[0] ** 2 + b[1] ** 2
                cx = (sx * (a[1] - b[1]) + sa * (b[1] - x[1]) + sb * (x[1] - a[1])) / d
                cy = (sx * (b[0] - a[0]) + sa * (x[0] - b[0]) + sb * (a[0] - x[0])) / d
                num_x += area * cx
                num_y += area * cy
                om += area
            assert odt_target(link) == (num_x / om, num_y / om)
            checked += 1
    assert checked >= 500


def test_target_minimises_star_energy():
    # star_energy is a convex quadratic in x; no grid point near the target beats it
    rng = random.Random(3)
    for _ in range(30):
        pts = list(SQUARE) + random_inner(rng, 5)
        tris = delaunay(pts, 4)
        v = rng.randrange(4, len(pts))
        link = []
        for t in tris:
            if v in t:
                r = t.index(v)
                link.append((pts[t[(r + 1) % 3]], pts[t[(r + 2) % 3]]))
        x = odt_target(link)
        best = star_energy(x, link)
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                y = (x[0] + F(dx, 16), x[1] + F(dy, 16))
                assert star_energy(y, link) >= best


def test_delaunay_construction_is_delaunay():
    rng = random.Random(4)
    for _ in range(40):
        inner = random_inner(rng, rng.randint(1, 15))
        pts = list(SQUARE) + inner
        tris = delaunay(pts, 4)
        check_triangulation(pts, tris, SQUARE)
        assert is_delaunay(pts, tris)


def test_energy_never_increases_and_result_is_delaunay():
    rng = random.Random(5)
    for _ in range(8):
        inner = random_inner(rng, rng.randint(4, 12))
        points, tris, energies = odt_smooth(SQUARE, inner, sweeps=6)
        assert all(e1 <= e0 for e0, e1 in zip(energies, energies[1:]))
        assert energies[-1] < energies[0]
        assert energies[-1] == energy(points, tris)
        check_triangulation(points, tris, SQUARE)
        assert is_delaunay(points, tris)


def test_vertex_move_lowers_energy_exactly():
    rng = random.Random(6)
    moved = 0
    for _ in range(20):
        pts = list(SQUARE) + random_inner(rng, 8)
        tris = delaunay(pts, 4)
        for v in range(4, len(pts)):
            e0 = energy(pts, tris)
            if move_vertex(pts, tris, v):
                moved += 1
                assert energy(pts, tris) < e0
                assert all(orient2d(pts[i], pts[j], pts[k]) > 0 for i, j, k in tris)
            else:
                assert energy(pts, tris) == e0
    assert moved > 100


def canon(tris):
    return frozenset(tuple(sorted(t)) for t in tris)


def all_triangulations(points, start):
    """Every triangulation of the point set (all points used), by breadth first
    search on the flip graph, which is connected for planar point sets."""
    seen = {canon(start)}
    queue = [list(start)]
    out = [list(start)]
    while queue:
        tris = queue.pop()
        owner = {}
        for t, (i, j, k) in enumerate(tris):
            for e in ((i, j), (j, k), (k, i)):
                owner[e] = t
        for (i, j), t in owner.items():
            u = owner.get((j, i))
            if u is None or u < t:
                continue
            a = [v for v in tris[t] if v not in (i, j)][0]
            b = [v for v in tris[u] if v not in (i, j)][0]
            # flippable iff the quad i, b, j, a is strictly convex
            if orient2d(points[a], points[i], points[b]) > 0 and orient2d(points[b], points[j], points[a]) > 0:
                new = list(tris)
                new[t] = (a, i, b)
                new[u] = (b, j, a)
                c = canon(new)
                if c not in seen:
                    seen.add(c)
                    queue.append(new)
                    out.append(new)
    return out


def test_delaunay_minimises_energy_among_all_triangulations():
    rng = random.Random(7)
    total = 0
    for trial in range(25):
        inner = random_inner(rng, rng.randint(2, 4), size=4)
        corners = [(F(0), F(0)), (F(4), F(0)), (F(4), F(4)), (F(0), F(4))]
        pts = corners + inner
        dt = delaunay(pts, 4)
        e_dt = energy(pts, dt)
        every = all_triangulations(pts, dt)
        total += len(every)
        for tris in every:
            e = energy(pts, tris)
            assert e >= e_dt
            if e == e_dt:
                assert is_delaunay(pts, tris)   # equality only for Delaunay triangulations
            else:
                assert not is_delaunay(pts, tris)
    assert total > 100
