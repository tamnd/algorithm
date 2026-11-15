# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-mode-control/. The authors are listed in prov/WP3VZ0.jsonl.

import math
import random
from fractions import Fraction

import ctlsim
from sliding_mode_control import sat, sgn, sliding_variable, smc

# Simulations: classical RK4 (ctlsim) with step DT, the control computed at
# the start of each step and held over the step (a sampled controller).
# Tolerances are stated at each check.
DT = 0.002


def steps(T, dt=DT):
    n = round(T / dt)
    assert abs(n * dt - T) < 1e-12
    return n


def page_plant(t, x, u):
    # x1' = x2, x2' = u + d with d = 0.5 sin 2t, so D = 0.5.
    return [x[1], u + 0.5 * math.sin(2 * t)]


def page_control(phi=0):
    # s = x1 + x2, f_hat = 0, b = 1, k = 1.5 = D + eta with eta = 1.
    return lambda t, x: smc(x, [1.0], lambda x: 0.0, lambda x: 1.0, 1.5, phi)[0]


def run_page(dt, phi=0, T=6.0):
    n = steps(T, dt)
    ts, xs, us = ctlsim.simulate(page_plant, [1.0, 0.0], 0.0, T, dt, control=page_control(phi))
    assert len(ts) == n + 1
    ss = [x[0] + x[1] for x in xs]
    return ts, xs, us, ss


def test_helpers():
    assert [sgn(-2), sgn(0), sgn(Fraction(1, 3))] == [-1, 0, 1]
    assert [sat(-3), sat(Fraction(1, 2)), sat(7)] == [-1, Fraction(1, 2), 1]
    assert sliding_variable([2, 3], [1, -1, 4]) == 2 - 3 + 4


def test_sliding_derivative_exact():
    # s' = delta - k sigma(s) exactly, for random rational data, n = 1..4.
    rng = random.Random(7)
    for _ in range(200):
        n = rng.randint(1, 4)
        x = [Fraction(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(n)]
        c = [Fraction(rng.randint(1, 9), rng.randint(1, 3)) for _ in range(n - 1)]
        a = Fraction(rng.randint(-5, 5), 2)
        bconst = Fraction(rng.randint(1, 6), rng.randint(1, 4)) * rng.choice([-1, 1])
        delta = Fraction(rng.randint(-7, 7), 3)
        k = abs(delta) + 1
        phi = rng.choice([0, Fraction(1, 2)])

        def f_hat(x):
            return a * x[0] * x[-1] - x[0] ** 2

        def b(x):
            return bconst * (1 + x[0] ** 2)

        u, s = smc(x, c, f_hat, b, k, phi)
        assert s == sliding_variable(c, x)
        xdot_n = f_hat(x) + delta + b(x) * u
        xdot = x[1:] + [xdot_n]
        sdot = sum(c[i] * xdot[i] for i in range(n - 1)) + xdot[n - 1]
        sigma = sat(s / phi) if phi else sgn(s)
        assert sdot == delta - k * sigma
        if phi == 0 and s != 0:
            # reaching condition s s' <= -eta |s| with eta = k - |delta| = 1
            assert s * sdot <= -abs(s)


def test_page_example_reaching_and_band():
    ts, xs, us, ss = run_page(DT)
    assert len(us) == 3000
    # the table values on the page, to 5e-6
    table = {
        0.5: (0.85762, -0.49318, 0.364431),
        1.0: (0.56424, -0.56077, 0.003476),
        2.0: (0.20759, -0.21039, -0.002799),
        6.0: (0.00336, -0.00233, 0.001034),
    }
    for t, (a, b, s) in table.items():
        i = steps(t)
        assert abs(xs[i][0] - a) < 5e-6 and abs(xs[i][1] - b) < 5e-6 and abs(ss[i] - s) < 5e-6
    # reaching time: theorem bound |s(0)| / eta = 1; measured 0.858
    t_reach = next(t for t, s in zip(ts, ss) if s <= 0)
    assert t_reach <= 1.0
    assert abs(t_reach - 0.858) < 1e-9
    # after reaching, |s| <= (k + D) dt up to O(dt^2); measured 0.00399
    band = max(abs(s) for t, s in zip(ts, ss) if t >= t_reach)
    assert band <= 2.0 * DT * 1.01
    # the sampled law switches at almost every step (chattering)
    switches = sum(1 for i in range(1, len(us)) if 2 <= ts[i] < 3 and sgn(us[i] + xs[i][1]) != sgn(us[i - 1] + xs[i - 1][1]))
    assert switches > 300
    # on the surface x1' = -x1 + s, so x1 decays; measured x1(6) = 0.00336
    assert abs(xs[-1][0]) < 0.004


def test_band_halves_with_step():
    ts, xs, us, ss = run_page(0.001)
    t_reach = next(t for t, s in zip(ts, ss) if s <= 0)
    band = max(abs(s) for t, s in zip(ts, ss) if t >= t_reach)
    assert band <= 2.0 * 0.001 * 1.01
    assert band > 1.9 * 0.001


def test_boundary_layer():
    # with sat(s / phi) and phi = 0.05, |s| ends within phi D / k = 0.01667
    # (measured 0.01663) and u has no jumps
    ts, xs, us, ss = run_page(DT, phi=0.05)
    assert max(abs(s) for t, s in zip(ts, ss) if t >= 2) <= 0.05 * 0.5 / 1.5
    jumps = max(abs(us[i] - us[i - 1]) for i in range(1, len(us)))
    assert jumps < 0.1


def test_third_order_with_nonlinear_gain():
    # x''' = sin x1 + (2 + cos x1) u + 0.3 cos t, s = 2 x1 + 3 x2 + x3,
    # k = 1.3 = D + 1, so reaching takes at most |s(0)| = 2 (measured 1.764).
    def plant(t, x, u):
        return [x[1], x[2], math.sin(x[0]) + (2 + math.cos(x[0])) * u + 0.3 * math.cos(t)]

    def control(t, x):
        return smc(x, [2.0, 3.0], lambda x: math.sin(x[0]), lambda x: 2 + math.cos(x[0]), 1.3)[0]

    T = 10.0
    ts, xs, us = ctlsim.simulate(plant, [1.0, 0.0, 0.0], 0.0, T, DT, control=control)
    assert len(us) == steps(T) == 5000
    ss = [2 * x[0] + 3 * x[1] + x[2] for x in xs]
    t_reach = next(t for t, s in zip(ts, ss) if s <= 0)
    assert t_reach <= 2.0
    assert max(abs(s) for t, s in zip(ts, ss) if t >= t_reach) < 2.0 * 1.3 * DT
    # on s = 0 the reduced system has the poles -1 and -2
    assert max(abs(v) for v in xs[-1]) < 0.002


def test_errors():
    for bad in [
        lambda: smc([1.0, 0.0], [1.0], lambda x: 0.0, lambda x: 1.0, 0.0),
        lambda: smc([1.0, 0.0], [1.0], lambda x: 0.0, lambda x: 1.0, 1.0, -1.0),
        lambda: smc([1.0, 0.0], [1.0, 2.0], lambda x: 0.0, lambda x: 1.0, 1.0),
        lambda: smc([1.0, 0.0], [1.0], lambda x: 0.0, lambda x: 0.0, 1.0),
    ]:
        try:
            bad()
        except (ValueError, ZeroDivisionError):
            continue
        raise AssertionError("no error")
