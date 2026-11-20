# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/roe-solver/. The authors are listed in prov/9FFHHH.jsonl.

import random
from fractions import Fraction
from math import cos, log2, pi, sqrt

from roe_solver import (
    cons_to_prim,
    euler_flux,
    prim_to_cons,
    roe_flux,
    roe_scalar,
    roe_waves,
    solve_euler,
    step,
)

SOD = ((1.0, 0.0, 1.0), (0.125, 0.0, 0.1))


def exact_solution(left, right, g=1.4):
    """Reference: the exact Riemann solution. Returns a function of xi = x / t giving (rho, u, p)."""
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

    def sample(xi):
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

    return sample


def sod_l1(m, t=0.2):
    """L1 error of the density against exact cell averages (16-point midpoint rule per cell)."""
    sample = exact_solution(*SOD)
    cells = [prim_to_cons(SOD[0] if (j + 0.5) / m < 0.5 else SOD[1]) for j in range(m)]
    cells, _ = solve_euler(cells, 1.0 / m, t)
    err = 0.0
    for j, q in enumerate(cells):
        ex = sum(sample(((j + (k + 0.5) / 16) / m - 0.5) / t)[0] for k in range(16)) / 16
        err += abs(q[0] - ex) / m
    return err


def density_wave(m, t):
    """Exact cell averages of rho = 1 + 0.2 sin(2 pi (x - t)), with u = 1 and p = 1."""
    dx = 1.0 / m
    return [1.0 + 0.2 * (cos(2 * pi * (j * dx - t)) - cos(2 * pi * ((j + 1) * dx - t))) / (2 * pi * dx) for j in range(m)]


def normal_shock(mach, g=1.4):
    """A shock at rest: the supersonic state (1, M c, 1) and the subsonic state behind it."""
    u = mach * sqrt(g)
    r = (g + 1.0) * mach**2 / ((g - 1.0) * mach**2 + 2.0)
    p = (2.0 * g * mach**2 - (g - 1.0)) / (g + 1.0)
    return (1.0, u, 1.0), (r, u / r, p)


def run_steps(cells, n, cfl=0.9):
    dx = 1.0 / len(cells)
    for _ in range(n):
        smax = max(abs(cons_to_prim(q)[1]) + sqrt(1.4 * cons_to_prim(q)[2] / q[0]) for q in cells)
        cells = step(cells, cfl * dx / smax, dx, roe_flux)
    return cells


def test_flux_at_the_sod_interface_by_hand() -> None:
    ql, qr = prim_to_cons(SOD[0]), prim_to_cons(SOD[1])
    lam, _, alpha = roe_waves(ql, qr)
    h = (3.5 + sqrt(0.125) * 2.8) / (1.0 + sqrt(0.125))
    c = sqrt(0.4 * h)
    a2 = 0.4 / (c * c) * (-0.875 * h + 2.25)
    assert abs(alpha[1] - a2) < 1e-14 and abs(alpha[0] - (-0.875 - a2) / 2) < 1e-14 and alpha[0] == alpha[2]
    f = roe_flux(ql, qr)
    assert abs(f[0] + c * alpha[0]) < 1e-14 and abs(f[1] - 0.55) < 1e-14 and abs(f[2] + c * alpha[0] * h) < 1e-14
    assert abs(f[0] - 0.390660) < 1e-6 and abs(f[2] - 1.295882) < 1e-6


def test_property_u() -> None:
    rng = random.Random(4)
    for _ in range(100):
        ql = prim_to_cons((rng.uniform(0.1, 3), rng.uniform(-3, 3), rng.uniform(0.1, 3)))
        qr = prim_to_cons((rng.uniform(0.1, 3), rng.uniform(-3, 3), rng.uniform(0.1, 3)))
        lam, vecs, alpha = roe_waves(ql, qr)
        df = [b - a for a, b in zip(euler_flux(ql), euler_flux(qr))]
        for i in range(3):
            assert abs(sum(alpha[k] * vecs[k][i] for k in range(3)) - (qr[i] - ql[i])) < 1e-11
            assert abs(sum(lam[k] * alpha[k] * vecs[k][i] for k in range(3)) - df[i]) < 1e-10 * (1 + abs(df[i]))


def test_consistency() -> None:
    rng = random.Random(1)
    for _ in range(50):
        q = prim_to_cons((rng.uniform(0.1, 2), rng.uniform(-2, 2), rng.uniform(0.1, 2)))
        assert all(abs(a - b) < 1e-12 for a, b in zip(roe_flux(q, q), euler_flux(q)))


def test_stationary_contact_is_kept_exactly() -> None:
    m = 40
    cells = [prim_to_cons((1.0 if j < m // 2 else 0.5, 0.0, 1.0)) for j in range(m)]
    cells, _ = solve_euler(cells, 1.0 / m, 0.1)
    w = [cons_to_prim(q) for q in cells]
    assert all(abs(x[0] - (1.0 if j < m // 2 else 0.5)) < 1e-13 for j, x in enumerate(w))
    assert all(abs(x[1]) < 1e-13 and abs(x[2] - 1.0) < 1e-13 for x in w)


def test_stationary_shock_is_kept_exactly() -> None:
    a, b = normal_shock(2.0)
    assert abs(b[0] - 8.0 / 3.0) < 1e-14 and abs(b[2] - 4.5) < 1e-14
    cells = [prim_to_cons(a if j < 20 else b) for j in range(40)]
    out = run_steps(cells, 30)
    assert all(abs(x - y) < 1e-12 for p, q in zip(cells, out) for x, y in zip(p, q))


def test_stationary_expansion_shock_is_also_kept() -> None:
    a, b = normal_shock(2.0)
    cells = [prim_to_cons(b if j < 20 else a) for j in range(40)]  # subsonic to supersonic: violates the entropy condition
    out = run_steps(cells, 30)
    assert all(abs(x - y) < 1e-12 for p, q in zip(cells, out) for x, y in zip(p, q))
    u = [-1.0] * 10 + [1.0] * 10  # the same for Burgers' equation
    out = step(u, 0.05, 0.1, lambda x, y: roe_scalar(x, y, lambda v: v * v / 2, lambda v: v))
    assert out == u


def test_sod_l1_error_decreases() -> None:
    e100, e200 = sod_l1(100), sod_l1(200)
    assert e200 < 0.0092 and e100 < 0.0137
    assert 0.4 < log2(e100 / e200) < 0.8


def test_first_order_on_a_smooth_wave() -> None:
    t, errs = 0.1, []
    for m in (25, 50, 100):
        cells = [prim_to_cons((r, 1.0, 1.0)) for r in density_wave(m, 0.0)]
        cells, _ = solve_euler(cells, 1.0 / m, t, periodic=True)
        errs.append(sum(abs(q[0] - e) for q, e in zip(cells, density_wave(m, t))) / m)
    orders = [log2(errs[i] / errs[i + 1]) for i in range(2)]
    assert all(abs(p - 1.0) < 0.2 for p in orders)


def test_conservation() -> None:
    m = 64
    cells = [prim_to_cons((r, 1.0, 1.0)) for r in density_wave(m, 0.0)]
    before = [sum(q[k] for q in cells) for k in range(3)]
    cells, _ = solve_euler(cells, 1.0 / m, 0.05, periodic=True)
    after = [sum(q[k] for q in cells) for k in range(3)]
    assert all(abs(a - b) <= 1e-12 * abs(a) for a, b in zip(before, after))
    rng = random.Random(2)
    u = [Fraction(rng.randint(-8, 8), 4) for _ in range(12)]
    total = sum(u)
    for _ in range(5):
        u = step(u, Fraction(1, 10), Fraction(1, 2), lambda x, y: roe_scalar(x, y, lambda v: v * v / 2, lambda v: v), periodic=True)
        assert sum(u) == total


def test_tvd_for_burgers() -> None:
    f, df = (lambda v: v * v / 2), (lambda v: v)
    m, dx = 80, 1.0 / 80
    u = [1.0 if 0.2 < (j + 0.5) * dx < 0.5 else -0.5 for j in range(m)]
    tv0 = sum(abs(u[j + 1] - u[j]) for j in range(m - 1))
    for _ in range(60):
        u = step(u, 0.9 * dx / max(abs(v) for v in u), dx, lambda x, y: roe_scalar(x, y, f, df))
        tv = sum(abs(u[j + 1] - u[j]) for j in range(m - 1))
        assert tv <= tv0 + 1e-12
        tv0 = tv


def test_negative_pressure_on_the_123_problem() -> None:
    m = 100
    cells = [prim_to_cons((1.0, -2.0, 0.4) if j < m // 2 else (1.0, 2.0, 0.4)) for j in range(m)]
    cells = run_steps(cells, 1)  # Roe's linearization is not positively conservative
    assert min(cons_to_prim(q)[2] for q in cells) < 0.0
