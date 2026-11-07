# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/strassen-algorithm/. The authors are listed in prov/MZ8PBV.jsonl.

import math
import random

import pytest

from strassen_algorithm import count_operations, strassen_algorithm as mul


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


def test_edges() -> None:
    assert mul([], []) == []
    assert mul([[3]], [[4]]) == [[12]]
    assert mul([[], []], [], p=2) == [[0, 0], [0, 0]]
    with pytest.raises(ValueError):
        mul([[1]], [[1]], n0=0)
    with pytest.raises(ValueError):
        mul([[1, 2]], [[1, 2]])


def test_identity_zero() -> None:
    rng = random.Random(3)
    for n in range(0, 12):
        a = rand(rng, n, n)
        eye = [[int(i == j) for j in range(n)] for i in range(n)]
        zero = [[0] * n for _ in range(n)]
        assert mul(a, eye, p=n) == a and mul(eye, a, p=n) == a
        assert mul(a, zero, p=n) == zero


def test_square_all_sizes_over_z() -> None:
    rng = random.Random(1969)
    for n in range(1, 21):
        for _ in range(3):
            a, b = rand(rng, n, n, -10**9, 10**9), rand(rng, n, n, -10**9, 10**9)
            assert mul(a, b) == schoolbook(a, b, n)


def test_random_shapes_and_cutoffs() -> None:
    rng = random.Random(4242)
    for _ in range(500):
        n, m, p = rng.randint(0, 10), rng.randint(0, 10), rng.randint(0, 10)
        a, b = rand(rng, n, m), rand(rng, m, p)
        assert mul(a, b, p=p, n0=rng.choice((1, 2, 3, 5))) == schoolbook(a, b, p)


def test_mod_p() -> None:
    rng = random.Random(17)
    for q in (2, 3, 5, 7, 11):
        for _ in range(40):
            n = rng.randint(1, 12)
            a, b = rand(rng, n, n, 0, q - 1), rand(rng, n, n, 0, q - 1)
            got = mul(a, b, mod=q)
            assert got == schoolbook(a, b, n, q)
            assert all(0 <= x < q for row in got for x in row)


def test_counts() -> None:
    for k in range(0, 11):
        n = 2**k
        assert count_operations(n) == 7 * 7**k - 6 * n * n
        assert round(7 ** k) == round(n ** math.log2(7))
    assert count_operations(16, 8) == 7872 < 2 * 16**3 - 16**2
    assert count_operations(1024) < 2 * 1024**3 - 1024**2 < count_operations(512) * 8
    assert count_operations(512) > 2 * 512**3 - 512**2
