# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/okamoto-uchiyama-cryptosystem/. The authors are listed in prov/4VE7MR.jsonl.
#
# There are no official test vectors for Okamoto-Uchiyama. The tests check the worked
# example of the page, round trips, the additive homomorphism, and the chosen ciphertext
# attack that factors N, all on toy keys with fixed seeds against a local simulated oracle.

import random
from math import gcd

import pytest

import okamoto_uchiyama_cryptosystem as ou


def test_worked_example() -> None:
    pk, sk = ou.keygen_from_primes(11, 13, None, g=2)
    assert pk == (1573, 2, 1328, 4)
    assert sk == (11, 13, 56, 9)
    c = ou.encrypt(pk, 7, None, r=5)
    assert c == 235
    assert pow(c, 10, 121) == 23
    assert ou.decrypt(sk, c) == 7


def test_tiny_key_all_messages() -> None:
    pk, sk = ou.keygen_from_primes(11, 13, None, g=2)
    for m in range(8):
        for r in range(1, 60):
            assert ou.decrypt(sk, ou.encrypt(pk, m, None, r)) == m


@pytest.fixture(scope="module")
def key():
    # p and q of 192 binary digits, so N has about 576: a toy key, not secure.
    return ou.keygen(192, random.Random(1998))


def test_round_trip(key) -> None:
    pk, sk = key
    rng = random.Random(1)
    bound = 1 << (pk[3] - 1)
    for m in [0, 1, bound - 1] + [rng.randrange(bound) for _ in range(20)]:
        assert ou.decrypt(sk, ou.encrypt(pk, m, rng)) == m


def test_additive_homomorphism(key) -> None:
    pk, sk = key
    rng = random.Random(2)
    bound = 1 << (pk[3] - 2)
    for _ in range(10):
        a, b = rng.randrange(bound), rng.randrange(bound)
        c = ou.add(pk, ou.encrypt(pk, a, rng), ou.encrypt(pk, b, rng))
        assert ou.decrypt(sk, c) == a + b


def test_probabilistic(key) -> None:
    pk, sk = key
    rng = random.Random(3)
    assert ou.encrypt(pk, 5, rng) != ou.encrypt(pk, 5, rng)


def test_rejects_large_message(key) -> None:
    pk, _ = key
    with pytest.raises(ValueError):
        ou.encrypt(pk, 1 << (pk[3] - 1), random.Random(4))


def test_chosen_ciphertext_attack_factors_n(key) -> None:
    # The attacker encrypts a number M larger than p and asks the local decryption
    # oracle for the result. The answer is M mod p, so p divides M minus the answer.
    pk, sk = key
    n = pk[0]

    def oracle(c: int) -> int:
        return ou.decrypt(sk, c)

    rng = random.Random(5)
    M = rng.randrange(n // 2, n)  # far above p
    answer = oracle(ou.raw_encrypt(pk, M, rng.randrange(1, n)))
    p = gcd(M - answer, n)
    assert p == sk[0]
    q = n // (p * p)
    assert q == sk[1]
    # With p and q the attacker builds the private key and reads any ciphertext.
    stolen = ou.keygen_from_primes(p, q, None, g=pk[1])[1]
    secret = rng.randrange(1 << (pk[3] - 1))
    assert ou.decrypt(stolen, ou.encrypt(pk, secret, rng)) == secret


def test_attack_on_tiny_key() -> None:
    pk, sk = ou.keygen_from_primes(11, 13, None, g=2)
    C = ou.raw_encrypt(pk, 100, 3)
    assert C == 1337
    assert ou.decrypt(sk, C) == 1
    assert gcd(100 - 1, pk[0]) == 11
