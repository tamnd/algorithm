# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zhang-calibration-method/. The authors are listed in prov/WSAQZX.jsonl.
"""Tests of Zhang's calibration method on synthetic views of a planar grid."""

import math
import random

from cvgeom import add_noise, axis_angle_to_R, make_K, rot_x, rot_y, rot_z
from cvla import cholesky, det, eye, inv, matvec, mul, norm, nullvec, sub, svd, transpose
from zhang_calibration_method import (calibrate, constraint_matrix, estimate_distortion,
                                      extrinsics_from_homography, homography_dlt,
                                      intrinsics_from_b, intrinsics_from_homographies,
                                      project_plane_points, rotation_to_vector)

GRID = [[float(X), float(Y)] for Y in range(5) for X in range(6)]
CENTER = [2.5, 2.0, 0.0]
K_SKEW = make_K(800, 780, 320, 240, 1.5)
K_ZERO = make_K(800, 780, 320, 240)
TILTS = [(0.35, 0.1, 0.0), (-0.1, 0.4, 0.3), (0.2, -0.35, -0.2), (-0.3, -0.2, 0.5),
         (0.15, 0.3, -0.4)]


def pose(a, b, c, depth=12.0):
    R = mul(mul(rot_x(a), rot_y(b)), rot_z(c))
    Rc = matvec(R, CENTER)
    return R, [0.0 - Rc[0], 0.0 - Rc[1], depth - Rc[2]]


def views(K, n, k1=0.0, k2=0.0):
    poses = [pose(*TILTS[i]) for i in range(n)]
    obs = [project_plane_points(K, k1, k2, R, t, GRID) for R, t in poses]
    return poses, obs


def rel(a, b):
    return norm(sub(a, b)) / norm(b)


def is_rotation(R, tol):
    return norm(sub(mul(transpose(R), R), eye(3))) <= tol and abs(det(R) - 1.0) <= tol


def test_homography_maps_the_grid():
    poses, obs = views(K_SKEW, 1)
    H = homography_dlt(GRID, obs[0])
    for p, q in zip(GRID, obs[0]):
        w = matvec(H, [p[0], p[1], 1.0])
        assert math.hypot(w[0] / w[2] - q[0], w[1] / w[2] - q[1]) <= 1e-8


def test_closed_form_exact_with_skew():
    for n in (3, 4, 5):
        poses, obs = views(K_SKEW, n)
        Hs = [homography_dlt(GRID, view) for view in obs]
        K = intrinsics_from_homographies(Hs)
        assert rel(K, K_SKEW) <= 1e-8
        for (R0, t0), H in zip(poses, Hs):
            R, t = extrinsics_from_homography(K, H)
            assert is_rotation(R, 1e-12)
            assert norm(sub(R, R0)) <= 1e-8
            assert rel(t, t0) <= 1e-8


def test_zero_skew_needs_two_views_only():
    poses, obs = views(K_ZERO, 2)
    Hs = [homography_dlt(GRID, view) for view in obs]
    assert rel(intrinsics_from_homographies(Hs, zero_skew=True), K_ZERO) <= 1e-8


def test_too_few_views_raise():
    _, obs = views(K_SKEW, 2)
    Hs = [homography_dlt(GRID, view) for view in obs]
    try:
        intrinsics_from_homographies(Hs)
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_b_against_cholesky():
    # B = lambda K^-T K^-1 and K^-T is lower triangular, so the Cholesky
    # factor L of B (after its sign is made positive) is a multiple of K^-T.
    _, obs = views(K_SKEW, 4)
    b = nullvec(constraint_matrix([homography_dlt(GRID, view) for view in obs]))
    if b[0] < 0.0:
        b = [-v for v in b]
    B = [[b[0], b[1], b[3]], [b[1], b[2], b[4]], [b[3], b[4], b[5]]]
    K = inv(transpose(cholesky(B)))
    K = [[v / K[2][2] for v in row] for row in K]
    assert rel(K, intrinsics_from_b(b)) <= 1e-8
    assert rel(intrinsics_from_b([-v for v in b]), K) <= 1e-8


def test_parallel_planes_are_degenerate():
    # Views that differ only by a translation have the same h1 and h2 up to
    # scale, so they add no new constraint: V keeps rank 2.
    obs = []
    for t in ([-2.5, -2.0, 10.0], [-1.0, -3.0, 14.0], [-3.5, 0.5, 12.0]):
        obs.append(project_plane_points(K_SKEW, 0.0, 0.0, eye(3), t, GRID))
    V = constraint_matrix([homography_dlt(GRID, view) for view in obs])
    _, s, _ = svd(V)
    assert s[1] / s[0] > 1e-6
    assert s[2] / s[0] <= 1e-10


def test_distortion_estimate_is_exact_with_true_poses():
    poses, obs = views(K_SKEW, 3, -0.25, 0.08)
    k1, k2 = estimate_distortion(K_SKEW, poses, GRID, obs)
    assert abs(k1 + 0.25) <= 1e-10 and abs(k2 - 0.08) <= 1e-10


def test_full_pipeline_exact_with_distortion():
    poses, obs = views(K_SKEW, 4, -0.25, 0.08)
    res = calibrate(GRID, obs)
    assert rel(res["K"], K_SKEW) <= 1e-6
    assert abs(res["k1"] + 0.25) <= 1e-6 and abs(res["k2"] - 0.08) <= 1e-6
    for (R0, t0), R, t in zip(poses, res["R"], res["t"]):
        assert is_rotation(R, 1e-12)
        assert norm(sub(R, R0)) <= 1e-6
        assert rel(t, t0) <= 1e-6
    # The closed form alone is biased by the distortion.
    assert rel(res["K0"], K_SKEW) > 1e-4


def test_lm_cost_never_increases():
    rng = random.Random(3)
    _, obs = views(K_SKEW, 4, -0.25, 0.08)
    obs = [add_noise(rng, view, 0.3) for view in obs]
    hist = calibrate(GRID, obs)["history"]
    assert len(hist) >= 3
    assert all(b <= a for a, b in zip(hist, hist[1:]))
    assert hist[-1] < hist[0]


def test_noise_sigma_02_five_views():
    # sigma = 0.2 pixel on 5 views of 30 points, zero skew, with distortion.
    rng = random.Random(7)
    _, obs = views(K_ZERO, 5, -0.25, 0.08)
    obs = [add_noise(rng, view, 0.2) for view in obs]
    res = calibrate(GRID, obs, zero_skew=True)
    K = res["K"]
    assert K[0][1] == 0.0
    assert abs(K[0][0] - 800.0) / 800.0 <= 0.01
    assert abs(K[1][1] - 780.0) / 780.0 <= 0.01
    assert abs(K[0][2] - 320.0) <= 5.0 and abs(K[1][2] - 240.0) <= 5.0
    rms = math.sqrt(res["history"][-1] / (2 * 5 * len(GRID)))
    assert 0.1 <= rms <= 0.2


def test_rotation_vector_round_trip():
    rng = random.Random(5)
    angles = [0.0, 1e-9, 0.5, 2.0, math.pi - 2e-4, math.pi - 1e-4, math.pi - 1e-6, math.pi]
    for theta in angles:
        axis = [rng.gauss(0.0, 1.0) for _ in range(3)]
        R = axis_angle_to_R(axis, theta)
        w = rotation_to_vector(R)
        assert norm(sub(axis_angle_to_R(w), R)) <= 1e-9
