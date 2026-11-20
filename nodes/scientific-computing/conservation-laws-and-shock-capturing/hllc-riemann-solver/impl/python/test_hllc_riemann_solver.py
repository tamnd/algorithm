# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hllc-riemann-solver/. The authors are listed in prov/HQEZ7E.jsonl.

import random
from math import cos, log2, pi, sqrt

from hllc_riemann_solver import (
    cons_to_prim,
    contact_speed,
    euler_flux,
    hllc_flux,
    prim_to_cons,
    solve_euler,
    star_state,
    wave_speeds,
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


def random_state(rng):
    return prim_to_cons((rng.uniform(0.1, 2), rng.uniform(-1, 1), rng.uniform(0.1, 2)))


def test_flux_at_the_sod_interface_by_hand() -> None:
    ql, qr = prim_to_cons(SOD[0]), prim_to_cons(SOD[1])
    sl, sr = wave_speeds(ql, qr)
    ss = contact_speed(ql, qr, sl, sr)
    assert abs(ss - (0.1 - 1.0) / (sl - 0.125 * sr)) < 1e-14  # both velocities are 0
    st = star_state(ql, sl, ss)
    assert abs(st[0] - sl / (sl - ss)) < 1e-14
    f = hllc_flux(ql, qr)
    assert abs(f[0] - st[0] * ss) < 1e-14  # the mass flux through the face is rho*_L S*
    assert all(abs(a - (b + sl * (c - d))) < 1e-14 for a, b, c, d in zip(f, euler_flux(ql), st, ql))
    assert abs(ss - 0.678118) < 1e-6
    assert abs(f[0] - 0.431067) < 1e-6 and abs(f[1] - 0.489954) < 1e-6 and abs(f[2] - 1.162864) < 1e-6


def test_consistency() -> None:
    rng = random.Random(1)
    for _ in range(50):
        q = random_state(rng)
        assert all(abs(a - b) < 1e-12 for a, b in zip(hllc_flux(q, q), euler_flux(q)))


def test_middle_states_have_equal_pressure_and_velocity_and_match_the_hll_average() -> None:
    rng = random.Random(3)
    for _ in range(50):
        ql, qr = random_state(rng), random_state(rng)
        sl, sr = wave_speeds(ql, qr)
        ss = contact_speed(ql, qr, sl, sr)
        a, b = star_state(ql, sl, ss), star_state(qr, sr, ss)
        assert abs(a[1] / a[0] - ss) < 1e-12 and abs(b[1] / b[0] - ss) < 1e-12
        (rl, ul, pl), (rr, ur, pr) = cons_to_prim(ql), cons_to_prim(qr)
        p_left = pl + rl * (sl - ul) * (ss - ul)  # the middle pressure from the momentum jump condition
        p_right = pr + rr * (sr - ur) * (ss - ur)
        assert abs(p_left - p_right) < 1e-12 * (1 + abs(p_left))
        fl, fr = euler_flux(ql), euler_flux(qr)
        for q, s, st in ((ql, sl, a), (qr, sr, b)):  # the jump conditions across S_L and S_R
            fs = (st[1], st[1] * ss + p_left, ss * (st[2] + p_left))
            assert all(abs((fs[i] - euler_flux(q)[i]) - s * (st[i] - q[i])) < 1e-10 for i in range(3))
        for i in range(3):  # (S* - S_L) U*_L + (S_R - S*) U*_R = S_R U_R - S_L U_L - (F_R - F_L)
            lhs = (ss - sl) * a[i] + (sr - ss) * b[i]
            rhs = sr * qr[i] - sl * ql[i] - (fr[i] - fl[i])
            assert abs(lhs - rhs) < 1e-10 * (1 + abs(rhs))


def test_an_isolated_contact_gives_the_exact_flux() -> None:
    for u in (0.3, -0.3):
        ql, qr = prim_to_cons((1.0, u, 1.0)), prim_to_cons((0.5, u, 1.0))
        want = euler_flux(ql) if u > 0 else euler_flux(qr)
        assert all(abs(a - b) < 1e-13 for a, b in zip(hllc_flux(ql, qr), want))


def test_stationary_contact_is_kept_exactly() -> None:
    m = 40
    cells = [prim_to_cons((1.0 if j < m // 2 else 0.5, 0.0, 1.0)) for j in range(m)]
    cells, _ = solve_euler(cells, 1.0 / m, 0.1)
    w = [cons_to_prim(q) for q in cells]
    assert all(abs(x[0] - (1.0 if j < m // 2 else 0.5)) < 1e-13 for j, x in enumerate(w))
    assert all(abs(x[1]) < 1e-13 and abs(x[2] - 1.0) < 1e-13 for x in w)


def test_moving_contact_keeps_u_and_p() -> None:
    m = 100
    cells = [prim_to_cons((1.0 if 0.25 < (j + 0.5) / m < 0.75 else 0.5, 1.0, 1.0)) for j in range(m)]
    cells, _ = solve_euler(cells, 1.0 / m, 0.5, periodic=True)
    exact = [0.5 if 0.25 < ((j + 0.5) / m) % 1.0 < 0.75 else 1.0 for j in range(m)]  # moved by 0.5
    err = sum(abs(q[0] - e) for q, e in zip(cells, exact)) / m
    assert err < 0.05
    assert all(abs(cons_to_prim(q)[1] - 1.0) < 1e-13 and abs(cons_to_prim(q)[2] - 1.0) < 1e-13 for q in cells)


def test_sod_l1_error_decreases() -> None:
    e100, e200 = sod_l1(100), sod_l1(200)
    assert e200 < 0.0095 and e100 < 0.0142
    assert 0.4 < log2(e100 / e200) < 0.8


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


def test_positivity_on_the_123_problem() -> None:
    m = 100
    cells = [prim_to_cons((1.0, -2.0, 0.4) if j < m // 2 else (1.0, 2.0, 0.4)) for j in range(m)]
    cells, _ = solve_euler(cells, 1.0 / m, 0.15)
    w = [cons_to_prim(q) for q in cells]
    assert min(x[0] for x in w) > 0.01 and min(x[2] for x in w) > 0.0
