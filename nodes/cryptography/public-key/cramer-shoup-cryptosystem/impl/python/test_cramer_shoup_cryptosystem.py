# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cramer-shoup-cryptosystem/. The authors are listed in prov/DP6M6E.jsonl.
"""Tests for the Cramer-Shoup cryptosystem.

There are no official test vectors for the original scheme. The tests use
the toy safe prime group of 64 binary digits and, for the exact counting
test of the rejection lemma, the group of squares modulo 23 (q = 11).
"""

import random
from collections import Counter

from cramer_shoup_cryptosystem import (
    TOY,
    Group,
    PrivateKey,
    decode,
    decrypt,
    encode,
    encrypt,
    in_group,
    keygen,
    tcr_hash,
)

SMALL = Group(23, 11, 4, 9)  # 4 and 9 are squares modulo 23, so both have order 11


def test_toy_group_parameters() -> None:
    p, q = TOY.p, TOY.q
    assert p == 2 * q + 1 and p % 4 == 3
    for n in (p, q):  # Fermat checks with several bases
        assert all(pow(a, n - 1, n) == 1 for a in (2, 3, 5, 7, 11, 13))
    assert in_group(TOY, TOY.g1) and in_group(TOY, TOY.g2)
    assert TOY.g1 != 1 and TOY.g2 != 1 and TOY.g1 != TOY.g2


def test_round_trip() -> None:
    rng = random.Random(1998)
    pk, sk = keygen(TOY, rng)
    for m in (1, 2, 5, 12345, TOY.q):
        ct = encrypt(pk, encode(TOY, m), rng)
        assert decode(TOY, decrypt(sk, ct)) == m


def test_small_group_round_trip_all_messages() -> None:
    rng = random.Random(23)
    pk, sk = keygen(SMALL, rng)
    for m in range(1, SMALL.q + 1):
        assert decode(SMALL, decrypt(sk, encrypt(pk, encode(SMALL, m), rng))) == m


def test_every_single_change_is_rejected() -> None:
    rng = random.Random(7)
    pk, sk = keygen(TOY, rng)
    p = TOY.p
    ct = encrypt(pk, encode(TOY, 42), rng)
    for i in range(4):
        changed = list(ct)
        changed[i] = changed[i] * TOY.g1 % p  # stays in the group
        assert decrypt(sk, tuple(changed)) is None
    # the ElGamal mauling (u1, u2, g1 e, v) is rejected
    u1, u2, e, v = ct
    assert decrypt(sk, (u1, u2, e * TOY.g1 % p, v)) is None


def test_non_members_are_rejected() -> None:
    rng = random.Random(8)
    pk, sk = keygen(TOY, rng)
    u1, u2, e, v = encrypt(pk, encode(TOY, 3), rng)
    p = TOY.p
    assert decrypt(sk, (p - u1, u2, e, v)) is None  # -u1 is not a square
    assert decrypt(sk, (u1, u2, e, 0)) is None
    assert decrypt(sk, (u1, u2, e, v + p)) is None


def test_variant_without_check_is_malleable() -> None:
    # Without the check of line L12, the ElGamal mauling works:
    # (u1, u2, g1 e, v) decrypts to g1 m.
    rng = random.Random(9)
    pk, sk = keygen(TOY, rng)
    p, q = TOY.p, TOY.q
    m = encode(TOY, 1000)
    u1, u2, e, v = encrypt(pk, m, rng)
    unchecked = e * TOY.g1 % p * pow(u1, (q - sk.z) % q, p) % p
    assert unchecked == TOY.g1 * m % p


def test_lite_tag_ignores_e() -> None:
    # "Cramer-Shoup lite": tag v = c^r, check u1^x1 u2^x2 = v. The tag does
    # not depend on e, so the mauled ciphertext passes and decrypts to g1 m.
    rng = random.Random(11)
    pk, sk = keygen(TOY, rng)
    p, q = TOY.p, TOY.q
    m = encode(TOY, 77)
    r = rng.randrange(q)
    u1, u2 = pow(TOY.g1, r, p), pow(TOY.g2, r, p)
    e, v = pow(pk.h, r, p) * m % p, pow(pk.c, r, p)
    e2 = e * TOY.g1 % p
    assert pow(u1, sk.x1, p) * pow(u2, sk.x2, p) % p == v  # the lite check passes
    assert e2 * pow(u1, (q - sk.z) % q, p) % p == TOY.g1 * m % p


def test_rejection_lemma_exact_count() -> None:
    # Fix a public key (c, d). Among the q^2 private keys (x1, x2, y1, y2)
    # that give it, an invalid query (u1, u2) = (g1^r1, g2^r2) with r1 != r2
    # and any alpha makes the expected v uniform: each value of the group is
    # hit by exactly q of those keys. So a guessed v passes with probability 1/q.
    p, q, g1, g2 = SMALL.p, SMALL.q, SMALL.g1, SMALL.g2
    x1, x2, y1, y2 = 3, 7, 2, 9
    c = pow(g1, x1, p) * pow(g2, x2, p) % p
    d = pow(g1, y1, p) * pow(g2, y2, p) % p
    keys = [
        (a1, a2, b1, b2)
        for a1 in range(q)
        for a2 in range(q)
        if pow(g1, a1, p) * pow(g2, a2, p) % p == c
        for b1 in range(q)
        for b2 in range(q)
        if pow(g1, b1, p) * pow(g2, b2, p) % p == d
    ]
    assert len(keys) == q * q
    u1, u2 = pow(g1, 4, p), pow(g2, 6, p)  # r1 = 4, r2 = 6: invalid
    for alpha in range(q):
        hits = Counter(
            pow(u1, (a1 + b1 * alpha) % q, p) * pow(u2, (a2 + b2 * alpha) % q, p) % p
            for a1, a2, b1, b2 in keys
        )
        assert len(hits) == q and set(hits.values()) == {q}
    # a valid pair (r1 = r2) gives the same v for every consistent key
    w1, w2 = pow(g1, 5, p), pow(g2, 5, p)
    vs = {pow(w1, (a1 + b1 * 3) % q, p) * pow(w2, (a2 + b2 * 3) % q, p) % p for a1, a2, b1, b2 in keys}
    assert len(vs) == 1


def test_cca_game_mauling_adversary_gets_nothing() -> None:
    # A local IND-CCA2 game: the adversary mauls the challenge in every way
    # it knows and asks the oracle; every answer is a rejection.
    rng = random.Random(10)
    pk, sk = keygen(TOY, rng)
    p = TOY.p
    m0, m1 = encode(TOY, 11), encode(TOY, 22)
    challenge = encrypt(pk, m1, rng)

    def oracle(ct: tuple[int, int, int, int]) -> int | None:
        assert ct != challenge
        return decrypt(sk, ct)

    u1, u2, e, v = challenge
    t = TOY.g2
    for query in (
        (u1, u2, e * t % p, v),
        (u1 * t % p, u2, e, v),
        (u1, u2 * t % p, e, v * t % p),
        (u1 * u1 % p, u2 * u2 % p, e * e % p, v * v % p),
    ):
        assert oracle(query) is None
    assert decrypt(sk, challenge) in (m0, m1)


def test_hash_is_deterministic_and_in_range() -> None:
    a = tcr_hash(TOY, 2, 3, 4)
    assert a == tcr_hash(TOY, 2, 3, 4) and 0 <= a < TOY.q
    assert a != tcr_hash(TOY, 3, 2, 4)


def test_private_key_fields() -> None:
    _, sk = keygen(SMALL, random.Random(1))
    assert isinstance(sk, PrivateKey)
    assert all(0 <= x < SMALL.q for x in (sk.x1, sk.x2, sk.y1, sk.y2, sk.z))
