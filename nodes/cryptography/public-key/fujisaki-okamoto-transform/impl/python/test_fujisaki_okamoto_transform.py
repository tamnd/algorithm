# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fujisaki-okamoto-transform/. The authors are listed in prov/4ZNST2.jsonl.
"""Tests for the FO transform with implicit rejection over ElGamal.

There are no official test vectors for FO applied to ElGamal. (ML-KEM, the
standard scheme built with this transform, has its own vectors, but it is a
different base scheme.) Randomness comes from a seeded generator.
"""

import random

from fujisaki_okamoto_transform import (
    GEN,
    P,
    Q,
    decaps,
    elgamal_decrypt,
    elgamal_encrypt,
    encaps,
    hash_g,
    hash_h,
    hash_rej,
    insecure_decaps_hash_m_only,
    insecure_encaps_hash_m_only,
    keygen,
)


def seeded(seed: int):
    rng = random.Random(seed)
    return lambda n: rng.randbytes(n)


def test_group_parameters() -> None:
    assert P == 2 * Q + 1
    for n in (P, Q):
        assert all(pow(a, n - 1, n) == 1 for a in (2, 3, 5, 7, 11, 13))
    assert pow(GEN, Q, P) == 1 and GEN != 1


def test_encaps_decaps_agree() -> None:
    rb = seeded(1999)
    pk, sk = keygen(rb)
    keys = set()
    for _ in range(20):
        c, k = encaps(pk, rb)
        assert decaps(sk, c) == k
        keys.add(k)
    assert len(keys) == 20


def test_encryption_is_derandomized() -> None:
    rb = seeded(2)
    pk, sk = keygen(rb)
    m = pow(GEN, 12345, P)
    c1 = elgamal_encrypt(pk, m, hash_g(m))
    c2 = elgamal_encrypt(pk, m, hash_g(m))
    assert c1 == c2  # T makes encryption deterministic
    assert elgamal_decrypt(sk.x, c1) == m


def test_implicit_rejection_of_mauled_ciphertext() -> None:
    rb = seeded(3)
    pk, sk = keygen(rb)
    c, k = encaps(pk, rb)
    mauled = (c[0], c[1] * GEN % P)  # the ElGamal mauling: plaintext times g
    k2 = decaps(sk, mauled)
    assert k2 != k
    assert k2 == hash_rej(sk.s, mauled)  # the pseudorandom rejection key
    assert decaps(sk, mauled) == k2  # deterministic


def test_rerandomized_ciphertext_is_rejected() -> None:
    # (c1 g^a, c2 h^a) decrypts to the same m under plain ElGamal, but its
    # randomness is no longer G(m), so the re-encryption check fails.
    rb = seeded(4)
    pk, sk = keygen(rb)
    c, k = encaps(pk, rb)
    a = 777
    rerand = (c[0] * pow(GEN, a, P) % P, c[1] * pow(pk.h, a, P) % P)
    assert elgamal_decrypt(sk.x, rerand) == elgamal_decrypt(sk.x, c)
    assert decaps(sk, rerand) == hash_rej(sk.s, rerand) != k


def test_rejection_key_depends_on_secret() -> None:
    rb = seeded(5)
    pk, sk = keygen(rb)
    _, sk_other = keygen(rb)
    bad = (GEN, GEN)
    assert decaps(sk, bad) != hash_rej(sk_other.s, bad)


def test_non_members_rejected_implicitly() -> None:
    rb = seeded(6)
    pk, sk = keygen(rb)
    c, k = encaps(pk, rb)
    bad = (P - c[0], c[1])  # -c1 is not a square
    assert decaps(sk, bad) == hash_rej(sk.s, bad)


def test_hash_m_only_without_t_is_broken() -> None:
    # Exercise 3 on the page: with randomized ElGamal, no re-encryption
    # check, and K = H(m), one rerandomized decapsulation query returns the
    # challenge key.
    rb = seeded(7)
    pk, sk = keygen(rb)
    c, k = insecure_encaps_hash_m_only(pk, rb)
    query = (c[0] * pow(GEN, 99, P) % P, c[1] * pow(pk.h, 99, P) % P)
    assert query != c
    assert insecure_decaps_hash_m_only(sk, query) == k


def test_key_binds_ciphertext() -> None:
    m = pow(GEN, 5, P)
    assert hash_h(m, (1, 2)) != hash_h(m, (2, 1))
