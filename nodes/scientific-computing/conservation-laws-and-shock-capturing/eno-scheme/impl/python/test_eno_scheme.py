# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eno-scheme/. The authors are listed in prov/Z4ZSZ2.jsonl.

import random
from fractions import Fraction
from math import cos, log2, pi, sqrt

from eno_scheme import eno_faces, face_weights, prim_to_cons, solve_euler, step

SOD = ((1.0, 0.0, 1.0), (0.125, 0.0, 0.1))
IDENT, ONE = (lambda v: v), (lambda v: 1.0)


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


def sod_l1(m, r, t=0.2):
    cells = [prim_to_cons(SOD[0] if (j + 0.5) / m < 0.5 else SOD[1]) for j in range(m)]
    cells, _ = solve_euler(cells, 1.0 / m, t, r=r)
    err = 0.0
    for j, q in enumerate(cells):
        ex = sum(exact_sod_density(((j + (k + 0.5) / 16) / m - 0.5) / t) for k in range(16)) / 16
        err += abs(q[0] - ex) / m
    return err


def averages(m, t):
    """Exact cell averages of sin(2 pi (x - t)) on [0, 1]."""
    dx = 1.0 / m
    return [(cos(2 * pi * (j * dx - t)) - cos(2 * pi * ((j + 1) * dx - t))) / (2 * pi * dx) for j in range(m)]


def advect(m, r, nu=0.5, t=1.0):
    dx = 1.0 / m
    n = round(t / (nu * dx))
    u = averages(m, 0.0)
    for _ in range(n):
        u = step(u, t / n, dx, IDENT, ONE, r, True)
    e = [a - b for a, b in zip(u, averages(m, t))]
    return sum(abs(x) for x in e) * dx


def brute_weights(r, x):
    """Reference: fit the polynomial of degree r - 1 whose averages over the unit cells [n, n + 1]
    are the unit vectors, by Gaussian elimination in Fraction, and evaluate it at x."""
    out = []
    for target in range(r):
        a = [[Fraction((n + 1) ** (p + 1) - n ** (p + 1), p + 1) for p in range(r)] + [Fraction(int(n == target))] for n in range(r)]
        for c in range(r):
            piv = next(i for i in range(c, r) if a[i][c] != 0)
            a[c], a[piv] = a[piv], a[c]
            for i in range(r):
                if i != c:
                    f = a[i][c] / a[c][c]
                    a[i] = [x1 - f * x2 for x1, x2 in zip(a[i], a[c])]
        coef = [a[p][r] / a[p][p] for p in range(r)]
        out.append(sum(cf * Fraction(x) ** p for p, cf in enumerate(coef)))
    return tuple(out)


def test_weights_match_a_brute_force_fit() -> None:
    for r in (1, 2, 3, 4):
        for k in range(r):
            wr, wl = face_weights(r, k)
            assert wr == brute_weights(r, k + 1) and wl == brute_weights(r, k)
            assert sum(wr) == 1 and sum(wl) == 1
    assert face_weights(3, 1)[0] == (Fraction(-1, 6), Fraction(5, 6), Fraction(1, 3))


def test_polynomials_are_reconstructed_exactly() -> None:
    rng = random.Random(7)
    for r in (2, 3, 4):
        coef = [Fraction(rng.randint(-5, 5)) for _ in range(r)]
        prim = lambda x: sum(c * Fraction(x) ** (p + 1) / (p + 1) for p, c in enumerate(coef))
        poly = lambda x: sum(c * Fraction(x) ** p for p, c in enumerate(coef))
        v = [prim(n + 1) - prim(n) for n in range(-r, 12 + r)]  # averages over [n, n + 1]
        minus, plus = eno_faces(v, r)
        assert minus == [poly(n + 1) for n in range(-1, 13)] and plus == [poly(n) for n in range(-1, 13)]


def test_hand_trace_in_fractions() -> None:
    u = [Fraction(x) for x in (0, 0, 1, 3, 4, 4)]
    minus, plus = eno_faces([u[0]] * 3 + u + [u[-1]] * 3, 3)
    assert minus == [0, 0, 0, Fraction(11, 6), Fraction(11, 3), 4, 4, 4]
    assert plus == [0, 0, 0, Fraction(1, 3), Fraction(13, 6), 4, 4, 4]


def test_stencils_avoid_jumps() -> None:
    # Piecewise constant data with jumps at least r cells apart: every face value is the cell value.
    for r in (2, 3, 4):
        u = [Fraction(x) for x in [0] * 6 + [5] * r + [2] * 6 + [-1] * r + [3] * 6]
        v = [u[0]] * r + u + [u[-1]] * r
        minus, plus = eno_faces(v, r)
        assert minus == plus == v[r - 1:len(v) - r + 1]


def test_exact_conservation_for_burgers_in_fractions() -> None:
    rng = random.Random(3)
    u = [Fraction(rng.randint(-8, 8), 4) for _ in range(10)]
    total = sum(u)
    for r in (1, 2, 3):
        v = step(u, Fraction(1, 10), Fraction(1, 2), lambda x: x * x / 2, abs, r, True)
        assert sum(v) == total


def test_constant_state() -> None:
    q = prim_to_cons((0.7, 0.3, 0.9))
    cells, _ = solve_euler([q] * 20, 0.05, 0.1)
    assert all(abs(a - b) < 1e-13 for c in cells for a, b in zip(c, q))


def test_order_r_on_smooth_advection() -> None:
    e1 = [advect(m, 1) for m in (20, 40)]
    e3 = [advect(m, 3) for m in (20, 40, 80)]
    assert abs(log2(e1[0] / e1[1]) - 0.69) < 0.02  # first order, still far from the asymptote
    assert all(abs(log2(e3[i] / e3[i + 1]) - 3.0) < 0.1 for i in range(2))
    assert abs(e3[0] - 0.0107088) < 1e-7


def test_third_order_on_a_smooth_euler_wave() -> None:
    t, errs = 0.1, []
    for m in (25, 50, 100):
        dx = 1.0 / m
        cells = [prim_to_cons((1.0 + 0.2 * r, 1.0, 1.0)) for r in averages(m, 0.0)]
        cells, _ = solve_euler(cells, dx, t, r=3, periodic=True)
        errs.append(sum(abs(q[0] - 1.0 - 0.2 * e) for q, e in zip(cells, averages(m, t))) * dx)
    assert all(abs(log2(errs[i] / errs[i + 1]) - 3.0) < 0.1 for i in range(2))


def test_small_overshoot_on_a_square_wave() -> None:
    m = 80
    u = [1.0 if 20 <= j < 40 else 0.0 for j in range(m)]
    for _ in range(80):
        u = step(u, 0.5 / m, 1.0 / m, IDENT, ONE, 3, True)
    over = max(u) - 1.0
    assert 1e-6 < over < 1e-4  # not TVD, but the overshoot is tiny
    assert min(u) > -1e-6


def test_sod_l1_error() -> None:
    e = [sod_l1(100, r) for r in (1, 2, 3)]
    assert abs(e[0] - 0.025915) < 5e-5 and abs(e[1] - 0.009678) < 5e-5 and abs(e[2] - 0.007662) < 5e-5
