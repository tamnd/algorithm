# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/topological-tetrahedral-mesh-improvement/. The authors are listed in prov/JMSVP1.jsonl.

import random
from collections import Counter
from fractions import Fraction as F
from itertools import combinations

from mg3geom import orient3d
from topological_tetrahedral_mesh_improvement import (degree3_edges, faces, flip23, flip32, improve, kuhn_cube_mesh,
                                                      mean_ratio, positive)


def volume6(points, tets):
    return sum(orient3d(*[points[i] for i in t]) for t in tets)


def boundary_faces(tets):
    c = Counter(frozenset(f) for t in tets for f in combinations(t, 3))
    assert all(v <= 2 for v in c.values())     # no face in three tetrahedra
    return {f for f, v in c.items() if v == 1}


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def segment_crosses_triangle(d, e, a, b, c):
    """Independent test by barycentric coordinates: solve
    d + s (e - d) = a + u (b - a) + v (c - a) with Cramer's rule in Fractions,
    and ask for 0 < s < 1, u > 0, v > 0, u + v < 1."""
    cols = [[e[i] - d[i] for i in range(3)], [a[i] - b[i] for i in range(3)], [a[i] - c[i] for i in range(3)]]
    rhs = [a[i] - d[i] for i in range(3)]
    m = [[cols[j][i] for j in range(3)] for i in range(3)]
    den = det3(m)
    if den == 0:
        return False
    sol = []
    for j in range(3):
        mj = [row[:] for row in m]
        for i in range(3):
            mj[i][j] = rhs[i]
        sol.append(F(det3(mj), den))
    s, u, v = sol
    return 0 < s < 1 and u > 0 and v > 0 and u + v < 1


def test_one_23_flip_and_back():
    P = [(0, 0, 0), (4, 0, 0), (0, 4, 0), (1, 1, 3), (1, 1, -2)]
    a, b, c, d, e = range(5)
    old = [positive(P, (a, b, c, d)), positive(P, (a, b, c, e))]
    new = flip23(P, old, frozenset((a, b, c)))
    assert new is not None and len(new) == 3
    assert all(orient3d(*[P[i] for i in t]) > 0 for t in new)
    assert volume6(P, new) == volume6(P, old) == 80     # 6 V: 16 * 3 + 16 * 2
    assert boundary_faces(new) == boundary_faces(old)
    (edge, ring, ks), = list(degree3_edges(new))
    assert set(edge) == {d, e} and set(ring) == {a, b, c}
    back = flip32(P, edge, ring)
    assert {frozenset(t) for t in back} == {frozenset(t) for t in old}


def test_invalid_23_flip():
    P = [(0, 0, 0), (4, 0, 0), (0, 4, 0), (1, 1, 3), (5, 5, -1)]
    old = [positive(P, (0, 1, 2, 3)), positive(P, (0, 1, 2, 4))]
    assert flip23(P, old, frozenset((0, 1, 2))) is None
    assert not segment_crosses_triangle(P[3], P[4], P[0], P[1], P[2])


def test_five_point_volume_identity():
    rng = random.Random(1)
    for _ in range(500):
        p = [tuple(F(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(3)) for _ in range(5)]
        s = sum((-1) ** i * orient3d(*[p[j] for j in range(5) if j != i]) for i in range(5))
        assert s == 0


def test_23_validity_matches_barycentric_test():
    rng = random.Random(2)
    seen = Counter()
    while sum(seen.values()) < 600:
        P = [tuple(rng.randint(-4, 4) for _ in range(3)) for _ in range(5)]
        sd, se = orient3d(P[0], P[1], P[2], P[3]), orient3d(P[0], P[1], P[2], P[4])
        if sd * se >= 0:
            continue      # abcd and abce must lie on opposite sides of abc
        old = [positive(P, (0, 1, 2, 3)), positive(P, (0, 1, 2, 4))]
        try:
            new = flip23(P, old, frozenset((0, 1, 2)))
        except ValueError:
            new = None
        ok = segment_crosses_triangle(P[3], P[4], P[0], P[1], P[2])
        assert (new is not None) == ok
        if new is not None:
            assert volume6(P, new) == volume6(P, old)
            assert all(orient3d(*[P[i] for i in t]) > 0 for t in new)
            assert boundary_faces(new) == boundary_faces(old)
        seen[ok] += 1
    assert seen[True] > 50 and seen[False] > 50


def test_32_validity_matches_barycentric_test():
    rng = random.Random(3)
    seen = Counter()
    while sum(seen.values()) < 600:
        P = [tuple(rng.randint(-4, 4) for _ in range(3)) for _ in range(5)]
        a, b, c, d, e = range(5)
        s = [orient3d(P[x], P[y], P[d], P[e]) for x, y in ((a, b), (b, c), (c, a))]
        if not (all(v > 0 for v in s) or all(v < 0 for v in s)):
            continue      # the three tetrahedra around de must form a valid ring
        three = [positive(P, (x, y, d, e)) for x, y in ((a, b), (b, c), (c, a))]
        (edge, ring, ks), = list(degree3_edges(three))
        try:
            new = flip32(P, edge, ring)
        except ValueError:
            new = None
        ok = segment_crosses_triangle(P[d], P[e], P[a], P[b], P[c])
        assert (new is not None) == ok
        if new is not None:
            assert volume6(P, new) == volume6(P, three)
            assert boundary_faces(new) == boundary_faces(three)
        seen[ok] += 1
    assert seen[True] > 50 and seen[False] > 50


def perturbed_cube(seed, n=2, amount=F(3, 8)):
    """The Kuhn mesh of [0, n]^3 with interior vertices moved randomly on a
    grid of step 1/16, redrawn until every tetrahedron stays positive."""
    rng = random.Random(seed)
    pts, tets = kuhn_cube_mesh(n)
    base = [tuple(F(x) for x in p) for p in pts]
    while True:
        P = []
        for p in base:
            if all(0 < x < n for x in p):
                k = int(amount * 16)
                P.append(tuple(x + F(rng.randint(-k, k), 16) for x in p))
            else:
                P.append(p)
        if all(orient3d(*[P[i] for i in t]) > 0 for t in tets):
            return P, tets


def test_hill_climbing_keeps_a_valid_mesh_and_raises_the_worst_quality():
    flips = 0
    for n, seed in ((2, 0), (3, 1), (3, 2)):
        P, tets = perturbed_cube(seed, n=n, amount=F(1, 2))
        before = min(mean_ratio(P, t) for t in tets)
        out, n23, n32 = improve(P, tets)
        flips += n23 + n32
        assert all(orient3d(*[P[i] for i in t]) > 0 for t in out)
        assert volume6(P, out) == 6 * n ** 3                  # the cube [0, n]^3
        assert boundary_faces(out) == boundary_faces(tets)    # same boundary, conforming
        assert min(mean_ratio(P, t) for t in out) >= before
        assert len(out) == len(tets) + n23 - n32
    assert flips >= 10


def test_each_flip_raises_the_sorted_quality_vector():
    # the termination argument: each accepted flip makes the ascending list of
    # qualities lexicographically larger, so no mesh repeats
    P, tets = perturbed_cube(1, n=3, amount=F(1, 2))
    prev = sorted(mean_ratio(P, t) for t in tets)
    k = 1
    while True:
        out, n23, n32 = improve(P, tets, max_flips=k)
        if n23 + n32 < k:
            break
        cur = sorted(mean_ratio(P, t) for t in out)
        assert cur > prev
        prev = cur
        k += 1
    assert k > 2
