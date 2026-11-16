# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/image-based-visual-servoing/. The authors are listed in prov/A4GWRN.jsonl.

import math
import random

from image_based_visual_servoing import features, ibvs_step, interaction_matrix, simulate
from rbm import eye, make_T, mul, norm, rot_x, rot_z, se3_exp, so3_exp, so3_log

SQUARE = [[-0.1, -0.1, 1.0], [0.1, -0.1, 1.0], [0.1, 0.1, 1.0], [-0.1, 0.1, 1.0]]


def pose_error(t):
    return norm(so3_log([row[:3] for row in t[:3]])), norm([t[0][3], t[1][3], t[2][3]])


def test_interaction_matrix_matches_finite_differences():
    rng = random.Random(7)
    h = 1e-6
    for _ in range(10):
        t = make_T(so3_exp([rng.uniform(-0.3, 0.3) for _ in range(3)]), [rng.uniform(-0.2, 0.2) for _ in range(3)])
        pts = [[rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3), rng.uniform(1.0, 2.0)] for _ in range(3)]
        s, depths = features(t, pts)
        lmat = interaction_matrix(s, depths)
        for j in range(6):
            d = [0.0] * 6
            d[j] = h
            sp = features(mul(t, se3_exp(d)), pts)[0]
            sm = features(mul(t, se3_exp([-x for x in d])), pts)[0]
            for i in range(len(s)):
                assert abs((sp[i] - sm[i]) / (2 * h) - lmat[i][j]) < 1e-6


def test_converges_to_the_goal_pose_with_each_matrix():
    s_star, z_star = features(eye(4), SQUARE)
    t0 = make_T(mul(rot_z(0.6), rot_x(0.1)), [0.05, -0.04, -0.3])
    for choice in ("current", "desired", "mean"):
        out = simulate(SQUARE, t0, s_star, 1.0, 0.05, 200, choice, z_star)
        errs = [o[2] for o in out]
        assert all(b <= a * (1 + 1e-9) for a, b in zip(errs, errs[1:]))
        ang, dist = pose_error(out[-1][0])
        assert ang < 1e-4 and dist < 1e-4


def test_quarter_turn_about_the_optical_axis():
    # With L at the current features the camera first moves back; with L at
    # the desired features it first moves forward. Both end at the goal.
    s_star, z_star = features(eye(4), SQUARE)
    t0 = make_T(rot_z(math.pi / 2), [0.0, 0.0, 0.0])
    s0, z0 = features(t0, SQUARE)
    v = ibvs_step(s0, s_star, z0, 1.0)
    assert max(abs(a - b) for a, b in zip(v, [0, 0, -1, 0, 0, -1])) < 1e-12
    extremes = []
    for choice in ("current", "desired"):
        out = simulate(SQUARE, t0, s_star, 1.0, 0.02, 500, choice, z_star)
        back = [-o[0][2][3] for o in out]
        extremes.append((max(back), min(back)))
        assert all(abs(o[0][0][3]) < 1e-12 and abs(o[0][1][3]) < 1e-12 for o in out)
        assert max(pose_error(out[-1][0])) < 1e-3
    assert extremes[0][0] > 0.4 and extremes[0][1] > -1e-12
    assert extremes[1][1] < -0.3 and extremes[1][0] < 1e-12


def test_half_turn_sends_the_camera_back_without_rotation():
    # At a rotation of pi, L^+ e is a pure backward translation, and the depth
    # follows Z <- Z + lam dt Z (1 + Z), which grows without bound.
    s_star, _ = features(eye(4), SQUARE)
    t0 = make_T(rot_z(math.pi), [0.0, 0.0, 0.0])
    out = simulate(SQUARE, t0, s_star, 1.0, 0.01, 60)
    z = 1.0
    for t, _, _ in out:
        depths = features(t, SQUARE)[1]
        assert abs(depths[0] - z) < 1e-12 * z
        assert max(abs(t[i][j] - t0[i][j]) for i in range(3) for j in range(3)) < 1e-12
        z += 0.01 * z * (1.0 + z)
    assert features(out[-1][0], SQUARE)[1][0] > 8.0
