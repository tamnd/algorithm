# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/obb-tree/. The authors are listed in prov/FZV7G9.jsonl.

import math
import random

from obb_tree import (
    OBB,
    apply,
    build,
    fit_obb,
    obb_overlap,
    overlap_pairs,
    principal_axis,
    rotation,
    triangles_overlap,
)


def _orient(a, b, c):
    v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return (v > 0) - (v < 0)


def _inside_convex(p, P):
    """p in the closed convex polygon P, in either orientation."""
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


def inside_box(p, box, tol=1e-9):
    d = (p[0] - box.center[0], p[1] - box.center[1])
    return abs(d[0] * box.u[0] + d[1] * box.u[1]) <= box.half[0] + tol and abs(d[0] * box.v[0] + d[1] * box.v[1]) <= box.half[1] + tol


def test_page_example():
    # a 4 by 1 rectangle turned by 30 degrees: the fitted box has the same axes and area
    R = rotation(math.radians(30))
    pts = [apply(R, (0, 0), p) for p in ((0, 0), (4, 0), (4, 1), (0, 1), (2, 0), (1, 1))]
    box = fit_obb(pts)
    assert abs(abs(box.u[0]) - math.cos(math.radians(30))) < 1e-9
    assert abs(4 * box.half[0] * box.half[1] - 4) < 1e-7
    # the axis-aligned box of the same points is much larger
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    assert abs((max(xs) - min(xs)) * (max(ys) - min(ys)) - (2 * math.sqrt(3) + 0.5) * (2 + math.sqrt(3) / 2)) < 1e-9


def test_principal_axis_of_a_thin_shape():
    rng = random.Random(1)
    for _ in range(50):
        a = rng.uniform(0, math.pi)
        R = rotation(a)
        pts = [apply(R, (0, 0), (rng.uniform(-5, 5), rng.uniform(-0.2, 0.2))) for _ in range(30)]
        pts += [apply(R, (0, 0), (-5, 0)), apply(R, (0, 0), (5, 0))]
        u = principal_axis(pts)
        assert abs(u[0] * math.cos(a) + u[1] * math.sin(a)) > 0.99


def test_box_overlap_against_a_reference():
    rng = random.Random(2)
    hits = 0
    for _ in range(2000):
        boxes = []
        for _ in range(2):
            a = rng.uniform(0, math.pi)
            boxes.append(OBB((rng.uniform(-3, 3), rng.uniform(-3, 3)), (math.cos(a), math.sin(a)), (rng.uniform(0.1, 2), rng.uniform(0.1, 2))))
        A, B = boxes
        expect = convex_overlap_reference(A.corners(), B.corners())
        assert obb_overlap(A, B) == expect
        hits += expect
    assert 400 < hits < 1600


def test_triangle_overlap_against_a_reference():
    rng = random.Random(3)
    for _ in range(2000):
        T = tuple((rng.uniform(-2, 2), rng.uniform(-2, 2)) for _ in range(3))
        U = tuple((rng.uniform(-2, 2), rng.uniform(-2, 2)) for _ in range(3))
        assert triangles_overlap(T, U) == convex_overlap_reference(T, U)


def test_every_box_holds_its_triangles():
    rng = random.Random(4)
    for _ in range(10):
        tris = random_object(rng, rng.randint(1, 60))
        root = build(tris)
        nodes = all_nodes(root)
        assert len(nodes) == 2 * len(tris) - 1
        assert sorted(n.tris[0] for n in nodes if n.leaf) == list(range(len(tris)))
        for n in nodes:
            assert all(inside_box(p, n.box) for i in n.tris for p in tris[i])
            if not n.leaf:
                assert sorted(n.left.tris + n.right.tris) == sorted(n.tris)


def test_overlap_query_against_brute_force():
    rng = random.Random(5)
    total = 0
    for _ in range(25):
        trisA = random_object(rng, 40)
        trisB = random_object(rng, 40)
        root_a, root_b = build(trisA), build(trisB)
        for _ in range(3):
            R = rotation(rng.uniform(0, 2 * math.pi))
            t = (rng.uniform(-8, 8), rng.uniform(-8, 8))
            got, tests = overlap_pairs(root_a, trisA, root_b, trisB, R, t)
            want = brute_pairs(trisA, trisB, R, t)
            assert got == want
            total += len(want)
    assert total > 100


def test_far_objects_need_one_box_test():
    rng = random.Random(6)
    trisA, trisB = random_object(rng, 30), random_object(rng, 30)
    got, tests = overlap_pairs(build(trisA), trisA, build(trisB), trisB, rotation(1.0), (100.0, 0.0))
    assert got == set() and tests == 1
