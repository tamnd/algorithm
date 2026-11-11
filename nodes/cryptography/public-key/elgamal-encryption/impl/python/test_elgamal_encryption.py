# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elgamal-encryption/. The authors are listed in prov/V93QWB.jsonl.
"""Tests for ElGamal encryption.

There is no official test vector file for ElGamal encryption. The fixed
numbers below come from Handbook of Applied Cryptography (Menezes, van
Oorschot and Vanstone, 1996), Example 8.19. The other tests check the round
trip, the homomorphism, the malleability, the leak in the full group Z_p^*
and the tight reduction from DDH, all on toy groups with fixed seeds.
"""

import random

import pytest

from elgamal_encryption import (
    TOY_GROUP,
    Group,
    PrivateKey,
    PublicKey,
    decode,
    decrypt,
    decrypt_exponent,
    encode,
    encrypt,
    encrypt_exponent,
    is_member,
    keygen,
    multiply,
    rerandomize,
)


def is_prime(n: int) -> bool:
    """Deterministic Miller-Rabin for n < 3.3 * 10^24 (bases 2 to 37)."""
    if n < 2:
        return False
    bases = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for b in bases:
        if n % b == 0:
            return n == b
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in bases:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def legendre(a: int, p: int) -> int:
    """The Legendre symbol by Euler's criterion, as +1, -1 or 0."""
    t = pow(a, (p - 1) // 2, p)
    return -1 if t == p - 1 else t


# Handbook of Applied Cryptography, Example 8.19: p = 2357, alpha = 2
# generates Z_2357^*, a = 1751, alpha^a = 1185, k = 1520, m = 2035,
# gamma = 1430, delta = 697, gamma^(p-1-a) = 872.
HAC = Group(2357, 2356, 2)


def test_hac_example_8_19() -> None:
    pk, sk = PublicKey(HAC, pow(2, 1751, 2357)), PrivateKey(HAC, 1751)
    assert pk.h == 1185
    assert encrypt(pk, 2035, r=1520) == (1430, 697)
    assert pow(1430, 2357 - 1 - 1751, 2357) == 872
    assert decrypt(sk, (1430, 697)) == 2035


def test_toy_group_is_a_safe_prime_group() -> None:
    p, q, g = TOY_GROUP.p, TOY_GROUP.q, TOY_GROUP.g
    assert p == 2 * q + 1 and p == 2**63 + 2679
    assert is_prime(p) and is_prime(q)
    assert g != 1 and pow(g, q, p) == 1
    # No safe prime lies between 2^63 and p.
    assert not any(is_prime(c) and is_prime((c - 1) // 2) for c in range(2**63 + 1, p, 2))


def test_round_trip_and_encoding() -> None:
    rng = random.Random(8519)
    pk, sk = keygen(TOY_GROUP, rng)
    for _ in range(300):
        m = rng.randrange(1, TOY_GROUP.q + 1)
        a = encode(TOY_GROUP, m)
        assert is_member(TOY_GROUP, a)
        assert decode(TOY_GROUP, a) == m
        assert decode(TOY_GROUP, decrypt(sk, encrypt(pk, a, rng=rng))) == m


def test_probabilistic() -> None:
    rng = random.Random(3)
    pk, _ = keygen(TOY_GROUP, rng)
    m = encode(TOY_GROUP, 42)
    assert len({encrypt(pk, m, rng=rng) for _ in range(50)}) == 50


def test_multiplicative_homomorphism_and_rerandomization() -> None:
    rng = random.Random(1985)
    pk, sk = keygen(TOY_GROUP, rng)
    p = TOY_GROUP.p
    for _ in range(100):
        a = pow(TOY_GROUP.g, rng.randrange(TOY_GROUP.q), p)
        b = pow(TOY_GROUP.g, rng.randrange(TOY_GROUP.q), p)
        ca, cb = encrypt(pk, a, rng=rng), encrypt(pk, b, rng=rng)
        assert decrypt(sk, multiply(TOY_GROUP, ca, cb)) == a * b % p
        cr = rerandomize(pk, ca, rng.randrange(1, TOY_GROUP.q))
        assert cr != ca and decrypt(sk, cr) == a


def test_malleability_attack() -> None:
    # Without the key, multiply c2 by t: the ciphertext now decrypts to m * t.
    rng = random.Random(77)
    pk, sk = keygen(TOY_GROUP, rng)
    m = encode(TOY_GROUP, 1000)
    c1, c2 = encrypt(pk, m, rng=rng)
    t = encode(TOY_GROUP, 2)
    assert decrypt(sk, (c1, c2 * t % TOY_GROUP.p)) == m * t % TOY_GROUP.p


def test_exponential_elgamal_tally() -> None:
    rng = random.Random(2024)
    pk, sk = keygen(TOY_GROUP, rng)
    votes = [rng.randrange(2) for _ in range(40)]
    total = encrypt(pk, 1, r=0)
    for v in votes:
        total = multiply(TOY_GROUP, total, encrypt_exponent(pk, v, rng=rng))
    assert decrypt_exponent(sk, total, bound=len(votes)) == sum(votes)
    assert decrypt_exponent(sk, encrypt_exponent(pk, 0, rng=rng), bound=5) == 0


def test_rejects_non_members() -> None:
    rng = random.Random(5)
    pk, sk = keygen(TOY_GROUP, rng)
    non_residue = TOY_GROUP.p - 1  # -1 is not a square when p = 3 (mod 4)
    with pytest.raises(ValueError):
        encrypt(pk, non_residue, rng=rng)
    c1, c2 = encrypt(pk, 4, rng=rng)
    with pytest.raises(ValueError):
        decrypt(sk, (c1, TOY_GROUP.p - c2))
    with pytest.raises(ValueError):
        decrypt(sk, (0, c2))


def legendre_adversary(pk: PublicKey, c: tuple[int, int]) -> int:
    """IND-CPA adversary in the full group Z_p^* for m0 = 1 (a residue) and
    m1 = a non-residue. It reads the quadratic character of the message."""
    p = pk.group.p
    c1, c2 = c
    mask = -1 if legendre(pk.h, p) == -1 and legendre(c1, p) == -1 else 1
    return 0 if legendre(c2, p) * mask == 1 else 1


def test_full_group_is_not_ind_cpa_and_the_reduction_is_tight() -> None:
    # In Z_2357^* the adversary always wins: advantage 1.
    rng = random.Random(819)
    p, n, g = HAC.p, HAC.q, HAC.g
    m0, m1 = 1, 2  # 2 is a generator, so it is a non-residue
    assert legendre(m1, p) == -1
    wins = 0
    for _ in range(500):
        pk, _ = keygen(HAC, rng)
        b = rng.randrange(2)
        wins += legendre_adversary(pk, encrypt(pk, (m0, m1)[b], rng=rng)) == b
    assert wins == 500

    # The reduction B of the page turns it into a DDH distinguisher. On a
    # Diffie-Hellman triple B outputs 1 when the adversary wins (probability
    # 1); on a random triple B outputs 1 with probability 1/2. So
    # Adv_DDH(B) = 1/2 = Adv_IND-CPA(A) / 2, as the theorem says.
    def reduction_b(gx: int, gy: int, gz: int) -> int:
        b = rng.randrange(2)
        pk = PublicKey(HAC, gx)
        c = (gy, (m0, m1)[b] * gz % p)
        return 1 if legendre_adversary(pk, c) == b else 0

    real = rand = 0
    trials = 2000
    for _ in range(trials):
        x, y, z = rng.randrange(n), rng.randrange(n), rng.randrange(n)
        real += reduction_b(pow(g, x, p), pow(g, y, p), pow(g, x * y, p))
        rand += reduction_b(pow(g, x, p), pow(g, y, p), pow(g, z, p))
    assert real == trials
    assert abs(rand / trials - 0.5) < 0.05


def test_subgroup_gives_the_legendre_adversary_nothing() -> None:
    rng = random.Random(4)
    pk, _ = keygen(TOY_GROUP, rng)
    for _ in range(100):
        c1, c2 = encrypt(pk, encode(TOY_GROUP, rng.randrange(1, 10**6)), rng=rng)
        assert legendre(c1, TOY_GROUP.p) == 1 and legendre(c2, TOY_GROUP.p) == 1
