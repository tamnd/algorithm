# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/active-disturbance-rejection-control/. The authors are listed in prov/1YHBZH.jsonl.

import math
import random
from fractions import Fraction

import ctlsim
from active_disturbance_rejection_control import control, eso_rhs, observer_gains

# Simulations: classical RK4 (ctlsim) on the joint state (y, y', z1, z2, z3)
# with step DT = 0.002; the control is computed once per step from the
# estimate and held over the step (a sampled controller). Tolerances are
# stated at each check.
DT = 0.002
B, B0, WC, R = 2.0, 1.5, 2.0, 1.0


def steps(T, dt):
    n = round(T / dt)
    assert abs(n * dt - T) < 1e-12
    return n


def dist(t):
    return 1.0 if t >= 5 else 0.0


def run(wo, T):
    # plant y'' = -y - 0.5 y' + d(t) + b u with b = 2; the controller uses b0 = 1.5
    def f(t, x, u):
        return [x[1], -x[0] - 0.5 * x[1] + dist(t) + B * u] + eso_rhs(x[2:], x[0], u, wo, B0)

    def ctrl(t, x):
        return control(x[2:], R, WC, B0)

    ts, xs, us = ctlsim.simulate(f, [0.0] * 5, 0.0, T, DT, control=ctrl)
    assert len(us) == steps(T, DT) <= 10000
    return ts, xs, us


def ideal(t):
    # y'' = wc^2 (1 - y) - 2 wc y', y(0) = y'(0) = 0
    return 1 - (1 + WC * t) * math.exp(-WC * t)


def charpoly(A):
    # Faddeev-LeVerrier in exact arithmetic: coefficients of det(sI - A), leading 1.
    n = len(A)
    M = [[Fraction(0)] * n for _ in range(n)]
    c = [Fraction(1)]
    for k in range(1, n + 1):
        AM = [[sum(A[i][l] * M[l][j] for l in range(n)) for j in range(n)] for i in range(n)]
        M = [[AM[i][j] + (c[-1] if i == j else 0) for j in range(n)] for i in range(n)]
        AM = [[sum(A[i][l] * M[l][j] for l in range(n)) for j in range(n)] for i in range(n)]
        c.append(-sum(AM[i][i] for i in range(n)) / k)
    return c


def polymul(p, q):
    out = [Fraction(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def routh_first_column(c):
    # first column of the Routh array of c[0] s^n + ... + c[n]; None if a pivot is 0
    c = [Fraction(v) for v in c]
    rows = [c[0::2], c[1::2]]
    w = len(rows[0])
    rows = [r + [Fraction(0)] * (w - len(r)) for r in rows]
    for _ in range(len(c) - 2):
        a, b = rows[-2], rows[-1]
        if b[0] == 0:
            return None
        rows.append([(b[0] * a[i + 1] - a[0] * b[i + 1]) / b[0] for i in range(w - 1)] + [Fraction(0)])
    return [r[0] for r in rows]


def hurwitz(c):
    col = routh_first_column(c)
    return col is not None and all(v > 0 for v in col)


def closed_loop_matrix(wc, wo, b0, b=None, a0=0, a1=0):
    # plant y'' = -a0 y - a1 y' + b u (b = b0 by default), state (y, y', z1, z2, z3), r = 0
    b = b0 if b is None else b
    b1, b2, b3 = observer_gains(wo)
    urow = [0, 0, -wc ** 2 / b0, -2 * wc / b0, -1 / b0]
    return [
        [0, 1, 0, 0, 0],
        [-a0, -a1] + [b * a for a in urow[2:]],
        [b1, 0, -b1, 1, 0],
        [b2, 0, -b2 + b0 * urow[2], b0 * urow[3], 1 + b0 * urow[4]],
        [b3, 0, -b3, 0, 0],
    ]


def test_separated_poles_exact():
    # with f = 0 and b = b0: det(sI - A) = (s + wc)^2 (s + wo)^3, exactly
    A = closed_loop_matrix(Fraction(2), Fraction(10), Fraction(3, 2))
    assert charpoly(A) == [1, 34, 424, 2320, 5200, 4000]
    rng = random.Random(5)
    for _ in range(20):
        wc = Fraction(rng.randint(1, 30), rng.randint(1, 5))
        wo = Fraction(rng.randint(1, 60), rng.randint(1, 5))
        b0 = Fraction(rng.choice([-1, 1]) * rng.randint(1, 9), rng.randint(1, 4))
        target = polymul(polymul([1, wc], [1, wc]), polymul(polymul([1, wo], [1, wo]), [1, wo]))
        assert charpoly(closed_loop_matrix(wc, wo, b0)) == target


def test_page_loop_hurwitz_exact():
    # page plant y'' = -y - 0.5 y' + 2 u, b0 = 3/2, wc = 2, wo = 10
    cp = charpoly(closed_loop_matrix(Fraction(2), Fraction(10), Fraction(3, 2), Fraction(2), 1, Fraction(1, 2)))
    assert cp == [1, Fraction(69, 2), 442, Fraction(10018, 3), Fraction(22072, 3), Fraction(16000, 3)]
    assert hurwitz(cp)
    # the gain error b / b0 the loop tolerates: b = 8 is Hurwitz, b = 17/2 is not
    for b, ok in [(Fraction(1, 100), True), (Fraction(8), True), (Fraction(17, 2), False)]:
        assert hurwitz(charpoly(closed_loop_matrix(Fraction(2), Fraction(10), Fraction(3, 2), b, 1, Fraction(1, 2)))) == ok
    # the Routh test itself: (s + 1)^5 is Hurwitz, s^2 - s + 1 is not
    assert hurwitz([1, 5, 10, 10, 5, 1]) and not hurwitz([1, -1, 1])


def test_observer_error_equation_exact():
    # x = (y, y', F) with y'' = F + b0 u: the error x - z obeys
    # e1' = e2 - 3 wo e1, e2' = e3 - 3 wo^2 e1, e3' = F' - wo^3 e1
    rng = random.Random(3)
    for _ in range(200):
        y, yd, F, Fd, u = (Fraction(rng.randint(-30, 30), rng.randint(1, 7)) for _ in range(5))
        z = [Fraction(rng.randint(-30, 30), rng.randint(1, 7)) for _ in range(3)]
        wo = Fraction(rng.randint(1, 40), rng.randint(1, 3))
        b0 = Fraction(rng.randint(1, 9), rng.randint(1, 4))
        zd = eso_rhs(z, y, u, wo, b0)
        e = [y - z[0], yd - z[1], F - z[2]]
        xd = [yd, F + b0 * u, Fd]
        ed = [a - b for a, b in zip(xd, zd)]
        assert ed == [e[1] - 3 * wo * e[0], e[2] - 3 * wo ** 2 * e[0], Fd - wo ** 3 * e[0]]


def test_control_cancels_estimate_exact():
    z = [Fraction(1, 3), Fraction(-2, 5), Fraction(7, 4)]
    u = control(z, 1, 2, Fraction(3, 2))
    # b0 u + z3 = wc^2 (r - z1) - 2 wc z2
    assert Fraction(3, 2) * u + z[2] == 4 * (1 - z[0]) - 4 * z[1]
    assert control([0, 0, 0], 1, 2, 3) == Fraction(4, 3)


def test_page_table():
    # wo = 10: (t, y, z3), within 5e-5
    ts, xs, us = run(10.0, 10.0)
    table = [(0.5, 0.26861, -0.04604), (1, 0.55035, -0.55420), (2, 0.87203, -0.76846), (3, 0.97251, -0.76831), (5, 0.99981, -0.75163), (5.5, 1.04458, -0.14171), (6, 1.04424, -0.07094), (8, 1.00524, 0.00093), (10, 1.00016, 0.00027)]
    for t, y, z3 in table:
        x = xs[steps(t, DT)]
        assert abs(x[0] - y) < 5e-5 and abs(x[4] - z3) < 5e-5
    # u(0) = 4 / 1.5 = 2.667. The total disturbance is F = -y - 0.5 y' + d + (b - b0) u;
    # at rest at y = 1 the plant needs u = (1 - d) / b, so F = -0.75 before t = 5
    # and F = 0 after it, which z3 approaches in the table.
    assert abs(us[0] - 4 / 1.5) < 1e-12
    # largest |y - 1| after the step disturbance: 0.0477, within 1 percent
    after = max(abs(x[0] - 1) for t, x in zip(ts, xs) if t >= 5)
    assert abs(after - 0.0477) < 0.01 * 0.0477


def test_deviation_from_ideal_scales_with_bandwidth():
    # max |y - ideal| for t < 5: wo = 10: 0.0514, 20: 0.0241, 40: 0.0113, within 1 percent;
    # each doubling of wo roughly halves it
    measured = {}
    for wo, want in [(10.0, 0.0514), (20.0, 0.0241), (40.0, 0.0113)]:
        ts, xs, us = run(wo, 5.0)
        dev = max(abs(x[0] - ideal(t)) for t, x in zip(ts, xs) if t < 5)
        assert abs(dev - want) < 0.01 * want
        measured[wo] = dev
    assert 2.0 < measured[10.0] / measured[20.0] < 2.3 and 2.0 < measured[20.0] / measured[40.0] < 2.3


def test_errors():
    for bad in [lambda: observer_gains(0), lambda: control([0, 0, 0], 1, 0, 1), lambda: control([0, 0, 0], 1, 2, 0), lambda: eso_rhs([0, 0, 0], 1, 0, -1, 1)]:
        try:
            bad()
        except ValueError:
            continue
        raise AssertionError("no error")
