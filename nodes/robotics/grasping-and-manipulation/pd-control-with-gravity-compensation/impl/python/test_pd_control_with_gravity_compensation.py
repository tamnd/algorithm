# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pd-control-with-gravity-compensation/. The authors are listed in prov/0ACG13.jsonl.

import math
import random

from pd_control_with_gravity_compensation import (
    NoGravity,
    TwoLinkArm,
    lyapunov,
    pd_gravity,
    rk4_step,
    simulate,
)

KP = [100.0, 100.0]
KD = [20.0, 20.0]


def test_example_torque():
    arm = TwoLinkArm()
    tau = pd_gravity(arm, [0.0, 0.0], [0.0, 0.0], [0.3, 0.4], KP, KD)
    assert abs(tau[0] - 59.43) < 1e-9
    assert abs(tau[1] - 49.81) < 1e-9


def test_converges_from_random_states():
    arm = TwoLinkArm()
    rng = random.Random(11)
    for _ in range(3):
        goal = [rng.uniform(-2, 2), rng.uniform(-2, 2)]
        q0 = [rng.uniform(-3, 3), rng.uniform(-3, 3)]
        qd0 = [rng.uniform(-1, 1), rng.uniform(-1, 1)]
        _, q, qd = simulate(arm, arm, goal, q0, qd0, KP, KD, 4e-3, 2000)[-1]
        assert max(abs(goal[i] - q[i]) for i in range(2)) < 1e-4
        assert max(abs(v) for v in qd) < 1e-3


def test_lyapunov_function_never_increases():
    arm = TwoLinkArm(m1=1.2, m2=0.8)
    goal = [1.0, -0.5]
    out = simulate(arm, arm, goal, [-1.0, 1.5], [2.0, -1.0], KP, KD, 2e-3, 2000)
    vs = [lyapunov(arm, q, qd, goal, KP) for _, q, qd in out]
    for k in range(len(vs) - 1):
        assert vs[k + 1] <= vs[k] + 1e-9
    assert vs[-1] < 1e-3 * vs[0]


def test_lyapunov_derivative_formula():
    # V' = -q'^T Kd q' along the closed loop, checked by a central difference.
    arm = TwoLinkArm(m1=0.7, m2=1.4, l1=0.8, l2=1.1)
    goal = [0.2, 0.9]
    rng = random.Random(5)

    def f(t, x):
        tau = pd_gravity(arm, x[:2], x[2:], goal, KP, KD)
        return x[2:] + arm.accel(x[:2], x[2:], tau)

    for _ in range(10):
        x = [rng.uniform(-3, 3), rng.uniform(-3, 3), rng.uniform(-2, 2), rng.uniform(-2, 2)]
        h = 1e-5
        xp = rk4_step(f, 0.0, x, h)
        xm = rk4_step(f, 0.0, x, -h)
        dv = (lyapunov(arm, xp[:2], xp[2:], goal, KP) - lyapunov(arm, xm[:2], xm[2:], goal, KP)) / (2 * h)
        want = -sum(KD[i] * x[2 + i] ** 2 for i in range(2))
        assert abs(dv - want) < 1e-4 * (1 + abs(want))


def test_plain_pd_rests_where_spring_holds_gravity():
    arm = TwoLinkArm()
    goal = [0.3, 0.4]
    _, q, qd = simulate(arm, NoGravity(), goal, [0.0, 0.0], [0.0, 0.0], KP, KD, 5e-3, 3600)[-1]
    assert max(abs(v) for v in qd) < 1e-6
    g = arm.gravity(q)
    for i in range(2):
        assert abs(KP[i] * (goal[i] - q[i]) - g[i]) < 1e-6
    assert goal[0] - q[0] > 0.2


def test_wrong_gravity_model_offset():
    arm = TwoLinkArm(m2=1.5)
    model = TwoLinkArm(m2=1.0)
    goal = [0.3, 0.4]
    _, q, qd = simulate(arm, model, goal, [0.0, 0.0], [0.0, 0.0], KP, KD, 5e-3, 3600)[-1]
    assert max(abs(v) for v in qd) < 1e-6
    g, gh = arm.gravity(q), model.gravity(q)
    for i in range(2):
        assert abs(KP[i] * (goal[i] - q[i]) - (g[i] - gh[i])) < 1e-6
    assert math.hypot(goal[0] - q[0], goal[1] - q[1]) > 1e-2
