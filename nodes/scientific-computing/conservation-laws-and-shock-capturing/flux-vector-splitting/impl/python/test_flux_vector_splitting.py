# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flux-vector-splitting/. The authors are listed in prov/6X7CE5.jsonl.

import random
from math import cos, log2, pi, sqrt

from flux_vector_splitting import (
    cons_to_prim,
    euler_flux,
    fvs_flux,
    fvs_scalar,
    prim_to_cons,
    solve_euler,
    step,
    steger_warming,
    van_leer,
)

SOD = ((1.0, 0.0, 1.0), (0.125, 0.0, 0.1))
G = 1.4


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


def sod_l1(m, split, t=0.2):
    """L1 error of the density against exact cell averages (16-point midpoint rule per cell)."""
    sample = exact_solution(*SOD)
    cells = [prim_to_cons(SOD[0] if (j + 0.5) / m < 0.5 else SOD[1]) for j in range(m)]
    cells, _ = solve_euler(cells, 1.0 / m, t, split=split)
    err = 0.0
    for j, q in enumerate(cells):
        ex = sum(sample(((j + (k + 0.5) / 16) / m - 0.5) / t)[0] for k in range(16)) / 16
        err += abs(q[0] - ex) / m
    return err


def density_wave(m, t):
    """Exact cell averages of rho = 1 + 0.2 sin(2 pi (x - t)), with u = 1 and p = 1."""
    dx = 1.0 / m
    return [1.0 + 0.2 * (cos(2 * pi * (j * dx - t)) - cos(2 * pi * ((j + 1) * dx - t))) / (2 * pi * dx) for j in range(m)]


def random_state(rng, umax=2.0):
    return prim_to_cons((rng.uniform(0.1, 2), rng.uniform(-umax, umax), rng.uniform(0.1, 2)))


def close(a, b, tol=1e-12):
    return all(abs(x - y) <= tol * (1.0 + abs(y)) for x, y in zip(a, b))


def jacobian(f, q, h=1e-6):
    cols = []
    for k in range(3):
        a, b = list(q), list(q)
        a[k] += h
        b[k] -= h
        cols.append([(x - y) / (2 * h) for x, y in zip(f(tuple(a)), f(tuple(b)))])
    return [[cols[j][i] for j in range(3)] for i in range(3)]


def char_poly(a):
    """Trace, sum of principal 2 by 2 minors, determinant: lambda^3 - t lambda^2 + s lambda - d."""
    t = a[0][0] + a[1][1] + a[2][2]
    s = sum(a[i][i] * a[j][j] - a[i][j] * a[j][i] for i in range(3) for j in range(i + 1, 3))
    d = a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1]) - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0]) + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    return t, s, d


def test_sod_interface_by_hand() -> None:
    ql, qr = prim_to_cons(SOD[0]), prim_to_cons(SOD[1])
    cl, cr = sqrt(G), sqrt(G * 0.1 / 0.125)
    # at u = 0: Steger-Warming gives rho c / (2 gamma) and rho c^3 / (2 gamma (gamma - 1)); van Leer rho c / 4 and rho c^3 / (2 (gamma^2 - 1))
    sw = ((cl - 0.125 * cr) / (2 * G), 0.55, (cl**3 - 0.125 * cr**3) / (2 * G * (G - 1)))
    vl = ((cl - 0.125 * cr) / 4, 0.55, (cl**3 - 0.125 * cr**3) / (2 * (G * G - 1)))
    assert close(fvs_flux(ql, qr, steger_warming), sw) and close(fvs_flux(ql, qr, van_leer), vl)
    assert abs(sw[0] - 0.375332) < 1e-6 and abs(vl[0] - 0.262732) < 1e-6 and abs(vl[2] - 0.785594) < 1e-6


def test_the_parts_add_up_to_the_flux() -> None:
    rng = random.Random(7)
    for _ in range(200):
        q = random_state(rng, 4.0)
        for split in (steger_warming, van_leer):
            fp, fm = split(q)
            assert close(tuple(a + b for a, b in zip(fp, fm)), euler_flux(q))
            assert close(fvs_flux(q, q, split), euler_flux(q))


def test_steger_warming_is_homogeneous() -> None:
    rng = random.Random(8)
    for _ in range(50):
        q, s = random_state(rng), rng.uniform(0.2, 5.0)
        sq = tuple(s * x for x in q)
        assert close(euler_flux(sq), tuple(s * x for x in euler_flux(q)))
        assert close(steger_warming(sq)[0], tuple(s * x for x in steger_warming(q)[0]))


def test_supersonic_flow_is_pure_upwind() -> None:
    rng = random.Random(9)
    for _ in range(50):
        rho, p = rng.uniform(0.1, 2), rng.uniform(0.1, 2)
        u = sqrt(G * p / rho) * rng.uniform(1.0, 3.0)
        q = prim_to_cons((rho, u, p))
        for split in (steger_warming, van_leer):
            fp, fm = split(q)
            assert close(fp, euler_flux(q)) and all(abs(x) < 1e-12 for x in fm)
            qm = prim_to_cons((rho, -u, p))
            assert close(split(qm)[1], euler_flux(qm)) and all(abs(x) < 1e-12 for x in split(qm)[0])


def test_van_leer_parts_are_smooth_at_the_sonic_point() -> None:
    for eps in (1e-2, 1e-3, 1e-4):
        q = prim_to_cons((1.0, (1.0 - eps) * sqrt(G), 1.0))
        assert max(abs(x) for x in van_leer(q)[1]) < 3.0 * eps * eps  # F- vanishes to second order at M = 1


def test_van_leer_jacobian_has_one_zero_eigenvalue() -> None:
    rng = random.Random(10)
    for _ in range(30):
        rho, p = rng.uniform(0.3, 2), rng.uniform(0.3, 2)
        q = prim_to_cons((rho, rng.uniform(-0.95, 0.95) * sqrt(G * p / rho), p))
        tp, sp, dp = char_poly(jacobian(lambda z: van_leer(z)[0], q))
        tm, sm, dm = char_poly(jacobian(lambda z: van_leer(z)[1], q))
        assert abs(dp) < 1e-6 and abs(dm) < 1e-6  # one eigenvalue is 0
        assert tp > 0 and sp > -1e-8 and tm < 0 and sm > -1e-8  # the other two: >= 0 for F+, <= 0 for F-


def test_a_contact_at_rest_is_smeared() -> None:
    a, b = prim_to_cons((1.0, 0.0, 1.0)), prim_to_cons((0.125, 0.0, 1.0))
    assert abs(fvs_flux(a, b)[0] - (sqrt(G) - 0.125 * sqrt(G / 0.125)) / 4) < 1e-12  # mass crosses the face
    cells, _ = solve_euler([a if j < 50 else b for j in range(100)], 0.01, 0.1)
    assert max(abs(cons_to_prim(q)[1]) for q in cells) > 0.02  # a velocity appears where there should be none
    assert sum(1 for q in cells if 0.2 < q[0] < 0.9) >= 5


def test_burgers_splitting_is_tvd() -> None:
    fp, fm = (lambda v: max(v, 0.0) ** 2 / 2), (lambda v: min(v, 0.0) ** 2 / 2)
    rng = random.Random(11)
    u = [rng.uniform(-1, 1) for _ in range(80)]
    tv = lambda w: sum(abs(w[j + 1] - w[j]) for j in range(len(w) - 1))
    for _ in range(40):
        before = tv(u)
        dx = 1.0 / 80
        u = step(u, 0.9 * dx / max(abs(v) for v in u), dx, lambda a, b: fvs_scalar(a, b, fp, fm))  # lam (f+' - f-') <= 0.9
        assert tv(u) <= before + 1e-12


def test_sod_converges() -> None:
    e100, e200 = sod_l1(100, van_leer), sod_l1(200, van_leer)
    s200 = sod_l1(200, steger_warming)
    assert e100 < 0.016 and e200 < 0.011 and s200 < 0.014 and e200 < s200


def test_first_order_on_a_smooth_wave() -> None:
    errs = []
    for m in (25, 50, 100):
        cells = [prim_to_cons((r, 1.0, 1.0)) for r in density_wave(m, 0.0)]
        out, _ = solve_euler(cells, 1.0 / m, 0.1, periodic=True)
        errs.append(sum(abs(q[0] - e) for q, e in zip(out, density_wave(m, 0.1))) / m)
    orders = [log2(errs[i] / errs[i + 1]) for i in range(2)]
    assert all(0.9 < o < 1.1 for o in orders)


def test_conservation_on_a_periodic_grid() -> None:
    rng = random.Random(12)
    cells = [random_state(rng, 0.5) for _ in range(40)]
    out, _ = solve_euler(cells, 1.0 / 40, 0.05, periodic=True, split=steger_warming)
    for i in range(3):
        assert abs(sum(q[i] for q in out) - sum(q[i] for q in cells)) < 1e-11
