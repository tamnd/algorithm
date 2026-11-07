# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cache-oblivious-matrix-multiplication/. The authors are listed in prov/M2GPXZ.jsonl.

import math
import random

import pytest

from cache_oblivious_matrix_multiplication import cache_oblivious_matrix_multiplication as mul
from cache_oblivious_matrix_multiplication import lru_misses, recursion_depth


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
    assert mul([[], []], [], p=2) == [[0, 0], [0, 0]]
    assert mul([[1, 2, 3]], [[1], [1], [1]]) == [[6]]
    with pytest.raises(ValueError):
        mul([[1, 2]], [[1, 2]])
    with pytest.raises(ValueError):
        mul([[1]], [[1]], base=0)


def test_identity_and_zero() -> None:
    rng = random.Random(21)
    for n in (1, 3, 6, 13):
        a = rand(rng, n, n)
        eye = [[int(i == j) for j in range(n)] for i in range(n)]
        zero = [[0] * n for _ in range(n)]
        assert mul(a, eye) == a
        assert mul(eye, a, base=4) == a
        assert mul(zero, a, base=2) == zero


def test_random_against_schoolbook() -> None:
    rng = random.Random(22)
    for _ in range(600):
        n, m, p = rng.randint(1, 9), rng.randint(1, 9), rng.randint(1, 9)
        a, b = rand(rng, n, m), rand(rng, m, p)
        assert mul(a, b, base=rng.randint(1, 5)) == schoolbook(a, b, p)


def test_mod_small_primes() -> None:
    rng = random.Random(23)
    for q in (2, 3, 5, 7):
        for _ in range(40):
            n, m, p = rng.randint(1, 12), rng.randint(1, 12), rng.randint(1, 12)
            a, b = rand(rng, n, m, 0, q - 1), rand(rng, m, p, 0, q - 1)
            assert mul(a, b, mod=q) == schoolbook(a, b, p, q)


def test_depth_is_logarithmic() -> None:
    assert recursion_depth(64, 64, 64) == 18
    for m, n, p in ((100, 7, 33), (1, 1, 1000), (999, 999, 999)):
        bound = sum(math.ceil(math.log2(x)) for x in (m, n, p))
        assert recursion_depth(m, n, p) <= bound
    a = [[1] * 3 for _ in range(1)]
    b = [[1] * 3000 for _ in range(3)]
    assert mul(a, b) == [[3] * 3000]


def test_lru_observed_counts() -> None:
    # n = 32, lines of 4 words; the recursion is never tuned to M
    counts = {cache: lru_misses(32, 4, cache) for cache in (48, 192, 384)}
    assert counts == {48: 5888, 192: 3040, 384: 2112}
    # i, k, j order makes 17408 misses at 48 words and 8704 at 192 and 384
    assert counts[48] < 17408 and counts[192] < 8704
