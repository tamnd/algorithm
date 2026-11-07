# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blocked-matrix-multiplication/. The authors are listed in prov/4VVM7H.jsonl.

import random

import pytest

from blocked_matrix_multiplication import blocked_matrix_multiplication as mul
from blocked_matrix_multiplication import explicit_transfers, lru_misses


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


def test_edges() -> None:
    assert mul([], []) == []
    assert mul([[5]], [[-3]]) == [[-15]]
    assert mul([[], []], [], p=3) == [[0, 0, 0], [0, 0, 0]]
    assert mul([[1, 2]], [[3], [4]], tile=1) == [[11]]
    with pytest.raises(ValueError):
        mul([[1, 2]], [[1, 2]])
    with pytest.raises(ValueError):
        mul([[1]], [[1]], tile=0)


def test_identity_and_zero() -> None:
    rng = random.Random(5)
    for n in (1, 2, 5, 7, 16):
        a = rand(rng, n, n)
        eye = [[int(i == j) for j in range(n)] for i in range(n)]
        zero = [[0] * n for _ in range(n)]
        assert mul(a, eye, tile=3) == a
        assert mul(eye, a, tile=4) == a
        assert mul(a, zero, tile=2) == zero


def test_random_against_schoolbook() -> None:
    rng = random.Random(11)
    for _ in range(600):
        n, m, p = rng.randint(1, 9), rng.randint(1, 9), rng.randint(1, 9)
        a, b = rand(rng, n, m), rand(rng, m, p)
        assert mul(a, b, tile=rng.randint(1, 10)) == schoolbook(a, b, p)


def test_mod_small_primes() -> None:
    rng = random.Random(12)
    for q in (2, 3, 5, 7):
        for _ in range(40):
            n, m, p = rng.randint(1, 12), rng.randint(1, 12), rng.randint(1, 12)
            a, b = rand(rng, n, m, 0, q - 1), rand(rng, m, p, 0, q - 1)
            assert mul(a, b, mod=q, tile=rng.randint(1, 5)) == schoolbook(a, b, p, q)


def test_explicit_transfer_formula() -> None:
    # aligned case: 2 n^3 / (b B) + 2 n^2 / B
    for n, b, line in ((8, 2, 2), (16, 4, 4), (64, 16, 8), (48, 8, 4)):
        assert explicit_transfers(n, n, n, b, line) == 2 * n ** 3 // (b * line) + 2 * n * n // line
    # unaligned tiles: each tile row of b words touches at most ceil(b/B) + 1 blocks
    for n, b, line in ((10, 3, 4), (13, 5, 4), (17, 6, 8)):
        tiles = -(-n // b)
        bound = 2 * (tiles ** 3 + tiles ** 2) * b * (-(-b // line) + 1)
        t = explicit_transfers(n, n, n, b, line)
        assert 2 * n ** 3 // (b * line) <= t <= bound


def test_lru_observed_counts() -> None:
    assert lru_misses(64, 8, 768, tile=16) == 6000
    assert lru_misses(64, 8, 768, tile=None) == 33792
    assert lru_misses(8, 2, 12, tile=2) == 336
    # the tiled order makes fewer misses than the i, k, j order once B does not fit
    for n in (24, 40):
        assert lru_misses(n, 4, 192, tile=8) < lru_misses(n, 4, 192)
