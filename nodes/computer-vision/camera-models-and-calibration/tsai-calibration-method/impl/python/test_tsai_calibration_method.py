# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tsai-calibration-method/. The authors are listed in prov/0E3W2B.jsonl.
"""Tests of Tsai's two-stage calibration on synthetic non-coplanar points."""

import math
import random

from cvgeom import add_noise, camera_matrix, make_K, project, rot_x, rot_y, rot_z
from cvla import det, eye, mul, norm, sub, transpose
from tsai_calibration_method import (calibrate, stage_one, stage_two_linear,
                                     tsai_project)

F, SX, KAPPA, CX, CY = 800.0, 1.02, 8e-7, 320.0, 240.0
R0 = mul(mul(rot_x(0.3), rot_y(-0.2)), rot_z(0.1))


def scene(t, n=40, seed=1, kappa1=KAPPA):
    rng = random.Random(seed)
    pts = [[rng.uniform(-1.0, 1.0) for _ in range(3)] for _ in range(n)]
    return pts, tsai_project(R0, t, F, SX, kappa1, CX, CY, pts)


def is_rotation(R, tol):
    return norm(sub(mul(transpose(R), R), eye(3))) <= tol and abs(det(R) - 1.0) <= tol


def test_forward_model_inverts_the_distortion():
    t = [0.2, 0.6, 5.0]
    pts, pix = scene(t)
    for X, (u, v) in zip(pts, pix):
        xc = [sum(R0[i][k] * X[k] for k in range(3)) + t[i] for i in range(3)]
        xd, yd = (u - CX) / SX, v - CY
        g = 1.0 + KAPPA * (xd * xd + yd * yd)
        assert abs(xd * g - F * xc[0] / xc[2]) <= 1e-9
        assert abs(yd * g - F * xc[1] / xc[2]) <= 1e-9


def test_no_distortion_matches_pinhole_reference():
    t = [0.2, 0.6, 5.0]
    pts, pix = scene(t, kappa1=0.0)
    P = camera_matrix(make_K(SX * F, F, CX, CY), R0, t)
    for X, p in zip(pts, pix):
        assert norm(sub(project(P, X), p)) <= 1e-9


def test_stage_one_exact_despite_distortion():
    for t in ([0.2, 0.6, 5.0], [-0.4, -0.6, 6.0], [0.3, 0.05, 4.0]):
        pts, pix = scene(t)
        R, tx, ty, sx = stage_one(pts, pix, CX, CY)
        assert is_rotation(R, 1e-12)
        assert norm(sub(R, R0)) <= 1e-8
        assert abs(tx - t[0]) <= 1e-8 and abs(ty - t[1]) <= 1e-8
        assert abs(sx - SX) <= 1e-8


def test_linear_stage_is_exact_without_distortion():
    t = [0.2, 0.6, 5.0]
    pts, pix = scene(t, kappa1=0.0)
    R, _, ty, _ = stage_one(pts, pix, CX, CY)
    f, tz = stage_two_linear(R, ty, pts, pix, CY)
    assert abs(f - F) <= 1e-8 * F and abs(tz - t[2]) <= 1e-8 * t[2]


def test_full_method_exact():
    for t in ([0.2, 0.6, 5.0], [-0.4, -0.6, 6.0]):
        pts, pix = scene(t)
        res = calibrate(pts, pix, CX, CY)
        assert abs(res["f"] - F) <= 1e-6 * F
        assert abs(res["t"][2] - t[2]) <= 1e-6 * t[2]
        assert abs(res["kappa1"] - KAPPA) <= 1e-6 * KAPPA
        assert norm(sub(res["t"], t)) <= 1e-6 * norm(t)
        # The linear stage alone is biased by the distortion.
        R, _, ty, _ = stage_one(pts, pix, CX, CY)
        f_lin, _ = stage_two_linear(R, ty, pts, pix, CY)
        assert abs(f_lin - F) > 1e-3 * F


def test_lm_cost_never_increases():
    rng = random.Random(4)
    pts, pix = scene([0.2, 0.6, 5.0])
    hist = calibrate(pts, add_noise(rng, pix, 0.3), CX, CY)["history"]
    assert len(hist) >= 3
    assert all(b <= a for a, b in zip(hist, hist[1:]))


def test_noise_sigma_01_sixty_points():
    # sigma = 0.1 pixel on 60 points; the worst of 5 seeds must pass.
    errs_f, errs_k, errs_r = [], [], []
    for seed in range(5):
        rng = random.Random(100 + seed)
        pts, pix = scene([0.2, 0.6, 5.0], n=60, seed=seed)
        res = calibrate(pts, add_noise(rng, pix, 0.1), CX, CY)
        assert is_rotation(res["R"], 1e-12)
        errs_f.append(abs(res["f"] - F) / F)
        errs_k.append(abs(res["kappa1"] - KAPPA) / KAPPA)
        errs_r.append(norm(sub(res["R"], R0)))
    assert max(errs_f) <= 0.005
    assert max(errs_k) <= 0.05
    assert max(errs_r) <= 0.005


def test_coplanar_points_raise():
    rng = random.Random(6)
    pts = [[rng.uniform(-1, 1), rng.uniform(-1, 1), 0.0] for _ in range(30)]
    pix = tsai_project(R0, [0.2, 0.6, 5.0], F, SX, KAPPA, CX, CY, pts)
    try:
        stage_one(pts, pix, CX, CY)
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_too_few_points_raise():
    pts, pix = scene([0.2, 0.6, 5.0], n=6)
    try:
        stage_one(pts, pix, CX, CY)
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_angle_of_recovered_rotation():
    pts, pix = scene([0.2, 0.6, 5.0])
    R, _, _, _ = stage_one(pts, pix, CX, CY)
    c = (sum(R[i][i] for i in range(3)) - 1.0) / 2.0
    c0 = (sum(R0[i][i] for i in range(3)) - 1.0) / 2.0
    assert abs(math.acos(c) - math.acos(c0)) <= 1e-8
