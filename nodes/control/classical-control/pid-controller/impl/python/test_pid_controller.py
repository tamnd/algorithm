# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pid-controller/. The authors are listed in prov/M0FN5Q.jsonl.

import cmath
import math
import random
from fractions import Fraction as Fr

import pytest

from ctlmat import polyval
from ctlsim import simulate
from pid_controller import (PID, ideal_to_parallel, ideal_to_series,
                            parallel_to_ideal, pid_frequency_response,
                            series_to_ideal)

# Plant P(s) = 1/(s + 1)^3 as a chain of three first order lags, y = x3.
# Simulation: RK4 with dt = 0.01 s, zero-order hold over h. Tolerances are
# given at each assert.

TU = 2 * math.pi / math.sqrt(3)   # ultimate period of 1/(s + 1)^3
ZN = dict(K=4.8, Ti=TU / 2, Td=TU / 8, N=10)


def plant(t, x, u):
    return [-x[0] + u, -x[1] + x[0], -x[2] + x[1]]


def run(pid, t1, h, dt=0.01, r=lambda t: 1.0, load=lambda t: 0.0):
    n = round(t1 / dt)
    assert abs(n * dt - t1) < 1e-9 and abs(round(h / dt) * dt - h) < 1e-12

    def ctl(t, x):
        return pid.step(r(t), x[2]) + load(t)

    ts, xs, us = simulate(plant, [0.0, 0.0, 0.0], 0.0, t1, dt, control=ctl, hold=h)
    assert len(ts) == n + 1
    return ts, [x[2] for x in xs], us


def test_integral_and_proportional_terms_are_exact():
    K, Ti, h = Fr(3, 2), Fr(5, 2), Fr(1, 10)
    pid = PID(K, Ti=Ti, Td=0, h=h, b=Fr(1, 2))
    r, y = Fr(2), Fr(1, 3)
    for k in range(25):
        u = pid.step(r, y)
        assert u == K * (Fr(1, 2) * r - y) + k * K * h / Ti * (r - y)


def test_derivative_filter_is_exact_on_a_ramp():
    # y_k = k h, r = 0: D_k = -K Td (1 - a_d^k) with a_d = Td/(Td + N h).
    K, Td, N, h = Fr(2), Fr(1, 2), Fr(5), Fr(1, 20)
    pid = PID(K, Ti=None, Td=Td, N=N, h=h, b=0)
    ad = Td / (Td + N * h)
    for k in range(30):
        u = pid.step(0, k * h)
        assert u == -K * k * h - K * Td * (1 - ad ** k)
    assert ad == Fr(2, 3)


def test_no_derivative_kick_with_c_zero():
    pid0 = PID(1.0, Ti=None, Td=1.0, N=10, h=0.1, c=0)
    pid1 = PID(1.0, Ti=None, Td=1.0, N=10, h=0.1, c=1)
    for p in (pid0, pid1):
        p.step(0.0, 0.0)
    u0, u1 = pid0.step(1.0, 0.0), pid1.step(1.0, 0.0)
    assert u0 == 1.0
    # c = 1: the kick is bd = K Td N/(Td + N h) = 5 on top of K r = 1
    assert abs(u1 - 6.0) < 1e-12


def test_closed_loop_step_has_zero_steady_state_error():
    ts, ys, us = run(PID(h=0.05, b=1, **ZN), t1=60.0, h=0.05)
    assert abs(ys[-1] - 1.0) < 1e-8
    over = max(ys) - 1.0
    assert 0.50 < over < 0.60          # measured 0.5503 with h = 0.05, N = 10
    assert abs(us[-1] - 1.0) < 1e-7    # P(0) = 1, so u tends to r


def test_set_point_weight_changes_only_the_set_point_response():
    load = lambda t: -0.5 if t >= 30.0 else 0.0
    ys_by_b = {}
    for b in (0.0, 0.5, 1.0):
        _, y_load, _ = run(PID(h=0.05, b=b, **ZN), t1=60.0, h=0.05, load=load)
        _, y_free, _ = run(PID(h=0.05, b=b, **ZN), t1=60.0, h=0.05)
        ys_by_b[b] = (y_load, y_free)
    base = [a - f for a, f in zip(*ys_by_b[1.0])]
    for b in (0.0, 0.5):
        diff = [a - f for a, f in zip(*ys_by_b[b])]
        assert max(abs(p - q) for p, q in zip(diff, base)) < 1e-12
    over = {b: max(ys_by_b[b][1]) - 1.0 for b in ys_by_b}
    assert over[0.0] < over[0.5] < over[1.0]
    assert over[0.0] < 0.05            # measured 0.0377


def continuous_pid_error(h, t1=20.0, dt=0.005):
    """Max |y_h(t_k) - y(t_k)| over the sampling instants, against the
    continuous PID (states x1, x2, x3, I, xf), both with RK4 and step dt."""
    K, Ti, Td, N = ZN["K"], ZN["Ti"], ZN["Td"], ZN["N"]

    def f(t, x, _):
        y = x[2]
        e = 1.0 - y
        u = K * (1.0 - y) + x[3] - K * N * (y - x[4])
        return [-x[0] + u, -x[1] + x[0], -x[2] + x[1], K / Ti * e, N / Td * (y - x[4])]

    _, xs, _ = simulate(f, [0.0] * 5, 0.0, t1, dt)
    pid = PID(h=h, b=1, **ZN)
    _, xs_h, _ = simulate(plant, [0.0] * 3, 0.0, t1, dt,
                          control=lambda t, x: pid.step(1.0, x[2]), hold=h)
    r = round(h / dt)
    return max(abs(xs[k][2] - xs_h[k][2]) for k in range(0, len(xs), r))


def test_sampled_pid_converges_to_the_continuous_pid():
    errs = [continuous_pid_error(h) for h in (0.08, 0.04, 0.02)]
    # first order in h: each halving should cut the error by about 2
    assert errs[1] < 0.65 * errs[0] and errs[2] < 0.65 * errs[1]
    assert errs[2] < 0.05


def test_back_calculation_reduces_overshoot_under_saturation():
    lim = dict(umin=-2.0, umax=2.0)
    _, y_sat, u_sat = run(PID(h=0.05, b=1, **ZN, **lim), t1=40.0, h=0.05)
    tt = math.sqrt(ZN["Ti"] * ZN["Td"])
    _, y_aw, u_aw = run(PID(h=0.05, b=1, Tt=tt, **ZN, **lim), t1=40.0, h=0.05)
    assert max(u_sat) == 2.0 and max(u_aw) == 2.0
    assert min(u_sat) >= -2.0 and min(u_aw) >= -2.0
    assert max(y_sat) - 1.0 > 0.5      # measured 0.569
    assert max(y_aw) - 1.0 < 0.2       # measured 0.162
    assert abs(y_aw[-1] - 1.0) < 1e-6


def test_back_calculation_fixed_point_under_saturation():
    # With e and u held, I converges to the value where
    # K h e / Ti + (h / Tt)(u - v) = 0, that is v = umax + Tt K e / Ti.
    K, Ti, Tt, h = 2.0, 4.0, 0.5, 0.01
    pid = PID(K, Ti=Ti, Td=0, h=h, Tt=Tt, umax=1.0)
    for _ in range(3000):
        u = pid.step(3.0, 0.0)
        v = K * 3.0 + pid.I
    assert u == 1.0
    assert abs(v - (1.0 + Tt * K * 3.0 / Ti)) < 1e-9


def test_form_conversions():
    rng = random.Random(7)
    for _ in range(200):
        Ks = Fr(rng.randint(1, 50), rng.randint(1, 9))
        Tis = Fr(rng.randint(1, 50), rng.randint(1, 9))
        Tds = Fr(rng.randint(1, 50), rng.randint(1, 9))
        K, Ti, Td = series_to_ideal(Ks, Tis, Tds)
        assert Ti >= 4 * Td
        assert parallel_to_ideal(*ideal_to_parallel(K, Ti, Td)) == (K, Ti, Td)
        k2, ti2, td2 = ideal_to_series(K, Ti, Td)
        # the series form is unique up to swapping Tis and Tds with
        # the matching gain; ideal_to_series returns Tis >= Tds
        hi, lo = max(Tis, Tds), min(Tis, Tds)
        assert abs(ti2 - hi) < 1e-9 * hi and abs(td2 - lo) < 1e-9 * hi
        s = 0.3j + 0.1
        c_ser = complex(Ks) * (1 + 1 / (complex(Tis) * s)) * (1 + complex(Tds) * s)
        c_id = complex(K) * (1 + 1 / (complex(Ti) * s) + complex(Td) * s)
        assert abs(c_ser - c_id) < 1e-9 * abs(c_id)
    with pytest.raises(ValueError):
        ideal_to_series(1.0, 1.0, 0.3)


def test_margins_of_the_ziegler_nichols_loop():
    # Ideal derivative: phase margin 30.62 degrees at 1.37545 rad/s.
    def loop(w, N):
        p = 1 / polyval([1, 3, 3, 1], 1j * w)
        return p * pid_frequency_response(ZN["K"], ZN["Ti"], ZN["Td"], N, w)

    for N, w_want, pm_want in ((None, 1.37545, 30.619), (10, 1.40479, 29.428)):
        lo, hi = 0.5, 3.0
        for _ in range(80):
            mid = (lo + hi) / 2
            if abs(loop(mid, N)) > 1:
                lo = mid
            else:
                hi = mid
        pm = 180 + math.degrees(cmath.phase(loop(lo, N)))
        assert abs(lo - w_want) < 1e-5 and abs(pm - pm_want) < 1e-3
