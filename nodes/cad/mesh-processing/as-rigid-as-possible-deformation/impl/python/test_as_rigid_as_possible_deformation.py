# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/as-rigid-as-possible-deformation/. The authors are listed in prov/QG8W8W.jsonl.

import math
import random

import pytest

from as_rigid_as_possible_deformation import GlobalSolver, arap, cotan_sign, energy, local_step, weight_lists
from mx1mesh import (best_rotation, box_mesh, det3, edges, mat_mul, mat_vec, norm, rotation_matrix, sub, to_float,
                     transpose)


def bar():
    p, f = box_mesh((1, 1, 4), (2, 2, 8))
    return to_float(p), f


def bent_bar_handles(p):
    """Fix the bottom cap; turn the top cap by 90 degrees and put it at the end of a quarter circle of length 4."""
    rho = 8 / math.pi
    R = rotation_matrix((1, 0, 0), math.pi / 2)  # takes +z to -y
    H = {}
    for i, x in enumerate(p):
        if x[2] == -2.0:
            H[i] = x
        elif x[2] == 2.0:
            r = mat_vec(R, (x[0], x[1], 0.0))
            H[i] = (r[0], r[1] - rho, r[2] - 2 + rho)
    return H


def trace(A):
    return A[0][0] + A[1][1] + A[2][2]


def random_rotation(rng):
    return rotation_matrix((rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1)), rng.uniform(0, math.pi))


def test_the_local_step_is_optimal() -> None:
    rng = random.Random(3)
    for _ in range(100):
        S = [[rng.gauss(0, 1) for _ in range(3)] for _ in range(3)]
        R = best_rotation(S)
        assert abs(det3(R) - 1) < 1e-12
        RtR = mat_mul(transpose(R), R)
        assert all(abs(RtR[a][b] - (a == b)) < 1e-12 for a in range(3) for b in range(3))
        best = trace(mat_mul(R, S))
        for _ in range(30):
            assert trace(mat_mul(random_rotation(rng), S)) <= best + 1e-12


def test_a_rigid_motion_has_zero_energy() -> None:
    p, f = bar()
    nbw = weight_lists(len(p), f, p)
    Q = rotation_matrix((1, 2, 3), 0.8)
    t = (0.3, -1.0, 2.0)
    q = [tuple(a + b for a, b in zip(mat_vec(Q, x), t)) for x in p]
    R = local_step(p, q, nbw)
    for Ri in R:  # the local step finds Q in every cell
        assert all(abs(Ri[a][b] - Q[a][b]) < 1e-9 for a in range(3) for b in range(3))
    assert energy(p, q, nbw, R) < 1e-20
    H = {i: q[i] for i in range(len(p)) if p[i][2] == -2.0}
    q2 = GlobalSolver(len(p), nbw, H).solve(p, nbw, [Q] * len(p), H)
    assert max(norm(sub(a, b)) for a, b in zip(q, q2)) < 1e-12  # the global step keeps the rigid motion
    # from the rest shape, with both caps moved rigidly, the iteration tends to the rigid motion, slowly
    caps = {i: q[i] for i in range(len(p)) if abs(p[i][2]) == 2.0}
    q3, h = arap(p, f, caps, iterations=60)
    assert h[-1] < 1e-5 * h[0] and max(norm(sub(a, b)) for a, b in zip(q, q3)) < 0.01


def test_the_energy_never_increases() -> None:
    p, f = bar()
    for weights in ("cotan", "uniform"):
        _, h = arap(p, f, bent_bar_handles(p), iterations=15, weights=weights)
        assert all(b <= a + 1e-12 * h[0] for a, b in zip(h, h[1:]))
        assert h[-1] < h[0] / 10


def test_the_global_step_is_a_least_squares_solve() -> None:
    rng = random.Random(5)
    p, f = bar()
    nbw = weight_lists(len(p), f, p)
    H = bent_bar_handles(p)
    R = [random_rotation(rng) for _ in p]
    solver = GlobalSolver(len(p), nbw, H)
    q = solver.solve(p, nbw, R, H)
    e = energy(p, q, nbw, R)
    for _ in range(20):
        d = [(0.0, 0.0, 0.0) if i in H else tuple(rng.gauss(0, 1e-3) for _ in range(3)) for i in range(len(p))]
        q2 = [tuple(a + b for a, b in zip(x, y)) for x, y in zip(q, d)]
        assert energy(p, q2, nbw, R) >= e - 1e-12


def test_bending_a_bar_keeps_its_shape() -> None:
    p, f = bar()
    H = bent_bar_handles(p)
    q, _ = arap(p, f, H, iterations=30)
    nbw = weight_lists(len(p), f, p)
    ident = [[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]] for _ in p]
    naive = GlobalSolver(len(p), nbw, H).solve(p, nbw, ident, H)
    rho = 8 / math.pi
    arc_mid = (0.0, -rho * (1 - math.cos(math.pi / 4)), -2 + rho * math.sin(math.pi / 4))
    mid = [i for i, x in enumerate(p) if x[2] == 0.0]

    def centre(x):
        return tuple(sum(x[i][c] for i in mid) / len(mid) for c in range(3))

    assert norm(sub(centre(q), arc_mid)) < 0.02
    assert norm(sub(centre(naive), arc_mid)) > 0.5

    def worst_stretch(x):
        return max(abs(norm(sub(x[i], x[j])) / norm(sub(p[i], p[j])) - 1) for i, j in edges(f))

    assert worst_stretch(q) < 0.2 < 0.9 < worst_stretch(naive)


def test_negative_cotangent_weights_are_refused() -> None:
    p = [(0.0, 0.0, 0.0), (1.0, -0.1, 0.0), (2.0, 0.0, 0.0), (1.0, 0.1, 0.0)]
    f = [(0, 1, 2), (0, 2, 3)]
    with pytest.raises(ValueError):
        weight_lists(4, f, p)
    assert all(w == 1.0 for row in weight_lists(4, f, p, "uniform") for _, w in row)


def test_the_sign_of_a_weight_is_exact() -> None:
    # four points on the circle of radius 5: the angles opposite the edge 0-2 add to 180 degrees, so w_02 = 0
    p = [(5.0, 0.0, 0.0), (4.0, 3.0, 0.0), (0.0, 5.0, 0.0), (-3.0, -4.0, 0.0)]
    f = [(0, 1, 2), (0, 2, 3)]
    assert cotan_sign(p, 0, 2, [1, 3]) == 0
    assert dict(weight_lists(4, f, p)[0])[2] == 0.0
    q = [(5.0, 0.0, 0.0), (4.0, 3.0, 0.0), (0.0, 5.0, 0.0), (-3.0, -4.000001, 0.0)]  # just outside: still >= 0
    assert cotan_sign(q, 0, 2, [1, 3]) == 1
    q[3] = (-3.0, -3.999999, 0.0)  # just inside the circle: the angles add to more than 180 degrees
    assert cotan_sign(q, 0, 2, [1, 3]) == -1
