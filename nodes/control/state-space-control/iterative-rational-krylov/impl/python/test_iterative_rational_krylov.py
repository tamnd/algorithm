# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-rational-krylov/. The authors are listed in prov/P106V2.jsonl.

import math
import random

from ctlmat import mul, solve, transpose
from iterative_rational_krylov import (
    default_shifts, h2_error, h2_norm, irka, poles, project, transfer,
    transfer_derivative,
)

CHAIN_A = [[-1, 1, 0, 0], [0, -2, 1, 0], [0, 0, -3, 1], [0, 0, 0, -4]]
CHAIN_B = [0, 0, 0, 1]
CHAIN_C = [1, 0, 0, 0]


def random_stable(rng, n):
    r = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    rho = max(sum(abs(v) for v in row) for row in r)
    a = [[r[i][j] - (rho + 0.3 if i == j else 0.0) for j in range(n)] for i in range(n)]
    b = [rng.uniform(-1, 1) for _ in range(n)]
    c = [rng.uniform(-1, 1) for _ in range(n)]
    return a, b, c


def assert_hermite(a, b, c, ar, br, cr, shifts, tol):
    for s in shifts:
        g, gr = transfer(a, b, c, s), transfer(ar, br, cr, s)
        dg, dgr = transfer_derivative(a, b, c, s), transfer_derivative(ar, br, cr, s)
        assert abs(g - gr) <= tol * (abs(g) + 1e-300)
        assert abs(dg - dgr) <= tol * (abs(dg) + 1e-300)


def test_h2_norm_of_first_order():
    # ||1/(s + a)||_H2^2 = 1/(2a)
    assert abs(h2_norm([[-1.0]], [1.0], [1.0]) - math.sqrt(0.5)) < 1e-14
    assert abs(h2_norm([[-3.0]], [2.0], [1.0]) - math.sqrt(4.0 / 6.0)) < 1e-14


def test_one_projection_interpolates_at_any_shifts():
    rng = random.Random(20)
    for _ in range(10):
        a, b, c = random_stable(rng, 6)
        shifts = [complex(rng.uniform(0.2, 3.0))]
        im = rng.uniform(0.2, 2.0)
        re = rng.uniform(0.2, 3.0)
        shifts += [complex(re, im), complex(re, -im)]
        ar, br, cr = project(a, b, c, shifts)
        assert len(ar) == 3
        assert_hermite(a, b, c, ar, br, cr, shifts, 1e-9)


def test_hermite_interpolation_on_500_random_projections():
    # oracle: G and G' evaluated directly from (A, b, c) by complex solves
    rng = random.Random(25)
    for _ in range(500):
        n = rng.randint(2, 4)
        a, b, c = random_stable(rng, n)
        r = rng.randint(1, n - 1)
        shifts = []
        while len(shifts) < r:
            if r - len(shifts) >= 2 and rng.random() < 0.5:
                re, im = rng.uniform(0.2, 3.0), rng.uniform(0.2, 2.0)
                shifts += [complex(re, im), complex(re, -im)]
            else:
                shifts.append(complex(rng.uniform(0.2, 3.0)))
        ar, br, cr = project(a, b, c, shifts)
        assert_hermite(a, b, c, ar, br, cr, shifts, 1e-7)


def test_real_and_complex_bases_give_the_same_model():
    rng = random.Random(21)
    a, b, c = random_stable(rng, 5)
    shifts = [complex(0.7, 0.9), complex(0.7, -0.9), complex(2.0, 0.0)]
    ar, br, cr = project(a, b, c, shifts)
    n = len(a)

    def col(mat, vecb, s):
        m = [[complex((s if i == j else 0) - mat[i][j]) for j in range(n)] for i in range(n)]
        return solve(m, [complex(x) for x in vecb])

    v = transpose([col(a, b, s) for s in shifts])
    w = transpose([col(transpose(a), c, s) for s in shifts])
    wt = transpose(w)
    e = mul(wt, v)
    ac = solve(e, mul(mul(wt, [[complex(x) for x in row] for row in a]), v))
    bc = solve(e, [sum(wt[i][k] * b[k] for k in range(n)) for i in range(3)])
    cc = [sum(c[k] * v[k][j] for k in range(n)) for j in range(3)]
    for s in [0.1j, 1.0 + 1.0j, 4.0, -0.5 + 3j]:
        g1, g2 = transfer(ar, br, cr, s), transfer(ac, bc, cc, s)
        assert abs(g1 - g2) < 1e-10 * abs(g1)


def test_converged_model_meets_h2_conditions():
    rng = random.Random(22)
    done = 0
    for _ in range(6):
        a, b, c = random_stable(rng, 6)
        for r in (1, 2, 3):
            ar, br, cr, s, it, ok = irka(a, b, c, r)
            if not ok:
                continue
            done += 1
            # the shifts are the mirror images of the reduced poles
            lam = sorted((-z for z in poles(ar)), key=lambda z: (round(z.real, 8), z.imag))
            ss = sorted(s, key=lambda z: (round(z.real, 8), z.imag))
            for x, y in zip(lam, ss):
                assert abs(x - y) < 1e-8 * abs(y)
            assert all(z.real < 0 for z in poles(ar))
            assert_hermite(a, b, c, ar, br, cr, s, 1e-7)
    assert done >= 15


def test_r1_against_brute_force():
    # For G_r = phi/(s + lam), the error is ||G||^2 - 2 phi G(lam) + phi^2/(2 lam).
    # The best phi is 2 lam G(lam), so the best lam maximizes 2 lam G(lam)^2.
    a, b, c = CHAIN_A, CHAIN_B, CHAIN_C

    def score(lam):
        return 2 * lam * transfer(a, b, c, lam).real ** 2

    grid = [10 ** (k / 2000.0) for k in range(-4000, 2001)]
    best = max(grid, key=score)
    lo, hi = best / 1.01, best * 1.01
    for _ in range(100):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if score(m1) < score(m2):
            lo = m1
        else:
            hi = m2
    lam = (lo + hi) / 2
    ar, br, cr, s, it, ok = irka(a, b, c, 1)
    assert ok
    assert abs(s[0].real - lam) < 1e-6 * lam
    g2 = h2_norm(a, b, c) ** 2
    assert abs(h2_error(a, b, c, ar, br, cr) - math.sqrt(g2 - score(lam))) < 1e-10


def test_chain_example_of_the_page():
    a, b, c = CHAIN_A, CHAIN_B, CHAIN_C
    assert abs(h2_norm(a, b, c) - 0.0222718) < 1e-7
    ar, br, cr, s, it, ok = irka(a, b, c, 2)
    assert ok
    assert abs(s[0] - complex(0.698811, -0.581699)) < 1e-6
    assert abs(h2_error(a, b, c, ar, br, cr) - 0.00281857) < 1e-8
    want = {1: 0.0127419, 3: 0.000223404}
    for r, e in want.items():
        red = irka(a, b, c, r)
        assert red[5]
        assert abs(h2_error(a, b, c, *red[:3]) - e) < 1e-6 * e * 10


def test_perturbations_do_not_lower_the_error():
    rng = random.Random(23)
    a, b, c = CHAIN_A, CHAIN_B, CHAIN_C
    ar, br, cr, s, it, ok = irka(a, b, c, 2)
    assert ok
    e0 = h2_error(a, b, c, ar, br, cr)
    for _ in range(40):
        d = 1e-3
        ap = [[x + d * rng.uniform(-1, 1) * abs(x) for x in row] for row in ar]
        bp = [x + d * rng.uniform(-1, 1) * abs(x) for x in br]
        cp = [x + d * rng.uniform(-1, 1) * abs(x) for x in cr]
        assert h2_error(a, b, c, ap, bp, cp) >= e0 - 1e-13


def test_full_order_reproduces_g():
    rng = random.Random(24)
    a, b, c = random_stable(rng, 4)
    ar, br, cr, s, it, ok = irka(a, b, c, 4)
    assert ok
    for z in [0.5j, 2.0, 1.0 + 3.0j]:
        g = transfer(a, b, c, z)
        assert abs(g - transfer(ar, br, cr, z)) < 1e-9 * abs(g)
    assert h2_error(a, b, c, ar, br, cr) < 1e-7 * h2_norm(a, b, c)


def test_default_shifts_are_positive_and_spread():
    s = default_shifts(CHAIN_A, 3)
    assert all(z.imag == 0 and z.real > 0 for z in s)
    assert s[0].real < s[1].real < s[2].real
