# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cannons-algorithm/. The authors are listed in prov/E9RHBT.jsonl.

import random

import pytest

from cannons_algorithm import cannon_with_cost, cannons_algorithm as mul


def schoolbook(a, b, p, mod=None):
    n, m = len(a), len(b)
    c = [[0] * p for _ in range(n)]
    for i in range(n):
        for j in range(p):
            s = 0
            for k in range(m):
                s += a[i][k] * b[k][j]
            c[i][j] = s % mod if mod is not None else s
    return c


def rand(rng, r, c, lo=-9, hi=9):
    return [[rng.randint(lo, hi) for _ in range(c)] for _ in range(r)]


def test_example() -> None:
    a = [[1, 2, 3], [4, 5, 6], [7, 8, 10]]
    b = [[1, 0, 2], [0, 1, 1], [1, 1, 0]]
    c, cost = cannon_with_cost(a, b, 3)
    assert c == [[4, 5, 4], [10, 11, 13], [17, 18, 22]]
    assert cost.supersteps == 4 and cost.h_total == 6 and cost.max_multiplications == 3


def test_edges() -> None:
    assert mul([], [], 2) == []
    assert mul([[5]], [[-3]], 1) == [[-15]]
    assert mul([[5]], [[-3]], 3) == [[-15]]
    assert mul([[], []], [], 2, p=2) == [[0, 0], [0, 0]]
    with pytest.raises(ValueError):
        mul([[1, 2]], [[1, 2]], 2)
    with pytest.raises(ValueError):
        mul([[1]], [[1]], 0)


def test_identity_and_zero() -> None:
    rng = random.Random(31)
    for n, q in ((4, 2), (6, 3), (5, 2), (7, 4)):
        a = rand(rng, n, n)
        eye = [[int(i == j) for j in range(n)] for i in range(n)]
        zero = [[0] * n for _ in range(n)]
        assert mul(a, eye, q) == a
        assert mul(eye, a, q) == a
        assert mul(zero, a, q) == zero


def test_random_against_schoolbook() -> None:
    rng = random.Random(32)
    for _ in range(600):
        n, m, p = rng.randint(1, 8), rng.randint(1, 8), rng.randint(1, 8)
        a, b = rand(rng, n, m), rand(rng, m, p)
        assert mul(a, b, rng.randint(1, 4)) == schoolbook(a, b, p)


def test_mod_small_primes() -> None:
    rng = random.Random(33)
    for mod in (2, 3, 5, 7):
        for _ in range(40):
            n = rng.randint(1, 9)
            a, b = rand(rng, n, n, 0, mod - 1), rand(rng, n, n, 0, mod - 1)
            assert mul(a, b, rng.randint(1, 3), mod=mod) == schoolbook(a, b, n, mod)


def test_bsp_cost() -> None:
    rng = random.Random(34)
    for n, q in ((8, 2), (8, 4), (12, 3), (12, 6), (16, 4)):
        a, b = rand(rng, n, n), rand(rng, n, n)
        c, cost = cannon_with_cost(a, b, q)
        assert c == schoolbook(a, b, n)
        assert cost.supersteps == q + 1
        assert cost.h_total == 2 * n * n // q          # 2 n^2 / sqrt(P) with P = q^2
        assert cost.max_multiplications == n ** 3 // (q * q)
    _, cost = cannon_with_cost(rand(rng, 6, 6), rand(rng, 6, 6), 1)
    assert cost.h_total == 0
