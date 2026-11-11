# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/goldwasser-micali-cryptosystem/. The authors are listed in prov/5FBQTT.jsonl.
"""Tests for Goldwasser-Micali encryption.

There is no official test vector for this scheme. The small example
(N = 77, y = 76) is the one worked on the page. The larger key uses the
Mersenne primes 2^31 - 1 and 2^61 - 1, both congruent to 3 modulo 4.
"""

import random
from math import gcd

from goldwasser_micali_cryptosystem import (
    PrivateKey,
    PublicKey,
    bits_of,
    bytes_of,
    decrypt,
    encrypt,
    is_square_mod_prime,
    jacobi,
    keygen,
    xor,
)

P_BIG, Q_BIG = 2**31 - 1, 2**61 - 1


def legendre(a: int, p: int) -> int:
    t = pow(a, (p - 1) // 2, p)
    return -1 if t == p - 1 else t


def test_jacobi_against_legendre_products() -> None:
    primes = [3, 5, 7, 11, 13, 17, 19, 23]
    for p in primes:
        for q in primes:
            n = p * q
            for a in range(n):
                assert jacobi(a, n) == legendre(a % p, p) * legendre(a % q, q)


def test_small_worked_example() -> None:
    pk, sk = PublicKey(77, 76), PrivateKey(7, 11)
    assert jacobi(76, 77) == 1
    assert not is_square_mod_prime(76 % 7, 7) and not is_square_mod_prime(76 % 11, 11)
    # bits 1, 0, 1 with r = 2, 3, 5
    cs = [76 * 2 * 2 % 77, 3 * 3 % 77, 76 * 5 * 5 % 77]
    assert cs == [73, 9, 52]
    assert all(jacobi(c, 77) == 1 for c in cs)
    assert decrypt(sk, cs) == [1, 0, 1]
    # the homomorphism and the bit flip from the page
    assert xor(pk, 73, 9) == 41 and decrypt(sk, [41]) == [1]
    assert xor(pk, 73, 52) == 23 and decrypt(sk, [23]) == [0]
    assert 9 * pk.y % 77 == 68 and decrypt(sk, [68]) == [1]


def test_round_trip_bytes() -> None:
    rng = random.Random(1982)
    pk, sk = keygen(P_BIG, Q_BIG, rng)
    assert jacobi(pk.y, pk.n) == 1
    msg = b"probabilistic encryption"
    cs = encrypt(pk, bits_of(msg), rng)
    assert len(cs) == 8 * len(msg)
    assert bytes_of(decrypt(sk, cs)) == msg


def test_probabilistic_and_all_ciphertexts_have_jacobi_one() -> None:
    rng = random.Random(7)
    pk, _ = keygen(P_BIG, Q_BIG, rng)
    ones = encrypt(pk, [1] * 40, rng)
    zeros = encrypt(pk, [0] * 40, rng)
    assert len(set(ones)) == 40 and len(set(zeros)) == 40
    assert all(jacobi(c, pk.n) == 1 and gcd(c, pk.n) == 1 for c in ones + zeros)


def test_xor_homomorphism_and_malleability() -> None:
    rng = random.Random(84)
    pk, sk = keygen(P_BIG, Q_BIG, rng)
    for a in (0, 1):
        for b in (0, 1):
            ca, cb = encrypt(pk, [a], rng)[0], encrypt(pk, [b], rng)[0]
            assert decrypt(sk, [xor(pk, ca, cb)]) == [a ^ b]
    # Without the key, multiplying by y flips the bit: GM is not IND-CCA2.
    c = encrypt(pk, [0], rng)[0]
    assert decrypt(sk, [c * pk.y % pk.n]) == [1]


def test_reduction_from_qr_is_tight() -> None:
    # The page's reduction B embeds its QR challenge z as the public y. Here
    # the IND-CPA adversary A is perfect (it uses p, to stand in for any A).
    # If z is a pseudosquare B wins always; if z is a square, every
    # ciphertext is a random square and B wins half the time. So
    # Adv_QR(B) = 1/2 = Adv_IND-CPA(A) / 2.
    rng = random.Random(1984)
    p, q = 1019, 1031  # both 3 mod 4
    n = p * q

    def adversary(c: int) -> int:
        return 0 if is_square_mod_prime(c % p, p) else 1

    def reduction(z: int) -> int:
        beta = rng.randrange(2)
        c = encrypt(PublicKey(n, z), [beta], rng)[0]
        return 1 if adversary(c) == beta else 0

    def random_element(square: bool) -> int:
        while True:
            r = rng.randrange(1, n)
            if gcd(r, n) == 1:
                return r * r % n if square else (n - r * r % n)

    trials = 3000
    pseudo = sum(reduction(random_element(False)) for _ in range(trials))
    square = sum(reduction(random_element(True)) for _ in range(trials))
    assert pseudo == trials
    assert abs(square / trials - 0.5) < 0.04
