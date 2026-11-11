# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regev-encryption/. The authors are listed in prov/EKXD4J.jsonl.
# Regev encryption has no standard test vectors; these tests check the
# algebra and the correctness condition on toy parameters.

import random

from regev_encryption import Regev


def test_many_bits_round_trip():
    rng = random.Random(2005)
    scheme = Regev(n=32, m=400, q=4093, sigma=1.0)
    pk, sk = scheme.keygen(rng)
    bits = [rng.getrandbits(1) for _ in range(300)]
    assert [scheme.decrypt(sk, scheme.encrypt(pk, b, rng)) for b in bits] == bits


def test_decryption_noise_is_the_subset_sum_of_errors():
    rng = random.Random(7)
    scheme = Regev(n=16, m=200, q=4093, sigma=2.0)
    (a, b), s = scheme.keygen(rng)
    e = [(bi - sum(x * y for x, y in zip(row, s))) % 4093 for row, bi in zip(a, b)]
    e = [x - 4093 if x > 2046 else x for x in e]
    assert max(abs(x) for x in e) < 20
    # every subset sum stays below q/4 here, so no ciphertext can fail
    assert sum(abs(x) for x in e) < 4093 // 4


def test_too_much_error_makes_decryption_fail():
    rng = random.Random(9)
    scheme = Regev(n=16, m=200, q=4093, sigma=150.0)
    pk, sk = scheme.keygen(rng)
    bits = [rng.getrandbits(1) for _ in range(300)]
    wrong = sum(scheme.decrypt(sk, scheme.encrypt(pk, b, rng)) != b for b in bits)
    # the subset sum of about 100 errors has deviation near 1500 > q/4 = 1023
    assert wrong > 60


def test_ciphertexts_of_zero_and_one_differ_by_half_q():
    rng = random.Random(3)
    scheme = Regev(n=8, m=50, q=257, sigma=0.5)
    pk, _ = scheme.keygen(rng)
    state = rng.getstate()
    u0, v0 = scheme.encrypt(pk, 0, rng)
    rng.setstate(state)
    u1, v1 = scheme.encrypt(pk, 1, rng)
    assert u0 == u1 and (v1 - v0) % 257 == 128
