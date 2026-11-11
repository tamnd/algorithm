# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/encrypted-key-exchange/. The authors are listed in prov/MY9FM0.jsonl.
#
# EKE has no official test vectors. These tests check the group, the
# encoding, agreement, and the partition attack on toy parameters.

import random

from encrypted_key_exchange import (
    P_1024,
    P_TOY,
    Group,
    bad_decrypt,
    bad_encrypt,
    decrypt,
    encrypt,
    partition_attack,
    run,
)


def miller_rabin(n: int, rounds: int = 20) -> bool:
    if n < 4:
        return n in (2, 3)
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    rng = random.Random(n)
    for _ in range(rounds):
        x = pow(rng.randrange(2, n - 1), d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


BIG = Group(P_1024)
TOY = Group(P_TOY)
WORDS = [b"word%03d" % i for i in range(256)]


def test_groups_are_safe_primes():
    for grp in (BIG, TOY):
        assert miller_rabin(grp.p) and miller_rabin(grp.q)
        assert grp.is_qr(grp.g) and pow(grp.g, grp.q, grp.p) == 1


def test_encoding_round_trip_and_every_ciphertext_decodes():
    rng = random.Random(1)
    for grp in (BIG, TOY):
        for _ in range(5):
            y = pow(grp.g, rng.randrange(1, grp.q), grp.p)
            c = encrypt(b"pw", y, grp)
            assert 0 <= c < grp.q and decrypt(b"pw", c, grp) == y
    for _ in range(200):     # any ciphertext under any password is a valid group element
        assert TOY.is_qr(decrypt(rng.choice(WORDS), rng.randrange(TOY.q), TOY))


def test_agreement_and_wrong_password():
    rng = random.Random(2)
    rb = lambda n: rng.randrange(n)  # noqa: E731
    sk_a, sk_b = run(b"correct horse", b"correct horse", BIG, rb)
    assert sk_a == sk_b
    sk_a, sk_b = run(b"correct horse", b"battery staple", BIG, rb)
    assert sk_a != sk_b


def eavesdrop(pw: bytes, enc, sessions: int, seed: int):
    rng = random.Random(seed)
    out = []
    for _ in range(sessions):
        y = pow(TOY.g, rng.randrange(1, TOY.q), TOY.p)
        out.append(enc(pw, y, TOY))
    return out


def test_partition_attack_breaks_the_bad_encoding():
    secret = WORDS[137]
    seen = eavesdrop(secret, bad_encrypt, 40, seed=3)
    alive = partition_attack(seen, WORDS, bad_decrypt, TOY)
    assert alive == [secret]


def test_partition_attack_learns_nothing_from_the_careful_encoding():
    secret = WORDS[137]
    seen = eavesdrop(secret, encrypt, 20, seed=4)
    alive = partition_attack(seen, WORDS, decrypt, TOY)
    assert alive == WORDS
