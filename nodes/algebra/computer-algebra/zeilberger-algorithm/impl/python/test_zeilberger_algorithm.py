# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zeilberger-algorithm/. The authors are listed in prov/8S5NXW.jsonl.
"""Tests for Zeilberger's algorithm, against the defining properties.

1. The telescoping identity sum_j a_j(n) F(n+j, k) = G(n, k+1) - G(n, k),
   with G = R F, is checked exactly at many integer points, with F computed
   from factorials (1/m! = 0 for m < 0).
2. The recurrence sum_j a_j(n) S(n+j) = 0 is checked for S(n) = sum_k F(n, k)
   computed by brute force.
3. Known minimal recurrences (2^n, sum of squares, Franel, Apery) are matched.
"""

import random
from fractions import Fraction
from math import factorial

import pytest

from zeilberger_algorithm import zeilberger


def binom(A, B):
    """C(A, B) as factorial factors, A and B given as (a, b, c) for a n + b k + c."""
    (a1, b1, c1), (a2, b2, c2) = A, B
    return [(a1, b1, c1, 1), (a2, b2, c2, -1), (a1 - a2, b1 - b2, c1 - c2, -1)]


def term(poly, x, facts, n, k):
    """F(n, k), or None where a numerator factorial has a negative argument."""
    v = Fraction(x) ** k * sum((c * Fraction(n) ** i * Fraction(k) ** j
                                for (i, j), c in poly.items()), Fraction(0))
    for a, b, c, e in facts:
        m = a * n + b * k + c
        if m < 0:
            if e > 0:
                return None
            return Fraction(0)
        v = v * factorial(m) if e > 0 else v / factorial(m)
    return v


def peval(p, n, k):
    return sum((c * Fraction(n) ** i * Fraction(k) ** j for (i, j), c in p.items()), Fraction(0))


def neval(p, n):
    return sum((c * Fraction(n) ** i for i, c in enumerate(p)), Fraction(0))


def check_telescoping(poly, x, facts, res, nmax=8):
    J, a, Rn, Rd = res
    checked = 0
    for n in range(nmax + 1):
        for k in range(-3, n + 6):
            vals = [term(poly, x, facts, n + j, k) for j in range(J + 1)]
            f0, f1 = term(poly, x, facts, n, k), term(poly, x, facts, n, k + 1)
            d0, d1 = peval(Rd, n, k), peval(Rd, n, k + 1)
            if None in vals or f0 is None or f1 is None or d0 == 0 or d1 == 0:
                continue
            lhs = sum((neval(a[j], n) * vals[j] for j in range(J + 1)), Fraction(0))
            rhs = peval(Rn, n, k + 1) / d1 * f1 - peval(Rn, n, k) / d0 * f0
            assert lhs == rhs, (n, k)
            checked += 1
    assert checked > 0


def S(poly, x, facts, n, kmax):
    return sum((term(poly, x, facts, n, k) or 0 for k in range(-3, kmax)), Fraction(0))


def check_sum(poly, x, facts, res, n0=0, nmax=9, width=lambda n: 2 * n + 6):
    J, a, _, _ = res
    for n in range(n0, nmax):
        s = [S(poly, x, facts, n + j, width(n + J)) for j in range(J + 1)]
        assert sum((neval(a[j], n) * s[j] for j in range(J + 1)), Fraction(0)) == 0, n


N, K, ONE = (1, 0, 0), (0, 1, 0), {(0, 0): 1}
CNK = binom(N, K)
CNKK = binom((1, 1, 0), K)  # C(n + k, k)


def test_known_recurrences():
    res = zeilberger(ONE, 1, CNK)
    assert res[:2] == (1, [[-2], [1]])
    res = zeilberger(ONE, 1, CNK * 2)
    assert res[:2] == (1, [[-2, -4], [1, 1]])
    # R = -k^2 (3n - 2k + 3) / (n - k + 1)^2 for the sum of squares
    assert res[2] == {(0, 2): -3, (1, 2): -3, (0, 3): 2}
    res = zeilberger(ONE, 1, CNK * 3)  # Franel numbers
    assert res[:2] == (2, [[-8, -16, -8], [-16, -21, -7], [4, 4, 1]])
    res = zeilberger(ONE, 1, CNK * 2 + CNKK * 2)  # Apery numbers
    assert res[:2] == (2, [[1, 3, 3, 1], [-117, -231, -153, -34], [8, 12, 6, 1]])
    for facts in (CNK, CNK * 2, CNK * 3, CNK * 2 + CNKK * 2):
        r = zeilberger(ONE, 1, facts)
        check_telescoping(ONE, 1, facts, r, nmax=6)
        check_sum(ONE, 1, facts, r)


def test_edges():
    # (-1)^k C(n, k) is Gosper-summable: order 0, S(n) = 0 for n >= 1
    res = zeilberger(ONE, -1, CNK)
    assert res[0] == 0
    check_telescoping(ONE, -1, CNK, res)
    check_sum(ONE, -1, CNK, res, n0=1)
    # a summand free of factorials: F = k, and F = 1
    for poly in ({(0, 1): 1}, ONE):
        res = zeilberger(poly, 1, [])
        assert res[0] == 0
        check_telescoping(poly, 1, [], res)
    # the zero summand
    assert zeilberger({}, 1, CNK)[0] == 0
    # a summand that needs order 2 is not found with max_order 1
    assert zeilberger(ONE, 1, CNK * 3, max_order=1) is None
    # a polynomial factor and a geometric factor: sum k C(n, k) 2^k = 2n 3^(n-1)
    poly = {(0, 1): 1}
    res = zeilberger(poly, 2, CNK)
    check_telescoping(poly, 2, CNK, res)
    check_sum(poly, 2, CNK, res)


def random_summand(rng):
    c, d = rng.randint(0, 1), rng.randint(0, 1)
    facts = binom((1, 0, c), (0, 1, d))  # C(n + c, k + d): finite support in k
    extra = rng.choice(["none", "cnk", "c2nk", "cnkk", "cnk2"])
    if extra == "cnk":
        facts += CNK
    elif extra == "c2nk":
        facts += binom((2, 0, 0), K)
    elif extra == "cnkk":
        facts += CNKK
    elif extra == "cnk2":
        facts += binom((1, 0, 0), (0, 2, 0))
    poly = {(rng.randint(0, 1), rng.randint(0, 2)): rng.randint(1, 3)}
    if rng.random() < 0.5:
        poly[(0, 0)] = poly.get((0, 0), 0) + rng.randint(-2, 2)
    poly = {e: v for e, v in poly.items() if v} or ONE
    return poly, rng.choice([1, -1, 2]), facts


@pytest.mark.parametrize("seed", range(8))
def test_random_summands(seed):
    rng = random.Random(500 + seed)
    for _ in range(8):
        poly, x, facts = random_summand(rng)
        res = zeilberger(poly, x, facts, max_order=3)
        assert res is not None
        check_telescoping(poly, x, facts, res, nmax=6)
        check_sum(poly, x, facts, res, n0=2, nmax=8)
