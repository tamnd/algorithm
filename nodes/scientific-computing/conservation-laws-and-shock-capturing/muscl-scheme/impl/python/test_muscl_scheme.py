# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/muscl-scheme/. The authors are listed in prov/7J4C0V.jsonl.

import random
from fractions import Fraction
from math import cos, log2, pi, sqrt

from muscl_scheme import (
    burgers_godunov,
    cons_to_prim,
    euler_flux,
    hllc_flux,
    mc,
    minmod,
    prim_to_cons,
    solve_euler,
    step,
    upwind_flux,
    van_leer,
)

SOD = ((1.0, 0.0, 1.0), (0.125, 0.0, 0.1))
LIMS = ("minmod", "vanleer", "mc")


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


def sod_l1(m, limiter, t=0.2):
    cells = [prim_to_cons(SOD[0] if (j + 0.5) / m < 0.5 else SOD[1]) for j in range(m)]
    cells, _ = solve_euler(cells, 1.0 / m, t, limiter=limiter)
    err = 0.0
    for j, q in enumerate(cells):
        ex = sum(exact_sod_density(((j + (k + 0.5) / 16) / m - 0.5) / t) for k in range(16)) / 16
        err += abs(q[0] - ex) / m
    return err


def averages(m, t):
    """Exact cell averages of sin(2 pi (x - t)) on [0, 1]."""
    dx = 1.0 / m
    return [(cos(2 * pi * (j * dx - t)) - cos(2 * pi * ((j + 1) * dx - t))) / (2 * pi * dx) for j in range(m)]


def advect(m, limiter, t=1.0, nu=0.8):
    dx = 1.0 / m
    n = round(t / (nu * dx))
    u = averages(m, 0.0)
    for _ in range(n):
        u = step(u, t / n, dx, lambda v: v, upwind_flux(1.0), limiter, periodic=True)
    e = [a - b for a, b in zip(u, averages(m, t))]
    return sum(abs(x) for x in e) * dx, max(abs(x) for x in e)


def test_limiters() -> None:
    assert minmod(1.0, 2.0) == 1.0 and minmod(-3.0, -2.0) == -2.0 and minmod(1.0, -1.0) == 0.0
    assert van_leer(1.0, 3.0) == 1.5 and van_leer(2.0, 0.0) == 0.0
    assert mc(1.0, 3.0) == 2.0 and abs(mc(1.0, 1.2) - 1.1) < 1e-15 and mc(-1.0, -3.0) == -2.0 and mc(1.0, -2.0) == 0.0
    for lim in (minmod, van_leer, mc):
        for r in (0.1, 0.5, 1.0, 2.0, 7.0):
            phi = lim(1.0, r)
            assert 0.0 <= phi <= min(2.0, 2.0 * r) + 1e-15  # the TVD region used in the proof
        assert lim(1.0, 1.0) == 1.0


def test_hand_trace_in_fractions() -> None:
    u = [Fraction(x) for x in (0, 0, 1, 3, 4, 4)]
    half = Fraction(1, 2)
    new = step(u, half, Fraction(1), lambda v: v, upwind_flux(1), "minmod")
    assert new == [0, 0, Fraction(3, 8), 2, Fraction(29, 8), 4]
    new = step(u, half, Fraction(1), lambda v: v, upwind_flux(1), "mc")
    assert new == [0, 0, Fraction(5, 16), 2, Fraction(59, 16), 4]


def test_constant_state_and_consistency() -> None:
    q = prim_to_cons((0.7, 0.3, 0.9))
    assert all(abs(a - b) < 1e-14 for a, b in zip(hllc_flux(q, q), euler_flux(q)))
    cells, _ = solve_euler([q] * 20, 0.05, 0.1)
    assert all(abs(a - b) < 1e-13 for c in cells for a, b in zip(c, q))


def test_exact_conservation_for_burgers_in_fractions() -> None:
    rng = random.Random(3)
    u = [Fraction(rng.randint(-8, 8), 4) for _ in range(12)]
    total = sum(u)
    for lim in LIMS:
        v = u
        for _ in range(4):
            v = step(v, Fraction(1, 10), Fraction(1, 2), lambda x: x * x / 2, burgers_godunov, lim, periodic=True)
            assert sum(v) == total


def test_tvd_and_no_new_extrema_for_advection() -> None:
    m = 60
    for lim in LIMS:
        for nu in (0.3, 0.9, 1.0):
            u = [1.0 if 10 <= j < 25 else (0.5 if 35 <= j < 40 else 0.0) for j in range(m)]
            tv0 = sum(abs(u[j] - u[j - 1]) for j in range(m))
            for _ in range(40):
                u = step(u, nu, 1.0, lambda v: v, upwind_flux(1.0), lim, periodic=True)
                tv = sum(abs(u[j] - u[j - 1]) for j in range(m))
                assert tv <= tv0 + 1e-12 and -1e-12 <= min(u) and max(u) <= 1.0 + 1e-12
                tv0 = tv


def test_tvd_for_burgers() -> None:
    m, dx = 80, 1.0 / 80
    u = [1.0 if 0.2 < (j + 0.5) * dx < 0.5 else -0.5 for j in range(m)]
    tv0 = sum(abs(u[j + 1] - u[j]) for j in range(m - 1))
    for _ in range(60):
        dt = 0.8 * dx / max(abs(v) for v in u)
        u = step(u, dt, dx, lambda x: x * x / 2, burgers_godunov, "minmod")
        tv = sum(abs(u[j + 1] - u[j]) for j in range(m - 1))
        assert tv <= tv0 + 1e-12 and -0.5 - 1e-12 <= min(u) and max(u) <= 1.0 + 1e-12
        tv0 = tv


def test_second_order_in_l1_and_clipping_in_max_norm() -> None:
    errs = [advect(m, "vanleer") for m in (20, 40, 80)]
    p1 = [log2(errs[i][0] / errs[i + 1][0]) for i in range(2)]
    pinf = [log2(errs[i][1] / errs[i + 1][1]) for i in range(2)]
    assert all(abs(p - 2.0) < 0.2 for p in p1)
    assert all(1.1 < p < 1.6 for p in pinf)  # the limiter clips the extrema
    assert abs(errs[0][0] - 0.019367) < 1e-6


def test_second_order_on_a_smooth_euler_wave() -> None:
    t, errs = 0.1, []
    for m in (25, 50, 100):
        dx = 1.0 / m
        cells = [prim_to_cons((1.0 + 0.2 * r, 1.0, 1.0)) for r in averages(m, 0.0)]
        cells, _ = solve_euler(cells, dx, t, limiter="vanleer", periodic=True)
        errs.append(sum(abs(q[0] - 1.0 - 0.2 * e) for q, e in zip(cells, averages(m, t))) * dx)
    assert all(abs(log2(errs[i] / errs[i + 1]) - 2.0) < 0.2 for i in range(2))


def test_sod_l1_error() -> None:
    e100, e200 = sod_l1(100, "minmod"), sod_l1(200, "minmod")
    assert abs(e100 - 0.00585) < 5e-5 and abs(e200 - 0.00347) < 5e-5
    assert sod_l1(100, "mc") < e100


def test_stationary_contact_is_kept_exactly() -> None:
    m = 40
    cells = [prim_to_cons((1.0 if j < m // 2 else 0.5, 0.0, 1.0)) for j in range(m)]
    for lim in LIMS:
        out, _ = solve_euler(cells, 1.0 / m, 0.1, limiter=lim)
        w = [cons_to_prim(q) for q in out]
        assert all(abs(a[0] - b[0]) < 1e-13 and abs(a[1]) < 1e-13 and abs(a[2] - 1.0) < 1e-13 for a, b in zip(w, map(cons_to_prim, cells)))
