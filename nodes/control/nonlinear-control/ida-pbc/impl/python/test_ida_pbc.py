# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ida-pbc/. The authors are listed in prov/ST8SKY.jsonl.

import math
import random
from fractions import Fraction

import ctlsim
from ida_pbc import MatchingError, matching_control

# Magnetic levitation, x = (lambda, theta, p): flux, position, momentum, with
# k = m = 1, g0 = 2, r = 1, target theta* = 1/2, lambda* = 2. Design alpha = 2,
# b = 1, r_d = 2. Exact checks use Fraction. The simulation uses classical RK4
# (ctlsim) with step DT = 0.01, with the feedback evaluated inside the right
# side. Tolerances are stated at each check.
K, M, G0, RES = Fraction(1), Fraction(1), Fraction(2), Fraction(1)
ALPHA, BW, RD = Fraction(2), Fraction(1), Fraction(2)
LAM_S, TH_S = Fraction(2), Fraction(1, 2)
ZS = TH_S + Fraction(LAM_S, ALPHA)
DT = 0.01


def steps(T, dt):
    n = round(T / dt)
    assert abs(n * dt - T) < 1e-12
    return n


def grad_h(x):
    lam, th, p = x
    # H = (1 - theta) lambda^2 / (2k) + p^2 / (2m) + m g0 theta
    return [(1 - th) * lam / K, -lam * lam / (2 * K) + M * G0, p / M]


JR = [[-RES, 0, 0], [0, 0, 1], [0, -1, 0]]
G = [[1], [0], [0]]


def jrd(alpha=ALPHA):
    return [[-RD, 0, -alpha], [0, 0, 1], [alpha, -1, 0]]


def h_d(x):
    lam, th, p = x
    return p * p / (2 * M) + lam ** 3 / (6 * K * ALPHA) - M * G0 * lam / ALPHA + BW * (th + lam / ALPHA - ZS) ** 2 / 2


def grad_hd(x):
    lam, th, p = x
    s = th + lam / ALPHA - ZS
    return [lam * lam / (2 * K * ALPHA) - M * G0 / ALPHA + BW * s / ALPHA, BW * s, p / M]


def control(x):
    # closed form of the matching solution: u = r (1 - theta) lambda / k - alpha p / m - r_d H_d,lambda
    lam, th, p = x
    return RES * (1 - th) * lam / K - ALPHA * p / M - RD * grad_hd(x)[0]


def plant(x, u):
    a = [sum(r * v for r, v in zip(row, grad_h(x))) for row in JR]
    return [a[0] + u, a[1], a[2]]


def rand_point(rng):
    return [Fraction(rng.randint(1, 60), rng.randint(1, 20)), Fraction(rng.randint(-20, 19), 20), Fraction(rng.randint(-30, 30), rng.randint(1, 9))]


def test_matching_exact():
    rng = random.Random(1)
    for _ in range(150):
        x = rand_point(rng)
        u = matching_control(JR, grad_h(x), G, jrd(), grad_hd(x))
        assert u == [control(x)]
        target = [sum(r * v for r, v in zip(row, grad_hd(x))) for row in jrd()]
        assert plant(x, u[0]) == target


def test_energy_decay_exact():
    # dH_d/dt = grad H_d^T (J_d - R_d) grad H_d = -r_d (H_d,lambda)^2
    rng = random.Random(2)
    for _ in range(150):
        x = rand_point(rng)
        gd = grad_hd(x)
        xdot = plant(x, control(x))
        assert sum(a * b for a, b in zip(gd, xdot)) == -RD * gd[0] ** 2


def test_target_is_strict_minimum_exact():
    xs = [LAM_S, TH_S, 0]
    assert grad_hd(xs) == [0, 0, 0] and control(xs) == 1 and plant(xs, 1) == [0, 0, 0]
    # potential part V(lambda, theta): Hessian [[lam/(k a) + b/a^2, b/a], [b/a, b]], det = b lam / (k a) > 0
    rng = random.Random(4)
    for _ in range(50):
        lam = Fraction(rng.randint(1, 100), rng.randint(1, 10))
        hll, hlt, htt = lam / (K * ALPHA) + Fraction(BW, ALPHA ** 2), Fraction(BW, ALPHA), BW
        assert htt > 0 and hll * htt - hlt * hlt == BW * lam / (K * ALPHA)
    # margin to the boundary lambda = 0: V(0, theta) >= 0 and V* = -2 m g0 lambda* / (3 alpha) = -4/3
    assert h_d(xs) == Fraction(-4, 3) == Fraction(-2 * M * G0 * LAM_S, 3 * ALPHA)


def test_lasalle_step_exact():
    # on H_d,lambda = 0 the closed loop gives d/dt H_d,lambda = -lambda p / (k m),
    # so H_d,lambda = 0 for all time forces p = 0 when lambda > 0
    rng = random.Random(6)
    for _ in range(100):
        lam = Fraction(rng.randint(1, 60), rng.randint(1, 20))
        p = Fraction(rng.randint(-30, 30), rng.randint(1, 9))
        th = ZS - lam / ALPHA - Fraction(ALPHA, BW) * (lam * lam / (2 * K * ALPHA) - Fraction(M * G0, ALPHA))
        x = [lam, th, p]
        assert grad_hd(x)[0] == 0
        lamd, thd, pd = plant(x, control(x))
        dhl = (lam / (K * ALPHA) + Fraction(BW, ALPHA ** 2)) * lamd + Fraction(BW, ALPHA) * thd
        assert dhl == -lam * p / (K * M)


def test_page_simulation():
    def f(t, x, u):
        return plant(x, control(x))

    T = 10.0
    ts, xs, us = ctlsim.simulate(f, [2.0, 0.3, 0.0], 0.0, T, DT)
    assert len(us) == steps(T, DT)
    hs = float(h_d([LAM_S, TH_S, 0]))
    # rows: lambda, theta, p, u within 5e-5, and H_d - H_d* within 1 percent
    table = {0.5: (2.04738, 0.30602, 0.03189, 1.43149, 1.614e-2), 1: (2.03087, 0.33331, 0.07436, 1.29427, 1.468e-2), 2: (1.97975, 0.41852, 0.07840, 1.12631, 7.474e-3), 4: (1.99471, 0.48943, 0.00642, 1.02937, 1.219e-4), 10: (1.99998, 0.49982, 0.00011, 1.00035, 2.427e-8)}
    hd = [h_d(x) - hs for x in xs]
    for t, row in table.items():
        i = steps(t, DT)
        x = xs[i]
        assert all(abs(a - b) < 5e-5 for a, b in zip(list(x) + [control(x)], row[:4]))
        assert abs(hd[i] - row[4]) < 0.01 * row[4]
    assert abs(hd[0] - 0.02) < 1e-12
    # H_d never increases (up to 1e-9 of RK4 error), and the energy balance
    # H_d(T) - H_d(0) = -r_d int (H_d,lambda)^2 dt holds within 1e-8 (Simpson rule)
    assert all(b - a < 1e-9 for a, b in zip(hd, hd[1:]))
    v = [grad_hd(x)[0] ** 2 for x in xs]
    simpson = DT / 3 * (v[0] + v[-1] + 4 * sum(v[1:-1:2]) + 2 * sum(v[2:-1:2]))
    assert abs((hd[-1] - hd[0]) + RD * simpson) < 1e-8
    # theta stays in [0.3, 0.5]; u runs from 1.6 down to u* = 1; error below 0.01 from t = 4.34 on
    assert all(0.3 - 1e-12 <= x[1] <= 0.5 for x in xs)
    uu = [control(x) for x in xs]
    assert abs(uu[0] - 1.6) < 1e-12 and min(uu) > 1.0 and max(uu) <= 1.6 + 1e-12
    err = [math.sqrt((x[0] - 2) ** 2 + (x[1] - 0.5) ** 2 + x[2] ** 2) for x in xs]
    assert max(err[steps(4.34, DT):]) < 0.01 and err[steps(4.33, DT)] >= 0.01


def test_matching_failure_and_errors():
    # a J_d whose coupling alpha = 3 does not fit the H_d built with alpha = 2:
    # the unactuated momentum row cannot be matched
    x = [Fraction(17, 10), Fraction(2, 5), Fraction(3, 10)]
    try:
        matching_control(JR, grad_h(x), G, jrd(3), grad_hd(x))
    except MatchingError:
        pass
    else:
        raise AssertionError("no error")
    # floats with a tolerance
    xf = [1.7, 0.4, 0.3]
    assert abs(matching_control(JR, grad_h(xf), G, jrd(), grad_hd(xf), tol=1e-12)[0] - 1.225) < 1e-12
    for bad in [lambda: matching_control(JR, grad_h(x), [[0], [0], [0]], jrd(), grad_hd(x)), lambda: matching_control(JR, grad_h(x), G[:2], jrd(), grad_hd(x))]:
        try:
            bad()
        except ValueError:
            continue
        raise AssertionError("no error")
