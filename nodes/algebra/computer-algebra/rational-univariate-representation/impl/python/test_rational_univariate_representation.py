# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rational-univariate-representation/. The authors are listed in prov/KJ9098.jsonl.
"""Tests for the rational univariate representation over Q.

The references are the defining properties: the zeros of fbar, mapped by the
rational functions g_i / g_1, give exactly the known solution set, with the
multiplicities in g_1; every generator vanishes on the parametrization modulo
fbar; and the characteristic polynomial of M_u matches a determinant.
"""

import random
from fractions import Fraction

import pytest

from rational_univariate_representation import (
    _deriv, _udivmod, _ugcd, groebner, normal_set, rur, _reduce)


def P(d: dict) -> dict:
    return {k: Fraction(v) for k, v in d.items() if v}


def ueval(p: list, t: Fraction) -> Fraction:
    r = Fraction(0)
    for c in reversed(p):
        r = r * t + c
    return r


def umul(a: list, b: list) -> list:
    if not a or not b:
        return []
    r = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] += x * y
    return r


def uadd(a: list, b: list) -> list:
    r = [Fraction(0)] * max(len(a), len(b))
    for i, x in enumerate(a):
        r[i] += x
    for i, x in enumerate(b):
        r[i] += x
    while r and r[-1] == 0:
        r.pop()
    return r


def mpoly_from_lin(coeffs: list, const, n: int) -> dict:
    """The linear polynomial const + sum coeffs[i] x_i."""
    d = {tuple(int(j == i) for j in range(n)): Fraction(c) for i, c in enumerate(coeffs)}
    d[tuple([0] * n)] = Fraction(const)
    return P(d)


def mmul(f: dict, g: dict) -> dict:
    r: dict = {}
    for a, x in f.items():
        for b, y in g.items():
            k = tuple(i + j for i, j in zip(a, b))
            r[k] = r.get(k, Fraction(0)) + x * y
    return P(r)


def madd(f: dict, g: dict) -> dict:
    r = dict(f)
    for k, v in g.items():
        r[k] = r.get(k, Fraction(0)) + v
    return P(r)


def upoly_in(lin: dict, p: list, n: int) -> dict:
    """p(lin) for a univariate p and a multivariate lin, by Horner."""
    r: dict = {}
    for c in reversed(p):
        r = madd(mmul(r, lin), {tuple([0] * n): Fraction(c)})
    return r


def inv3(A: list) -> list:
    """Inverse of a small square matrix over Q (Gauss-Jordan)."""
    n = len(A)
    M = [[Fraction(x) for x in row] + [Fraction(int(i == j)) for j in range(n)]
         for i, row in enumerate(A)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c])
        M[c], M[p] = M[p], M[c]
        M[c] = [x / M[c][c] for x in M[c]]
        for r in range(n):
            if r != c and M[r][c]:
                f = M[r][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [row[n:] for row in M]


def lagrange(xs: list, ys: list) -> list:
    out: list = []
    for i, (xi, yi) in enumerate(zip(xs, ys)):
        term = [Fraction(yi)]
        for j, xj in enumerate(xs):
            if j != i:
                term = umul(term, [Fraction(-xj, xi - xj), Fraction(1, xi - xj)])
        out = uadd(out, term)
    return out


def ideal_with_points(rng: random.Random, n: int, k: int, maxmult: int) -> tuple:
    """Generators of an ideal whose zeros are k known rational points.

    In coordinates z = A x the ideal is <q(z_1), z_i - L_i(z_1)> with
    q = prod (z_1 - a_j)^(m_j); then the generators are mixed by adding
    random multiples of each other, which keeps the ideal.
    """
    while True:
        A = [[rng.randint(-2, 2) for _ in range(n)] for _ in range(n)]
        try:
            Ainv = inv3(A)
            break
        except StopIteration:
            continue
    a = rng.sample(range(-4, 5), k)
    mult = [rng.randint(1, maxmult) for _ in range(k)]
    zvals = [[Fraction(a[j])] + [Fraction(rng.randint(-3, 3)) for _ in range(n - 1)]
             for j in range(k)]
    z = [mpoly_from_lin(A[i], 0, n) for i in range(n)]  # z_i as polynomials in x
    q = [Fraction(1)]
    for aj, mj in zip(a, mult):
        for _ in range(mj):
            q = umul(q, [Fraction(-aj), Fraction(1)])
    gens = [upoly_in(z[0], q, n)]
    for i in range(1, n):
        L = lagrange([v[0] for v in zvals], [v[i] for v in zvals])
        gens.append(madd(z[i], {m: -c for m, c in upoly_in(z[0], L, n).items()}))
    for _ in range(n):
        i, j = rng.sample(range(n), 2) if n > 1 else (0, 0)
        if i != j:
            r = mpoly_from_lin([rng.randint(-1, 1) for _ in range(n)], rng.randint(-1, 1), n)
            gens[i] = madd(gens[i], mmul(r, gens[j]))
    points = [[sum(Ainv[i][j] * v[j] for j in range(n)) for i in range(n)] for v in zvals]
    return gens, points, mult


def check_against_points(gens: list, n: int, points: list, mult: list) -> None:
    lam, fbar, g1, gs = rur(gens, n)
    us = [sum(l * c for l, c in zip(lam, p)) for p in points]
    assert len(set(us)) == len(points)  # u separates the points
    expect = [Fraction(1)]
    for t in us:
        expect = umul(expect, [-t, Fraction(1)])
    assert fbar == expect
    assert len(g1) <= len(fbar) - 1 and all(len(g) <= len(fbar) - 1 for g in gs)
    for p, m, t in zip(points, mult, us):
        den = ueval(g1, t)
        prod = Fraction(m)
        for s in us:
            if s != t:
                prod *= t - s
        assert den == prod  # multiplicity is encoded in g1
        assert [ueval(g, t) / den for g in gs] == p


def test_examples():
    F = [P({(2, 0): 1, (0, 2): 1, (0, 0): -5}), P({(1, 1): 1, (0, 0): -2})]
    lam, fbar, g1, gs = rur(F, 2)
    assert lam == [1, 0]
    assert fbar == [4, 0, -5, 0, 1]
    assert g1 == [0, -10, 0, 4]
    assert gs == [[-16, 0, 10], [-20, 0, 8]]
    F = [P({(2, 0): 1, (0, 0): -1}), P({(0, 2): 1, (0, 0): -1})]
    lam, fbar, g1, gs = rur(F, 2)
    assert lam == [1, 2] and fbar == [9, 0, -10, 0, 1]
    assert g1 == [0, -20, 0, 4] and gs == [[12, 0, 4], [-24, 0, 8]]
    check_against_points(F, 2, [[1, 1], [1, -1], [-1, 1], [-1, -1]], [1, 1, 1, 1])


def test_edges():
    # unit ideal and an ideal with no zeros
    assert rur([P({(0, 0): 3})], 2)[1] == [1]
    assert rur([P({(1,): 1}), P({(1,): 1, (0,): -1})], 1)[1:] == ([1], [], [[]])
    # zero polynomials among the generators are ignored
    F = [P({}), P({(1, 0): 1, (0, 0): -2}), P({(0, 1): 1, (0, 0): 3})]
    check_against_points(F, 2, [[2, -3]], [1])
    # one variable with a double root
    F = [P({(3,): 1, (2,): -3, (0,): 4})]  # (x - 2)^2 (x + 1)
    check_against_points(F, 1, [[2], [-1]], [2, 1])
    # a fat point: <x^2, y - x> has one zero of multiplicity 2
    check_against_points([P({(2, 0): 1}), P({(0, 1): 1, (1, 0): -1})], 2, [[0, 0]], [2])
    # three variables, a single point
    F = [mpoly_from_lin([1, 0, 0], -1, 3), mpoly_from_lin([0, 1, 0], 2, 3),
         mpoly_from_lin([0, 0, 1], 0, 3)]
    check_against_points(F, 3, [[1, -2, 0]], [1])
    # positive dimension is rejected
    with pytest.raises(ValueError):
        rur([P({(1, 1): 1})], 2)
    with pytest.raises(ValueError):
        rur([P({(1, 0, 0): 1, (0, 1, 0): -1})], 3)


@pytest.mark.parametrize("seed", range(6))
def test_known_points(seed):
    rng = random.Random(1000 + seed)
    for _ in range(50):
        n = rng.choice([1, 2, 2, 3])
        k = rng.randint(1, 4 if n < 3 else 2)
        gens, points, mult = ideal_with_points(rng, n, k, 2 if n < 3 else 1)
        check_against_points(gens, n, points, mult)


def det(M: list) -> Fraction:
    M = [row[:] for row in M]
    n, d = len(M), Fraction(1)
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c]), None)
        if p is None:
            return Fraction(0)
        if p != c:
            M[c], M[p] = M[p], M[c]
            d = -d
        d *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return d


@pytest.mark.parametrize("seed", range(4))
def test_random_dense_systems(seed):
    """Two random quadrics in two variables: the parametrization satisfies them."""
    rng = random.Random(77 + seed)
    done = 0
    while done < 50:
        mons = [(2, 0), (1, 1), (0, 2), (1, 0), (0, 1), (0, 0)]
        F = [P({m: rng.randint(-3, 3) for m in mons}) for _ in range(2)]
        try:
            lam, fbar, g1, gs = rur(F, 2)
        except ValueError:
            continue
        done += 1
        if len(fbar) == 1:
            continue
        # fbar squarefree and g1 invertible modulo fbar
        assert len(_ugcd(fbar, _deriv(fbar))) == 1
        assert len(_ugcd(fbar, g1)) == 1
        for f in F:
            deg = max(sum(e) for e in f) if f else 0
            num: list = []
            for e, c in f.items():
                term = [c]
                for i, k in enumerate(e):
                    for _ in range(k):
                        term = umul(term, gs[i])
                for _ in range(deg - sum(e)):
                    term = umul(term, g1)
                num = uadd(num, term)
            assert _udivmod(num, fbar)[1] == []
        # D equals the degree of det(T I - M_u), checked at a few values of T
        G = groebner(F, 2)
        B = normal_set(G, 2)
        D = len(B)
        idx = {b: k for k, b in enumerate(B)}
        Mu = [[Fraction(0)] * D for _ in range(D)]
        for col, b in enumerate(B):
            for i in range(2):
                xb = b[:i] + (b[i] + 1,) + b[i + 1:]
                for e, c in _reduce({xb: Fraction(1)}, G).items():
                    Mu[idx[e]][col] += lam[i] * c
        xs = list(range(D + 1))
        vals = [det([[Fraction(t) * (r == c) - Mu[r][c] for c in range(D)]
                     for r in range(D)]) for t in xs]
        charpoly = lagrange(xs, vals)
        assert len(charpoly) == D + 1 and charpoly[-1] == 1
        sqf = _udivmod(charpoly, _ugcd(charpoly, _deriv(charpoly)))[0]
        assert [c / sqf[-1] for c in sqf] == fbar
