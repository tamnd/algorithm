# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nessyahu-tadmor-scheme/. The authors are listed in prov/40T9VJ.jsonl.

import random
from fractions import Fraction
from math import cos, log2, pi, sqrt

from nessyahu_tadmor_scheme import prim_to_cons, slope, solve_euler, staggered_step, step

SOD = ((1.0, 0.0, 1.0), (0.125, 0.0, 0.1))
IDENT = lambda v: v


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


def advect(m, nu, theta=1.5, t=1.0):
    dx = 1.0 / m
    n = round(t / (2 * nu * dx))
    u = averages(m, 0.0)
    for _ in range(n):
        u = step(u, t / (2 * n), dx, IDENT, theta, True)
    e = [a - b for a, b in zip(u, averages(m, t))]
    return sum(abs(x) for x in e) * dx, max(abs(x) for x in e)


def test_hand_trace_against_the_linear_formula() -> None:
    # For f(u) = u: W_{j+1/2} = (1/2 + nu) u_j + (1/2 - nu) u_{j+1} + kappa (u'_j - u'_{j+1}).
    u = [Fraction(x) for x in (0, 0, 1, 3, 4, 4)]
    th, nu = Fraction(3, 2), Fraction(1, 4)
    kappa = (1 - 4 * nu * nu) / 8
    ext = [u[0], u[0]] + u + [u[-1], u[-1]]
    d = {k: slope(ext[k - 1], ext[k], ext[k + 1], th) for k in range(1, len(ext) - 1)}
    ref = [(Fraction(1, 2) + nu) * ext[k] + (Fraction(1, 2) - nu) * ext[k + 1] + kappa * (d[k] - d[k + 1]) for k in range(2, 8)]
    w = staggered_step(u, nu, IDENT, th)
    assert w == ref == [0, Fraction(7, 64), Fraction(3, 2), Fraction(217, 64), 4, 4]
    assert staggered_step(w, nu, IDENT, th, shift=1) == [0, Fraction(49, 4096), Fraction(1305, 4096), Fraction(8359, 4096), Fraction(14863, 4096), 4]


def test_exact_conservation_for_burgers_in_fractions() -> None:
    rng = random.Random(3)
    u = [Fraction(rng.randint(-8, 8), 4) for _ in range(12)]
    total = sum(u)
    for theta in (1, Fraction(3, 2), 2):
        v = u
        for _ in range(2):
            v = step(v, Fraction(1, 10), Fraction(1, 2), lambda x: x * x / 2, theta, True)
            assert sum(v) == total


def test_constant_state_and_consistency() -> None:
    q = prim_to_cons((0.7, 0.3, 0.9))
    cells, _ = solve_euler([q] * 20, 0.05, 0.1)
    assert all(abs(a - b) < 1e-13 for c in cells for a, b in zip(c, q))
    assert staggered_step([Fraction(3)] * 6, Fraction(1, 3), lambda x: x * x / 2) == [3] * 6


def test_courant_one_half_is_an_exact_shift() -> None:
    # At nu = 1/2 the staggered cell [x_j, x_{j+1}] receives exactly the old cell j.
    rng = random.Random(5)
    u = [Fraction(rng.randint(0, 9)) for _ in range(10)]
    w = staggered_step(u, Fraction(1, 2), IDENT, 2, True)
    assert w == u
    assert advect(40, 0.5)[0] < 1e-14


def test_tvd_and_no_new_extrema_for_advection() -> None:
    m = 60
    for theta in (1.0, 1.5, 2.0):
        for nu in (0.2, 0.5, -0.4):
            u = [1.0 if 10 <= j < 25 else (0.5 if 35 <= j < 40 else 0.0) for j in range(m)]
            tv0 = sum(abs(u[j] - u[j - 1]) for j in range(m))
            for k in range(40):
                u = staggered_step(u, nu, IDENT, theta, True, k % 2)
                tv = sum(abs(u[j] - u[j - 1]) for j in range(m))
                assert tv <= tv0 + 1e-12 and -1e-12 <= min(u) and max(u) <= 1.0 + 1e-12
                tv0 = tv


def test_tvd_for_burgers() -> None:
    m, dx = 80, 1.0 / 80
    u = [1.0 if 0.2 < (j + 0.5) * dx < 0.5 else -0.5 for j in range(m)]
    tv0 = sum(abs(u[j + 1] - u[j]) for j in range(m - 1))
    for _ in range(30):
        u = step(u, 0.4 * dx / max(abs(v) for v in u), dx, lambda x: x * x / 2)
        tv = sum(abs(u[j + 1] - u[j]) for j in range(m - 1))
        assert tv <= tv0 + 1e-12 and -0.5 - 1e-12 <= min(u) and max(u) <= 1.0 + 1e-12
        tv0 = tv


def test_error_grows_when_the_time_step_falls() -> None:
    errs = [advect(40, nu)[0] for nu in (0.4, 0.2, 0.1, 0.05)]
    assert abs(errs[0] - 0.005769) < 1e-6 and abs(errs[3] - 0.046198) < 1e-6
    assert all(errs[i] < errs[i + 1] for i in range(3))  # the viscosity grows like 1 / dt


def test_second_order_on_smooth_advection() -> None:
    errs = [advect(m, 0.4)[0] for m in (20, 40, 80)]
    assert all(abs(log2(errs[i] / errs[i + 1]) - 2.0) < 0.1 for i in range(2))


def test_second_order_on_a_smooth_euler_wave() -> None:
    t, errs = 0.1, []
    for m in (25, 50, 100):
        dx = 1.0 / m
        cells = [prim_to_cons((1.0 + 0.2 * r, 1.0, 1.0)) for r in averages(m, 0.0)]
        cells, _ = solve_euler(cells, dx, t, periodic=True)
        errs.append(sum(abs(q[0] - 1.0 - 0.2 * e) for q, e in zip(cells, averages(m, t))) * dx)
    assert all(abs(log2(errs[i] / errs[i + 1]) - 2.0) < 0.15 for i in range(2))
    assert abs(errs[0] - 0.0017865) < 1e-7


def test_sod_l1_error() -> None:
    e100, e200 = sod_l1(100, 1.5), sod_l1(200, 1.5)
    assert abs(e100 - 0.005485) < 5e-5 and abs(e200 - 0.002955) < 5e-5
    assert sod_l1(100, 1.0) > e100
