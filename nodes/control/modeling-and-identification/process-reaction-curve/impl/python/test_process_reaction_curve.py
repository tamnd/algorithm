# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/process-reaction-curve/. The authors are listed in prov/QACT9Z.jsonl.

import math
import random

from ctlsim import lti, simulate
from process_reaction_curve import fit_fopdt, fopdt_step


def _third_order(dt, t_end):
    # 1/(s+1)^3 as three first order lags in series, unit step at t = 0.
    a = [[-1.0, 0.0, 0.0], [1.0, -1.0, 0.0], [0.0, 1.0, -1.0]]
    b = [[1.0], [0.0], [0.0]]
    ts, xs, _ = simulate(lti(a, b), [0.0, 0.0, 0.0], 0.0, t_end, dt, control=lambda t, x: 1.0)
    return ts, [x[2] for x in xs]


def test_worked_example_third_order_lag():
    ts, y = _third_order(0.01, 20.0)
    k, dead, tau = fit_fopdt(ts, y, 1.0, "tangent")
    assert abs(k - 1.0) < 1e-5
    assert abs(dead - 0.805472) < 1e-3 and abs(tau - 3.694528) < 1e-3
    k, dead, tau = fit_fopdt(ts, y, 1.0, "two-point")
    assert abs(dead - 1.149590) < 1e-3 and abs(tau - 2.108662) < 1e-3


def test_coarse_table_of_the_page():
    ts = [0.5 * i for i in range(41)]
    y = [1 - math.exp(-t) * (1 + t + t * t / 2) for t in ts]
    _, dead, tau = fit_fopdt(ts, y, 1.0, "two-point")
    assert abs(dead - 1.1387) < 1e-4 and abs(tau - 2.1315) < 1e-4
    _, dead, tau = fit_fopdt(ts, y, 1.0, "tangent")
    assert abs(dead - 0.7832) < 1e-4 and abs(tau - 3.7633) < 1e-4


def test_random_fopdt_responses_are_recovered():
    # Oracle: the closed form FOPDT step response. The dead time is a sample
    # time, so the chord tangent gives L exactly and T = h / (1 - e^(-h/T)).
    rng = random.Random(42)
    for _ in range(500):
        k = rng.choice((-1, 1)) * rng.uniform(0.2, 5.0)
        tau = rng.uniform(0.5, 5.0)
        h = tau / 20
        dead = h * rng.randint(0, 40)
        du = rng.choice((-1, 1)) * rng.uniform(0.5, 2.0)
        y0 = rng.uniform(-3, 3)
        ts = [h * i for i in range(int((dead + 16 * tau) / h) + 1)]
        y = [y0 + du * fopdt_step(k, dead, tau, t) for t in ts]
        k2, l2, t2 = fit_fopdt(ts, y, du, "two-point")
        assert abs(k2 - k) < 1e-5 * abs(k)
        assert abs(l2 - dead) < 0.01 * tau and abs(t2 - tau) < 0.01 * tau
        k3, l3, t3 = fit_fopdt(ts, y, du, "tangent")
        assert abs(l3 - dead) < 1e-9 * (1 + dead)
        assert abs(t3 - h / (1 - math.exp(-h / tau))) < 1e-5 * tau


def test_negative_gain_and_offset():
    ts = [0.1 * i for i in range(301)]
    y = [2 + 0.5 * fopdt_step(-6, 1.0, 2.0, t) for t in ts]
    k, dead, tau = fit_fopdt(ts, y, 0.5, "two-point")
    assert abs(k + 6) < 1e-4 and abs(dead - 1.0) < 0.01 and abs(tau - 2.0) < 0.01


def test_no_dead_time():
    ts = [0.05 * i for i in range(400)]
    y = [fopdt_step(1.0, 0.0, 1.0, t) for t in ts]
    _, dead, _ = fit_fopdt(ts, y, 1.0, "tangent")
    assert abs(dead) < 1e-12


def test_bad_arguments():
    ts = [0.0, 1.0, 2.0, 3.0]
    y = [0.0, 0.5, 0.9, 1.0]
    for args in ((ts, y, 0.0), (ts, [0.0] * 4, 1.0), (ts[:2], y[:2], 1.0),
                 ([0.0, 2.0, 1.0, 3.0], y, 1.0), (ts, y, 1.0, "other")):
        try:
            fit_fopdt(*args)
        except ValueError:
            continue
        raise AssertionError("expected ValueError for %r" % (args,))
