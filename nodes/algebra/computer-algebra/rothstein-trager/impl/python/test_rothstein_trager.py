# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rothstein-trager/. The authors are listed in prov/2HTAE6.jsonl.
import random
from fractions import Fraction as F

import pytest

from rothstein_trager import (deriv, norm, padd, pdivmod, pgcd, pmul, pscale,
                              resultant_formal, rothstein_trager, rt_resultant)


def trace(b, q):
    """Trace of multiplication by b on Q[z]/(q), with the basis 1, z, ..., z^(k-1)."""
    k = len(q) - 1
    t = F(0)
    for i in range(k):
        col = pdivmod(pmul(b, [F(0)] * i + [F(1)]), q)[1]
        t += col[i] if i < len(col) else 0
    return t


def amul(a, b, q):
    return pdivmod(pmul(a, b), q)[1]


def derivative_numerator(pairs, D):
    """Sum over pairs of Tr( z * S'(z, x) * (D / S)(z, x) ): the numerator over D of d/dx of the answer."""
    total = []
    for q, S in pairs:
        # exact division D / S in (Q[z]/q)[x]; S is monic in x
        a = [[c] for c in D]
        quo = [[] for _ in range(max(len(a) - len(S) + 1, 0))]
        while len(a) >= len(S) and any(a):
            k, c = len(a) - len(S), pdivmod(a[-1], q)[1]
            quo[k] = c
            a = [padd(a[i], pscale(amul(c, S[i - k], q), -1)) if 0 <= i - k < len(S) else a[i]
                 for i in range(len(a))]
            a = [pdivmod(x, q)[1] for x in a]
            while a and not a[-1]:
                a.pop()
        assert not any(a), "S does not divide D"
        Sp = [pscale(S[i], i) for i in range(1, len(S))]
        prod = [[] for _ in range(len(Sp) + len(quo))]
        for i, x in enumerate(Sp):
            for j, y in enumerate(quo):
                prod[i + j] = padd(prod[i + j], amul(x, y, q))
        z = [F(0), F(1)] if len(q) > 2 else [-q[0]]
        coeffs = [trace(amul(z, c, q), q) for c in prod]
        total = padd(total, coeffs)
    return total


def check(A, D):
    R, pairs = rothstein_trager(A, D)
    assert derivative_numerator(pairs, D) == norm(A)
    # the q of the pairs multiply to the squarefree part of R without the root 0
    prod = [F(1)]
    for q, _ in pairs:
        prod = pmul(prod, q)
    Rs = pdivmod(R, pgcd(R, deriv(R)))[0]
    if Rs and Rs[0] == 0:
        Rs = Rs[1:]
    assert pscale(prod, 1) == pscale(Rs, 1 / Rs[-1])
    return R, pairs


def test_examples():
    R, pairs = check([F(1)], [F(-2), F(0), F(1)])
    assert R == [F(1), F(0), F(-8)]
    assert pairs == [([F(-1, 8), F(0), F(1)], [[F(0), F(-4)], [F(1)]])]
    D = [F(-1), F(1), F(-1), F(1)]  # (x - 1)(x^2 + 1)
    R, pairs = check([F(3, 2), F(-3, 2), F(2)], D)
    assert R == [F(5), F(-21), F(32), F(-16)]
    assert pairs[0] == ([F(-1), F(1)], [[F(-1)], [F(1)]])
    assert pairs[1] == ([F(5, 16), F(-1), F(1)], [[F(2), F(-4)], [F(1)]])


def test_edges():
    with pytest.raises(ValueError):
        rothstein_trager([F(1)], [F(3)])
    with pytest.raises(ValueError):
        rothstein_trager([F(1), F(1)], [F(1), F(1)])
    assert rothstein_trager([], [F(1), F(1)])[1] == []
    check([F(5)], [F(-3), F(2)])                       # 5/(2x - 3)
    check([F(1)], [F(0), F(1), F(0), F(1)])           # 1/(x^3 + x)
    check([F(1)], [F(1), F(0), F(0), F(0), F(1)])     # 1/(x^4 + 1), one irreducible quartic in z
    check([F(1), F(2)], [F(1), F(0), F(1)])           # (2x + 1)/(x^2 + 1)
    # residues sqrt(2) twice and sqrt(3) once: q = (z^2 - 2)(z^2 - 3) must split at line L7
    D = pmul([F(-2), F(0), F(0), F(0), F(1)], [F(-3), F(0), F(1)])
    R, pairs = check([F(-12), F(-24), F(0), F(8), F(6)], D)
    assert sorted(pairs) == [([F(-3), F(0), F(1)], [[F(0), F(-1)], [F(1)]]),
                             ([F(-2), F(0), F(1)], [[F(0), F(-1)], [], [F(1)]])]


def test_resultant_matches_definition():
    rng = random.Random(3)
    for _ in range(400):
        n = rng.randint(1, 4)
        D = [F(rng.randint(-3, 3)) for _ in range(n)] + [F(rng.choice([1, 2]))]
        A = [F(rng.randint(-3, 3)) for _ in range(n)]
        R = rt_resultant(A, D)
        for z in (F(1, 3), F(-2), F(7, 5)):
            r = F(0)
            for c in reversed(R):
                r = r * z + c
            assert r == resultant_formal(D, padd(A, pscale(deriv(D), -z)), n, n - 1)


def test_random_by_differentiation():
    rng = random.Random(1976)
    done = 0
    while done < 80:
        # D as a product of distinct small factors, which forces splittings and rational roots
        factors = rng.sample([[F(-1), F(1)], [F(1), F(1)], [F(-2), F(1)], [F(1), F(0), F(1)],
                              [F(-2), F(0), F(1)], [F(-3), F(0), F(1)], [F(1), F(1), F(1)],
                              [F(0), F(1)], [F(2), F(0), F(1)]], rng.randint(1, 3))
        D = [F(1)]
        for f in factors:
            D = pmul(D, f)
        if len(pgcd(D, deriv(D))) > 1 or len(D) > 6:
            continue
        A = norm([F(rng.randint(-4, 4)) for _ in range(len(D) - 1)])
        if not A:
            continue
        check(A, pscale(D, rng.choice([1, 2, -3])))
        done += 1


def test_random_algebraic_residues():
    # A/D = sum over two quadratic fields of sum_{c^2 = a} c S'/S with S = x^k + e + b c,
    # so the residues are irrational and the gcd degrees can differ, which forces splittings
    rng = random.Random(1984)
    done = 0
    while done < 20:
        D, A = [F(1)], []
        for a in rng.sample([2, 3, 5, 6, 7], 2):
            k, b, e = rng.randint(1, 2), rng.choice([-2, -1, 1, 2]), rng.randint(-2, 2)
            y = [F(e)] + [F(0)] * (k - 1) + [F(1)]                      # x^k + e
            N = padd(pmul(y, y), [F(-b * b * a)])                       # S(c) S(-c)
            num = [F(0)] * (k - 1) + [F(-2 * a * b * k)]                # -2abk x^(k-1)
            A = padd(pmul(A, N), pmul(num, D))
            D = pmul(D, N)
        if len(pgcd(D, deriv(D))) > 1:
            continue
        _, pairs = check(A, D)
        assert sum(len(q) - 1 for q, _ in pairs) >= 4
        done += 1
