# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-dop-tree/. The authors are listed in prov/ZJ32AH.jsonl.

import math
import random

from k_dop_tree import (
    DIRS,
    apply,
    build,
    dop_corners,
    dop_of_points,
    dop_overlap,
    moved_dop,
    overlap_pairs,
    rotation,
    triangles_overlap,
)


def _orient(a, b, c):
    v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return (v > 0) - (v < 0)


def _inside_convex(p, P):
    s = {_orient(P[i], P[(i + 1) % len(P)], p) for i in range(len(P))}
    return not (1 in s and -1 in s)


def _cross_segments(a, b, c, d):
    return _orient(a, b, c) * _orient(a, b, d) < 0 and _orient(c, d, a) * _orient(c, d, b) < 0


def convex_overlap_reference(P, Q):
    """Two convex polygons meet if a vertex of one is in the other or two edges cross."""
    if any(_inside_convex(p, Q) for p in P) or any(_inside_convex(q, P) for q in Q):
        return True
    return any(_cross_segments(P[i], P[(i + 1) % len(P)], Q[j], Q[(j + 1) % len(Q)]) for i in range(len(P)) for j in range(len(Q)))


def random_object(rng, n, spread=10.0, size=1.5):
    tris = []
    for _ in range(n):
        c = (rng.uniform(-spread, spread), rng.uniform(-spread / 3, spread / 3))
        tris.append(tuple((c[0] + rng.uniform(-size, size), c[1] + rng.uniform(-size, size)) for _ in range(3)))
    return tris


def brute_pairs(trisA, trisB, R, t):
    moved = [tuple(apply(R, t, p) for p in T) for T in trisB]
    return {(i, j) for i, T in enumerate(trisA) for j, U in enumerate(moved) if triangles_overlap(T, U)}


def all_nodes(node):
    out = [node]
    if not node.leaf:
        out += all_nodes(node.left) + all_nodes(node.right)
    return out


def inside_dop(p, D, tol=1e-9):
    return all(lo - tol <= d[0] * p[0] + d[1] * p[1] <= hi + tol for d, (lo, hi) in zip(DIRS, D))


def test_page_example():
    # the triangle (0,0), (4,0), (0,4) has the 8-DOP x in [0,4], y in [0,4], x+y in [0,4], x-y in [-4,4]
    D = dop_of_points([(0, 0), (4, 0), (0, 4)], margin=False)
    assert D == ((0, 4), (0, 4), (0, 4), (-4, 4))
    corners = dop_corners(D)
    assert sorted(corners) == [(0, 0), (0, 4), (4, 0)]
    # the square [3,5] x [3,5] meets the box [0,4] x [0,4] but not the 8-DOP: x+y >= 6 > 4
    S = dop_of_points([(3, 3), (5, 3), (5, 5), (3, 5)], margin=False)
    assert not dop_overlap(D, S)
    assert dop_overlap(D[:2], S[:2])


def test_corners_of_random_dops():
    rng = random.Random(1)
    for _ in range(300):
        pts = [(rng.uniform(-5, 5), rng.uniform(-5, 5)) for _ in range(rng.randint(1, 8))]
        D = dop_of_points(pts, margin=False)
        C = dop_corners(D)
        assert 1 <= len(C) <= 8
        assert all(inside_dop(c, D) for c in C)
        # the corners have the same 8-DOP as the points
        E = dop_of_points(C, margin=False)
        assert all(abs(a - b) < 1e-9 for p, q in zip(D, E) for a, b in zip(p, q))


def test_interval_test_is_exact_in_the_plane():
    rng = random.Random(2)
    hits = 0
    for _ in range(1500):
        P = dop_of_points([(rng.uniform(-3, 3), rng.uniform(-3, 3)) for _ in range(rng.randint(2, 5))], margin=False)
        Q = dop_of_points([(rng.uniform(-3, 3), rng.uniform(-3, 3)) for _ in range(rng.randint(2, 5))], margin=False)
        expect = convex_overlap_reference(dop_corners(P), dop_corners(Q))
        assert dop_overlap(P, Q) == expect
        hits += expect
    assert 300 < hits < 1200


def test_triangle_overlap_against_a_reference():
    rng = random.Random(3)
    for _ in range(2000):
        T = tuple((rng.uniform(-2, 2), rng.uniform(-2, 2)) for _ in range(3))
        U = tuple((rng.uniform(-2, 2), rng.uniform(-2, 2)) for _ in range(3))
        assert triangles_overlap(T, U) == convex_overlap_reference(T, U)


def test_moved_dop_contains_the_moved_points():
    rng = random.Random(4)
    looser = 0
    for _ in range(300):
        pts = [(rng.uniform(-5, 5), rng.uniform(-5, 5)) for _ in range(6)]
        R, t = rotation(rng.uniform(0, 2 * math.pi)), (rng.uniform(-5, 5), rng.uniform(-5, 5))
        moved = [apply(R, t, p) for p in pts]
        M = moved_dop(dop_of_points(pts), R, t)
        tight = dop_of_points(moved)
        assert all(inside_dop(p, M) for p in moved)
        assert all(m[0] <= s[0] + 1e-9 and s[1] <= m[1] + 1e-9 for m, s in zip(M, tight))
        looser += any(m[1] - m[0] > s[1] - s[0] + 1e-6 for m, s in zip(M, tight))
    assert looser > 200


def test_every_dop_holds_its_triangles():
    rng = random.Random(5)
    for _ in range(10):
        tris = random_object(rng, rng.randint(1, 60))
        root = build(tris)
        nodes = all_nodes(root)
        assert len(nodes) == 2 * len(tris) - 1
        assert sorted(n.tris[0] for n in nodes if n.leaf) == list(range(len(tris)))
        for n in nodes:
            assert all(inside_dop(p, n.dop) for i in n.tris for p in tris[i])
            if not n.leaf:
                assert sorted(n.left.tris + n.right.tris) == sorted(n.tris)


def test_overlap_query_against_brute_force():
    rng = random.Random(6)
    total = 0
    for _ in range(25):
        trisA = random_object(rng, 40)
        trisB = random_object(rng, 40)
        root_a, root_b = build(trisA), build(trisB)
        for _ in range(3):
            R = rotation(rng.uniform(0, 2 * math.pi))
            t = (rng.uniform(-8, 8), rng.uniform(-8, 8))
            got, tests = overlap_pairs(root_a, trisA, root_b, trisB, R, t)
            assert got == brute_pairs(trisA, trisB, R, t)
            assert tests <= (2 * 40 - 1) ** 2
            total += len(got)
    assert total > 100


def test_far_objects_need_one_test():
    rng = random.Random(7)
    trisA, trisB = random_object(rng, 30), random_object(rng, 30)
    got, tests = overlap_pairs(build(trisA), trisA, build(trisB), trisB, rotation(1.0), (100.0, 0.0))
    assert got == set() and tests == 1
