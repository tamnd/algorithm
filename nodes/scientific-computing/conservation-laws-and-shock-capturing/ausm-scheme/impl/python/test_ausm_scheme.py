# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ausm-scheme/. The authors are listed in prov/H6NW64.jsonl.

import random
from fractions import Fraction
from math import cos, log2, pi, sqrt

from ausm_scheme import ausm_flux, cons_to_prim, euler_flux, mach_split, pressure_split, prim_to_cons, solve_euler, step

SOD = ((1.0, 0.0, 1.0), (0.125, 0.0, 0.1))
G = 1.4


def exact_sod_density(xi, g=G):
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


def sod(m, flux=ausm_flux, t=0.2):
    cells = [prim_to_cons(SOD[0] if (j + 0.5) / m < 0.5 else SOD[1]) for j in range(m)]
    cells, n = solve_euler(cells, 1.0 / m, t, flux=flux)
    ex = [sum(exact_sod_density(((j + (k + 0.5) / 16) / m - 0.5) / t) for k in range(16)) / 16 for j in range(m)]
    return sum(abs(q[0] - e) for q, e in zip(cells, ex)) / m, n, cells


def rusanov(ql, qr):
    """Reference baseline: the Rusanov flux."""
    s = max(abs(w[1]) + sqrt(G * w[2] / w[0]) for w in (cons_to_prim(ql), cons_to_prim(qr)))
    fl, fr = euler_flux(ql), euler_flux(qr)
    return tuple(0.5 * (a + b) - 0.5 * s * (y - x) for a, b, x, y in zip(fl, fr, ql, qr))


def close(a, b, tol=1e-12):
    return all(abs(x - y) <= tol * (1.0 + abs(y)) for x, y in zip(a, b))


def test_split_values_by_hand() -> None:
    q = Fraction
    assert mach_split(q(1, 2)) == (q(9, 16), q(-1, 16))
    assert pressure_split(q(1, 2), q(1)) == (q(27, 32), q(5, 32))
    assert mach_split(q(0)) == (q(1, 4), q(-1, 4)) and pressure_split(q(0), q(1)) == (q(1, 2), q(1, 2))


def test_splits_add_up_and_have_signs() -> None:
    grid = [Fraction(k, 16) for k in range(-40, 41)]
    for m in grid:
        mp, mm = mach_split(m)
        pp, pm = pressure_split(m, Fraction(3))
        assert mp + mm == m and pp + pm == 3
        assert mp >= 0 >= mm and pp >= 0 and pm >= 0
    for a, b in zip(grid, grid[1:]):  # M+, M- and p+ do not decrease in M, p- does not increase
        assert mach_split(a)[0] <= mach_split(b)[0] and mach_split(a)[1] <= mach_split(b)[1]
        assert pressure_split(a, 1)[0] <= pressure_split(b, 1)[0] and pressure_split(a, 1)[1] >= pressure_split(b, 1)[1]


def test_splits_are_smooth_at_the_sonic_points() -> None:
    h = Fraction(1, 1000)
    for s in (1, -1):
        one = Fraction(s)
        for f in (lambda m: mach_split(m)[0], lambda m: mach_split(m)[1], lambda m: pressure_split(m, 1)[0], lambda m: pressure_split(m, 1)[1]):
            inside, outside = (f(one - s * h) - f(one)) / (-s * h), (f(one + s * h) - f(one)) / (s * h)
            assert abs(inside - outside) <= h  # the one-sided slopes agree up to O(h)


def test_consistency_with_the_euler_flux() -> None:
    rng = random.Random(5)
    for _ in range(200):
        q = prim_to_cons((rng.uniform(0.1, 3.0), rng.uniform(-4.0, 4.0), rng.uniform(0.1, 3.0)))
        assert close(ausm_flux(q, q), euler_flux(q))


def test_supersonic_flow_is_pure_upwinding() -> None:
    rng = random.Random(7)
    for _ in range(100):
        wl, wr = [(rng.uniform(0.1, 2.0), 0.0, rng.uniform(0.1, 2.0)) for _ in range(2)]
        cl, cr = sqrt(G * wl[2] / wl[0]), sqrt(G * wr[2] / wr[0])
        speed = rng.uniform(1.0, 3.0) * max(cl, cr)
        ql, qr = prim_to_cons((wl[0], speed, wl[2])), prim_to_cons((wr[0], speed, wr[2]))
        assert close(ausm_flux(ql, qr), euler_flux(ql))
        ql, qr = prim_to_cons((wl[0], -speed, wl[2])), prim_to_cons((wr[0], -speed, wr[2]))
        assert close(ausm_flux(ql, qr), euler_flux(qr))


def test_face_fluxes_by_hand() -> None:
    ql, qr = prim_to_cons(SOD[0]), prim_to_cons(SOD[1])
    assert close(ausm_flux(ql, qr), (0.0, 0.55, 0.0))  # states at rest: no mass or energy crosses
    got = ausm_flux(prim_to_cons((1.0, 0.5, 1.0)), prim_to_cons((0.5, 0.5, 1.0)))
    assert close(got, (0.453188, 1.307226, 1.642806), 1e-6)


def test_stationary_contact_is_kept_exactly() -> None:
    m = 100
    cells = [prim_to_cons((1.0 if (j + 0.5) / m < 0.5 else 0.125, 0.0, 1.0)) for j in range(m)]
    out, n = solve_euler(cells, 1.0 / m, 0.1)
    assert out == cells and n == 67


def test_first_step_pressure_bound() -> None:
    # Two states at rest: the cell right of the jump gains momentum lam (pL - pR) / 2 and keeps rho and E.
    (rl, _, pl), (rr, _, pr) = SOD
    lam_star = 2.0 / (pl - pr) * sqrt(2.0 * rr * pr / (G - 1.0))
    cells = [prim_to_cons(SOD[0])] * 4 + [prim_to_cons(SOD[1])] * 4
    for f in (0.99, 1.01):
        lam = f * lam_star
        new = step(cells, lam, 1.0)
        p = (G - 1.0) * (new[4][2] - 0.5 * new[4][1] ** 2 / new[4][0])
        assert abs(p - (pr - (G - 1.0) * (lam * (pl - pr) / 2.0) ** 2 / (2.0 * rr))) < 1e-12
        assert (p > 0.0) == (f < 1.0)
    assert abs(lam_star * sqrt(G * pl / rl) - 0.6574) < 1e-4  # the largest safe Courant number for Sod


def test_sod_against_the_exact_solution() -> None:
    e100, n, cells = sod(100)
    assert n == 87 and abs(e100 - 0.01484) < 5e-5
    e50, _, _ = sod(50)
    assert abs(e50 - 0.0225) < 1e-4 and e100 < e50
    assert e100 < sod(100, rusanov)[0]  # sharper than the Rusanov baseline
    u = [cons_to_prim(q)[1] for q in cells]
    assert 1.0 < max(u) < 1.02  # the glitch in the first cell right of the jump; exact u* = 0.9274


def test_first_order_on_a_smooth_wave() -> None:
    t, errs = 0.1, []
    for m in (25, 50, 100):
        dx = 1.0 / m
        avg = lambda j, s: (cos(2 * pi * (j * dx - s)) - cos(2 * pi * ((j + 1) * dx - s))) / (2 * pi * dx)
        cells = [prim_to_cons((1.0 + 0.2 * avg(j, 0.0), 1.0, 1.0)) for j in range(m)]
        out, _ = solve_euler(cells, dx, t, periodic=True)
        errs.append(sum(abs(q[0] - 1.0 - 0.2 * avg(j, t)) for j, q in enumerate(out)) * dx)
    assert abs(errs[0] - 0.007065) < 1e-6
    assert all(0.95 < log2(errs[i] / errs[i + 1]) < 1.05 for i in range(2))


def test_moving_contact_is_not_kept() -> None:
    m = 100
    cells = [prim_to_cons((1.0 if (j + 0.5) / m < 0.3 else 0.125, 1.0, 1.0)) for j in range(m)]
    out, _ = solve_euler(cells, 1.0 / m, 0.2)
    dev = max(abs(cons_to_prim(q)[1] - 1.0) for q in out)
    assert 0.02 < dev < 0.04  # u and p are no longer constant
