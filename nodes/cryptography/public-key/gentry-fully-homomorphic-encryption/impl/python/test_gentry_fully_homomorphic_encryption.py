# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gentry-fully-homomorphic-encryption/. The authors are listed in prov/V27SZY.jsonl.
#
# There are no official test vectors for DGHV or for Gentry's scheme. The tests check the worked
# example of the page, round trips, XOR and AND, the growth of the noise, and the failure of
# decryption once the noise passes p/2, on toy keys from fixed seeds. The keys are not secure.

import random

import pytest

import gentry_fully_homomorphic_encryption as dghv

# The hand-sized key of the worked example.
P = 1001
X = (1000003, 523526, 377376)


def test_worked_example() -> None:
    assert X == (1001 * 999 + 4, 1001 * 523 + 3, 1001 * 377 - 1)
    assert X[0] % 2 == 1 and dghv.centered_mod(X[0], P) == 4
    c1 = (1 + 2 * 2 + 2 * (X[1] + X[2])) % X[0]  # m = 1, r = 2, S = {1, 2}
    c2 = (1 + 2 * (-1) + 2 * X[1]) % X[0]  # m = 1, r = -1, S = {1}
    assert (c1, c2) == (801806, 47048)
    assert dghv.noise(P, c1) == 5 and dghv.noise(P, c2) == 1
    s, m = dghv.add(c1, c2), dghv.mul(c1, c2)
    assert (s, dghv.noise(P, s), dghv.decrypt(P, s)) == (848854, 6, 0)
    assert (m, dghv.noise(P, m), dghv.decrypt(P, m)) == (37723368688, 5, 1)
    c11 = dghv.mul(c1, c1)
    assert (c11, dghv.noise(P, c11)) == (642892861636, 25)
    c4 = dghv.mul(c11, c11)
    assert c4 == 413311231542525040596496
    assert 5**4 == 625 > P // 2
    assert dghv.noise(P, c4) == 625 - 1001 == -376
    assert dghv.decrypt(P, c4) == 0  # wrong: the AND of four ones is 1


@pytest.fixture(scope="module")
def key():
    return dghv.keygen(random.Random(2009))


def test_keygen_conditions(key) -> None:
    pk, p = key
    assert p % 2 == 1 and p.bit_length() == dghv.ETA
    assert pk[0] == max(pk) and pk[0] % 2 == 1
    assert dghv.centered_mod(pk[0], p) % 2 == 0
    assert all(abs(dghv.centered_mod(x, p)) < 2**dghv.RHO for x in pk)


def test_round_trip(key) -> None:
    pk, sk = key
    rng = random.Random(1)
    for _ in range(50):
        m = rng.getrandbits(1)
        c = dghv.encrypt(pk, m, rng)
        assert dghv.decrypt(sk, c) == m
        assert dghv.noise_bits(sk, c) <= dghv.RHO2 + 2


def test_xor_and_truth_tables(key) -> None:
    pk, sk = key
    rng = random.Random(2)
    for a in (0, 1):
        for b in (0, 1):
            ca, cb = dghv.encrypt(pk, a, rng), dghv.encrypt(pk, b, rng)
            assert dghv.decrypt(sk, dghv.add(ca, cb)) == a ^ b
            assert dghv.decrypt(sk, dghv.mul(ca, cb)) == a & b


def test_full_adder(key) -> None:
    pk, sk = key
    rng = random.Random(3)
    for word in range(8):
        a, b, cin = word & 1, (word >> 1) & 1, (word >> 2) & 1
        s, carry = dghv.full_adder(*(dghv.encrypt(pk, v, rng) for v in (a, b, cin)))
        assert dghv.decrypt(sk, s) == (a + b + cin) % 2
        assert dghv.decrypt(sk, carry) == (a + b + cin) // 2


def test_noise_growth_under_add_and_mul(key) -> None:
    pk, sk = key
    rng = random.Random(4)
    cs = [dghv.encrypt(pk, 1, rng) for _ in range(8)]
    # Addition: the noise adds, so it grows by at most one binary digit per level.
    s = dghv.add(cs[0], cs[1])
    assert dghv.noise(sk, s) == dghv.noise(sk, cs[0]) + dghv.noise(sk, cs[1])
    assert dghv.noise_bits(sk, s) <= max(dghv.noise_bits(sk, cs[0]), dghv.noise_bits(sk, cs[1])) + 1
    # Multiplication: the noise multiplies, so its length about doubles per level.
    bits = []
    for k in (1, 2, 4):
        prod = dghv.product(cs[:k])
        exact = 1
        for c in cs[:k]:
            exact *= dghv.noise(sk, c)
        assert dghv.noise(sk, prod) == exact  # no wrap yet
        assert dghv.decrypt(sk, prod) == 1
        bits.append(dghv.noise_bits(sk, prod))
    low = min(dghv.noise_bits(sk, c) for c in cs[:4])
    assert bits[1] >= 2 * low - 1 and bits[2] >= 4 * low - 3
    assert bits[2] < dghv.ETA - 1  # depth 2 is still inside the bound


def test_decryption_fails_past_the_bound(key) -> None:
    pk, sk = key
    rng = random.Random(5)
    wrong = 0
    for _ in range(8):
        cs = [dghv.encrypt(pk, 1, rng) for _ in range(8)]  # depth 3
        exact = 1
        for c in cs:
            exact *= dghv.noise(sk, c)
        assert abs(exact) > sk // 2  # the true noise is past p/2
        prod = dghv.product(cs)
        assert dghv.noise(sk, prod) != exact  # so it wraps modulo p
        wrong += dghv.decrypt(sk, prod) != 1
    assert wrong >= 1  # and the result is no longer reliable


def test_ciphertexts_grow_without_reduction(key) -> None:
    pk, sk = key
    rng = random.Random(6)
    a, b = dghv.encrypt(pk, 1, rng), dghv.encrypt(pk, 0, rng)
    assert dghv.mul(a, b).bit_length() > pk[0].bit_length() + dghv.GAMMA // 2
