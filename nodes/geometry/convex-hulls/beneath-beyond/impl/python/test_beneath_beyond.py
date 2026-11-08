# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/beneath-beyond/. The authors are listed in prov/TY8J2Y.jsonl.

import random
from itertools import combinations
from math import gcd

from beneath_beyond import beneath_beyond, cross, orient3d, sub


def plane_key(n, d):
    g = 0
    for v in (*n, d):
        g = gcd(g, abs(v))
    return (n[0] // g, n[1] // g, n[2] // g, d // g)


def brute_planes(pts):
    """Outward facet planes of the hull: planes through three points with all points on or below."""
    found = set()
    for a, b, c in combinations(sorted(set(pts)), 3):
        n = cross(sub(b, a), sub(c, a))
        if n == (0, 0, 0):
            continue
        d = n[0] * a[0] + n[1] * a[1] + n[2] * a[2]
        side = [n[0] * p[0] + n[1] * p[1] + n[2] * p[2] - d for p in pts]
        if all(s <= 0 for s in side):
            found.add(plane_key(n, d))
        elif all(s >= 0 for s in side):
            found.add(plane_key((-n[0], -n[1], -n[2]), -d))
    return found


def hull2(points):
    """Doubled area and vertices of the 2D hull (Andrew's monotone chain)."""
    p = sorted(set(points))
    if len(p) < 3:
        return 0, p

    def turn(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower, upper = [], []
    for q in p:
        while len(lower) >= 2 and turn(lower[-2], lower[-1], q) <= 0:
            lower.pop()
        lower.append(q)
    for q in reversed(p):
        while len(upper) >= 2 and turn(upper[-2], upper[-1], q) <= 0:
            upper.pop()
        upper.append(q)
    h = lower[:-1] + upper[:-1]
    area2 = sum(h[i][0] * h[(i + 1) % len(h)][1] - h[(i + 1) % len(h)][0] * h[i][1] for i in range(len(h)))
    return area2, h


def check(pts, tris):
    # each triangle is nondegenerate and no point is beyond it
    for i, j, k in tris:
        a, b, c = pts[i], pts[j], pts[k]
        assert cross(sub(b, a), sub(c, a)) != (0, 0, 0)
        assert all(orient3d(a, b, c, p) <= 0 for p in pts)
    # a closed oriented surface: each directed edge once, with its reverse
    edges = [e for i, j, k in tris for e in ((i, j), (j, k), (k, i))]
    assert len(edges) == len(set(edges))
    assert all((v, u) in set(edges) for u, v in edges)
    # the facet planes are exactly the brute-force ones
    by_plane = {}
    for i, j, k in tris:
        a = pts[i]
        n = cross(sub(pts[j], a), sub(pts[k], a))
        d = n[0] * a[0] + n[1] * a[1] + n[2] * a[2]
        by_plane.setdefault(plane_key(n, d), []).append((i, j, k))
    assert set(by_plane) == brute_planes(pts)
    # on each plane the triangles have the area of the face, and every extreme point is used
    used = {pts[i] for t in tris for i in t}
    for key, group in by_plane.items():
        n, d = key[:3], key[3]
        axis = max(range(3), key=lambda r: abs(n[r]))
        keep = [r for r in range(3) if r != axis]
        on = [p for p in pts if n[0] * p[0] + n[1] * p[1] + n[2] * p[2] == d]
        area2, corners = hull2([(p[keep[0]], p[keep[1]]) for p in on])
        tri_sum = sum(cross(sub(pts[j], pts[i]), sub(pts[k], pts[i]))[axis] for i, j, k in group)
        sign = 1 if n[axis] > 0 else -1  # each triangle normal is a positive multiple of n
        assert tri_sum == sign * area2
        for c in corners:
            assert any((p[keep[0]], p[keep[1]]) == c for p in on if p in used)


def test_cube_with_inner_and_face_points():
    pts = [(x, y, z) for x in (0, 2) for y in (0, 2) for z in (0, 2)] + [(1, 1, 1), (1, 1, 2), (1, 0, 0), (2, 1, 1)]
    for seed in range(20):
        tris = beneath_beyond(pts, seed)
        check(pts, tris)
        assert {pts[i] for t in tris for i in t} >= {(x, y, z) for x in (0, 2) for y in (0, 2) for z in (0, 2)}


def test_tetrahedron_and_example():
    pts = [(0, 0, 0), (6, 0, 0), (0, 6, 0), (0, 0, 6), (1, 2, 1), (4, 3, 2), (6, 5, -1)]
    expected = {"abd", "adc", "cdf", "dbf", "acg", "bag", "cfg", "fbg"}

    def rotations(t):
        return {t, t[1:] + t[:1], t[2:] + t[:2]}

    for seed in range(10):
        tris = beneath_beyond(pts, seed)
        check(pts, tris)
        names = ["".join("abcdefg"[i] for i in t) for t in tris]
        assert len(names) == 8
        assert all(rotations(name) & expected for name in names)


def test_low_dimension():
    assert beneath_beyond([]) == []
    assert beneath_beyond([(1, 2, 3)] * 5) == []
    assert beneath_beyond([(i, 2 * i, -i) for i in range(6)]) == []
    assert beneath_beyond([(x, y, x + y) for x in range(3) for y in range(3)]) == []


def test_random_small_against_brute_force():
    rng = random.Random(2024)
    for trial in range(500):
        size = rng.choice([1, 2, 3, 50])
        n = rng.randint(4, 18)
        pts = [tuple(rng.randint(-size, size) for _ in range(3)) for _ in range(n)]
        tris = beneath_beyond(pts, trial)
        spans = any(orient3d(*q) != 0 for q in combinations(pts, 4))
        assert bool(tris) == spans
        if tris:
            check(pts, tris)


def test_larger_general_position():
    rng = random.Random(5)
    pts = list({tuple(rng.randint(-10**6, 10**6) for _ in range(3)) for _ in range(1500)})
    tris = beneath_beyond(pts, 1)
    edges = {e for i, j, k in tris for e in ((i, j), (j, k), (k, i))}
    assert all((v, u) in edges for u, v in edges)
    verts = {i for t in tris for i in t}
    assert len(verts) - len(edges) // 2 + len(tris) == 2
    sample = rng.sample(range(len(pts)), 200)
    for i, j, k in tris:
        assert all(orient3d(pts[i], pts[j], pts[k], pts[q]) <= 0 for q in sample)
