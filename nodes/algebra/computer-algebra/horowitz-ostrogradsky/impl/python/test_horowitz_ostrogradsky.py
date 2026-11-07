# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/horowitz-ostrogradsky/. The authors are listed in prov/KX6NMH.jsonl.

import random
from fractions import Fraction

import pytest

from horowitz_ostrogradsky import add, deriv, gcd_poly, horowitz_ostrogradsky, mul, scale, trim

F = Fraction


def check(A, D):
    """Check the output by differentiation and by the degree and square-free conditions."""
    B, Dm, C, Ds = horowitz_ostrogradsky(A, D)
    A, D = trim(A), trim(D)
    # (B/Dm)' + C/Ds = A/D, cross-multiplied by D * Dm^2 * Ds.
    lhs = mul(A, mul(mul(Dm, Dm), Ds))
    num = add(mul(add(mul(deriv(B), Dm), scale(F(-1), mul(B, deriv(Dm)))), Ds), mul(C, mul(Dm, Dm)))
    assert lhs == mul(D, num)
    assert mul(Dm, Ds) == D
    assert len(B) < len(Dm) or not B
    assert len(C) < len(Ds) or not C
    assert len(gcd_poly(Ds, deriv(Ds))) == 1  # Ds is square-free
    return B, Dm, C, Ds


def test_worked_example():
    B, Dm, C, Ds = check([1], [1, 0, 2, 0, 1])  # 1/(x^2 + 1)^2
    assert B == [0, F(1, 2)] and Dm == [1, 0, 1]
    assert C == [F(1, 2)] and Ds == [1, 0, 1]


def test_second_example():
    D = mul(mul([-1, 1], [-1, 1]), [1, 0, 1])  # (x - 1)^2 (x^2 + 1)
    B, Dm, C, Ds = check([0, 0, 1], D)
    assert B == [F(-1, 2)] and Dm == [-1, 1]
    assert C == [F(1, 2), F(1, 2)] and Ds == [-1, 1, -1, 1]


def rand_poly(rng, deg, size=4):
    p = [F(rng.randint(-size, size)) for _ in range(deg + 1)]
    if p[-1] == 0:
        p[-1] = F(rng.choice([-1, 1]))
    return p


def test_random():
    rng = random.Random(31415)
    for _ in range(500):
        D = [F(rng.randint(1, 3))]
        for _ in range(rng.randint(1, 3)):
            p = rand_poly(rng, rng.randint(1, 2))
            for _ in range(rng.randint(1, 3)):
                D = mul(D, p)
        if len(D) > 9:
            continue
        A = trim(rand_poly(rng, rng.randint(0, len(D) - 2)))
        check(A, D)


def test_edge_cases():
    assert horowitz_ostrogradsky([], [1, 0, 1]) == ([], [1], [], [1, 0, 1])
    B, Dm, C, Ds = check([3], [-2, 1])  # square-free: no rational part
    assert B == [] and Dm == [1] and C == [3]
    B, Dm, C, Ds = check([1], [0, 0, 0, 0, 0, 1])  # 1/x^5 = (-1/(4x^4))'
    assert B == [F(-1, 4)] and C == []
    check([5, -1], mul([2, 3], mul([2, 3], [2, 3])))  # a non-monic cube
    with pytest.raises(ValueError):
        horowitz_ostrogradsky([1, 1], [1, 1])
