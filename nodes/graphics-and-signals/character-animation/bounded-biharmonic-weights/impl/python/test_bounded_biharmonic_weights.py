# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bounded-biharmonic-weights/. The authors are listed in prov/W8RNMB.jsonl.
"""Tests of bounded biharmonic weights.

The active set solver is compared with a brute force search over every face
of the box and checked against the KKT conditions. The weights interpolate
the handles, lie in [0, 1], sum to 1 after normalization and keep the
symmetry of the domain. Without the bounds, the weights of a strip go
negative, which the bounds prevent. The check values of the page hold.
"""

import random

from bounded_biharmonic_weights import (
    bbw,
    bilaplacian,
    box_qp,
    brute_force_box_qp,
    cotangent_laplacian,
    energy,
    grid,
    lumped_mass,
)


def q_of(verts, tris):
    return bilaplacian(cotangent_laplacian(verts, tris), lumped_mass(verts, tris))


def test_laplacian_and_mass():
    verts, tris = grid(4, 3, width=3.0, height=2.0)
    lap = cotangent_laplacian(verts, tris)
    n = len(verts)
    for i in range(n):
        assert abs(sum(lap[i])) < 1e-12
        for j in range(n):
            assert abs(lap[i][j] - lap[j][i]) < 1e-12
    assert abs(sum(lumped_mass(verts, tris)) - 6.0) < 1e-12


def test_active_set_against_brute_force_on_meshes():
    for nx, ny, w, handles in ((3, 2, 2.0, (0, 1)), (3, 3, 1.0, (0, 8)), (4, 2, 3.0, (0, 1, 7))):
        verts, tris = grid(nx, ny, width=w)
        q = q_of(verts, tris)
        for k in range(len(handles)):
            fixed = {h: (1.0 if j == k else 0.0) for j, h in enumerate(handles)}
            x, _ = box_qp(q, fixed)
            _, e = brute_force_box_qp(q, fixed)
            assert abs(energy(q, x) - e) <= 1e-10 * (1.0 + e)


def test_active_set_against_brute_force_on_random_problems():
    rng = random.Random(6)
    for _ in range(15):
        n = 7
        b = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(n)]
        q = [[sum(b[k][i] * b[k][j] for k in range(n)) + (0.1 if i == j else 0.0) for j in range(n)] for i in range(n)]
        fixed = {0: 1.0, 1: 0.0}
        x, _ = box_qp(q, fixed)
        _, e = brute_force_box_qp(q, fixed)
        assert abs(energy(q, x) - e) <= 1e-10 * (1.0 + e)


def test_kkt_conditions():
    verts, tris = grid(7, 7)
    q = q_of(verts, tris)
    handles = (0, 6, 24, 45)
    for k in range(len(handles)):
        fixed = {h: (1.0 if j == k else 0.0) for j, h in enumerate(handles)}
        x, _ = box_qp(q, fixed)
        g = [sum(q[i][j] * x[j] for j in range(len(x))) for i in range(len(x))]
        for i in range(len(x)):
            if i in fixed:
                continue
            assert -1e-15 <= x[i] <= 1.0 + 1e-15
            if 1e-12 < x[i] < 1.0 - 1e-12:
                assert abs(g[i]) < 1e-9
            elif x[i] <= 1e-12:
                assert g[i] > -1e-9
            else:
                assert g[i] < 1e-9


def test_interpolation_bounds_and_partition_of_unity():
    verts, tris = grid(7, 7)
    handles = [0, 6, 24, 45]
    w = bbw(verts, tris, handles)
    for k, h in enumerate(handles):
        for j in range(len(handles)):
            assert abs(w[j][h] - (1.0 if j == k else 0.0)) < 1e-12
    for i in range(len(verts)):
        assert abs(sum(wk[i] for wk in w) - 1.0) < 1e-12
        assert all(-1e-15 <= wk[i] <= 1.0 + 1e-12 for wk in w)


def test_symmetry():
    verts, tris = grid(7, 7)
    w = bbw(verts, tris, [0, 6, 42, 48])
    for i in range(7):
        for j in range(7):
            assert abs(w[0][j * 7 + i] - w[0][i * 7 + j]) < 1e-9
            assert abs(w[1][j * 7 + i] - w[2][i * 7 + j]) < 1e-9


def test_bounds_matter_on_a_strip():
    verts, tris = grid(5, 2, width=4.0)
    q = q_of(verts, tris)
    free = bbw(verts, tris, [0, 2], bounded=False, normalize=False)
    bound = bbw(verts, tris, [0, 2], normalize=False)
    assert min(free[0]) < -0.4 and max(free[1]) > 1.4
    assert min(bound[0]) >= 0.0 and max(bound[1]) <= 1.0
    assert energy(q, bound[0]) >= energy(q, free[0])
    verts, tris = grid(3, 3)
    a = bbw(verts, tris, [0, 8], bounded=False)
    b = bbw(verts, tris, [0, 8])
    assert max(abs(x - y) for x, y in zip(a[0], b[0])) < 1e-12


def test_check_values_of_the_page():
    verts, tris = grid(5, 2, width=4.0)
    free = bbw(verts, tris, [0, 2], bounded=False, normalize=False)
    bound = bbw(verts, tris, [0, 2], normalize=False)
    want_free = (1.0, 0.5914, 0.0, -0.3326, -0.4325)
    want_bound = (1.0, 0.5428, 0.0, 0.0, 0.0)
    for i in range(5):
        assert abs(free[0][i] - want_free[i]) < 5e-5
        assert abs(bound[0][i] - want_bound[i]) < 5e-5
    for i in range(10):
        assert abs(bound[0][i] + bound[1][i] - 1.0) < 1e-12
