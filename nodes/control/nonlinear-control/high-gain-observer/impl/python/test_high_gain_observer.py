# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/high-gain-observer/. The authors are listed in prov/CY2X2T.jsonl.

import math
import random
from fractions import Fraction

import ctlsim
from high_gain_observer import observer_rhs, peak_bound_n2, saturate

# Simulations: classical RK4 (ctlsim) on the joint state (plant, observer),
# with the observer evaluated inside the right side. Steps: DT = 0.002 for
# eps >= 0.01 and DT_FAST = 0.0005 for eps down to 0.0025, so that
# DT / eps <= 0.2. Tolerances are stated at each check.
DT = 0.002
DT_FAST = 0.0005


def steps(T, dt):
    n = round(T / dt)
    assert abs(n * dt - T) < 1e-12
    return n


def vdp(t, x, u):
    return [x[1], -x[0] + (1 - x[0] ** 2) * x[1]]


def estimate_vdp(eps, T=4.0):
    # Van der Pol plant; the observer uses phi0 = 0 and alpha = (2, 1).
    def f(t, z, u):
        return vdp(t, z[:2], None) + observer_rhs(z[2:], z[0], None, eps, [2.0, 1.0], lambda xh, u: 0.0)

    ts, zs, us = ctlsim.simulate(f, [2.0, 0.0, 0.0, 0.0], 0.0, T, DT)
    assert len(us) == steps(T, DT)
    return ts, zs


def test_scaled_error_equation_exact():
    # eps eta' = A0 eta + eps B delta with eta_i = (x_i - xh_i) / eps^(n-i), exactly.
    rng = random.Random(11)
    for _ in range(150):
        n = rng.randint(1, 4)
        x = [Fraction(rng.randint(-20, 20), rng.randint(1, 6)) for _ in range(n)]
        xh = [Fraction(rng.randint(-20, 20), rng.randint(1, 6)) for _ in range(n)]
        eps = Fraction(1, rng.randint(2, 50))
        alpha = [Fraction(rng.randint(1, 9)) for _ in range(n)]
        u = Fraction(rng.randint(-5, 5))

        def phi(x, u):
            return x[0] * x[-1] - x[0] ** 3 + u

        def phi0(xh, u):
            return xh[0] * xh[-1] + u

        xdot = x[1:] + [phi(x, u)]
        xhdot = observer_rhs(xh, x[0], u, eps, alpha, phi0)
        eta = [(x[i] - xh[i]) / eps ** (n - 1 - i) for i in range(n)]
        etadot = [(xdot[i] - xhdot[i]) / eps ** (n - 1 - i) for i in range(n)]
        delta = phi(x, u) - phi0(xh, u)
        for i in range(n):
            a0eta = -alpha[i] * eta[0] + (eta[i + 1] if i + 1 < n else 0)
            assert eps * etadot[i] == a0eta + (eps * delta if i == n - 1 else 0)


def test_page_example_scaling():
    # late errors (t >= 2) and the peak of |e2|, measured:
    # eps = 0.04: 0.00742, 0.372, 18.46; 0.02: 0.00189, 0.189, 36.82; 0.01: 0.000475, 0.0950, 73.59
    expected = {0.04: (0.00742, 0.372, 18.46), 0.02: (0.00189, 0.189, 36.82), 0.01: (0.000475, 0.0950, 73.59)}
    for eps, (m1, m2, pk) in expected.items():
        ts, zs = estimate_vdp(eps)
        late = [z for t, z in zip(ts, zs) if t >= 2]
        e1 = max(abs(z[0] - z[2]) for z in late)
        e2 = max(abs(z[1] - z[3]) for z in late)
        peak = max(abs(z[1] - z[3]) for z in zs)
        assert abs(e1 - m1) < 0.01 * m1 and abs(e2 - m2) < 0.01 * m2 and abs(peak - pk) < 0.01 * pk
        # order eps^2 in x1, eps in x2, 1 / eps for the peak
        assert 4.5 < e1 / eps ** 2 < 4.8 and 9.2 < e2 / eps < 9.6 and 0.73 < peak * eps < 0.74
        # the linear part predicts the peak |e1(0)| / (e eps) within 0.4 percent
        assert abs(peak - peak_bound_n2(2.0, eps)) < 0.004 * peak


def test_table_eps_002():
    ts, zs = estimate_vdp(0.02)
    table = {0.02: (1.99961, -0.03882, 1.99981, 36.78373), 0.5: (1.83772, -0.53452, 1.83796, -0.51069), 2.0: (0.32332, -1.83297, 0.32407, -1.75703)}
    for t, row in table.items():
        z = zs[steps(t, DT)]
        assert all(abs(a - b) < 5e-6 for a, b in zip(z, row))


def test_peaking_closed_form():
    # delta = 0: plant x' = 0 at x = (2, 0); e2(t) = -(t / eps) exp(-t / eps) e1(0) / eps
    eps = 0.05

    def f(t, z, u):
        return [0.0, 0.0] + observer_rhs(z[2:], z[0], None, eps, [2.0, 1.0], lambda xh, u: 0.0)

    ts, zs, us = ctlsim.simulate(f, [2.0, 0.0, 0.0, 0.0], 0.0, 0.5, DT)
    assert len(us) == steps(0.5, DT)
    for t, z in zip(ts, zs):
        tau = t / eps
        # RK4 error with DT / eps = 0.04, against a peak of 14.7
        assert abs((z[1] - z[3]) - (-tau * math.exp(-tau) * 2.0 / eps)) < 1e-5


def output_feedback(eps, guard, T):
    # x1' = x2, x2' = x2^3 + u; state feedback u = -x2^3 - x1 - x2, with the
    # estimates of the observer (phi0 = xh2^3 + u). guard = None: no
    # saturation; guard = 1: u and the xh2 in phi0 are clipped to [-1, 1].
    def control(xh):
        v = -xh[1] ** 3 - xh[0] - xh[1]
        return v if guard is None else saturate(v, guard)

    def phi0(xh, u):
        v = xh[1] if guard is None else saturate(xh[1], guard)
        return v ** 3 + u

    def f(t, z, u):
        uu = control(z[2:])
        return [z[1], z[1] ** 3 + uu] + observer_rhs(z[2:], z[0], uu, eps, [2.0, 1.0], phi0)

    z = [0.1, 0.0, 0.0, 0.0]
    n = steps(T, DT_FAST)
    assert n <= 10000
    peak_x, peak_u = 0.0, 0.0
    for k in range(n):
        try:
            z = ctlsim.rk4_step(f, k * DT_FAST, z, None, DT_FAST)
        except OverflowError:
            return None, (k + 1) * DT_FAST, peak_u
        peak_x = max(peak_x, abs(z[0]), abs(z[1]))
        peak_u = max(peak_u, abs(control(z[2:])))
        if peak_x > 1e6:
            return None, (k + 1) * DT_FAST, peak_u
    return z, peak_x, peak_u


def test_peaking_without_saturation():
    # eps = 0.01: |x| reaches 0.758 and |u| 52; eps = 0.005: 3.08 and 393;
    # eps = 0.0025: the state escapes before t = 0.02.
    z, px, pu = output_feedback(0.005, None, 1.0)
    assert z is not None and 3.0 < px < 3.2 and 390 < pu < 400
    z, t_escape, pu = output_feedback(0.0025, None, 1.0)
    assert z is None and t_escape < 0.02


def test_saturation_recovers_state_feedback():
    # with the guard, |u| <= 1, the state never exceeds its initial size 0.1,
    # and at t = 5 it is within 0.01 of 0 (state feedback decays like e^(-t/2)).
    z, px, pu = output_feedback(0.0025, 1.0, 5.0)
    assert z is not None and px <= 0.1 + 1e-6 and pu <= 1.0
    assert max(abs(z[0]), abs(z[1])) < 0.01
    assert max(abs(z[0] - z[2]), abs(z[1] - z[3])) < 1e-3


def test_errors_and_exact_types():
    assert observer_rhs([0, 0], 1, None, 1, [2, 1], lambda xh, u: 0) == [2, 1]
    assert observer_rhs([0, 0], 1, None, Fraction(1, 2), [2, 1], lambda xh, u: 0) == [4, 4]
    assert saturate(-3, 1) == -1 and saturate(0.5, 1) == 0.5
    for bad in [lambda: observer_rhs([0.0], 1.0, None, 0.0, [1.0], lambda xh, u: 0.0), lambda: observer_rhs([0.0, 0.0], 1.0, None, 0.1, [1.0], lambda xh, u: 0.0)]:
        try:
            bad()
        except ValueError:
            continue
        raise AssertionError("no error")
