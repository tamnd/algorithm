# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/automatic-rigging/. The authors are listed in prov/FM8DXC.jsonl.
"""Tests of automatic rigging by heat diffusion.

The A* embedding is compared with a brute force search over all
assignments. The Cholesky solve is compared with Gaussian elimination. The
heat weights are nonnegative and sum to 1 at every vertex, also at vertices
that see no bone, they tend to the nearest bone weights as c grows, and the
check value of the page holds.
"""

import random

from anim import norm, solve, sub
from automatic_rigging import (
    brute_force_embedding,
    cholesky,
    cholesky_solve,
    embed,
    heat_system,
    heat_weights,
    nearest_visible,
    rig,
)

L_SHAPE = [(0.0, -0.3), (2.3, -0.3), (2.3, 2.0), (1.7, 2.0), (1.7, 0.3), (0.0, 0.3)]
U_SHAPE = [(0.0, 0.0), (3.0, 0.0), (3.0, 3.0), (2.0, 3.0), (2.0, 1.0), (1.0, 1.0), (1.0, 3.0), (0.0, 3.0)]


def resample(poly, h):
    out = []
    n = len(poly)
    for e in range(n):
        a, b = poly[e], poly[(e + 1) % n]
        k = max(1, round(norm(sub(b, a)) / h))
        for s in range(k):
            out.append((a[0] + (b[0] - a[0]) * s / k, a[1] + (b[1] - a[1]) * s / k))
    return out


def inside(poly, p):
    c = False
    n = len(poly)
    for e in range(n):
        a, b = poly[e], poly[(e + 1) % n]
        if (a[1] > p[1]) != (b[1] > p[1]):
            x = a[0] + (p[1] - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if p[0] < x:
                c = not c
    return c


def test_embedding_matches_brute_force_on_a_chain():
    cands = [(0.5 * x, 0.5 * y - 0.25) for x in range(5) for y in range(5)]
    cands = [p for p in cands if inside(L_SHAPE, p)]
    parents, offsets = [-1, 0, 1], [None, (2.0, 0.0), (0.0, 1.6)]
    cost, part, _ = embed(parents, offsets, cands, L_SHAPE)
    bf_cost, _ = brute_force_embedding(parents, offsets, cands, L_SHAPE)
    assert abs(cost - bf_cost) < 1e-12
    assert cands[part[1]][0] > 1.7 and cands[part[2]][1] > 1.0


def test_embedding_matches_brute_force_on_random_trees():
    rng = random.Random(4)
    box = [(0.0, 0.0), (3.0, 0.0), (3.0, 3.0), (0.0, 3.0)]
    for _ in range(4):
        cands = [(rng.uniform(0, 3), rng.uniform(0, 3)) for _ in range(6)]
        parents = [-1, 0, 0, 1]
        offsets = [None] + [(rng.uniform(-1.5, 1.5), rng.uniform(-1.5, 1.5)) for _ in range(3)]
        shape = rng.choice([box, U_SHAPE])
        cost, part, expanded = embed(parents, offsets, cands, shape)
        bf_cost, _ = brute_force_embedding(parents, offsets, cands, shape)
        assert abs(cost - bf_cost) < 1e-12
        assert expanded <= 1 + 6 + 6**2 + 6**3


def test_cholesky_against_gaussian_elimination():
    rng = random.Random(5)
    n = 12
    b = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(n)]
    a = [[sum(b[k][i] * b[k][j] for k in range(n)) + (n if i == j else 0.0) for j in range(n)] for i in range(n)]
    rhs = [rng.gauss(0, 1) for _ in range(n)]
    x = cholesky_solve(cholesky(a), rhs)
    y = solve(a, rhs)
    assert max(abs(p - q) for p, q in zip(x, y)) < 1e-10
    poly = resample(L_SHAPE, 0.2)
    bones = [((0.2, 0.0), (2.0, 0.0)), ((2.0, 0.0), (2.0, 1.5))]
    a, rhs = heat_system(poly, bones)
    for r in rhs:
        x = cholesky_solve(cholesky(a), r)
        y = solve(a, r)
        assert max(abs(p - q) for p, q in zip(x, y)) < 1e-10


def test_weights_are_a_partition_of_unity_and_nonnegative():
    poly = resample(L_SHAPE, 0.1)
    bones = [((0.2, 0.0), (2.0, 0.0)), ((2.0, 0.0), (2.0, 1.5))]
    w = heat_weights(poly, bones)
    for j in range(len(poly)):
        assert abs(sum(wi[j] for wi in w) - 1.0) < 1e-12
        assert all(-1e-15 <= wi[j] <= 1.0 + 1e-12 for wi in w)
    assert w[0][poly.index((0.0, -0.3))] > 0.99
    assert w[1][poly.index((2.3, 2.0))] > 0.99


def test_vertices_that_see_no_bone():
    poly = resample(U_SHAPE, 0.25)
    bones = [((0.5, 0.5), (0.5, 2.5)), ((0.5, 0.5), (1.5, 0.5))]
    hidden = [j for j in range(len(poly)) if not nearest_visible(poly, bones, j)[1]]
    assert poly.index((3.0, 3.0)) in hidden
    w = heat_weights(poly, bones)
    for j in range(len(poly)):
        assert abs(w[0][j] + w[1][j] - 1.0) < 1e-12
        assert w[0][j] >= 0.0 and w[1][j] >= 0.0
    j = poly.index((3.0, 3.0))
    assert w[1][j] > w[0][j]


def test_large_c_tends_to_the_nearest_bone():
    poly = resample(L_SHAPE, 0.15)
    bones = [((0.2, 0.0), (2.0, 0.0)), ((2.0, 0.0), (2.0, 1.5))]
    w = heat_weights(poly, bones, c=1e7)
    for j in range(len(poly)):
        _, ids = nearest_visible(poly, bones, j)
        for i in range(2):
            p = 1.0 / len(ids) if i in ids else 0.0
            assert abs(w[i][j] - p) < 1e-3


def test_rig_end_to_end():
    cands = [(0.25 + 0.5 * x, 0.5 * y) for x in range(5) for y in range(4)]
    cands = [p for p in cands if inside(L_SHAPE, p)]
    poly = resample(L_SHAPE, 0.25)
    joints, w = rig(poly, [-1, 0, 1], [None, (2.0, 0.0), (0.0, 1.6)], cands)
    assert 1.7 < joints[1][0] < 2.3 and joints[2][1] > 1.0
    for j in range(len(poly)):
        assert abs(w[0][j] + w[1][j] - 1.0) < 1e-12


def test_check_value_of_the_page():
    square = [(-1.0, -1.0), (1.0, -1.0), (1.0, 1.0), (-1.0, 1.0)]
    bones = [((-0.5, -0.5), (0.5, -0.5)), ((-0.5, 0.5), (0.5, 0.5))]
    w = heat_weights(square, bones)
    for got, want in zip(w[0], (0.9, 0.9, 0.1, 0.1)):
        assert abs(got - want) < 1e-12
    for got, want in zip(w[1], (0.1, 0.1, 0.9, 0.9)):
        assert abs(got - want) < 1e-12
