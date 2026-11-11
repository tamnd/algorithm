# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/paillier-cryptosystem/. The authors are listed in prov/97TJVN.jsonl.
#
# There are no official test vectors for Paillier in an open standard (ISO/IEC 18033-6
# Annex B has examples, but the text is not free). The tests check the worked example of
# the page, round trips, the homomorphisms and the malleability, on toy keys with fixed seeds.

import random
from math import gcd

import pytest

import paillier_cryptosystem as pc


def test_worked_example() -> None:
    n, sk = pc.keygen_from_primes(7, 11)
    assert (n, sk[1], sk[2]) == (77, 30, 18)
    c = pc.encrypt(n, 42, None, r=23)
    assert (1 + 42 * n) % (n * n) == 3235
    assert pow(23, n, n * n) == 606
    assert c == 3840
    assert pow(c, sk[1], n * n) == 2157
    assert pc.decrypt(sk, c) == 42
    c2 = pc.encrypt(n, 15, None, r=10)
    assert c2 == 3442
    assert pc.add(n, c, c2) == 1539
    assert pc.decrypt(sk, 1539) == 57
    assert pc.decrypt(sk, pc.mul_plain(n, c, 3)) == 42 * 3 % 77


def test_tiny_key_all_messages() -> None:
    # Every message and every r of the tiny key decrypts correctly.
    n, sk = pc.keygen_from_primes(7, 11)
    for m in range(n):
        for r in range(1, n):
            if gcd(r, n) == 1:
                assert pc.decrypt(sk, pc.encrypt(n, m, None, r)) == m


@pytest.fixture(scope="module")
def key512():
    return pc.keygen(512, random.Random(1999))


def test_round_trip(key512) -> None:
    n, sk = key512
    assert n.bit_length() == 512
    rng = random.Random(1)
    for m in [0, 1, 2, n - 1, n // 2] + [rng.randrange(n) for _ in range(20)]:
        assert pc.decrypt(sk, pc.encrypt(n, m, rng)) == m


def test_probabilistic(key512) -> None:
    n, sk = key512
    rng = random.Random(2)
    c1, c2 = pc.encrypt(n, 7, rng), pc.encrypt(n, 7, rng)
    assert c1 != c2
    assert pc.decrypt(sk, c1) == pc.decrypt(sk, c2) == 7


def test_additive_homomorphism(key512) -> None:
    n, sk = key512
    rng = random.Random(3)
    for _ in range(10):
        a, b = rng.randrange(n), rng.randrange(n)
        ca, cb = pc.encrypt(n, a, rng), pc.encrypt(n, b, rng)
        assert pc.decrypt(sk, pc.add(n, ca, cb)) == (a + b) % n
        k = rng.randrange(n)
        assert pc.decrypt(sk, pc.add_plain(n, ca, k)) == (a + k) % n
        assert pc.decrypt(sk, pc.mul_plain(n, ca, k)) == a * k % n
        assert pc.decrypt(sk, pc.mul_plain(n, ca, -1)) == (-a) % n


def test_encrypted_sum_of_votes(key512) -> None:
    # A tally: each voter encrypts 0 or 1, the product of the ciphertexts encrypts the sum.
    n, sk = key512
    rng = random.Random(4)
    votes = [rng.randrange(2) for _ in range(50)]
    total = pc.encrypt(n, 0, rng)
    for v in votes:
        total = pc.add(n, total, pc.encrypt(n, v, rng))
    assert pc.decrypt(sk, total) == sum(votes)


def test_rerandomize(key512) -> None:
    n, sk = key512
    rng = random.Random(5)
    c = pc.encrypt(n, 123, rng)
    d = pc.rerandomize(n, c, rng)
    assert d != c and pc.decrypt(sk, d) == 123


def test_malleability_breaks_cca(key512) -> None:
    # One decryption query on a changed ciphertext reveals the challenge message:
    # the scheme is IND-CPA but not IND-CCA2.
    n, sk = key512
    rng = random.Random(6)
    secret = rng.randrange(n)
    challenge = pc.encrypt(n, secret, rng)

    def oracle(c: int) -> int:
        assert c != challenge
        return pc.decrypt(sk, c)

    shifted = pc.add_plain(n, challenge, 1)
    assert (oracle(shifted) - 1) % n == secret


def test_decryption_with_known_factors_tests_nth_residues(key512) -> None:
    # z is an N-th residue mod N^2 iff z^lam = 1 (mod N^2); encryptions of 0 are N-th residues.
    n, sk = key512
    rng = random.Random(7)
    lam = sk[1]
    z = pc.encrypt(n, 0, rng)
    assert pow(z, lam, n * n) == 1
    assert pow(pc.encrypt(n, 5, rng), lam, n * n) != 1


def test_rejects_bad_input(key512) -> None:
    n, sk = key512
    with pytest.raises(ValueError):
        pc.encrypt(n, n, random.Random(8))
    with pytest.raises(ValueError):
        pc.decrypt(sk, 0)
    with pytest.raises(ValueError):
        pc.keygen_from_primes(7, 7)
