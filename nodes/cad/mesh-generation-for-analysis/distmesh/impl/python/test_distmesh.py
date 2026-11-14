# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distmesh/. The authors are listed in prov/M30YY9.jsonl.

import random
from fractions import Fraction as F
from itertools import combinations

from distmesh import delaunay, disk, distmesh, square, to_int
from mg3geom import boundary_edges, exact, incircle, is_valid_planar_mesh, mean_ratio, orient2d


def is_delaunay(ipts, tris):
    """Exact empty circle test of every triangle against every point."""
    for t in tris:
        a, b, c = (ipts[i] for i in t)
        for k, p in enumerate(ipts):
            if k not in t and incircle(a, b, c, p) > 0:
                return False
    return True


def brute_delaunay(ipts):
    """All counterclockwise triples whose circumcircle has no point strictly inside."""
    out = set()
    for i, j, k in combinations(range(len(ipts)), 3):
        if orient2d(ipts[i], ipts[j], ipts[k]) < 0:
            j, k = k, j
        if orient2d(ipts[i], ipts[j], ipts[k]) == 0:
            continue
        if all(incircle(ipts[i], ipts[j], ipts[k], p) <= 0 for p in ipts):
            out.add(frozenset((i, j, k)))
    return out


def test_delaunay_matches_brute_force():
    rng = random.Random(5)
    compared = 0
    for _ in range(60):
        n = rng.randint(3, 14)
        pts = list({(rng.randint(-20, 20), rng.randint(-20, 20)) for _ in range(n)})
        if len(pts) < 3 or all(orient2d(pts[0], pts[1], p) == 0 for p in pts):
            continue
        tris = delaunay(pts)
        brute = brute_delaunay(pts)
        # the Delaunay triangulation is unique when no fourth point is on a
        # circumcircle of the brute force triangles
        if all(incircle(*[pts[i] for i in t], p) != 0
               for t in brute for k, p in enumerate(pts) if k not in t):
            assert {frozenset(t) for t in tris} == brute
            compared += 1
        assert all(orient2d(*[pts[i] for i in t]) > 0 for t in tris)
        assert is_delaunay(pts, tris)
    assert compared >= 20


def check_mesh(fd, pts, tris):
    E = [exact(p) for p in pts]
    assert len({p for p in E}) == len(E)                       # distinct points
    assert all(orient2d(*[E[i] for i in t]) > 0 for t in tris)   # counterclockwise
    assert is_valid_planar_mesh(E, tris)                        # conforming
    assert is_delaunay([to_int(p) for p in pts], tris)          # exact Delaunay
    for t in tris:
        c = (sum(pts[i][0] for i in t) / 3, sum(pts[i][1] for i in t) / 3)
        assert fd(c) < 0                                        # centroid inside
        assert all(fd(pts[i]) < 1e-6 for i in t)                # vertices inside or on the boundary, to the rounding
    assert min(mean_ratio(*[pts[i] for i in t]) for t in tris) > 0.7


def test_unit_disk():
    pts, tris, it, converged = distmesh(disk, 0.2, (-1, -1, 1, 1))
    assert converged and it < 1000
    check_mesh(disk, pts, tris)
    # every boundary vertex lies on the circle, to rounding
    for a, b in boundary_edges(tris):
        assert abs(disk(pts[a])) < 1e-6
    area = sum(F(orient2d(*[exact(pts[i]) for i in t])) for t in tris) / 2
    assert 3.10 < area < 3.1416                                  # inscribed polygon


def test_square_with_fixed_corners():
    corners = ((-1, -1), (1, -1), (1, 1), (-1, 1))
    pts, tris, it, converged = distmesh(square, 0.25, (-1, -1, 1, 1), pfix=corners)
    assert converged
    check_mesh(square, pts, tris)
    E = [exact(p) for p in pts]
    assert all(-1 <= c <= 1 for p in E for c in p)              # exactly inside the closed square
    area = sum(orient2d(*[E[i] for i in t]) for t in tris) / 2
    assert area == 4                                            # the triangles cover the square exactly


def test_iteration_cap_still_gives_a_delaunay_mesh():
    pts, tris, it, converged = distmesh(disk, 0.2, (-1, -1, 1, 1), max_iter=3)
    assert it == 3 and not converged
    assert is_valid_planar_mesh([exact(p) for p in pts], tris)
    assert is_delaunay([to_int(p) for p in pts], tris)
