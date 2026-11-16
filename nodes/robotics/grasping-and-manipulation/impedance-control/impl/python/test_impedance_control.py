# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/impedance-control/. The authors are listed in prov/TVY2W5.jsonl.

import math
import random

from impedance_control import (
    TwoLinkArm,
    free_space,
    impedance_control,
    matvec2,
    simple_impedance,
    simulate,
    wall,
)

MD = [1.0, 1.0]
KD = [400.0, 400.0]
DD = [40.0, 40.0]  # critical damping: Dd = 2 sqrt(Kd Md)
K_ENV = 1e4
X_WALL = 1.0
X0 = [1.05, 0.5]


def test_kinematics_against_finite_differences():
    arm = TwoLinkArm(l1=0.9, l2=0.7)
    rng = random.Random(1)
    for _ in range(10):
        q = [rng.uniform(-3, 3) for _ in range(2)]
        qd = [rng.uniform(-2, 2) for _ in range(2)]
        h = 1e-6
        xp = arm.fk([q[i] + h * qd[i] for i in range(2)])
        xm = arm.fk([q[i] - h * qd[i] for i in range(2)])
        v = matvec2(arm.jacobian(q), qd)
        jp = matvec2(arm.jacobian([q[i] + h * qd[i] for i in range(2)]), qd)
        jm = matvec2(arm.jacobian([q[i] - h * qd[i] for i in range(2)]), qd)
        jq = arm.jdot_qdot(q, qd)
        for i in range(2):
            assert abs((xp[i] - xm[i]) / (2 * h) - v[i]) < 1e-7
            assert abs((jp[i] - jm[i]) / (2 * h) - jq[i]) < 1e-6
        x = arm.fk(arm.ik(arm.fk(q), 1.0 if math.sin(q[1]) > 0 else -1.0))
        assert max(abs(x[i] - arm.fk(q)[i]) for i in range(2)) < 1e-12


def test_closed_loop_is_the_target_impedance():
    # For any state and any contact force, Md x~'' + Dd x~' + Kd x~ = F_ext.
    arm = TwoLinkArm()
    rng = random.Random(4)
    for _ in range(20):
        q = [rng.uniform(-2, 2), rng.uniform(0.3, 2.8)]
        qd = [rng.uniform(-2, 2) for _ in range(2)]
        x0, x0d, x0dd, fe = ([rng.uniform(-1, 1) for _ in range(2)] for _ in range(4))
        tau = impedance_control(arm, q, qd, x0, x0d, x0dd, fe, MD, DD, KD)
        qdd = arm.accel(q, qd, tau, fe)
        j = arm.jacobian(q)
        x, xd = arm.fk(q), matvec2(j, qd)
        jq = arm.jdot_qdot(q, qd)
        xdd = [matvec2(j, qdd)[i] + jq[i] for i in range(2)]
        for i in range(2):
            lhs = MD[i] * (xdd[i] - x0dd[i]) + DD[i] * (xd[i] - x0d[i]) + KD[i] * (x[i] - x0[i])
            assert abs(lhs - fe[i]) < 1e-9


def test_free_space_error_matches_closed_form():
    arm = TwoLinkArm()
    w = 20.0

    def goal(t):
        return (
            [0.9 + 0.1 * math.sin(t), 0.5 + 0.1 * math.cos(t)],
            [0.1 * math.cos(t), -0.1 * math.sin(t)],
            [-0.1 * math.sin(t), -0.1 * math.cos(t)],
        )

    def law(t, q, qd, fe):
        x0, x0d, x0dd = goal(t)
        return impedance_control(arm, q, qd, x0, x0d, x0dd, fe, MD, DD, KD)

    q0 = arm.ik([0.85, 0.65])
    out = simulate(arm, law, free_space, q0, [0.0, 0.0], 1e-3, 1000)
    e0 = [arm.fk(q0)[i] - goal(0.0)[0][i] for i in range(2)]
    ed0 = [-goal(0.0)[1][i] for i in range(2)]
    for t, q, _ in out[::50]:
        x = arm.fk(q)
        for i in range(2):
            want = (e0[i] + (ed0[i] + w * e0[i]) * t) * math.exp(-w * t)
            assert abs((x[i] - goal(t)[0][i]) - want) < 1e-7


def test_contact_force_at_rest():
    arm = TwoLinkArm()
    env = wall(X_WALL, K_ENV)

    def law(t, q, qd, fe):
        return impedance_control(arm, q, qd, X0, [0.0, 0.0], [0.0, 0.0], fe, MD, DD, KD)

    out = simulate(arm, law, env, arm.ik([0.9, 0.5]), [0.0, 0.0], 1e-3, 1500)
    x = arm.fk(out[-1][1])
    force = env(x, None)
    want = K_ENV * KD[0] / (K_ENV + KD[0]) * (X0[0] - X_WALL)
    assert abs(-force[0] - want) < 1e-6
    assert abs(x[0] - (KD[0] * X0[0] + K_ENV * X_WALL) / (KD[0] + K_ENV)) < 1e-9
    # The impedances are decoupled: the y motion never sees the contact.
    assert max(abs(arm.fk(q)[1] - X0[1]) for _, q, _ in out) < 1e-9


def test_law_without_force_sensor():
    arm = TwoLinkArm()
    env = wall(X_WALL, K_ENV)

    def law(t, q, qd, fe):
        return simple_impedance(arm, q, qd, X0, DD, KD)

    out = simulate(arm, law, env, arm.ik([0.9, 0.5]), [0.0, 0.0], 1e-3, 2500)
    x = arm.fk(out[-1][1])
    want = K_ENV * KD[0] / (K_ENV + KD[0]) * (X0[0] - X_WALL)
    assert abs(-env(x, None)[0] - want) < 1e-4
    assert abs(x[1] - X0[1]) < 1e-6
    # Without inertia shaping the arm's own mass couples x and y on the way.
    assert max(abs(arm.fk(q)[1] - X0[1]) for _, q, _ in out) > 1e-4
