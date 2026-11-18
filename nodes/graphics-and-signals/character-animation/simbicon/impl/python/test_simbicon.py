# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simbicon/. The authors are listed in prov/FMSJGE.jsonl.
"""Tests of the SIMBICON toy.

Exact checks: the stance hip rule makes the net hip torque on the torso equal
to the torso PD torque, the feedback law, and the order and timing of the
state machine. The dynamics are checked by energy in free flight. The walk
itself is measured: the number of foot strikes without a fall in this toy,
with and without the balance feedback.
"""

import math
import random

import simbicon as s


def energy(q, qd):
    d, dp = s._dirs(q)
    e = 0.0
    for m, inertia, own, terms in s.BODIES:
        x, y = s.point(q, terms, d)
        vx, vy = s.point_vel(q, qd, terms, dp)
        e += 0.5 * m * (vx * vx + vy * vy) + 0.5 * inertia * qd[own] ** 2 + m * s.G * y
    return e


def test_stance_hip_rule_gives_torso_torque():
    rng = random.Random(1)
    gait = s.make_gait()
    for _ in range(200):
        q = [rng.uniform(-1, 1), 0.9] + [rng.uniform(-0.3, 0.3) for _ in range(5)]
        qd = [rng.uniform(-0.5, 0.5) for _ in range(7)]
        state = rng.randrange(4)
        tau = s.control(state, q, qd, gait)
        if max(abs(t) for t in tau) >= s.TORQUE_LIMIT:
            continue
        Q = s.joint_torques_to_generalized(tau)
        want = s.pd(s.KP_JOINT, s.KD_JOINT, gait[state][3], q[s.TORSO], qd[s.TORSO])
        assert abs(Q[s.TORSO] - want) < 1e-9
        # the swing thigh gets the world frame PD torque
        th = s.LEGS[s.swing_side(state)][0]
        sh = s.LEGS[s.swing_side(state)][1]
        _, cd, cv, _, swh, _, _ = gait[state]
        d = q[0] - s.foot(q, s.stance_side(state))[0]
        target = swh + cd * d + cv * qd[0]
        tb = s.pd(s.KP_JOINT, s.KD_JOINT, target, q[th], qd[th])
        tk = tau[1] if s.swing_side(state) == "L" else tau[3]
        assert abs(Q[th] - (tb - tk)) < 1e-9
        assert abs(Q[sh] - tk) < 1e-9


def test_feedback_law():
    assert abs(s.balance_target(-0.70, 2.20, 0.0, 0.1, 1.0) - (-0.48)) < 1e-15
    assert abs(s.balance_target(0.40, 0.0, 0.20, 0.3, 1.5) - 0.70) < 1e-15


def test_free_flight_energy():
    q = [0.0, 3.0, 0.2, 0.3, -0.4, -0.2, 0.5]
    qd = [0.5, 1.0, 1.0, -2.0, 3.0, 1.5, -1.0]
    e0 = energy(q, qd)
    dt = 1e-4
    worst = 0.0
    for _ in range(3000):
        qdd = s.dynamics(q, qd, [0.0] * 7)
        qd = [a + dt * b for a, b in zip(qd, qdd)]
        q = [a + dt * b for a, b in zip(q, qd)]
        worst = max(worst, abs(energy(q, qd) - e0))
    assert worst / abs(e0) < 2e-4


def test_state_machine_order_and_timing():
    r = s.simulate(steps=2000)
    tr = r["transitions"]
    states = [st for _, st in tr]
    assert states[:8] == [0, 1, 2, 3, 0, 1, 2, 3]
    starts = [0.0] + [t for t, _ in tr]
    for (t, st), t0 in zip(tr, starts):
        if st in (0, 2):
            assert abs((t - t0) - 0.30) < 1.5e-3
    # contact states end at a foot strike
    assert len(r["strikes"]) == sum(1 for st in states if st in (1, 3))


def test_measured_walk_with_feedback():
    r = s.simulate(steps=5000)
    assert r["fell_at"] is None
    assert len(r["strikes"]) >= 12
    xs = [x for _, x in r["strikes"]]
    assert all(b > a for a, b in zip(xs, xs[1:]))
    assert 3.0 < r["distance"] < 9.0


def test_measured_fall_without_feedback():
    table = (
        (0.30, 0.0, 0.0, 0.0, 0.40, -1.10, -0.05),
        (None, 0.0, 0.0, 0.0, -0.70, -0.05, -0.10),
    )
    r = s.simulate(gait=s.make_gait(table), steps=5000)
    assert r["fell_at"] is not None
    assert len(r["strikes"]) < 5


def test_solver():
    rng = random.Random(3)
    A = [[rng.uniform(-1, 1) for _ in range(5)] for _ in range(5)]
    for i in range(5):
        A[i][i] += 3.0
    x = [rng.uniform(-1, 1) for _ in range(5)]
    b = [sum(A[i][k] * x[k] for k in range(5)) for i in range(5)]
    y = s.solve(A, b)
    assert all(math.isclose(a, c, abs_tol=1e-12) for a, c in zip(x, y))
