# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybrid-position-force-control/. The authors are listed in prov/YQZW8R.jsonl.

import math
import random

from hybrid_position_force_control import (
    TwoLinkArm,
    hybrid_control,
    inv2,
    matvec2,
    simulate,
    task_inertia,
    wall,
)

SF = [1.0, 0.0]
F_DES = [10.0, 0.0]
K_ENV = 1e5


def gains(kfi):
    return ([400.0, 400.0], [40.0, 40.0], [kfi, kfi], [600.0, 600.0])


def slide(t):
    return [0.0, 0.5 + 0.1 * math.sin(2 * t)], [0.0, 0.2 * math.cos(2 * t)], [0.0, -0.4 * math.sin(2 * t)]


def test_task_space_closed_loop():
    # x'' = S_p a_p + Lam^-1 (S_f F_f + F_ext) for any state and contact force.
    arm = TwoLinkArm()
    rng = random.Random(2)
    kp, kd, kfi, kv = gains(5.0)
    for _ in range(20):
        q = [rng.uniform(-2, 2), rng.uniform(0.3, 2.8)]
        qd = [rng.uniform(-2, 2) for _ in range(2)]
        xs, xds, xdds, fd, fm, fi, fe = ([rng.uniform(-1, 1) for _ in range(2)] for _ in range(7))
        tau = hybrid_control(arm, q, qd, xs, xds, xdds, fd, fm, fi, SF, (kp, kd, kfi, kv))
        qdd = arm.accel(q, qd, tau, fe)
        j = arm.jacobian(q)
        jq = arm.jdot_qdot(q, qd)
        xdd = [matvec2(j, qdd)[i] + jq[i] for i in range(2)]
        x, xd = arm.fk(q), matvec2(j, qd)
        ap = [xdds[i] + kd[i] * (xds[i] - xd[i]) + kp[i] * (xs[i] - x[i]) for i in range(2)]
        ff = [fd[i] + kfi[i] * fi[i] - kv[i] * xd[i] for i in range(2)]
        lam, _ = task_inertia(arm, q, qd)
        extra = matvec2(inv2(lam), [SF[i] * ff[i] + fe[i] for i in range(2)])
        for i in range(2):
            assert abs(xdd[i] - ((1 - SF[i]) * ap[i] + extra[i])) < 1e-9


def test_force_and_slide_with_exact_model():
    arm = TwoLinkArm()
    q0 = arm.ik([1.0, 0.5])
    out = simulate(arm, arm, wall(1.0, K_ENV), slide, F_DES, SF, gains(0.0), q0, 1e-3, 1500)
    for t, q, _, fa in out:
        err = arm.fk(q)[1] - slide(t)[0][1]
        # The y error is the critically damped response to the initial speed error 0.2.
        assert abs(err + 0.2 * t * math.exp(-20.0 * t)) < 1e-5
        if t >= 0.5:
            assert abs(fa[0] - F_DES[0]) < 1e-4
            assert abs(arm.fk(q)[0] - (1.0 + F_DES[0] / K_ENV)) < 1e-9


def test_integral_term_removes_force_offset_of_a_wrong_model():
    arm = TwoLinkArm()
    model = TwoLinkArm(m2=0.8)
    q0 = arm.ik([1.0, 0.5])

    def hold(t):
        return [0.0, 0.5], [0.0, 0.0], [0.0, 0.0]

    errs = []
    for kfi in (0.0, 20.0):
        out = simulate(arm, model, wall(1.0, K_ENV), hold, F_DES, SF, gains(kfi), q0, 2e-3, 1500)
        errs.append(abs(out[-1][3][0] - F_DES[0]))
    assert errs[0] > 0.05
    assert errs[1] < 1e-6
