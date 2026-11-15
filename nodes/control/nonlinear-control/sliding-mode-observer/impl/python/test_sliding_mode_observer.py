# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-mode-observer/. The authors are listed in prov/V32494.jsonl.

import math

import ctlsim
from sliding_mode_observer import SlidingModeObserver, sgn

# The plant is integrated with classical RK4 (ctlsim) with step dt = h, the
# sampling period of the observer; the observer itself takes one explicit
# Euler step per sample, as a sampled implementation does. Tolerances are
# stated at each check.

G, FR = 9.81, 0.2


def F(t, x):
    # the unknown part: friction and an external torque, |F| <= 1.1 here
    return -FR * x[1] + 0.5 * math.sin(2 * t)


def pend(t, x, u):
    return [x[1], -G * math.sin(x[0]) + F(t, x)]


def steps(T, h):
    n = round(T / h)
    assert abs(n * h - T) < 1e-12
    return n


def run(h, T=5.0, lam=3.0, alpha=4.0):
    obs = SlidingModeObserver(lambda y, u: -G * math.sin(y), lam, alpha, h)
    est = [list(obs.xh)]
    inj = []

    def sample(t, x):
        est.append(obs.step(x[0]))
        inj.append(obs.injection)
        return None

    ts, xs, us = ctlsim.simulate(pend, [1.0, 0.0], 0.0, T, h, control=sample)
    assert len(us) == steps(T, h)
    e1 = [x[0] - e[0] for x, e in zip(xs, est)]
    e2 = [x[1] - e[1] for x, e in zip(xs, est)]
    return ts, xs, e1, e2, inj


def test_one_step_by_hand():
    obs = SlidingModeObserver(lambda y, u: -y, 2.0, 3.0, 0.5, xh0=(0.0, 1.0))
    # e = 4, v1 = 2 * 2 = 4, v2 = 3; xh1 = 0 + 0.5 (1 + 4), xh2 = 1 + 0.5 (-4 + 3)
    assert obs.step(4.0) == [2.5, 0.5]
    assert obs.injection == 3.0
    # e = 2.5 - 2.5 = 0: no injection
    assert obs.step(2.5) == [2.75, 0.5 + 0.5 * (-2.5)]
    assert obs.injection == 0.0


def test_gains_certified():
    # alpha > L + 2 L^2 / lam^2 with L = 2, a safe bound on |F| for this motion
    lam, alpha, L = 3.0, 4.0, 2.0
    assert alpha > L + 2 * L * L / (lam * lam)


def test_page_example():
    h = 0.002
    ts, xs, e1, e2, inj = run(h)
    assert max(abs(F(t, x)) for t, x in zip(ts, xs)) < 1.1
    table = {0.25: (0.289902, -0.919116), 0.5: (-0.058885, -0.780191), 1.0: (0.000009, -0.006787), 2.0: (-0.000003, 0.008478)}
    for t, (a, b) in table.items():
        i = steps(t, h)
        assert abs(e1[i] - a) < 5e-7 and abs(e2[i] - b) < 5e-7
    # |e2| < 0.05 for good from t = 0.774 (measured)
    i = steps(0.774, h)
    assert all(abs(v) < 0.05 for v in e2[i:]) and abs(e2[i - 1]) >= 0.05
    late = steps(3.0, h)
    assert max(abs(v) for v in e1[late:]) < 3e-5
    assert max(abs(v) for v in e2[late:]) < 0.025
    # equivalent output injection: the mean of alpha sgn(e) over windows of
    # 0.5 matches the mean of F within 0.079 (measured), below 2 max|e2| / 0.5
    w = steps(0.5, h)
    errs = []
    for i0 in range(late, len(inj) - w + 1, w):
        mean_inj = sum(inj[i0:i0 + w]) / w
        mean_F = sum(F(ts[i], xs[i]) for i in range(i0, i0 + w)) / w
        errs.append(abs(mean_inj - mean_F))
    assert len(errs) == 4 and max(errs) < 0.085


def test_accuracy_with_sampling_period():
    # halving h: e1 drops about 4 times (order h^2), e2 about 2 times (order h)
    h = 0.001
    ts, xs, e1, e2, inj = run(h)
    late = steps(3.0, h)
    m1 = max(abs(v) for v in e1[late:])
    m2 = max(abs(v) for v in e2[late:])
    assert m1 < 8e-6 and m2 < 0.012
    assert 2.5e-5 / m1 > 3 and 0.0207 / m2 > 1.7


def test_linear_observer_is_worse():
    # xh1' = xh2 + 20 e, xh2' = f0 + 100 e: the unknown F leaves an error of
    # 0.0057 in e1 and 0.12 in e2 (measured), more than 100 and 5 times the
    # sliding mode observer.
    h = 0.002
    xh = [0.0, 0.0]
    est = [list(xh)]

    def sample(t, x):
        e = x[0] - xh[0]
        xh[0], xh[1] = xh[0] + h * (xh[1] + 20.0 * e), xh[1] + h * (-G * math.sin(x[0]) + 100.0 * e)
        est.append(list(xh))
        return None

    ts, xs, us = ctlsim.simulate(pend, [1.0, 0.0], 0.0, 5.0, h, control=sample)
    late = steps(3.0, h)
    m1 = max(abs(x[0] - e[0]) for x, e in zip(xs[late:], est[late:]))
    m2 = max(abs(x[1] - e[1]) for x, e in zip(xs[late:], est[late:]))
    assert m1 > 100 * 2.6e-5 and m2 > 5 * 0.021


def test_errors_and_sign():
    assert [sgn(-0.1), sgn(0.0), sgn(3)] == [-1, 0, 1]
    for bad in [lambda: SlidingModeObserver(lambda y, u: 0.0, 0.0, 1.0, 0.1), lambda: SlidingModeObserver(lambda y, u: 0.0, 1.0, 1.0, 0.0)]:
        try:
            bad()
        except ValueError:
            continue
        raise AssertionError("no error")
