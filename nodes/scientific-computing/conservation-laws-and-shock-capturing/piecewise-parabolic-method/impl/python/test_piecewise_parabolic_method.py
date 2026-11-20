# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/piecewise-parabolic-method/. The authors are listed in prov/4Q3HCS.jsonl.

import random
from fractions import Fraction
from math import cos, log2, pi, sqrt

from piecewise_parabolic_method import advect_step, parabola, ppm_faces, prim_to_cons, right_flux_average, solve_euler

SOD = ((1.0, 0.0, 1.0), (0.125, 0.0, 0.1))


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


def averages(m, t):
    """Exact cell averages of sin(2 pi (x - t)) on [0, 1]."""
    dx = 1.0 / m
    return [(cos(2 * pi * (j * dx - t)) - cos(2 * pi * ((j + 1) * dx - t))) / (2 * pi * dx) for j in range(m)]


def advect(m, nu=0.5, t=1.0):
    dx = 1.0 / m
    n = round(t / (nu * dx))
    u = averages(m, 0.0)
    for _ in range(n):
        u = advect_step(u, t / (n * dx))
    return sum(abs(a - b) for a, b in zip(u, averages(m, t))) * dx


def tv(u):
    return sum(abs(u[j] - u[j - 1]) for j in range(len(u)))


def test_hand_trace_in_fractions() -> None:
    u = [Fraction(x) for x in (0, 0, 1, 3, 4, 4)]
    q = Fraction
    assert ppm_faces(u) == [(0, 0), (0, 0), (q(1, 4), 2), (2, q(15, 4)), (4, 4), (4, 4)]
    assert advect_step(u, q(1, 2), periodic=False) == [0, 0, q(9, 32), 2, q(119, 32), 4]


def test_face_values_are_exact_for_cubics() -> None:
    # Averages of x^3 + x over [n, n + 1]: the slopes are not limited, so the faces use 7/12 and -1/12.
    prim = lambda x: Fraction(x) ** 4 / 4 + Fraction(x) ** 2 / 2
    v = [prim(n + 1) - prim(n) for n in range(2, 14)]
    pf = ppm_faces(v)
    for j in range(1, 10):
        x = Fraction(j + 3)
        assert pf[j][1] == x ** 3 + x == Fraction(7, 12) * (v[j] + v[j + 1]) - Fraction(1, 12) * (v[j - 1] + v[j + 2])


def test_flux_formula_matches_direct_integration() -> None:
    rng = random.Random(2)
    for _ in range(50):
        al, a, ar = (Fraction(rng.randint(-9, 9), 4) for _ in range(3))
        nu = Fraction(rng.randint(1, 10), 10)
        lo = 1 - nu  # Simpson's rule is exact for parabolas
        simpson = (parabola(al, a, ar, lo) + 4 * parabola(al, a, ar, (lo + 1) / 2) + parabola(al, a, ar, Fraction(1))) / 6
        assert right_flux_average(al, a, ar, nu) == simpson
        assert right_flux_average(al, a, ar, Fraction(1)) == a  # the mean of the parabola is the cell average


def test_parabolas_are_monotone_and_bounded() -> None:
    rng = random.Random(4)
    u = [Fraction(rng.randint(0, 20)) for _ in range(40)]
    pf = ppm_faces(u, periodic=True)
    for j, (al, ar) in enumerate(pf):
        lo, hi = min(u[j - 1], u[j], u[(j + 1) % 40]), max(u[j - 1], u[j], u[(j + 1) % 40])
        vals = [parabola(al, u[j], ar, Fraction(k, 16)) for k in range(17)]
        steps = [vals[k + 1] - vals[k] for k in range(16)]
        assert all(s >= 0 for s in steps) or all(s <= 0 for s in steps)
        assert all(lo <= x <= hi for x in vals)


def test_exact_conservation_in_fractions() -> None:
    rng = random.Random(3)
    u = [Fraction(rng.randint(-8, 8), 4) for _ in range(16)]
    total = sum(u)
    for _ in range(3):
        u = advect_step(u, Fraction(3, 7))
        assert sum(u) == total


def test_courant_one_is_an_exact_shift() -> None:
    rng = random.Random(6)
    u = [Fraction(rng.randint(0, 9)) for _ in range(12)]
    assert advect_step(u, Fraction(1)) == u[-1:] + u[:-1]


def test_tvd_and_no_new_extrema_for_advection() -> None:
    m = 80
    for nu in (0.3, 0.5, 0.9, 1.0):
        u = [1.0 if 20 <= j < 40 else (0.5 if 50 <= j < 55 else 0.0) for j in range(m)]
        t0 = tv(u)
        for _ in range(60):
            u = advect_step(u, nu)
            assert tv(u) <= t0 + 1e-12 and -1e-12 <= min(u) and max(u) <= 1.0 + 1e-12
            t0 = tv(u)
    rng = random.Random(1)
    for _ in range(100):
        u = [rng.random() for _ in range(30)]
        v = advect_step(u, rng.random())
        assert tv(v) <= tv(u) + 1e-12 and min(u) - 1e-12 <= min(v) and max(v) <= max(u) + 1e-12


def test_order_on_smooth_advection() -> None:
    e = [advect(m) for m in (20, 40, 80)]
    assert abs(e[0] - 0.0189537) < 1e-7
    assert all(2.2 < log2(e[i] / e[i + 1]) < 2.5 for i in range(2))  # above 2, below 3: clipped extrema


def test_euler_wave_and_sod() -> None:
    t, errs = 0.1, []
    for m in (25, 50, 100):
        dx = 1.0 / m
        cells = [prim_to_cons((1.0 + 0.2 * r, 1.0, 1.0)) for r in averages(m, 0.0)]
        cells, _ = solve_euler(cells, dx, t, periodic=True)
        errs.append(sum(abs(q[0] - 1.0 - 0.2 * e) for q, e in zip(cells, averages(m, t))) * dx)
    assert all(1.9 < log2(errs[i] / errs[i + 1]) < 2.3 for i in range(2))
    m, t = 100, 0.2
    cells = [prim_to_cons(SOD[0] if (j + 0.5) / m < 0.5 else SOD[1]) for j in range(m)]
    cells, n = solve_euler(cells, 1.0 / m, t)
    err = sum(abs(q[0] - sum(exact_sod_density(((j + (k + 0.5) / 16) / m - 0.5) / t) for k in range(16)) / 16) for j, q in enumerate(cells)) / m
    assert n == 87 and abs(err - 0.005261) < 5e-5
