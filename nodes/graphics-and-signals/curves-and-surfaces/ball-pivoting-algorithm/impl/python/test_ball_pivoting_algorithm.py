# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ball-pivoting-algorithm/. The authors are listed in prov/S69GHG.jsonl.

import math
import random
from collections import Counter
from fractions import Fraction
from itertools import combinations

from ball_pivoting_algorithm import ball_center, ball_pivoting


def mesh_stats(tris):
    """(closed manifold?, Euler characteristic) of an oriented triangle mesh."""
    directed = Counter()
    for a, b, c in tris:
        for u, v in ((a, b), (b, c), (c, a)):
            directed[(u, v)] += 1
    for (u, v), m in directed.items():
        if m != 1 or directed.get((v, u)) != 1:
            return False, None
    link = {}
    for a, b, c in tris:
        for u, v, w in ((a, b, c), (b, c, a), (c, a, b)):
            link.setdefault(u, {})[v] = w
    for u, nxt in link.items():
        start = next(iter(nxt))
        x, steps = start, 0
        while True:
            x = nxt[x]
            steps += 1
            if x == start:
                break
        if steps != len(nxt):
            return False, None
    return True, len(link) - len(directed) // 2 + len(tris)


def fibonacci_sphere(n, center=(0.0, 0.0, 0.0), r=1.0):
    pts, nms = [], []
    golden = math.pi * (3 - math.sqrt(5))
    for i in range(n):
        z = 1 - 2 * (i + 0.5) / n
        s = math.sqrt(1 - z * z)
        x, y = s * math.cos(golden * i), s * math.sin(golden * i)
        nms.append((x, y, z))
        pts.append((center[0] + r * x, center[1] + r * y, center[2] + r * z))
    return pts, nms


def test_ball_center_exact():
    # the ball through three points: equal distance rho, on the side of the normal
    rng = random.Random(3)
    for _ in range(200):
        p = [tuple(rng.uniform(-1, 1) for _ in range(3)) for _ in range(3)]
        c = ball_center(*p, 2.0)
        if c is None:
            continue
        for q in p:
            assert abs(math.dist(c, q) - 2.0) < 1e-9
        n = [(p[1][(t + 1) % 3] - p[0][(t + 1) % 3]) * (p[2][(t + 2) % 3] - p[0][(t + 2) % 3])
             - (p[1][(t + 2) % 3] - p[0][(t + 2) % 3]) * (p[2][(t + 1) % 3] - p[0][(t + 1) % 3]) for t in range(3)]
        assert sum(n[t] * (c[t] - p[0][t]) for t in range(3)) >= 0
    assert ball_center((0, 0, 0), (4, 0, 0), (0, 4, 0), 1.0) is None  # circumradius 2 sqrt 2 > 1


def in_circle_exact(a, b, c, d):
    """Sign of the in-circle determinant, exact over Fraction (positive: d inside, for a b c ccw)."""
    m = [[Fraction(p[0]) - Fraction(d[0]), Fraction(p[1]) - Fraction(d[1])] for p in (a, b, c)]
    rows = [(x, y, x * x + y * y) for x, y in m]
    (a1, a2, a3), (b1, b2, b3), (c1, c2, c3) = rows
    return a1 * (b2 * c3 - b3 * c2) - a2 * (b1 * c3 - b3 * c1) + a3 * (b1 * c2 - b2 * c1)


def circumradius2_exact(a, b, c):
    ax, ay = Fraction(a[0]), Fraction(a[1])
    bx, by = Fraction(b[0]) - ax, Fraction(b[1]) - ay
    cx, cy = Fraction(c[0]) - ax, Fraction(c[1]) - ay
    d = 2 * (bx * cy - by * cx)
    ux = (cy * (bx * bx + by * by) - by * (cx * cx + cy * cy)) / d
    uy = (bx * (cx * cx + cy * cy) - cx * (bx * bx + by * by)) / d
    return ux * ux + uy * uy


def test_planar_output_is_the_delaunay_rho_complex():
    """On a plane with normals +z, an empty rho-ball above a triangle is an empty circumdisk of
    radius at most rho. So the output must be a subset of the Delaunay triangles with
    circumradius at most rho: a subset of the alpha complex for alpha = rho."""
    rng = random.Random(11)
    equal = 0
    for trial in range(30):
        n = rng.randint(8, 30)
        pts = [(rng.randint(0, 400) / 100, rng.randint(0, 400) / 100, 0.0) for _ in range(n)]
        pts = list(dict.fromkeys(pts))
        nms = [(0.0, 0.0, 1.0)] * len(pts)
        rho = rng.choice([0.6, 0.9, 1.5, 3.0])
        out = ball_pivoting(pts, nms, rho)
        want = set()
        for a, b, c in combinations(range(len(pts)), 3):
            o = (Fraction(pts[b][0]) - Fraction(pts[a][0])) * (Fraction(pts[c][1]) - Fraction(pts[a][1])) \
                - (Fraction(pts[b][1]) - Fraction(pts[a][1])) * (Fraction(pts[c][0]) - Fraction(pts[a][0]))
            if o == 0:
                continue
            if o < 0:
                b, c = c, b
            if circumradius2_exact(pts[a], pts[b], pts[c]) > Fraction(rho) ** 2:
                continue
            if all(in_circle_exact(pts[a], pts[b], pts[c], pts[d]) < 0 for d in range(len(pts)) if d not in (a, b, c)):
                want.add(frozenset((a, b, c)))
        got = [frozenset(t) for t in out]
        assert len(set(got)) == len(got)
        assert set(got) <= want
        for a, b, c in out:  # counterclockwise seen from +z
            assert (pts[b][0] - pts[a][0]) * (pts[c][1] - pts[a][1]) - (pts[b][1] - pts[a][1]) * (pts[c][0] - pts[a][0]) > 0
        equal += set(got) == want
    # equality is not guaranteed (a triangle that meets the rest only at its three used vertices
    # is never reached), but it holds on these inputs
    assert equal == 30


def test_output_balls_are_empty_brute_force():
    rng = random.Random(5)
    pts, nms = fibonacci_sphere(150)
    pts = [tuple(x + rng.uniform(-0.01, 0.01) for x in p) for p in pts]
    rho = 0.35
    tris = ball_pivoting(pts, nms, rho)
    assert tris
    for a, b, c in tris:
        ctr = ball_center(pts[a], pts[b], pts[c], rho)
        assert ctr is not None
        assert all(math.dist(ctr, pts[d]) >= rho - 1e-9 for d in range(len(pts)))
    directed = Counter((u, v) for a, b, c in tris for u, v in ((a, b), (b, c), (c, a)))
    assert max(directed.values()) == 1  # every edge in at most two triangles, opposite directions


def test_sphere_and_two_spheres_are_closed():
    pts, nms = fibonacci_sphere(400)
    tris = ball_pivoting(pts, nms, 0.2)
    ok, chi = mesh_stats(tris)
    assert ok and chi == 2
    assert len({v for t in tris for v in t}) == 400
    assert len(tris) == 2 * 400 - 4

    p1, n1 = fibonacci_sphere(200, (0.0, 0.0, 0.0), 1.0)
    p2, n2 = fibonacci_sphere(200, (3.0, 0.5, 0.2), 1.0)
    tris = ball_pivoting(p1 + p2, n1 + n2, 0.3)
    ok, chi = mesh_stats(tris)
    assert ok and chi == 4


def test_torus_is_closed():
    pts, nms = [], []
    big, small, nu, nv = 3.0, 1.0, 48, 16
    for i in range(nu):
        for j in range(nv):
            u = 2 * math.pi * (i + 0.5 * (j % 2)) / nu
            v = 2 * math.pi * j / nv
            nrm = (math.cos(u) * math.cos(v), math.sin(u) * math.cos(v), math.sin(v))
            nms.append(nrm)
            pts.append(((big + small * math.cos(v)) * math.cos(u), (big + small * math.cos(v)) * math.sin(u),
                        small * math.sin(v)))
    tris = ball_pivoting(pts, nms, 0.5)
    ok, chi = mesh_stats(tris)
    assert ok and chi == 0


def test_radius_too_small_or_large_gaps():
    pts, nms = fibonacci_sphere(400)
    assert ball_pivoting(pts, nms, 0.05) == []  # no three points fit on a ball of this radius
    # a hole in the sampling larger than the ball stays open
    keep = [i for i, p in enumerate(pts) if p[2] < 0.8]
    sub = [pts[i] for i in keep]
    tris = ball_pivoting(sub, [nms[i] for i in keep], 0.2)
    directed = Counter((u, v) for a, b, c in tris for u, v in ((a, b), (b, c), (c, a)))
    border = [e for e in directed if (e[1], e[0]) not in directed]
    assert border  # the mesh has a boundary loop around the cap that was removed
    assert all(sub[u][2] > 0.5 and sub[v][2] > 0.5 for u, v in border)


def test_edge_cases():
    assert ball_pivoting([], [], 1.0) == []
    assert ball_pivoting([(0.0, 0.0, 0.0), (1.0, 0.0, 0.0)], [(0.0, 0.0, 1.0)] * 2, 1.0) == []
    pts = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
    assert ball_pivoting(pts, [(0.0, 0.0, 1.0)] * 3, 1.0) == [(0, 1, 2)]
    assert ball_pivoting(pts, [(0.0, 0.0, -1.0)] * 3, 1.0) == [(0, 2, 1)]
