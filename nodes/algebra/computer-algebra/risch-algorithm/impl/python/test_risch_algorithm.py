# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/risch-algorithm/. The authors are listed in prov/GY4RMM.jsonl.
"""Tests for the Risch algorithm with one exponential monomial t = exp(b).

Every answer is checked by differentiation in Q(x)[t, 1/t]. Integrable cases
are built from known antiderivatives, and the answer must match them (the
rational parts y_k are unique). A FAIL answer is compared with a direct
linear algebra search for a rational solution of y' + k b' y = f_k.
"""

import random
from fractions import Fraction as Q

from risch_algorithm import (add, deg, deriv, exquo, gcd, hermite_reduce,
                             mul, norm, rat_add, rat_deriv, risch_exp, scale, sub)

ONE = [Q(1)]


def rat_eq(x, y):
    return not norm(sub(mul(x[0], y[1]), mul(y[0], x[1])))


def rat_mul(x, y):
    return (mul(x[0], y[0]), mul(x[1], y[1]))


def check(b, f, out):
    ys, R, rest = out
    db = deriv(b)
    for k in set(f) | set(ys):
        want = f.get(k, ([], ONE))
        if k == 0:
            got = rat_add(rat_deriv(R), rest)
        else:
            y = ys.get(k, ([], ONE))
            got = rat_add(rat_deriv(y), rat_mul((scale(db, k), ONE), y))
        assert rat_eq(got, want), k
    D = rest[1]
    assert deg(gcd(D, deriv(D))) <= 0  # squarefree


def rand_poly(rng, d, lo=-3, hi=3):
    return norm([rng.randint(lo, hi) for _ in range(d + 1)])


def rand_den(rng, maxpow=3):
    d = ONE
    for _ in range(rng.randint(0, 2)):
        p = norm([rng.randint(-3, 3), rng.choice([1, 2])] + ([1] if rng.random() < 0.3 else []))
        for _ in range(rng.randint(1, maxpow)):
            d = mul(d, p)
    return d


def brute_rde(fk, g):
    """Search y = q / d with deg q <= deg a + deg d + 2 by Gaussian elimination."""
    a, d = g
    N = deg(a) + deg(d) + 3
    cols = []
    for j in range(N):  # image of q = x^j in q' d - q d' + fk q d
        q = [Q(0)] * j + [Q(1)]
        cols.append(add(sub(mul(deriv(q), d), mul(q, deriv(d))), mul(mul(fk, q), d)))
    rhs = mul(a, d)
    rows = max([len(c) for c in cols] + [len(rhs)])
    M = [[(c[i] if i < len(c) else Q(0)) for c in cols] + [rhs[i] if i < len(rhs) else Q(0)]
         for i in range(rows)]
    r = 0
    for c in range(N):
        piv = next((i for i in range(r, rows) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                t = M[i][c] / M[r][c]
                M[i] = [x - t * y for x, y in zip(M[i], M[r])]
        r += 1
    return all(any(x != 0 for x in row[:N]) or row[N] == 0 for row in M)


def test_known():
    # e^(x^2) and e^x / x and x^2 e^(-x^2) have no elementary integral
    assert risch_exp([0, 0, 1], {1: ([1], ONE)}) is None
    assert risch_exp([0, 1], {1: ([1], [0, 1])}) is None
    assert risch_exp([0, 0, -1], {1: ([0, 0, 1], ONE)}) is None
    # x e^x = ((x - 1) e^x)'
    ys, R, rest = risch_exp([0, 1], {1: ([0, 1], ONE)})
    assert rat_eq(ys[1], ([-1, 1], ONE))
    # (2x^2 + 1) e^(x^2) = (x e^(x^2))'
    ys, _, _ = risch_exp([0, 0, 1], {1: ([1, 0, 2], ONE)})
    assert rat_eq(ys[1], ([0, 1], ONE))
    # (x - 1) / x^2 e^x = (e^x / x)'
    ys, _, _ = risch_exp([0, 1], {1: ([-1, 1], [0, 0, 1])})
    assert rat_eq(ys[1], (ONE, [0, 1]))


def test_edges():
    assert risch_exp([0, 1], {}) == ({}, ([], ONE), ([], ONE))
    out = risch_exp([0, 1], {0: ([5], ONE)})  # a constant
    check([Q(0), Q(1)], {0: ([5], ONE)}, out)
    out = risch_exp([0, 1], {2: ([], ONE), 0: ([], [1, 1])})  # zero coefficients
    assert out[0] == {}
    f = {-3: ([7], ONE)}  # negative power: 7 e^(-3x) = (-7/3 e^(-3x))'
    ys, _, _ = risch_exp([0, 1], f)
    assert rat_eq(ys[-3], ([Q(-7, 3)], ONE))
    f = {0: ([1], mul(mul([1, 0, 1], [1, 0, 1]), mul([1, 0, 1], [1, 0, 1])))}  # 1/(x^2+1)^4
    out = risch_exp([0, 1], f)
    check([Q(0), Q(1)], f, out)
    assert rat_eq((out[2][1], ONE), ([1, 0, 1], ONE))


def test_random_integrable():
    rng = random.Random(1)
    for _ in range(60):
        b = norm(rand_poly(rng, rng.randint(1, 3)))
        if deg(b) < 1:
            b = [Q(0), Q(1)]
        db = deriv(b)
        f, want = {}, {}
        for k in rng.sample([-2, -1, 1, 2, 3], rng.randint(1, 3)):
            y = (rand_poly(rng, rng.randint(0, 3)), rand_den(rng))
            g = gcd(*y) if y[0] else y[1]
            if not y[0]:
                continue
            y = (exquo(y[0], g), exquo(y[1], g))
            want[k] = y
            f[k] = rat_add(rat_deriv(y), rat_mul((scale(db, k), ONE), y))
        if rng.random() < 0.7:
            f[0] = (rand_poly(rng, rng.randint(0, 5)), rand_den(rng, 4))
        out = risch_exp(b, f)
        assert out is not None
        check(b, f, out)
        for k, y in want.items():
            assert rat_eq(out[0][k], y)


def test_random_against_brute_force():
    rng = random.Random(2)
    fails = 0
    for _ in range(80):
        b = norm(rand_poly(rng, rng.randint(1, 2)))
        if deg(b) < 1:
            b = [Q(0), Q(1)]
        k = rng.choice([-1, 1, 2])
        g = (rand_poly(rng, rng.randint(0, 3)), rand_den(rng, 2))
        if not g[0]:
            continue
        out = risch_exp(b, {k: g})
        assert (out is not None) == brute_rde(scale(deriv(b), k), g)
        if out is None:
            fails += 1
        else:
            check(b, {k: g}, out)
    assert fails > 20  # random integrands are usually not integrable


def test_hermite():
    rng = random.Random(3)
    for _ in range(40):
        A, D = rand_poly(rng, rng.randint(0, 8)), rand_den(rng, 5)
        if not A:
            continue
        R, rest = hermite_reduce(A, D)
        assert rat_eq(rat_add(rat_deriv(R), rest), (A, D))
        assert deg(gcd(rest[1], deriv(rest[1]))) <= 0
