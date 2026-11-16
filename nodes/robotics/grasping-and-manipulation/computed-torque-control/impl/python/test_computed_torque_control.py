# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/computed-torque-control/. The authors are listed in prov/YZJ7AN.jsonl.

import math
import random

from computed_torque_control import TwoLinkArm, computed_torque, rk4_step, simulate, solve2


def traj(t):
    q = [0.5 * math.sin(t), 0.3 * math.cos(2 * t)]
    qd = [0.5 * math.cos(t), -0.6 * math.sin(2 * t)]
    qdd = [-0.5 * math.sin(t), -1.2 * math.cos(2 * t)]
    return q, qd, qdd


def test_mass_matrix_check_values():
    arm = TwoLinkArm()
    for q2, want in ((0.0, [[5, 2], [2, 1]]), (math.pi / 2, [[3, 1], [1, 1]])):
        m = arm.mass([0.3, q2])
        for i in range(2):
            for j in range(2):
                assert abs(m[i][j] - want[i][j]) < 1e-12


def test_model_conserves_energy_without_torque():
    # Independent check of M, C and g: with tau = 0 the energy is constant.
    arm = TwoLinkArm()
    x = [0.4, -0.7, 0.5, -0.2]
    e0 = arm.energy(x[:2], x[2:])
    for k in range(2000):
        x = rk4_step(lambda t, s: s[2:] + arm.accel(s[:2], s[2:], [0.0, 0.0]), k * 1e-3, x, 1e-3)
    assert abs(arm.energy(x[:2], x[2:]) - e0) < 1e-7


def test_skew_symmetry_of_model():
    arm = TwoLinkArm(m1=1.3, m2=0.7, l1=0.9, l2=0.6)
    rng = random.Random(7)
    for _ in range(20):
        q = [rng.uniform(-3, 3) for _ in range(2)]
        qd = [rng.uniform(-2, 2) for _ in range(2)]
        h = 1e-6
        mp = arm.mass([q[i] + h * qd[i] for i in range(2)])
        mm = arm.mass([q[i] - h * qd[i] for i in range(2)])
        mdot = [[(mp[i][j] - mm[i][j]) / (2 * h) for j in range(2)] for i in range(2)]
        c = arm.coriolis(q, qd)
        s = [[mdot[i][j] - 2 * c[i][j] for j in range(2)] for i in range(2)]
        for i in range(2):
            for j in range(2):
                assert abs(s[i][j] + s[j][i]) < 1e-6


def test_exact_model_gives_linear_error_dynamics():
    arm = TwoLinkArm()
    w = 5.0
    kp, kd = [w * w, w * w], [2 * w, 2 * w]
    qs, qds, _ = traj(0.0)
    e0 = [0.2, -0.1]
    ed0 = [-0.1, -0.3]
    q0 = [qs[i] - e0[i] for i in range(2)]
    qd0 = [qds[i] - ed0[i] for i in range(2)]
    out = simulate(arm, arm, traj, q0, qd0, kp, kd, 1e-3, 2000)
    for t, q, _ in out[::100]:
        want_q = traj(t)[0]
        for i in range(2):
            e_closed = (e0[i] + (ed0[i] + w * e0[i]) * t) * math.exp(-w * t)
            assert abs((want_q[i] - q[i]) - e_closed) < 1e-8


def test_wrong_model_leaves_the_predicted_offset():
    arm = TwoLinkArm(m2=1.5)
    model = TwoLinkArm(m2=1.0)
    kp, kd = [100.0, 100.0], [20.0, 20.0]
    goal = [0.3, 0.4]

    def hold(t):
        return goal, [0.0, 0.0], [0.0, 0.0]

    out = simulate(arm, model, hold, [0.0, 0.0], [0.0, 0.0], kp, kd, 2e-3, 3000)
    _, q, qd = out[-1]
    e = [goal[i] - q[i] for i in range(2)]
    assert max(abs(v) for v in qd) < 1e-6
    # At rest: g(q) = Mhat(q) Kp e + ghat(q), so Kp e = Mhat^(-1) (g - ghat).
    dg = [arm.gravity(q)[i] - model.gravity(q)[i] for i in range(2)]
    want = solve2(model.mass(q), dg)
    for i in range(2):
        assert abs(kp[i] * e[i] - want[i]) < 1e-6
    assert max(abs(v) for v in e) > 1e-2


def test_torque_matches_inverse_dynamics_when_on_track():
    # On the desired trajectory the law gives tau = M qd'' + C qd' + g.
    arm = TwoLinkArm()
    qs, qds, qdds = traj(0.7)
    tau = computed_torque(arm, qs, qds, qs, qds, qdds, [9.0, 9.0], [6.0, 6.0])
    acc = arm.accel(qs, qds, tau)
    for i in range(2):
        assert abs(acc[i] - qdds[i]) < 1e-12
