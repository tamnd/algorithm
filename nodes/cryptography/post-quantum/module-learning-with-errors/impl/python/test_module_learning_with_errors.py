# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/module-learning-with-errors/. The authors are listed in prov/4H2DFX.jsonl.
"""Tests for the FIPS 203 NTT and Module-LWE sampling.

The only official values used are the first eight entries of the two zeta
tables of FIPS 203 Appendix A. Module-LWE itself has no test vectors; the
full ML-KEM known answer tests cover the whole scheme, which this code does
not implement. The NTT is checked against schoolbook multiplication.
"""

import random

from module_learning_with_errors import (
    GAMMAS,
    Q,
    ZETAS,
    add,
    base_case_multiply,
    centered,
    mul_schoolbook,
    multiply_ntts,
    ntt,
    ntt_inv,
    sample_module_lwe,
    sample_poly_cbd,
)


def test_zeta_tables_fips203_appendix_a():
    # FIPS 203 Appendix A: zeta^BitRev7(i) mod 3329, first entries.
    assert ZETAS[:8] == [1, 1729, 2580, 3289, 2642, 630, 1897, 848]
    # FIPS 203 Appendix A: zeta^(2 BitRev7(i) + 1) mod 3329, written there as
    # 17, -17, 2761, -2761, 583, -583, 2649, -2649.
    assert [centered(g) for g in GAMMAS[:8]] == [17, -17, -568, 568, 583, -583, -680, 680]
    assert [g % Q for g in (17, -17, 2761, -2761, 583, -583, 2649, -2649)] == GAMMAS[:8]


def test_zeta_is_primitive_256th_root():
    assert pow(17, 128, Q) == Q - 1
    assert pow(17, 256, Q) == 1
    assert 128 * 3303 % Q == 1


def test_base_case():
    # (1 + 2X)(3 + 4X) = 3 + 10X + 8X^2 = (3 + 8 gamma) + 10X mod X^2 - gamma.
    assert base_case_multiply(1, 2, 3, 4, 17) == ((3 + 8 * 17) % Q, 10)


def test_ntt_roundtrip():
    rng = random.Random(1)
    for _ in range(5):
        f = [rng.randrange(Q) for _ in range(256)]
        assert ntt_inv(ntt(f)) == f


def test_ntt_product_equals_schoolbook():
    rng = random.Random(2)
    for _ in range(5):
        a = [rng.randrange(Q) for _ in range(256)]
        b = [rng.randrange(Q) for _ in range(256)]
        assert ntt_inv(multiply_ntts(ntt(a), ntt(b))) == mul_schoolbook(a, b)


def test_ntt_product_small_polys_500():
    # 500 random products of sparse polynomials, checked against schoolbook.
    rng = random.Random(3)
    for _ in range(500):
        a = [0] * 256
        b = [0] * 256
        for _ in range(3):
            a[rng.randrange(256)] = rng.randrange(Q)
            b[rng.randrange(256)] = rng.randrange(Q)
        assert ntt_inv(multiply_ntts(ntt(a), ntt(b))) == mul_schoolbook(a, b)


def test_ntt_of_x_power():
    # x^128 * x^128 = x^256 = -1.
    x128 = [0] * 256
    x128[128] = 1
    prod = ntt_inv(multiply_ntts(ntt(x128), ntt(x128)))
    assert prod == [Q - 1] + [0] * 255


def test_cbd():
    rng = random.Random(4)
    for eta in (2, 3):
        f = sample_poly_cbd(rng.randbytes(64 * eta), eta)
        assert all(-eta <= centered(x) <= eta for x in f)
    # All-zero bytes give 0; all-one bytes give eta - eta = 0 as well.
    assert sample_poly_cbd(bytes(128), 2) == [0] * 256
    assert sample_poly_cbd(bytes([255]) * 128, 2) == [0] * 256
    # Byte 0x03 with eta = 2: bits (1, 1) minus bits (0, 0) give coefficient 0 = 2.
    assert sample_poly_cbd(bytes([0x03]) + bytes(127), 2)[0] == 2


def test_module_lwe_relation():
    rng = random.Random(5)
    for k, eta1 in ((2, 3), (3, 2)):
        A_hat, t, t_hat, s, e = sample_module_lwe(k, eta1, 2, rng)
        A = [[ntt_inv(p) for p in row] for row in A_hat]
        for i in range(k):
            acc = [0] * 256
            for j in range(k):
                acc = add(acc, mul_schoolbook(A[i][j], s[j]))
            assert add(acc, e[i]) == t[i]
            assert all(abs(centered(x)) <= 2 for x in e[i])
