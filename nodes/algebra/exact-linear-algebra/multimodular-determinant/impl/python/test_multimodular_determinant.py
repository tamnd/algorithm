# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multimodular-determinant/. The authors are listed in prov/BETBZR.jsonl.

import itertools
import random
from fractions import Fraction
from math import prod

import pytest

from multimodular_determinant import det_mod_p, hadamard_int, is_prime, multimodular_det, multimodular_det_trace


def leibniz(a):
    n = len(a)
    total = 0
    for s in itertools.permutations(range(n)):
        inv = sum(1 for i in range(n) for j in range(i + 1, n) if s[i] > s[j])
        total += (-1) ** inv * prod(a[i][s[i]] for i in range(n))
    return total


def det_fraction(a):
    n = len(a)
    m = [[Fraction(v) for v in row] for row in a]
    det = Fraction(1)
    for k in range(n):
        piv = next((i for i in range(k, n) if m[i][k] != 0), None)
        if piv is None:
            return 0
        if piv != k:
            m[k], m[piv] = m[piv], m[k]
            det = -det
        det *= m[k][k]
        for i in range(k + 1, n):
            f = m[i][k] / m[k][k]
            for j in range(k, n):
                m[i][j] -= f * m[k][j]
    return int(det)


def test_worked_example():
    a = [[3, 1, 4], [1, 5, 9], [2, 6, 5]]
    assert hadamard_int(a) == 425
    assert [det_mod_p(a, p) for p in (7, 11, 13)] == [1, 9, 1]
    d, used = multimodular_det_trace(a, start=7)
    assert (d, used) == (-90, [7, 11, 13])
    assert multimodular_det(a) == -90


def test_edges():
    assert multimodular_det([]) == 1
    assert multimodular_det([[7]]) == 7
    assert multimodular_det([[-5]], start=2) == -5
    assert multimodular_det([[0]]) == 0
    assert multimodular_det([[0, 1], [1, 0]]) == -1  # zero pivot, needs a swap
    assert multimodular_det([[0, 0], [3, 4]]) == 0  # zero row
    assert multimodular_det([[0, 2], [0, 4]]) == 0  # zero column
    assert multimodular_det([[1, 2], [2, 4]], start=2) == 0  # singular
    assert multimodular_det([[2, 0, 0], [0, 3, 0], [0, 0, 35]], start=2) == 210  # det divisible by the first primes
    with pytest.raises(ValueError):
        multimodular_det([[1, 2]])


def test_is_prime():
    small = [n for n in range(2000) if n > 1 and all(n % q for q in range(2, n))]
    assert [n for n in range(2000) if is_prime(n)] == small
    assert is_prime(2**61 - 1) and not is_prime(2**61 + 1)


def test_random_small_vs_leibniz():
    rng = random.Random(7)
    for _ in range(600):
        n = rng.randrange(0, 6)
        a = [[rng.randrange(-6, 7) for _ in range(n)] for _ in range(n)]
        if n and rng.random() < 0.2:  # make it singular
            a[rng.randrange(n)] = [2 * v for v in a[rng.randrange(n)]]
        start = rng.choice([2, 3, 50, 1 << 31])
        assert multimodular_det(a, start) == leibniz(a)


def test_rank_deficient():
    rng = random.Random(8)
    for _ in range(100):
        n = rng.randrange(2, 8)
        r = rng.randrange(1, n)
        u = [[rng.randrange(-4, 5) for _ in range(r)] for _ in range(n)]
        v = [[rng.randrange(-4, 5) for _ in range(n)] for _ in range(r)]
        a = [[sum(u[i][k] * v[k][j] for k in range(r)) for j in range(n)] for i in range(n)]
        assert multimodular_det(a, rng.choice([2, 1 << 31])) == 0


def test_large_entries():
    rng = random.Random(9)
    for _ in range(40):
        n = rng.randrange(1, 11)
        bits = rng.choice([8, 64, 200])
        a = [[rng.randrange(-2**bits, 2**bits) for _ in range(n)] for _ in range(n)]
        d, used = multimodular_det_trace(a)
        assert d == det_fraction(a)
        assert abs(d) <= hadamard_int(a)
        h = hadamard_int(a)
        # the number of primes is the least s with p_1 ... p_s > 2H, and each prime exceeds 2^31
        assert prod(used) > 2 * h and prod(used[:-1]) <= 2 * h
        assert len(used) <= (2 * h).bit_length() // 31 + 1


def test_hadamard_tight():
    # a Sylvester-Hadamard matrix of order 8 attains the bound: |det| = 8^4
    h = [[1]]
    for _ in range(3):
        h = [r + r for r in h] + [r + [-v for v in r] for r in h]
    assert hadamard_int(h) == 8**4
    assert abs(multimodular_det(h, start=2)) == 8**4
