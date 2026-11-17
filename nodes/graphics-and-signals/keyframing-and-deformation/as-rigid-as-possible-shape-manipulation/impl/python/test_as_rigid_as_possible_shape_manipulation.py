# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/as-rigid-as-possible-shape-manipulation/. The authors are listed in prov/6TBSNN.jsonl.
import math
import random

import pytest

from anim import solve
from as_rigid_as_possible_shape_manipulation import ArapManipulator, cholesky, cholesky_solve, grid_mesh, local_frame

VERTS, TRIS = grid_mesh(5, 1)
# Handles: the two left vertices and the two right vertices of the 5 by 1 bar.
HANDLES = [0, 6, 5, 11]
_M = {}


def manip():
    if "m" not in _M:
        _M["m"] = ArapManipulator(VERTS, TRIS, HANDLES)
    return _M["m"]


def close_pts(a, b, eps):
    return all(math.dist(p, q) <= eps for p, q in zip(a, b))


def rigid(p, ang=0.9, t=(2.0, -1.0)):
    c, s = math.cos(ang), math.sin(ang)
    return (c * p[0] - s * p[1] + t[0], s * p[0] + c * p[1] + t[1])


def test_local_frame_reconstructs_the_third_vertex():
    rng = random.Random(61)
    for _ in range(20):
        p = [(rng.uniform(-2, 2), rng.uniform(-2, 2)) for _ in range(3)]
        x, y = local_frame(*p)
        e = (p[1][0] - p[0][0], p[1][1] - p[0][1])
        q = (p[0][0] + x * e[0] - y * e[1], p[0][1] + x * e[1] + y * e[0])
        assert math.dist(q, p[2]) < 1e-12


def test_cholesky_matches_gaussian_elimination():
    rng = random.Random(62)
    n = 8
    b = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    a = [[sum(b[k][i] * b[k][j] for k in range(n)) + (n if i == j else 0) for j in range(n)] for i in range(n)]
    rhs = [rng.uniform(-1, 1) for _ in range(n)]
    x1 = cholesky_solve(cholesky(a), rhs)
    x2 = solve(a, rhs)
    assert max(abs(u - v) for u, v in zip(x1, x2)) < 1e-12


def test_one_handle_is_not_enough():
    with pytest.raises(ValueError):
        ArapManipulator(VERTS, TRIS, [0])


def test_rest_handles_give_rest_mesh():
    m = manip()
    inter, final = m.solve([VERTS[v] for v in HANDLES])
    assert close_pts(inter, VERTS, 1e-10)
    assert close_pts(final, VERTS, 1e-10)


def test_rigid_motion_of_handles_moves_mesh_rigidly():
    m = manip()
    inter, final = m.solve([rigid(VERTS[v]) for v in HANDLES])
    want = [rigid(p) for p in VERTS]
    assert close_pts(inter, want, 1e-10)
    assert close_pts(final, want, 1e-10)


def test_uniform_scale_survives_step1_only():
    m = manip()
    inter, final = m.solve([(2 * VERTS[v][0], 2 * VERTS[v][1]) for v in HANDLES])
    assert close_pts(inter, [(2 * x, 2 * y) for x, y in VERTS], 1e-10)
    # Step 2 pulls the free triangles back to the rest size: the fitted triangles have the rest
    # edge lengths, and the free vertical edges (length 2 after step 1) come back close to 1.
    fitted = m.fitted_triangles(inter)
    for t, w in zip(m.tris, fitted):
        for o in range(3):
            a, b = t[o], t[(o + 1) % 3]
            assert abs(math.dist(w[o], w[(o + 1) % 3]) - math.dist(VERTS[a], VERTS[b])) < 1e-12
    for a, b in ((1, 7), (2, 8), (3, 9), (4, 10)):
        assert abs(math.dist(inter[a], inter[b]) - 2) < 1e-10
        assert math.dist(final[a], final[b]) < 1.2


def test_handles_are_met_exactly():
    m = manip()
    rng = random.Random(63)
    targets = [(VERTS[v][0] + rng.uniform(-1, 1), VERTS[v][1] + rng.uniform(-1, 1)) for v in HANDLES]
    inter, final = m.solve(targets)
    for v, p in zip(HANDLES, targets):
        assert inter[v] == p and final[v] == p


def test_fit_equals_procrustes_rotation():
    m = manip()
    targets = [(VERTS[v][0], VERTS[v][1] + (1.5 if v in (5, 11) else 0.0)) for v in HANDLES]
    inter, _ = m.solve(targets)
    fitted = m.fitted_triangles(inter)
    for t, w in zip(m.tris, fitted):
        a = [complex(*VERTS[i]) for i in t]
        b = [complex(*inter[i]) for i in t]
        ca, cb = sum(a) / 3, sum(b) / 3
        alpha = sum((x - ca).conjugate() * (y - cb) for x, y in zip(a, b))
        rot = alpha / abs(alpha)
        want = [cb + rot * (x - ca) for x in a]
        assert all(abs(complex(*p) - q) < 1e-12 for p, q in zip(w, want))


def test_each_step_is_a_minimum():
    m = manip()
    rng = random.Random(65)
    targets = [(VERTS[v][0], VERTS[v][1] + (1.5 if v in (5, 11) else 0.0)) for v in HANDLES]
    inter, final = m.solve(targets)
    fitted = m.fitted_triangles(inter)
    e1, e2 = m.energy1(inter), m.energy2(final, fitted)
    for _ in range(10):
        k = rng.choice(m.free)
        d = (rng.uniform(-1e-3, 1e-3), rng.uniform(-1e-3, 1e-3))
        p1 = list(inter)
        p1[k] = (p1[k][0] + d[0], p1[k][1] + d[1])
        p2 = list(final)
        p2[k] = (p2[k][0] + d[0], p2[k][1] + d[1])
        assert m.energy1(p1) > e1
        assert m.energy2(p2, fitted) > e2


def test_worked_example_bend():
    m = manip()
    targets = [(VERTS[v][0], VERTS[v][1] + (1.5 if v in (5, 11) else 0.0)) for v in HANDLES]
    inter, final = m.solve(targets)
    # The free edges keep close to their rest length after step 2.
    worst = 0.0
    for t in TRIS:
        for o in range(3):
            a, b = t[o], t[(o + 1) % 3]
            worst = max(worst, abs(math.dist(final[a], final[b]) / math.dist(VERTS[a], VERTS[b]) - 1))
    assert worst < 0.2
    # The bar stays symmetric about its center point (2.5, 1.25) after the move.
    for v in range(len(VERTS)):
        i, j = v % 6, v // 6
        w = (5 - i) + 6 * (1 - j)
        p, q = final[v], final[w]
        assert abs(p[0] + q[0] - 5) < 1e-9 and abs(p[1] + q[1] - 2.5) < 1e-9
    # The numbers quoted on the page for the vertex that starts at (2, 0).
    assert math.dist(inter[2], (2.18, 0.54)) < 1e-12
    assert math.dist(final[2], (2.1903, 0.5898)) < 1e-4
