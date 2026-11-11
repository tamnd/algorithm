# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rabin-signature/. The authors are listed in prov/SMWJN1.jsonl.
"""Tests for Rabin-Williams signatures. No official test vector for
Rabin-Williams signatures is used: IEEE 1363 defines the primitive but this
page found no vector that it could copy. The tests check the toy example of
the page, the tweak lemma on every value of a small modulus, round trips and
rejections on a toy key of 512 binary digits from a fixed seed, and the
factoring of N from two different roots."""

import math
import random

from rabin_signature import (PrivateKey, crt, factor_from_two_roots, hash_to_int, keygen, sign, sign_hash,
                             tweaks, verify, verify_hash)

TOY = PrivateKey(11, 7, b"\x00" * 32)  # p = 3 (mod 8), q = 7 (mod 8), N = 77
KEY = keygen(512, seed=1979)


def test_toy_example() -> None:
    assert tweaks(10, 11, 7) == (-1, 1)
    roots = sorted(sign_hash(TOY, 10, choice=c)[2] for c in range(4))
    assert roots == [12, 23, 54, 65]
    for s in roots:
        assert s * s % 77 == 67 and verify_hash(77, 10, (-1, 1, s))
    assert factor_from_two_roots(77, 23, 12) == 11
    assert factor_from_two_roots(77, 23, 54) is None  # 54 = -23


def test_tweak_lemma_exhaustive() -> None:
    for p, q in ((11, 7), (19, 23), (43, 31)):
        n = p * q
        for h in range(1, n):
            if math.gcd(h, n) != 1:
                continue
            good = [(e, f) for e in (1, -1) for f in (1, 2)
                    if pow(h * pow(e * f, -1, n) % p, (p - 1) // 2, p) == 1
                    and pow(h * pow(e * f, -1, n) % q, (q - 1) // 2, q) == 1]
            assert good == [tweaks(h, p, q)]


def test_key_shape() -> None:
    assert KEY.p % 8 == 3 and KEY.q % 8 == 7 and KEY.n.bit_length() == 512


def test_round_trips_and_determinism() -> None:
    for i in range(40):
        m = b"message %d" % i
        sig = sign(KEY, m)
        assert verify(KEY.n, m, sig)
        assert sign(KEY, m) == sig  # the root choice is a fixed function of H(M)


def test_rejections() -> None:
    m = b"pay 10"
    e, f, s = sign(KEY, m)
    n = KEY.n
    assert not verify(n, b"pay 11", (e, f, s))
    assert not verify(n, m, (-e, f, s))
    assert not verify(n, m, (e, 3 - f, s))
    assert not verify(n, m, (e, f, (s + 1) % n))
    assert not verify(n, m, (e, f, s + n))
    assert not verify(n, m, (2, f, s))
    # The negated root also verifies: a second signature on the same message.
    assert verify(n, m, (e, f, n - s))


def test_hash_range() -> None:
    for i in range(20):
        assert 0 <= hash_to_int(b"%d" % i, KEY.n) < KEY.n


def test_two_different_roots_factor_n() -> None:
    h = hash_to_int(b"signed twice by a careless signer", KEY.n)
    _, _, s0 = sign_hash(KEY, h, choice=0)
    _, _, s1 = sign_hash(KEY, h, choice=1)
    g = factor_from_two_roots(KEY.n, s0, s1)
    assert g in (KEY.p, KEY.q)


def test_unhashed_root_oracle_factors_n() -> None:
    # A signer that returns square roots of raw values chosen by the attacker:
    # the attacker sends x^2 and wins when the answer is not +x or -x.
    rng = random.Random(5)
    n, queries = KEY.n, 0
    while True:
        x = rng.randrange(2, n)
        queries += 1
        _, _, s = sign_hash(KEY, x * x % n)
        g = factor_from_two_roots(n, s, x)
        if g:
            break
    assert g in (KEY.p, KEY.q) and queries < 30


def test_crt() -> None:
    assert crt(1, 11, 2, 7) == 23
