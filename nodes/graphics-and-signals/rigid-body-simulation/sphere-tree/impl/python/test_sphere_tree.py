# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sphere-tree/. The authors are listed in prov/0FMTPB.jsonl.

import itertools
import math
import random

from sphere_tree import (
    _circle2,
    _circle3,
    apply,
    build,
    min_enclosing_circle,
    overlap_pairs,
    rotation,
    triangles_overlap,
)


def brute_circle(points):
    """The smallest circle through 2 or 3 of the points that holds all of them."""
    best = None
    cands = [_circle2(a, b) for a, b in itertools.combinations(points, 2)]
    cands += [_circle3(a, b, c) for a, b, c in itertools.combinations(points, 3)]
    for c, r in cands:
        if all(math.dist(c, p) <= r + 1e-9 for p in points) and (best is None or r < best[1]):
            best = (c, r)
    return best


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


def chain():
    return [((2 * k, 0), (2 * k + 1.5, 0), (2 * k + 0.5, 1)) for k in range(4)]


def test_page_example():
    root = build(chain())
    # the root circle: the vertices (0, 0) and (7.5, 0) are a diameter, and every other vertex is inside
    assert abs(root.center[0] - 3.75) < 1e-9 and abs(root.center[1]) < 1e-9
    assert abs(root.radius - 3.75) < 1e-6
    tris = chain()
    pairs, possible, tests = overlap_pairs(root, tris, root, tris, rotation(math.pi / 2), (7.0, 0.5))
    assert pairs == {(3, 0)} and possible == []
    pairs, possible, tests = overlap_pairs(root, tris, root, tris, rotation(math.pi / 2), (20.0, 0.0))
    assert pairs == set() and tests == 1


def test_min_enclosing_circle_against_brute_force():
    rng = random.Random(1)
    for _ in range(200):
        pts = [(rng.uniform(-5, 5), rng.uniform(-5, 5)) for _ in range(rng.randint(2, 9))]
        c, r = min_enclosing_circle(pts, seed=rng.randint(0, 99))
        bc, br = brute_circle(pts)
        assert all(math.dist(c, p) <= r + 1e-9 for p in pts)
        assert abs(r - br) < 1e-9


def test_circle_does_not_depend_on_the_seed():
    rng = random.Random(2)
    for _ in range(50):
        pts = [(rng.gauss(0, 3), rng.gauss(0, 1)) for _ in range(40)]
        radii = [min_enclosing_circle(pts, seed=s)[1] for s in range(5)]
        assert max(radii) - min(radii) < 1e-9


def test_triangle_overlap_on_simple_cases():
    T = ((0, 0), (2, 0), (0, 2))
    assert triangles_overlap(T, ((1, 1), (3, 1), (1, 3)))  # they share the point (1, 1)
    assert not triangles_overlap(T, ((1.1, 1.1), (3, 1), (1, 3)))
    assert triangles_overlap(T, ((0.2, 0.2), (0.5, 0.2), (0.2, 0.5)))  # one inside the other


def test_every_circle_holds_its_triangles():
    rng = random.Random(3)
    for _ in range(10):
        tris = random_object(rng, rng.randint(1, 60))
        root = build(tris)
        nodes = all_nodes(root)
        assert len(nodes) == 2 * len(tris) - 1
        assert sorted(n.tris[0] for n in nodes if n.leaf) == list(range(len(tris)))
        for n in nodes:
            assert all(math.dist(n.center, p) <= n.radius for i in n.tris for p in tris[i])
            if not n.leaf:
                assert sorted(n.left.tris + n.right.tris) == sorted(n.tris)


def test_overlap_query_against_brute_force():
    rng = random.Random(4)
    total = 0
    for _ in range(25):
        trisA, trisB = random_object(rng, 40), random_object(rng, 40)
        root_a, root_b = build(trisA), build(trisB)
        for _ in range(3):
            R = rotation(rng.uniform(0, 2 * math.pi))
            t = (rng.uniform(-8, 8), rng.uniform(-8, 8))
            got, possible, tests = overlap_pairs(root_a, trisA, root_b, trisB, R, t)
            assert got == brute_pairs(trisA, trisB, R, t) and possible == []
            assert tests <= (2 * 40 - 1) ** 2
            total += len(got)
    assert total > 100


def test_a_stopped_query_covers_every_contact():
    rng = random.Random(5)
    for _ in range(15):
        trisA, trisB = random_object(rng, 30), random_object(rng, 30)
        root_a, root_b = build(trisA), build(trisB)
        R, t = rotation(rng.uniform(0, 2 * math.pi)), (rng.uniform(-5, 5), rng.uniform(-5, 5))
        want = brute_pairs(trisA, trisB, R, t)
        last = None
        for level in range(0, 14):
            got, possible, tests = overlap_pairs(root_a, trisA, root_b, trisB, R, t, max_level=level)
            assert got <= want
            covered = set(got)
            for a, b in possible:
                assert math.dist(a.center, apply(R, t, b.center)) <= a.radius + b.radius
                covered |= {(i, j) for i in a.tris for j in b.tris}
            assert want <= covered
            if last is not None:
                assert tests >= last
            last = tests
        full = overlap_pairs(root_a, trisA, root_b, trisB, R, t)
        assert full[0] == want
