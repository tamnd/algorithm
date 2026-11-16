# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/position-based-visual-servoing/. The authors are listed in prov/CP9B6Z.jsonl.

import math
import random

from position_based_visual_servoing import pbvs_step, simulate
from rbm import T_inv, eye, make_T, mul, norm, rot_z, so3_exp, so3_log

GOAL = make_T(eye(3), [0.0, 0.0, 1.0])  # target 1 m ahead of the desired camera


def rand_pose(rng, ang, dist):
    return make_T(so3_exp([rng.uniform(-ang, ang) for _ in range(3)]), [rng.uniform(-dist, dist) for _ in range(3)])


def error_pose(t_wc, t_wt):
    # The current camera in the desired camera frame: T_c*t T_ct^-1.
    return mul(GOAL, mul(T_inv(t_wt), t_wc))


def parts(t):
    return [row[:3] for row in t[:3]], [t[0][3], t[1][3], t[2][3]]


def test_first_twist_of_the_example():
    t0 = make_T(rot_z(math.pi / 2), [0.2, 0.1, -0.3])
    v = pbvs_step(mul(T_inv(t0), GOAL), GOAL, 1.0)
    want = [0.0, 0.0, -math.pi / 2, -0.1, 0.2, 0.3]
    assert max(abs(a - b) for a, b in zip(v, want)) < 1e-12


def test_rotation_decays_geometrically_about_a_fixed_axis():
    rng = random.Random(3)
    t_wt = rand_pose(rng, 1.0, 1.0)
    t_wc = mul(t_wt, mul(T_inv(GOAL), rand_pose(rng, 1.0, 0.3)))
    out = simulate(t_wc, t_wt, GOAL, 2.0, 0.01, 150)
    w0 = so3_log(parts(error_pose(out[0], t_wt))[0])
    for k, t in enumerate(out):
        w = so3_log(parts(error_pose(t, t_wt))[0])
        f = (1.0 - 2.0 * 0.01) ** k
        assert max(abs(a - f * b) for a, b in zip(w, w0)) < 1e-12


def test_camera_center_moves_on_a_straight_line():
    rng = random.Random(5)
    t_wt = rand_pose(rng, 1.0, 1.0)
    t_wc = mul(t_wt, mul(T_inv(GOAL), rand_pose(rng, 1.2, 0.4)))
    dt = 0.005
    out = simulate(t_wc, t_wt, GOAL, 1.0, dt, 600)
    p0 = parts(error_pose(out[0], t_wt))[1]
    for k, t in enumerate(out):
        p = parts(error_pose(t, t_wt))[1]
        assert norm([a - math.exp(-k * dt) * b for a, b in zip(p, p0)]) < 5e-3 * norm(p0)


def test_half_turn_about_the_optical_axis_is_a_pure_rotation():
    t0 = make_T(rot_z(math.pi), [0.0, 0.0, 0.0])
    out = simulate(t0, GOAL, GOAL, 1.0, 0.02, 400)
    for t in out:
        assert norm(parts(t)[1]) < 1e-12
    assert norm(so3_log(parts(out[-1])[0])) < 1e-3


def test_biased_pose_estimate_gives_a_wrong_final_pose():
    # The loop drives the estimate to the goal, so the true pose ends at
    # T_c*t B^-1 when the estimator returns T_ct B.
    bias = make_T(so3_exp([0.0, 0.02, 0.0]), [0.01, 0.0, 0.0])
    t0 = make_T(rot_z(math.pi / 2), [0.2, 0.1, -0.3])
    out = simulate(t0, GOAL, GOAL, 1.0, 0.02, 600, lambda t_ct: mul(t_ct, bias))
    want = mul(GOAL, mul(bias, T_inv(GOAL)))
    assert max(abs(out[-1][i][j] - want[i][j]) for i in range(3) for j in range(4)) < 1e-5
    assert norm(parts(out[-1])[1]) > 9e-3
