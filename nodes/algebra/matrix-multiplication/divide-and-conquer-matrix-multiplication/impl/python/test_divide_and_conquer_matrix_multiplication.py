# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/divide-and-conquer-matrix-multiplication/. The authors are listed in prov/4CTYKM.jsonl.

import random

import pytest

from divide_and_conquer_matrix_multiplication import divide_and_conquer_matrix_multiplication as mul


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
    a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    b = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
    assert mul(a, b) == [[30, 24, 18], [84, 69, 54], [138, 114, 90]]


def test_edges() -> None:
    assert mul([], []) == []
    assert mul([[4]], [[-3]]) == [[-12]]
    assert mul([[], [], []], [], p=2) == [[0, 0], [0, 0], [0, 0]]
    assert mul([[1, 2, 3]], [[1], [1], [1]]) == [[6]]
    with pytest.raises(ValueError):
        mul([[1, 2]], [[1]])


def test_identity_zero() -> None:
    rng = random.Random(5)
    for n in range(0, 10):
        a = rand(rng, n, n)
        eye = [[int(i == j) for j in range(n)] for i in range(n)]
        zero = [[0] * n for _ in range(n)]
        assert mul(a, eye, p=n) == a and mul(eye, a, p=n) == a
        assert mul(zero, a, p=n) == zero


def test_random_over_z() -> None:
    rng = random.Random(31337)
    for _ in range(500):
        n, m, p = rng.randint(0, 9), rng.randint(0, 9), rng.randint(0, 9)
        a, b = rand(rng, n, m, -10**6, 10**6), rand(rng, m, p, -10**6, 10**6)
        assert mul(a, b, p=p) == schoolbook(a, b, p)


def test_random_mod_p() -> None:
    rng = random.Random(8)
    for q in (2, 3, 5, 7, 13):
        for _ in range(60):
            n, m, p = rng.randint(1, 8), rng.randint(1, 8), rng.randint(1, 8)
            a, b = rand(rng, n, m, 0, q - 1), rand(rng, m, p, 0, q - 1)
            assert mul(a, b, mod=q) == schoolbook(a, b, p, q)


def test_powers_of_two_and_odd() -> None:
    rng = random.Random(77)
    for n in (1, 2, 4, 8, 16, 3, 5, 7, 15, 17):
        a, b = rand(rng, n, n), rand(rng, n, n)
        assert mul(a, b) == schoolbook(a, b, n)
