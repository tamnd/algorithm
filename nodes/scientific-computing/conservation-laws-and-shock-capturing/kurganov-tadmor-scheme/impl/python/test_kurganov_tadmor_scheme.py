# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kurganov-tadmor-scheme/. The authors are listed in prov/WYYX6A.jsonl.

import random
from fractions import Fraction
from math import cos, log2, pi, sqrt

from kurganov_tadmor_scheme import euler_flux, face_fluxes, minmod3, prim_to_cons, rate, slope, solve_euler, step

SOD = ((1.0, 0.0, 1.0), (0.125, 0.0, 0.1))
IDENT, ONE = (lambda v: v), (lambda v: 1)


def exact_sod_density(xi, g=1.4):
    """Reference: the exact Sod density at xi = x / t, from the star state found by bisection."""
    (rl, ul, pl), (rr, ur, pr) = SOD
    cl, cr = sqrt(g * pl / rl), sqrt(g * pr / rr)
    z = (g - 1.0) / (2.0 * g)

    def fl(p):  # rarefaction to the left
        return 2.0 * cl / (g - 1.0) * ((p / pl) ** z - 1.0)

    def fr(p):  # shock to the right
        return (p - pr) * sqrt(2.0 / ((g + 1.0) * rr) / (p + (g - 1.0) / (g + 1.0) * pr))

    lo, hi = pr, pl
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        lo, hi = (lo, mid) if fl(mid) + fr(mid) > 0.0 else (mid, hi)
    ps = 0.5 * (lo + hi)
    us = 0.5 * (fr(ps) - fl(ps))
    r = ps / pr
    rs_r = rr * (r + (g - 1.0) / (g + 1.0)) / ((g - 1.0) / (g + 1.0) * r + 1.0)
    shock = ur + cr * sqrt((g + 1.0) / (2.0 * g) * r + z)
    cs = cl * (ps / pl) ** z
    if xi <= -cl:
        return rl
    if xi <= us - cs:
        return rl * (2.0 / (g + 1.0) + (g - 1.0) / ((g + 1.0) * cl) * (-xi)) ** (2.0 / (g - 1.0))
    if xi <= us:
        return rl * (ps / pl) ** (1.0 / g)
    return rs_r if xi <= shock else rr


def sod_l1(m, theta, t=0.2):
    cells = [prim_to_cons(SOD[0] if (j + 0.5) / m < 0.5 else SOD[1]) for j in range(m)]
    cells, _ = solve_euler(cells, 1.0 / m, t, theta=theta)
    err = 0.0
    for j, q in enumerate(cells):
        ex = sum(exact_sod_density(((j + (k + 0.5) / 16) / m - 0.5) / t) for k in range(16)) / 16
        err += abs(q[0] - ex) / m
    return err


def averages(m, t):
    """Exact cell averages of sin(2 pi (x - t)) on [0, 1]."""
    dx = 1.0 / m
    return [(cos(2 * pi * (j * dx - t)) - cos(2 * pi * ((j + 1) * dx - t))) / (2 * pi * dx) for j in range(m)]


def advect(m, nu, theta=1.5, method="ssp3", t=1.0):
    dx = 1.0 / m
    n = round(t / (nu * dx))
    u = averages(m, 0.0)
    for _ in range(n):
        u = step(u, t / n, dx, IDENT, lambda v: 1.0, theta, True, method)
    e = [a - b for a, b in zip(u, averages(m, t))]
    return sum(abs(x) for x in e) * dx, max(abs(x) for x in e)


def test_minmod_slope() -> None:
    assert minmod3(1.0, 2.0, 3.0) == 1.0 and minmod3(-1.0, -2.0, -0.5) == -0.5 and minmod3(1.0, -1.0, 2.0) == 0.0
    assert slope(0.0, 1.0, 3.0, 1.5) == 1.5 and slope(0.0, 1.0, 3.0, 1.0) == 1.0 and slope(0.0, 1.0, 0.5, 2.0) == 0.0
    for theta in (1.0, 1.5, 2.0):
        for r in (0.1, 0.5, 1.0, 3.0, 9.0):
            s = slope(0.0, 1.0, 1.0 + r, theta)  # s = phi(r) for a left difference of 1
            assert 0.0 <= s <= theta and s <= theta * r + 1e-15


def test_hand_trace_in_fractions() -> None:
    u = [Fraction(x) for x in (0, 0, 1, 3, 4, 4)]
    th = Fraction(3, 2)
    # For f(u) = u and a = 1 the face flux is the left face value u_j + s_j / 2.
    assert face_fluxes(u, IDENT, ONE, th) == [0, 0, 0, Fraction(7, 4), Fraction(15, 4), 4, 4]
    assert rate(u, Fraction(1), IDENT, ONE, th) == [0, 0, Fraction(-7, 4), -2, Fraction(-1, 4), 0]
    assert step(u, Fraction(1, 4), Fraction(1), IDENT, ONE, th, method="euler") == [0, 0, Fraction(9, 16), Fraction(5, 2), Fraction(63, 16), 4]


def test_exact_conservation_for_burgers_in_fractions() -> None:
    rng = random.Random(3)
    u = [Fraction(rng.randint(-8, 8), 4) for _ in range(12)]
    total = sum(u)
    for method in ("euler", "ssp2", "ssp3"):
        v = u
        for _ in range(2):
            v = step(v, Fraction(1, 10), Fraction(1, 2), lambda x: x * x / 2, abs, Fraction(3, 2), True, method)
            assert sum(v) == total


def test_constant_state_and_consistency() -> None:
    q = prim_to_cons((0.7, 0.3, 0.9))
    h = face_fluxes([q] * 5, euler_flux, lambda w: 2.0)
    assert all(abs(a - b) < 1e-14 for f in h for a, b in zip(f, euler_flux(q)))
    cells, _ = solve_euler([q] * 20, 0.05, 0.1)
    assert all(abs(a - b) < 1e-13 for c in cells for a, b in zip(c, q))


def test_tvd_and_no_new_extrema_for_advection() -> None:
    m = 60
    for theta in (1.0, 1.5, 2.0):
        for nu in (0.2, 2.0 / (2.0 + theta)):  # the bound of Theorem 1
            for method in ("euler", "ssp2"):
                u = [1.0 if 10 <= j < 25 else (0.5 if 35 <= j < 40 else 0.0) for j in range(m)]
                tv0 = sum(abs(u[j] - u[j - 1]) for j in range(m))
                for _ in range(30):
                    u = step(u, nu, 1.0, IDENT, lambda v: 1.0, theta, True, method)
                    tv = sum(abs(u[j] - u[j - 1]) for j in range(m))
                    assert tv <= tv0 + 1e-12 and -1e-12 <= min(u) and max(u) <= 1.0 + 1e-12
                    tv0 = tv


def test_tvd_for_burgers() -> None:
    m, dx = 80, 1.0 / 80
    u = [1.0 if 0.2 < (j + 0.5) * dx < 0.5 else -0.5 for j in range(m)]
    tv0 = sum(abs(u[j + 1] - u[j]) for j in range(m - 1))
    for _ in range(60):
        dt = 0.4 * dx / max(abs(v) for v in u)
        u = step(u, dt, dx, lambda x: x * x / 2, abs)
        tv = sum(abs(u[j + 1] - u[j]) for j in range(m - 1))
        assert tv <= tv0 + 1e-12 and -0.5 - 1e-12 <= min(u) and max(u) <= 1.0 + 1e-12
        tv0 = tv


def test_error_does_not_depend_on_the_time_step() -> None:
    e_big, e_small = advect(40, 0.4)[0], advect(40, 0.05)[0]
    assert abs(e_big - 0.019093) < 1e-6 and abs(e_small - 0.019294) < 1e-6
    assert abs(e_small / e_big - 1.0) < 0.02  # the dissipation is not of order 1 / dt


def test_order_on_smooth_advection() -> None:
    errs = [advect(m, 0.4)[0] for m in (20, 40, 80)]
    assert log2(errs[1] / errs[2]) > 1.85  # the limiter clips the extrema on coarse grids


def test_second_order_on_a_smooth_euler_wave() -> None:
    t, errs = 0.1, []
    for m in (25, 50, 100):
        dx = 1.0 / m
        cells = [prim_to_cons((1.0 + 0.2 * r, 1.0, 1.0)) for r in averages(m, 0.0)]
        cells, _ = solve_euler(cells, dx, t, periodic=True)
        errs.append(sum(abs(q[0] - 1.0 - 0.2 * e) for q, e in zip(cells, averages(m, t))) * dx)
    assert all(abs(log2(errs[i] / errs[i + 1]) - 2.0) < 0.15 for i in range(2))
    assert abs(errs[0] - 0.0019461) < 1e-7


def test_sod_l1_error() -> None:
    e100, e200 = sod_l1(100, 1.5), sod_l1(200, 1.5)
    assert abs(e100 - 0.00700) < 5e-5 and abs(e200 - 0.003832) < 5e-5
    assert sod_l1(100, 1.0) > e100  # theta = 1 is the most dissipative choice
