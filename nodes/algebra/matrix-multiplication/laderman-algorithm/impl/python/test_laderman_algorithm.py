# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/laderman-algorithm/. The authors are listed in prov/JHP9MS.jsonl.

import random

import pytest

from laderman_algorithm import OUTPUTS, PRODUCTS, count_multiplications, laderman_algorithm as mul


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
    assert mul(a, b) == [[4, 5, 4], [10, 11, 13], [17, 18, 22]]


def test_scheme_shape() -> None:
    assert len(PRODUCTS) == 23
    adds = sum(len(u) - 1 + len(v) - 1 for u, v in PRODUCTS)
    adds += sum(len(v) - 1 for v in OUTPUTS.values())
    assert adds == 98
    assert count_multiplications(3) == 23
    assert count_multiplications(9) == 529
    assert count_multiplications(27, n0=3) == 23 * 23 * 27


def test_edges() -> None:
    assert mul([], []) == []
    assert mul([[5]], [[-3]]) == [[-15]]
    assert mul([[], []], [], p=2) == [[0, 0], [0, 0]]
    with pytest.raises(ValueError):
        mul([[1, 2]], [[1, 2]])
    with pytest.raises(ValueError):
        mul([[1]], [[1]], n0=0)


def test_identity_and_zero() -> None:
    rng = random.Random(3)
    for n in (2, 3, 4, 6, 9, 10):
        a = rand(rng, n, n)
        eye = [[int(i == j) for j in range(n)] for i in range(n)]
        zero = [[0] * n for _ in range(n)]
        assert mul(a, eye) == a
        assert mul(eye, a) == a
        assert mul(zero, a) == zero


def test_random_3x3_over_z() -> None:
    rng = random.Random(77)
    for _ in range(600):
        a, b = rand(rng, 3, 3, -100, 100), rand(rng, 3, 3, -100, 100)
        assert mul(a, b) == schoolbook(a, b, 3)


def test_random_shapes_and_recursion() -> None:
    rng = random.Random(78)
    for _ in range(80):
        n, m, p = rng.randint(1, 11), rng.randint(1, 11), rng.randint(1, 11)
        a, b = rand(rng, n, m), rand(rng, m, p)
        assert mul(a, b, n0=rng.choice([1, 2, 3])) == schoolbook(a, b, p)
    a, b = rand(rng, 27, 27), rand(rng, 27, 27)
    assert mul(a, b, n0=3) == schoolbook(a, b, 27)


def test_mod_small_primes() -> None:
    rng = random.Random(79)
    for q in (2, 3, 5, 7):
        for _ in range(40):
            n = rng.choice([3, 4, 5, 6, 9])
            a, b = rand(rng, n, n, 0, q - 1), rand(rng, n, n, 0, q - 1)
            assert mul(a, b, mod=q) == schoolbook(a, b, n, q)
