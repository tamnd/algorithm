# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/matrix-exponentiation/. The authors are listed in prov/VTJXE5.jsonl.

import random

import pytest

from matrix_exponentiation import (BOOLEAN, INTEGERS, MIN_PLUS, count_products, identity,
                                   matrix_exponentiation as power, modular)

INF = float("inf")


def schoolbook(x, y, add, mul, zero):
    n = len(x)
    c = [[zero] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            acc = zero
            for k in range(n):
                acc = add(acc, mul(x[i][k], y[k][j]))
            c[i][j] = acc
    return c


def slow_power(a, k, add=lambda x, y: x + y, mul=lambda x, y: x * y, zero=0, one=1):
    n = len(a)
    r = [[one if i == j else zero for j in range(n)] for i in range(n)]
    for _ in range(k):
        r = schoolbook(r, a, add, mul, zero)
    return r


def test_example() -> None:
    a = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
    r = power(a, 13)
    assert r == [[2730, 2731, 2731], [2731, 2730, 2731], [2731, 2731, 2730]]
    assert count_products(13) == 5


def test_edges() -> None:
    assert power([], 5) == []
    assert power([[7]], 0) == [[1]]
    assert power([[0, 0], [0, 0]], 0) == [[1, 0], [0, 1]]
    assert power([[2]], 10) == [[1024]]
    assert power([[0, 1], [0, 0]], 2) == [[0, 0], [0, 0]]
    with pytest.raises(ValueError):
        power([[1]], -1)


def test_random_over_z() -> None:
    rng = random.Random(1234)
    for _ in range(300):
        n = rng.randint(0, 4)
        a = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(n)]
        k = rng.randint(0, 20)
        assert power(a, k) == slow_power(a, k)


def test_mod_p() -> None:
    rng = random.Random(55)
    for q in (2, 3, 5, 7, 1_000_000_007):
        s = modular(q)
        for _ in range(40):
            n = rng.randint(1, 4)
            a = [[rng.randrange(q) for _ in range(n)] for _ in range(n)]
            k = rng.randint(0, 40)
            want = [[x % q for x in row] for row in slow_power(a, k)]
            assert power(a, k, s) == want


def test_min_plus_with_infinity() -> None:
    rng = random.Random(9)
    for _ in range(200):
        n = rng.randint(1, 5)
        a = [[rng.choice([INF, INF, rng.randint(0, 9)]) for _ in range(n)] for _ in range(n)]
        if rng.random() < 0.3:
            a[0] = [INF] * n  # a vertex with no out-edges
        k = rng.randint(0, 9)
        assert power(a, k, MIN_PLUS) == slow_power(a, k, min, lambda x, y: x + y, INF, 0)
    eye = identity(3, MIN_PLUS)
    assert eye == [[0, INF, INF], [INF, 0, INF], [INF, INF, 0]]


def test_boolean_with_empty_rows() -> None:
    rng = random.Random(10)
    for _ in range(200):
        n = rng.randint(1, 5)
        a = [[rng.random() < 0.3 for _ in range(n)] for _ in range(n)]
        if rng.random() < 0.3:
            a[rng.randrange(n)] = [False] * n
        k = rng.randint(0, 9)
        assert power(a, k, BOOLEAN) == slow_power(a, k, lambda x, y: x or y, lambda x, y: x and y, False, True)


def test_large_exponent_and_counts() -> None:
    q = 1_000_000_007
    fib = power([[1, 1], [1, 0]], 10**18, modular(q))
    assert fib[0][1] == 209783453  # F(10^18) mod 10^9 + 7
    for k in range(1, 2000):
        c = count_products(k)
        assert k.bit_length() - 1 <= c <= 2 * (k.bit_length() - 1)
    assert count_products(15) == 6
    assert power([[1, 1], [0, 1]], 12345, INTEGERS) == [[1, 12345], [0, 1]]
