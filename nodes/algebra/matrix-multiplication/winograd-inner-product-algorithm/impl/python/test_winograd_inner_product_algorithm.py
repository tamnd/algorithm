# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/winograd-inner-product-algorithm/. The authors are listed in prov/FZ993N.jsonl.

import random

import pytest

from winograd_inner_product_algorithm import (multiplication_count,
                                              winograd_inner_product_algorithm as mul)


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
    assert mul([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[19, 22], [43, 50]]
    assert multiplication_count(2, 2, 2) == 8
    assert multiplication_count(4, 4, 4) == 48
    assert multiplication_count(100, 100, 100) == 510000


def test_edges() -> None:
    assert mul([], [], p=0) == []
    assert mul([[3]], [[4]]) == [[12]]
    assert mul([[], []], [], p=3) == [[0, 0, 0], [0, 0, 0]]
    assert mul([[1, 2, 3]], [[4], [5], [6]]) == [[32]]
    with pytest.raises(ValueError):
        mul([[1, 2]], [[1, 2]])
    with pytest.raises(ValueError):
        mul([[]], [])


def test_identity_and_zero() -> None:
    rng = random.Random(7)
    for n in range(0, 7):
        a = rand(rng, n, n)
        eye = [[int(i == j) for j in range(n)] for i in range(n)]
        zero = [[0] * n for _ in range(n)]
        assert mul(a, eye, p=n) == a
        assert mul(eye, a, p=n) == a
        assert mul(a, zero, p=n) == zero


def test_random_over_z() -> None:
    rng = random.Random(2024)
    for _ in range(600):
        n, m, p = rng.randint(0, 7), rng.randint(0, 9), rng.randint(0, 7)
        a, b = rand(rng, n, m, -50, 50), rand(rng, m, p, -50, 50)
        assert mul(a, b, p=p) == schoolbook(a, b, p)


def test_mod_small_primes() -> None:
    rng = random.Random(31)
    for q in (2, 3, 5, 7, 11, 13):
        for _ in range(60):
            n, m, p = rng.randint(1, 6), rng.randint(0, 7), rng.randint(1, 6)
            a, b = rand(rng, n, m, 0, q - 1), rand(rng, m, p, 0, q - 1)
            assert mul(a, b, p=p, mod=q) == schoolbook(a, b, p, q)


def test_counts_against_classical() -> None:
    for n in range(2, 40):
        assert multiplication_count(n, n, n) <= n ** 3
        if n % 2 == 0:
            assert multiplication_count(n, n, n) == n ** 3 // 2 + n ** 2
    assert multiplication_count(3, 3, 3) == (9 + 3 + 3) + 9
