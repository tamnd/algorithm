# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hermite-reduction/. The authors are listed in prov/4X5MRR.jsonl.

import random
from fractions import Fraction
from typing import List, Tuple

import pytest

from hermite_reduction import (
    P,
    Poly,
    RatFun,
    add,
    deg,
    deriv,
    divmod_poly,
    gcd,
    hermite_reduce,
    mul,
    sub,
)


def peval(a: Poly, x: Fraction) -> Fraction:
    s = Fraction(0)
    for c in reversed(a):
        s = s * x + c
    return s


def rat_deriv(r: RatFun) -> RatFun:
    n, d = r
    return sub(mul(deriv(n), d), mul(n, deriv(d))), mul(d, d)


def same(x: RatFun, y: RatFun) -> bool:
    """Equality of fractions by cross-multiplication."""
    return mul(x[0], y[1]) == mul(y[0], x[1])


def check(A: Poly, D: Poly, rng: random.Random) -> Tuple[RatFun, RatFun]:
    g, h = hermite_reduce(A, D)
    gd = rat_deriv(g)
    total = (add(mul(gd[0], h[1]), mul(h[0], gd[1])), mul(gd[1], h[1]))
    # defining property: A/D = g' + h, checked symbolically and at random points
    assert same(total, (A, D))
    for _ in range(5):
        x = Fraction(rng.randint(-50, 50), rng.randint(1, 7))
        if peval(D, x) != 0 and peval(g[1], x) != 0 and peval(h[1], x) != 0:
            lhs = peval(A, x) / peval(D, x)
            rhs = peval(gd[0], x) / peval(gd[1], x) + peval(h[0], x) / peval(h[1], x)
            assert lhs == rhs
    # h is proper with a squarefree denominator
    assert deg(h[0]) < deg(h[1])
    assert deg(gcd(h[1], deriv(h[1]))) == 0
    return g, h


def solve(M: List[List[Fraction]], v: List[Fraction]) -> List[Fraction]:
    """Gaussian elimination over Q for a square nonsingular system."""
    n = len(v)
    A = [row[:] + [v[i]] for i, row in enumerate(M)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[p] = A[p], A[c]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c] / A[c][c]
                A[r] = [a - f * b for a, b in zip(A[r], A[c])]
    return [A[i][n] / A[i][i] for i in range(n)]


def horowitz(A: Poly, D: Poly) -> Tuple[RatFun, RatFun]:
    """Independent oracle: Horowitz-Ostrogradsky by undetermined coefficients.
    For proper A/D: A/D = (B/D1)' + C/D2 with D1 = gcd(D, D'), D2 = D/D1."""
    D1 = gcd(D, deriv(D))
    D2, r = divmod_poly(D, D1)
    assert not r
    m, k = deg(D1), deg(D2)
    n = m + k
    # A = B' D2 - B (D2 D1' / D1) + C D1, unknowns b_0..b_{m-1}, c_0..c_{k-1}
    T, r = divmod_poly(mul(D2, deriv(D1)), D1)
    assert not r
    cols: List[Poly] = []
    for i in range(m):
        e = [Fraction(0)] * i + [Fraction(1)]
        cols.append(sub(mul(deriv(e), D2), mul(e, T)))
    for i in range(k):
        e = [Fraction(0)] * i + [Fraction(1)]
        cols.append(mul(e, D1))
    M = [[(c[row] if row < len(c) else Fraction(0)) for c in cols] for row in range(n)]
    x = solve(M, [(A[row] if row < len(A) else Fraction(0)) for row in range(n)])
    B = P(*x[:m])
    C = P(*x[m:])
    return (B, D1), (C, D2)


def rand_poly(rng: random.Random, d: int) -> Poly:
    while True:
        p = P(*[rng.randint(-4, 4) for _ in range(d)], rng.randint(1, 3))
        if deg(p) == d:
            return p


def rand_denominator(rng: random.Random) -> Poly:
    D = P(rng.randint(1, 3))
    for _ in range(rng.randint(1, 3)):
        f = rand_poly(rng, rng.randint(1, 2))
        for _ in range(rng.randint(1, 4)):
            D = mul(D, f)
    return D


def test_worked_example() -> None:
    A = P(-8, 8, -4, 0, -24, 0, 0, 1)
    D = P(0, 0, 8, 0, 12, 0, 6, 0, 1)  # x^2 (x^2 + 2)^3
    g, h = check(A, D, random.Random(1))
    # g = (3x^3 + 8x^2 + 6x + 4) / (x (x^2 + 2)^2), h = 1/x
    assert same(g, (P(4, 6, 8, 3), P(0, 4, 0, 4, 0, 1)))
    assert same(h, (P(1), P(0, 1)))


def test_classic_examples() -> None:
    rng = random.Random(2)
    # 1/(x^2 + 1)^2 = (x / (2 (x^2 + 1)))' + 1 / (2 (x^2 + 1))
    g, h = check(P(1), P(1, 0, 2, 0, 1), rng)
    assert same(g, (P(0, 1), P(2, 0, 2))) and same(h, (P(1), P(2, 0, 2)))
    # 1/x^3 = (-1/(2 x^2))', h = 0
    g, h = check(P(1), P(0, 0, 0, 1), rng)
    assert same(g, (P(-1), P(0, 0, 2))) and h[0] == []
    # a squarefree denominator needs no reduction
    g, h = check(P(1), P(-1, 0, 1), rng)
    assert g[0] == [] and same(h, (P(1), P(-1, 0, 1)))


def test_edge_cases() -> None:
    rng = random.Random(3)
    g, h = check([], P(1, 1), rng)  # zero numerator
    assert g[0] == [] and h[0] == []
    g, h = check(P(3, 0, 1), P(1), rng)  # a polynomial: g = x^3/3 + 3x
    assert same(g, (P(0, 3, 0, Fraction(1, 3)), P(1))) and h[0] == []
    g, h = check(P(1, 2, 3), P(2), rng)  # constant denominator
    assert h[0] == []
    with pytest.raises(ZeroDivisionError):
        hermite_reduce(P(1), [])
    # many reduction steps: 1/x^30
    g, h = check(P(1), P(*([0] * 30 + [1])), rng)
    assert same(g, (P(-1), P(*([0] * 29 + [29])))) and h[0] == []


def test_random_against_horowitz() -> None:
    rng = random.Random(4110)
    for _ in range(500):
        D = rand_denominator(rng)
        A = P(*[rng.randint(-6, 6) for _ in range(rng.randint(0, deg(D) + 3))])
        g, h = check(A, D, rng)
        # compare the proper part with the linear-algebra oracle
        q, a = divmod_poly(A, D)
        g2, h2 = horowitz(a, D)
        # g - g2 is a polynomial (the integral of q, up to a constant) and h = h2
        diff = (sub(mul(g[0], g2[1]), mul(g2[0], g[1])), mul(g[1], g2[1]))
        assert not divmod_poly(diff[0], diff[1])[1]
        assert same(h, h2)
