# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ring-learning-with-errors/. The authors are listed in prov/4YZXDV.jsonl.
"""Tests for the negacyclic NTT and Ring-LWE sampling.

Ring-LWE is a problem, not a standard algorithm, so there are no official
test vectors. The NTT is checked against schoolbook multiplication and
against direct evaluation at the roots of x^n + 1.
"""

import random

from ring_learning_with_errors import (
    as_lwe_samples,
    bit_reverse,
    intt,
    mul_ntt,
    mul_schoolbook,
    ntt,
    ntt_tables,
    primitive_root_2n,
    rotation_matrix,
    sample_ring_lwe,
)


def test_schoolbook_small():
    # (1 + x) (1 + x) = 1 + 2x + x^2 = 2x in Z[x]/(x^2 + 1).
    assert mul_schoolbook([1, 1], [1, 1], 17) == [0, 2]
    # x^3 * x = x^4 = -1 in Z_17[x]/(x^4 + 1).
    assert mul_schoolbook([0, 0, 0, 1], [0, 1, 0, 0], 17) == [16, 0, 0, 0]


def test_root():
    for n, q in ((8, 17), (256, 7681), (256, 12289), (1024, 12289)):
        psi = primitive_root_2n(n, q)
        assert pow(psi, n, q) == q - 1 and pow(psi, 2 * n, q) == 1


def test_ntt_is_evaluation():
    n, q = 16, 97
    psi = primitive_root_2n(n, q)
    fwd, bwd = ntt_tables(n, q, psi)
    rng = random.Random(1)
    a = [rng.randrange(q) for _ in range(n)]
    f = ntt(a, q, fwd)
    for i in range(n):
        root = pow(psi, 2 * bit_reverse(i, 4) + 1, q)
        assert pow(root, n, q) == q - 1
        assert f[i] == sum(c * pow(root, k, q) for k, c in enumerate(a)) % q


def test_ntt_roundtrip_and_product():
    rng = random.Random(2)
    for n, q in ((8, 17), (64, 257), (256, 7681), (256, 12289)):
        fwd, bwd = ntt_tables(n, q, primitive_root_2n(n, q))
        for _ in range(3):
            a = [rng.randrange(q) for _ in range(n)]
            b = [rng.randrange(q) for _ in range(n)]
            assert intt(ntt(a, q, fwd), q, bwd) == a
            assert mul_ntt(a, b, q, fwd, bwd) == mul_schoolbook(a, b, q)


def test_ntt_random_500():
    rng = random.Random(3)
    tables = {}
    for _ in range(500):
        n, q = rng.choice(((4, 17), (8, 17), (8, 97), (16, 97), (32, 193)))
        if (n, q) not in tables:
            tables[(n, q)] = ntt_tables(n, q, primitive_root_2n(n, q))
        fwd, bwd = tables[(n, q)]
        a = [rng.randrange(q) for _ in range(n)]
        b = [rng.randrange(q) for _ in range(n)]
        assert mul_ntt(a, b, q, fwd, bwd) == mul_schoolbook(a, b, q)


def test_ring_lwe_sample_and_rotation():
    rng = random.Random(4)
    n, q = 256, 7681
    a, b, s, e = sample_ring_lwe(n, q, 2, rng)
    fwd, bwd = ntt_tables(n, q, primitive_root_2n(n, q))
    # b - a s = e, with small coefficients.
    diff = [(x - y) % q for x, y in zip(b, mul_ntt(a, s, q, fwd, bwd))]
    assert diff == e
    assert all(min(x, q - x) <= 2 for x in diff)
    # The same sample is n LWE samples with the rotation matrix of a.
    A, bb = as_lwe_samples(a, b, q)
    As = [sum(x * y for x, y in zip(row, s)) % q for row in A]
    assert [(x - y) % q for x, y in zip(bb, As)] == e


def test_rotation_matrix_small():
    # a = 1 + 2x + 3x^2 in Z_17[x]/(x^3 + 1): columns a, x a, x^2 a.
    M = rotation_matrix([1, 2, 3], 17)
    assert M == [[1, 14, 15], [2, 1, 14], [3, 2, 1]]
