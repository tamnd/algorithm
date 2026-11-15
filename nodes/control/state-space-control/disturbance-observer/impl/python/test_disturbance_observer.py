# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/disturbance-observer/. The authors are listed in prov/1HYDAN.jsonl.

import math
import random
from fractions import Fraction

import pytest

import ctlmat as cm
from ctlsim import simulate
from disturbance_observer import compensate, dob_filter, filter_output, filter_rhs, is_hurwitz, q_filter


def tf_of_realization(Af, Bf, Cf, Df, s):
    """Return the two transfer functions [y -> d_hat, u -> d_hat] at the complex point s."""
    n = len(Af)
    M = [[(s if i == j else 0) - Af[i][j] for j in range(n)] for i in range(n)]
    out = []
    for j in range(2):
        x = cm.solve([[complex(v) for v in r] for r in M], [complex(Bf[i][j]) for i in range(n)])
        out.append(sum(c * v for c, v in zip(Cf, x)) + Df[j])
    return out


def test_transfer_function_matches_formula():
    rng = random.Random(10)
    cases = [
        ([1], [Fraction(1, 100), 0], Fraction(1, 100), 1),  # 1 / (J s)
        ([1], [1, 2, 0], Fraction(1, 10), 2),  # 1 / (s^2 + 2 s), k = r
        ([1], [1, 2, 0], Fraction(1, 10), 3),  # k > r
        ([1, 3], [1, 4, 5, 2], Fraction(1, 5), 2),  # (s + 3) / (s^3 + 4 s^2 + 5 s + 2)
    ]
    for N, D, tau, k in cases:
        Af, Bf, Cf, Df = dob_filter(N, D, tau, k)
        den = cm.polymul(N, q_filter(tau, k))
        assert len(Af) == len(den) - 1
        assert Df[1] == 0  # no feedthrough from u
        for _ in range(5):
            s = complex(rng.uniform(-3, 3), rng.uniform(-3, 3))
            got = tf_of_realization(Af, Bf, Cf, Df, s)
            want_y = cm.polyval(D, s) / cm.polyval(den, s)
            want_u = -cm.polyval(N, s) / cm.polyval(den, s)
            assert abs(got[0] - want_y) < 1e-9 * (1 + abs(want_y))
            assert abs(got[1] - want_u) < 1e-9 * (1 + abs(want_u))


def test_feedthrough_from_y_only_when_k_equals_r():
    assert dob_filter([1], [1, 2, 0], 1, 2)[3][0] != 0
    assert dob_filter([1], [1, 2, 0], 1, 3)[3][0] == 0


def motor_run(J, Jn, tau, kp, load, t1, use_dob, k=1, t_on=0.05):
    """Speed loop for J w' = u + d with u_c = kp (r - w), r = 0, d = -load for t >= t_on."""
    Af, Bf, Cf, Df = dob_filter([1], [Jn, 0], tau, k)
    Af = [[float(v) for v in r] for r in Af]
    Bf = [[float(v) for v in r] for r in Bf]
    Cf = [float(v) for v in Cf]
    Df = [float(v) for v in Df]
    frhs = filter_rhs(Af, Bf)
    nf = len(Af)

    def d(t):
        return -load if t >= t_on else 0.0

    def control(w, xf):
        uc = kp * (0.0 - w)
        if not use_dob:
            return uc, 0.0
        dh = filter_output(Cf, Df, xf, w, 0.0)  # Df[1] = 0, so u is not needed
        return compensate(uc, dh), dh

    def f(t, s, _):
        w, xf = s[0], s[1:]
        u, _dh = control(w, xf)
        return [(u + d(t)) / J] + frhs(t, xf, (w, u))

    ts, ss, _ = simulate(f, [0.0] * (1 + nf), 0.0, t1, 0.0005)
    dhs = [control(s[0], s[1:])[1] for s in ss]
    return ts, [s[0] for s in ss], dhs


def test_estimate_is_filtered_disturbance_when_model_is_exact():
    tau, J = 0.01, 0.01
    # the load acts from t = 0, so no RK4 step crosses a jump of d
    ts, ws, dhs = motor_run(J, J, tau, 0.5, 0.1, 0.2, True, t_on=0.0)
    assert min(ws) < -1e-3  # the speed moves, so the estimate is not trivial
    for t, dh in zip(ts, dhs):
        want = -0.1 * (1 - math.exp(-t / tau))
        assert abs(dh - want) < 1e-7  # RK4 error with dt = tau / 20


def test_offset_removed():
    J, tau, kp, load = 0.01, 0.01, 0.5, 0.1
    _, ws, _ = motor_run(J, J, tau, kp, load, 1.0, False)
    assert abs(ws[-1] - (-load / kp)) < 1e-6  # offset 0.2 rad/s without the observer
    _, ws, _ = motor_run(J, J, tau, kp, load, 1.0, True)
    assert abs(ws[-1]) < 1e-6
    # the true inertia is twice the nominal one: still no offset
    _, ws, _ = motor_run(2 * J, J, tau, kp, load, 2.0, True)
    assert abs(ws[-1]) < 1e-6


def test_equivalent_to_pi_for_first_order_case():
    # DOB with P_n = 1 / (Jn s), Q = 1 / (tau s + 1) and u_c = -kp w is the PI
    # controller u = -(kp + Jn / tau) w - (kp / tau) * integral of w.
    J, Jn, tau, kp = 0.02, 0.01, 0.01, 0.5
    ts, ws, _ = motor_run(J, Jn, tau, kp, 0.1, 0.3, True, t_on=0.0)
    Kp, Ki = kp + Jn / tau, kp / tau

    def f(t, s, _):
        w, z = s
        return [(-Kp * w - Ki * z - 0.1) / J, w]

    _, ss, _ = simulate(f, [0.0, 0.0], 0.0, 0.3, 0.0005)
    assert max(abs(a - b[0]) for a, b in zip(ws, ss)) < 1e-9


def test_higher_order_plant_constant_disturbance():
    # P = P_n = 1 / (s^2 + 2 s), k = 2: d_hat = Q d, so d_hat tends to d.
    N, D, tau, k = [1], [1, 2, 0], 0.05, 2
    Af, Bf, Cf, Df = dob_filter(N, D, tau, k)
    Af = [[float(v) for v in r] for r in Af]
    Bf = [[float(v) for v in r] for r in Bf]
    frhs = filter_rhs(Af, Bf)

    def f(t, s, _):
        x1, x2, xf = s[0], s[1], s[2:]
        u = math.sin(3 * t)
        d = 0.7
        return [x2, -2 * x2 + u + d] + frhs(t, xf, (x1, u))

    ts, ss, _ = simulate(f, [0.0] * (2 + len(Af)), 0.0, 1.0, 0.001)
    s = ss[-1]
    dh = filter_output(Cf, [float(v) for v in Df], s[2:], s[0], math.sin(3 * ts[-1]))
    want = 0.7 * (1 - math.exp(-1.0 / tau) * (1 + 1.0 / tau))  # step response of 1 / (tau s + 1)^2
    assert abs(dh - want) < 1e-6


def test_is_hurwitz_against_roots():
    rng = random.Random(11)
    assert is_hurwitz([1, 2, 3, 4])  # 2 * 3 > 4
    assert not is_hurwitz([1, 1, 1, 1])  # roots -1 and +-i
    assert not is_hurwitz([1, 0, 1])
    assert is_hurwitz([5]) and is_hurwitz([-1, -3, -2])
    for _ in range(200):
        m = rng.randint(1, 5)
        roots = []
        while len(roots) < m:
            re = rng.choice([-3, -2, -1, 1, 2]) * rng.randint(1, 3)
            if len(roots) <= m - 2 and rng.random() < 0.5:
                im = rng.randint(1, 3)
                roots += [complex(re, im), complex(re, -im)]
            else:
                roots.append(complex(re, 0))
        p = [1]
        for z in roots:
            p = cm.polymul(p, [1, -z])
        p = [int(round(c.real)) for c in p]
        assert is_hurwitz(p) == all(z.real < 0 for z in roots)


def test_rejections():
    with pytest.raises(ValueError):
        dob_filter([1, 1, 1, 1], [1, 0, 0, 0, 0], 0.1, 1)  # N has the roots +-i
    with pytest.raises(ValueError):
        dob_filter([1], [1, 2, 0], 0.1, 1)  # k < relative degree
    with pytest.raises(ValueError):
        dob_filter([1], [1, 0], 0, 1)  # tau = 0
    with pytest.raises(ValueError):
        dob_filter([1, -1], [1, 2, 3], 0.1, 1)  # N has the root s = 1
    with pytest.raises(ValueError):
        dob_filter([1, 1], [1, 2], 0.1, 1)  # not strictly proper
