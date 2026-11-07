# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lazard-rioboo-trager/. The authors are listed in prov/J2RB9Z.jsonl.

import random
from fractions import Fraction

import pytest

from lazard_rioboo_trager import (
    add,
    bivariate_subresultant,
    deriv,
    inverse_mod,
    lazard_rioboo_trager,
    mul,
    pdivmod,
    pgcd,
    scale,
    square_free,
    trim,
)

F = Fraction


def rem_mod_q(S, P, Q):
    """Remainder of P (in Q[t][x]) by S, monic in x, with coefficients in Q[t]/(Q)."""
    r = [pdivmod(c, Q)[1] for c in P]
    while r and not r[-1]:
        r.pop()
    while len(r) >= len(S):
        c = r[-1]
        s = len(r) - len(S)
        for i, b in enumerate(S):
            r[s + i] = pdivmod(add(r[s + i], scale(-1, mul(c, b))), Q)[1]
        while r and not r[-1]:
            r.pop()
    return r


def certify(A, D):
    """An exact certificate that sum alpha log S_i(alpha, x) differentiates to A/D.

    For each root alpha of Q_i, S_i(alpha, x) is monic of degree i and divides
    D and A - alpha D'. Distinct alphas give coprime factors, since a common
    root b of D would give A(b) = alpha D'(b) with D'(b) != 0. If moreover the
    degrees add up to deg D, the factors S_i(alpha, x) multiply to D / lc(D), and
    each root b of D lies in exactly one of them, with A(b)/D'(b) = alpha. Then
    the derivative sum_alpha alpha S_x / S = sum_b (A(b)/D'(b)) / (x - b) = A/D.
    """
    A, D = trim(A), trim(D)
    pairs = lazard_rioboo_trager(A, D)
    total = 0
    Dt = [[c] for c in D]
    Dp = deriv(D)
    # A - t D' in Q[t][x]: the coefficient of x^k is A_k - D'_k t.
    Bt = [trim([A[k] if k < len(A) else 0, -Dp[k]]) for k in range(len(Dp))]
    for idx, (Q, S) in enumerate(pairs):
        assert len(pgcd(Q, deriv(Q))) == 1  # square-free
        for Q2, _ in pairs[idx + 1:]:
            assert len(pgcd(Q, Q2)) == 1  # pairwise coprime
        i = len(S) - 1
        assert S[-1] == [F(1)]  # monic in x
        assert rem_mod_q(S, Dt, Q) == []
        assert rem_mod_q(S, Bt, Q) == []
        total += i * (len(Q) - 1)
    if A:
        assert total == len(D) - 1
    return pairs


def test_bronstein_example():
    A = [6, 0, -3, 0, 1]  # x^4 - 3x^2 + 6
    D = [4, 0, 5, 0, -5, 0, 1]  # x^6 - 5x^4 + 5x^2 + 4
    R = bivariate_subresultant(trim(A), trim(D), 0)[0]
    assert R == scale(45796, mul(mul([1, 0, 4], [1, 0, 4]), [1, 0, 4]))  # 214^2 (4t^2 + 1)^3
    pairs = certify(A, D)
    assert pairs == [([F(1, 4), 0, 1], [[0, -4], [-3], [0, 2], [1]])]  # x^3 + 2t x^2 - 3x - 4t


def test_small_examples():
    assert certify([1], [0, 1, 0, 1]) == [([-1, 1], [[], [1]]), ([F(1, 2), 1], [[1], [], [1]])]
    assert certify([1], [-2, 0, 1]) == [([F(-1, 8), 0, 1], [[0, -4], [1]])]  # 1/(x^2 - 2)
    assert certify([0, 1], [-1, 0, 1]) == [([F(-1, 2), 1], [[-1], [], [1]])]  # x/(x^2 - 1)
    assert certify([0, 0, 3], [1, 0, 0, 1]) == [([-1, 1], [[1], [], [], [1]])]  # all of D
    assert certify([5], [3, 1]) == [([-5, 1], [[3], [1]])]
    assert lazard_rioboo_trager([], [1, 0, 1]) == []


def test_random():
    rng = random.Random(1990)
    count = 0
    while count < 500:
        D = [F(rng.randint(1, 3))]
        for _ in range(rng.randint(1, 3)):
            p = [F(rng.randint(-3, 3)) for _ in range(rng.randint(1, 2))] + [F(1)]
            D = mul(D, p)
        if len(D) > 5 or len(pgcd(D, deriv(D))) > 1:
            continue
        A = trim([F(rng.randint(-3, 3)) for _ in range(len(D) - 1)])
        certify(A, D)
        count += 1


def test_inverse_and_square_free():
    m = [F(1), 0, 0, 1]
    a = [F(2), 1]
    assert pdivmod(mul(a, inverse_mod(a, m)), m)[1] == [1]
    f = mul(mul([F(-1), 1], [F(-1), 1]), [F(2), 1])
    assert square_free(f) == [[2, 1], [-1, 1]]


def test_bad_input():
    with pytest.raises(ValueError):
        lazard_rioboo_trager([1], [1, 2, 1])
    with pytest.raises(ValueError):
        lazard_rioboo_trager([1, 1], [1, 1])
