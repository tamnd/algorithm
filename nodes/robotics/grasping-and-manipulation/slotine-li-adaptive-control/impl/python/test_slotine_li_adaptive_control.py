# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slotine-li-adaptive-control/. The authors are listed in prov/RN7MPK.jsonl.

import math
import random

from slotine_li_adaptive_control import (
    TwoLinkArm,
    closed_loop,
    lyapunov,
    regressor,
    rk4_step,
    simulate,
    slotine_li,
)

LAM = [5.0, 5.0]
KD = [20.0, 20.0]
GAMMA = [1.0, 1.0, 1.0, 20.0, 20.0]


def traj(t):
    q = [0.5 * math.sin(t), 0.3 * math.cos(2 * t)]
    qd = [0.5 * math.cos(t), -0.6 * math.sin(2 * t)]
    qdd = [-0.5 * math.sin(t), -1.2 * math.cos(2 * t)]
    return q, qd, qdd


def test_regressor_matches_model():
    rng = random.Random(3)
    for _ in range(20):
        arm = TwoLinkArm(*[rng.uniform(0.5, 2.0) for _ in range(4)])
        q, qd, v, a = ([rng.uniform(-3, 3) for _ in range(2)] for _ in range(4))
        y = regressor(q, qd, v, a)
        pi = arm.params()
        m, c, g = arm.mass(q), arm.coriolis(q, qd), arm.gravity(q)
        for i in range(2):
            want = sum(m[i][j] * a[j] + c[i][j] * v[j] for j in range(2)) + g[i]
            assert abs(sum(y[i][k] * pi[k] for k in range(5)) - want) < 1e-12


def test_tracking_with_wrong_parameters_and_energy_balance():
    arm = TwoLinkArm()
    pi0 = [0.5 * p for p in arm.params()]
    dt = 4e-3
    out = simulate(arm, traj, [0.2, 0.1], [0.0, 0.0], pi0, LAM, KD, GAMMA, dt, 2500)
    vs, ws = [], []
    for t, q, qd, ph in out:
        qs, qds, _ = traj(t)
        vs.append(lyapunov(arm, q, qd, qs, qds, ph, LAM, GAMMA))
        s = [qd[i] - qds[i] + LAM[i] * (q[i] - qs[i]) for i in range(2)]
        ws.append(sum(KD[i] * s[i] ** 2 for i in range(2)))
    for k in range(len(vs) - 1):
        assert vs[k + 1] <= vs[k] + 1e-9
    # V(0) - V(T) equals the integral of s^T Kd s (Simpson's rule).
    inner = sum((4 if k % 2 else 2) * ws[k] for k in range(1, len(ws) - 1))
    dissipated = dt / 3 * (ws[0] + inner + ws[-1])
    assert abs((vs[0] - vs[-1]) - dissipated) < 1e-3
    t, q, _, _ = out[-1]
    qs = traj(t)[0]
    assert max(abs(q[i] - qs[i]) for i in range(2)) < 0.02


def test_lyapunov_derivative_formula():
    arm = TwoLinkArm(m1=0.8, m2=1.3, l1=1.1, l2=0.7)
    f = closed_loop(arm, traj, LAM, KD, GAMMA)
    rng = random.Random(9)
    for _ in range(10):
        t = rng.uniform(0, 5)
        x = [rng.uniform(-2, 2) for _ in range(4)] + [p * rng.uniform(0.3, 1.7) for p in arm.params()]
        h = 1e-5
        xp, xm = rk4_step(f, t, x, h), rk4_step(f, t, x, -h)

        def v(y, tt):
            qs, qds, _ = traj(tt)
            return lyapunov(arm, y[:2], y[2:4], qs, qds, y[4:], LAM, GAMMA)

        dv = (v(xp, t + h) - v(xm, t - h)) / (2 * h)
        qs, qds, _ = traj(t)
        s = [x[2 + i] - qds[i] + LAM[i] * (x[i] - qs[i]) for i in range(2)]
        want = -sum(KD[i] * s[i] ** 2 for i in range(2))
        assert abs(dv - want) < 1e-4 * (1 + abs(want))


def test_exact_parameters_on_the_sliding_surface():
    # With pi_hat = pi, Gamma = 0 and s(0) = 0, s stays 0 and q~ = q~(0) e^(-lambda t).
    arm = TwoLinkArm()
    qs, qds, _ = traj(0.0)
    qt0 = [0.1, -0.2]
    q0 = [qs[i] + qt0[i] for i in range(2)]
    qd0 = [qds[i] - LAM[i] * qt0[i] for i in range(2)]
    out = simulate(arm, traj, q0, qd0, arm.params(), LAM, KD, [0.0] * 5, 2e-3, 1000)
    for t, q, _, _ in out[::100]:
        qs = traj(t)[0]
        for i in range(2):
            assert abs((q[i] - qs[i]) - qt0[i] * math.exp(-LAM[i] * t)) < 1e-9


def test_set_point_does_not_identify_the_parameters():
    arm = TwoLinkArm()
    goal = [0.4, 0.6]

    def hold(t):
        return goal, [0.0, 0.0], [0.0, 0.0]

    pi0 = [0.5 * p for p in arm.params()]
    out = simulate(arm, hold, [0.0, 0.0], [0.0, 0.0], pi0, LAM, KD, GAMMA, 6e-3, 2500)
    _, q, qd, ph = out[-1]
    assert max(abs(goal[i] - q[i]) for i in range(2)) < 1e-3
    # The inertial parameters a1, a2, a3 stop changing far from the truth.
    pi = arm.params()
    assert abs(ph[1] - pi[1]) > 1.0
    _, _, _, ph_mid = out[1250]
    assert max(abs(ph[k] - ph_mid[k]) for k in range(3)) < 1e-2
    tau, _ = slotine_li(q, qd, goal, [0.0, 0.0], [0.0, 0.0], ph, LAM, KD, GAMMA)
    assert all(math.isfinite(v) for v in tau)
