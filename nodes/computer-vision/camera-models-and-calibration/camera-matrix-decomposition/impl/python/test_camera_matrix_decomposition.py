# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/camera-matrix-decomposition/. The authors are listed in prov/VTG4C0.jsonl.
"""Tests of the decomposition P -> K, R, t, C."""

import math
import random

from camera_matrix_decomposition import (center_from_null_vector,
                                         decompose_camera_matrix,
                                         intrinsics_by_cholesky)
from cvgeom import camera_center, camera_matrix, make_K, random_rotation
from cvla import det, eye, mul, norm, scale, sub, transpose


def close(a, b, tol):
    return norm(sub(a, b)) <= tol


def random_camera(rng):
    K = make_K(rng.uniform(300, 1500), rng.uniform(300, 1500),
               rng.uniform(200, 500), rng.uniform(150, 400), rng.uniform(-5, 5))
    R = random_rotation(rng)
    t = [rng.uniform(-3, 3) for _ in range(3)]
    return K, R, t


def check_valid(K, R):
    assert all(K[i][j] == 0.0 for i in range(3) for j in range(i))
    assert all(K[i][i] > 0.0 for i in range(3))
    assert K[2][2] == 1.0
    assert close(mul(transpose(R), R), eye(3), 1e-12)
    assert abs(det(R) - 1.0) <= 1e-12


def test_page_example():
    # K = [[4, 1, 3], [0, 5, 2], [0, 0, 1]], R = rotation by 90 degrees
    # about Z, t = (1, 2, 4), and P scaled by -2.
    P = [[-2.0, 8.0, -6.0, -36.0],
         [-10.0, 0.0, -4.0, -36.0],
         [0.0, 0.0, -2.0, -8.0]]
    K, R, t, C = decompose_camera_matrix(P)
    assert close(K, [[4.0, 1.0, 3.0], [0.0, 5.0, 2.0], [0.0, 0.0, 1.0]], 1e-12)
    assert close(R, [[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]], 1e-12)
    assert close(t, [1.0, 2.0, 4.0], 1e-12)
    assert close(C, [-2.0, 1.0, -4.0], 1e-12)


def test_exact_recovery_any_scale():
    rng = random.Random(1)
    for _ in range(40):
        K0, R0, t0 = random_camera(rng)
        lam = rng.uniform(0.01, 100.0) * rng.choice([-1.0, 1.0])
        P = scale(camera_matrix(K0, R0, t0), lam)
        K, R, t, C = decompose_camera_matrix(P)
        check_valid(K, R)
        assert close(K, K0, 1e-10 * norm(K0))
        assert close(R, R0, 1e-10)
        assert close(t, t0, 1e-10)
        C0 = [-v for v in [sum(R0[j][i] * t0[j] for j in range(3)) for i in range(3)]]
        assert close(C, C0, 1e-10)


def test_center_three_ways():
    rng = random.Random(2)
    for _ in range(20):
        K0, R0, t0 = random_camera(rng)
        P = scale(camera_matrix(K0, R0, t0), rng.uniform(-5.0, 5.0))
        _, _, _, C = decompose_camera_matrix(P)
        assert close(C, center_from_null_vector(P), 1e-9)
        assert close(C, camera_center(P), 1e-9)
        Ch = C + [1.0]
        assert all(abs(sum(row[k] * Ch[k] for k in range(4))) <= 1e-9 * norm(P)
                   for row in P)


def test_against_cholesky_reference():
    rng = random.Random(3)
    for _ in range(20):
        K0, R0, t0 = random_camera(rng)
        P = scale(camera_matrix(K0, R0, t0), rng.uniform(-5.0, 5.0))
        K, _, _, _ = decompose_camera_matrix(P)
        assert close(K, intrinsics_by_cholesky(P), 1e-9 * norm(K))


def test_any_nonsingular_P_is_a_finite_camera():
    # A random 3 x 4 matrix (for example a noisy DLT estimate) still
    # decomposes, and K [R | t] gives P back up to scale.
    rng = random.Random(4)
    for _ in range(40):
        P = [[rng.gauss(0.0, 1.0) for _ in range(4)] for _ in range(3)]
        K, R, t, _ = decompose_camera_matrix(P)
        check_valid(K, R)
        Q = camera_matrix(K, R, t)
        s = sum(a * b for ra, rb in zip(P, Q) for a, b in zip(ra, rb)) / \
            sum(b * b for rb in Q for b in rb)
        assert close(scale(Q, s), P, 1e-10 * norm(P))


def test_sign_of_scale_puts_points_in_front():
    # With det M > 0 after the sign fix, a point in front of the true camera
    # has a positive third coordinate in K [R | t].
    rng = random.Random(5)
    K0, R0, t0 = make_K(800, 800, 320, 240), eye(3), [0.0, 0.0, 5.0]
    P = scale(camera_matrix(K0, R0, t0), -3.0)
    K, R, t, _ = decompose_camera_matrix(P)
    for _ in range(10):
        X = [rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1)]
        z = sum(R[2][k] * X[k] for k in range(3)) + t[2]
        assert z > 0.0


def test_singular_left_block_raises():
    # An affine camera has last row (0, 0, 0, 1), so M is singular.
    P = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    try:
        decompose_camera_matrix(P)
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_rotation_angle_and_zero_skew():
    K0 = make_K(500, 500, 0, 0)
    R0 = [[math.cos(0.3), 0.0, math.sin(0.3)], [0.0, 1.0, 0.0],
          [-math.sin(0.3), 0.0, math.cos(0.3)]]
    K, R, _, _ = decompose_camera_matrix(camera_matrix(K0, R0, [0.0, 0.0, 1.0]))
    assert abs(K[0][1]) <= 1e-12
    trace = sum(R[i][i] for i in range(3))
    assert abs(math.acos((trace - 1.0) / 2.0) - 0.3) <= 1e-12
