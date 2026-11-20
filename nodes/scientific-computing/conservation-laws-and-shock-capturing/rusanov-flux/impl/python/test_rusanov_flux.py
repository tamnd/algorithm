# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rusanov-flux/. The authors are listed in prov/PDKD22.jsonl.

import random
from fractions import Fraction
from math import cos, log2, pi, sqrt

from rusanov_flux import (
    cons_to_prim,
    euler_flux,
    prim_to_cons,
    rusanov_euler,
    rusanov_scalar,
    solve_euler,
    step,
)

SOD = ((1.0, 0.0, 1.0), (0.125, 0.0, 0.1))


def exact_sample(left, right, xi, g=1.4):
    """Reference: the exact Riemann solution (rho, u, p) at xi = x / t, with p* found by bisection."""
    (rl, ul, pl), (rr, ur, pr) = left, right
    cl, cr = sqrt(g * pl / rl), sqrt(g * pr / rr)
    z = (g - 1.0) / (2.0 * g)

    def fk(p, rk, pk, ck):
        if p > pk:
            return (p - pk) * sqrt(2.0 / ((g + 1.0) * rk) / (p + (g - 1.0) / (g + 1.0) * pk))
        return 2.0 * ck / (g - 1.0) * ((p / pk) ** z - 1.0)

    lo, hi = 1e-12, 1e4
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if fk(mid, rl, pl, cl) + fk(mid, rr, pr, cr) + ur - ul > 0.0:
            hi = mid
        else:
            lo = mid
    ps = 0.5 * (lo + hi)
    us = 0.5 * (ul + ur) + 0.5 * (fk(ps, rr, pr, cr) - fk(ps, rl, pl, cl))
    rk, uk, pk, ck, sg = (rl, ul, pl, cl, 1.0) if xi <= us else (rr, ur, pr, cr, -1.0)
    xs, uss, uks = sg * xi, sg * us, sg * uk
    if ps > pk:
        if xs <= uks - ck * sqrt((g + 1.0) / (2.0 * g) * ps / pk + z):
            return (rk, uk, pk)
        r, gg = ps / pk, (g - 1.0) / (g + 1.0)
        return (rk * (r + gg) / (gg * r + 1.0), us, ps)
    if xs <= uks - ck:
        return (rk, uk, pk)
    if xs >= uss - ck * (ps / pk) ** z:
        return (rk * (ps / pk) ** (1.0 / g), us, ps)
    w = 2.0 / (g + 1.0) + (g - 1.0) / ((g + 1.0) * ck) * (uks - xs)
    return (rk * w ** (2.0 / (g - 1.0)), sg * 2.0 / (g + 1.0) * (ck + 0.5 * (g - 1.0) * uks + xs), pk * w ** (2.0 * g / (g - 1.0)))


def sod_l1(m, t=0.2):
    """L1 error of the density against exact cell averages (16-point midpoint rule per cell)."""
    cells = [prim_to_cons(SOD[0] if (j + 0.5) / m < 0.5 else SOD[1]) for j in range(m)]
    cells, _ = solve_euler(cells, 1.0 / m, t)
    err = 0.0
    for j, q in enumerate(cells):
        ex = sum(exact_sample(*SOD, ((j + (k + 0.5) / 16) / m - 0.5) / t)[0] for k in range(16)) / 16
        err += abs(q[0] - ex) / m
    return err


def density_wave(m, t):
    """Exact cell averages of rho = 1 + 0.2 sin(2 pi (x - t)), with u = 1 and p = 1."""
    dx = 1.0 / m
    return [1.0 + 0.2 * (cos(2 * pi * (j * dx - t)) - cos(2 * pi * ((j + 1) * dx - t))) / (2 * pi * dx) for j in range(m)]


def test_flux_at_the_sod_interface_by_hand() -> None:
    f = rusanov_euler(prim_to_cons(SOD[0]), prim_to_cons(SOD[1]))
    s = sqrt(1.4)  # c_L is the larger speed
    assert abs(f[0] - 0.5 * s * 0.875) < 1e-14
    assert abs(f[1] - 0.55) < 1e-14
    assert abs(f[2] - 0.5 * s * 2.25) < 1e-14
    assert abs(f[0] - 0.517657) < 1e-6 and abs(f[2] - 1.331118) < 1e-6


def test_consistency() -> None:
    rng = random.Random(1)
    for _ in range(50):
        q = prim_to_cons((rng.uniform(0.1, 2), rng.uniform(-2, 2), rng.uniform(0.1, 2)))
        assert all(abs(a - b) < 1e-12 for a, b in zip(rusanov_euler(q, q), euler_flux(q)))


def test_sod_l1_error_decreases() -> None:
    e100, e200 = sod_l1(100), sod_l1(200)
    assert e200 < 0.0155 and e100 < 0.022
    assert 0.3 < log2(e100 / e200) < 0.8  # about 1/2 near discontinuities


def test_first_order_on_a_smooth_wave() -> None:
    t, errs = 0.1, []
    for m in (25, 50, 100):
        cells = [prim_to_cons((r, 1.0, 1.0)) for r in density_wave(m, 0.0)]
        cells, _ = solve_euler(cells, 1.0 / m, t, periodic=True)
        errs.append(sum(abs(q[0] - e) for q, e in zip(cells, density_wave(m, t))) / m)
    orders = [log2(errs[i] / errs[i + 1]) for i in range(2)]
    assert all(abs(p - 1.0) < 0.2 for p in orders)


def test_conservation_on_a_periodic_grid() -> None:
    m = 64
    cells = [prim_to_cons((r, 1.0, 1.0)) for r in density_wave(m, 0.0)]
    before = [sum(q[k] for q in cells) for k in range(3)]
    cells, _ = solve_euler(cells, 1.0 / m, 0.05, periodic=True)
    after = [sum(q[k] for q in cells) for k in range(3)]
    assert all(abs(a - b) <= 1e-12 * abs(a) for a, b in zip(before, after))


def test_exact_conservation_for_burgers_in_fractions() -> None:
    f, df = (lambda u: u * u / 2), (lambda u: u)
    rng = random.Random(2)
    u = [Fraction(rng.randint(-8, 8), 4) for _ in range(12)]
    total = sum(u)
    for _ in range(5):
        u = step(u, Fraction(1, 10), Fraction(1, 2), lambda a, b: rusanov_scalar(a, b, f, df), periodic=True)
        assert sum(u) == total


def test_tvd_and_no_new_extrema_for_burgers() -> None:
    f, df = (lambda u: u * u / 2), (lambda u: u)
    m, dx = 80, 1.0 / 80
    u = [1.0 if 0.2 < (j + 0.5) * dx < 0.5 else -0.5 for j in range(m)]
    tv0 = sum(abs(u[j + 1] - u[j]) for j in range(m - 1))
    for _ in range(60):
        dt = 0.9 * dx / max(abs(v) for v in u)
        u = step(u, dt, dx, lambda a, b: rusanov_scalar(a, b, f, df))
        tv = sum(abs(u[j + 1] - u[j]) for j in range(m - 1))
        assert tv <= tv0 + 1e-12
        assert -0.5 - 1e-12 <= min(u) and max(u) <= 1.0 + 1e-12
        tv0 = tv


def test_stationary_contact_is_smeared_but_u_and_p_stay_exact() -> None:
    m = 40
    cells = [prim_to_cons((1.0 if j < m // 2 else 0.5, 0.0, 1.0)) for j in range(m)]
    cells, _ = solve_euler(cells, 1.0 / m, 0.1)
    w = [cons_to_prim(q) for q in cells]
    assert all(abs(x[1]) < 1e-13 and abs(x[2] - 1.0) < 1e-13 for x in w)
    assert abs(w[m // 2][0] - 0.5) > 0.05  # the contact is not kept


def test_positivity_on_the_123_problem() -> None:
    m = 100
    cells = [prim_to_cons((1.0, -2.0, 0.4) if j < m // 2 else (1.0, 2.0, 0.4)) for j in range(m)]
    cells, _ = solve_euler(cells, 1.0 / m, 0.15)
    w = [cons_to_prim(q) for q in cells]
    assert min(x[0] for x in w) > 0.0 and min(x[2] for x in w) > 0.0
