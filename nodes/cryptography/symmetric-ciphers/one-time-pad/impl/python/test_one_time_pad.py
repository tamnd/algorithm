# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/one-time-pad/. The authors are listed in prov/K0CNG3.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from one_time_pad import (
    crib_drag,
    extend,
    generate_key,
    is_perfectly_secret,
    malleate,
    otp_decrypt,
    otp_encrypt,
    posterior,
    xor,
)

# Two public domain texts of the same length: the Declaration of
# Independence (1776) and the Gettysburg Address (1863), cut to 71 bytes.
M1 = b"We hold these truths to be self-evident, that all men are created equal"
M2 = b"Four score and seven years ago our fathers brought forth on this contin"


def test_example_and_edge_cases() -> None:
    m = b"HELLO"
    k = bytes([0x58, 0x4D, 0x43, 0x4B, 0x59])
    c = otp_encrypt(m, k)
    assert c == bytes([0x10, 0x08, 0x0F, 0x07, 0x16])
    assert otp_decrypt(c, k) == m
    assert otp_encrypt(b"", b"") == b""
    with pytest.raises(ValueError):
        otp_encrypt(b"AB", b"A")
    with pytest.raises(ValueError):
        otp_encrypt(b"AB", b"ABC")
    assert len(generate_key(32)) == 32


def test_against_integer_xor() -> None:
    rng = random.Random(16)
    for _ in range(600):
        n = rng.randrange(40)
        m = bytes(rng.randrange(256) for _ in range(n))
        k = bytes(rng.randrange(256) for _ in range(n))
        c = otp_encrypt(m, k)
        expected = (int.from_bytes(m, "big") ^ int.from_bytes(k, "big")).to_bytes(n, "big")
        assert c == expected
        assert otp_decrypt(c, k) == m
        assert xor(c, m) == k  # known plaintext gives the key, which is useless if never reused


def test_two_time_pad_crib_drag() -> None:
    rng = random.Random(5)
    key = bytes(rng.randrange(256) for _ in M1)
    c1, c2 = otp_encrypt(M1, key), otp_encrypt(M2, key)
    x = xor(c1, c2)
    assert x == xor(M1, M2)  # the key cancels
    # Step 1: drag " and ". At offset 10 the other message reads "ese t".
    assert crib_drag(x, b" and ") == [(10, b"ese t"), (26, b" slgf")]
    # Step 2: guess that "ese t" is part of "hold these truths" in the first message.
    assert extend(x, b"hold these truths", 3) == b"r score and seven"
    # Step 3: drag " that ". The only hit gives "rs bro", from "fathers brought".
    assert crib_drag(x, b" that ") == [(40, b"rs bro")]
    assert extend(x, b"fathers brought forth", 35) == b"dent, that all men ar"
    # With one message known, the other is recovered in full, and then the key.
    assert extend(x, M1, 0) == M2
    assert xor(c1, M1) == key


def test_malleability() -> None:
    rng = random.Random(17)
    m = b"PAY ALICE 0100 DOLLARS"
    k = bytes(rng.randrange(256) for _ in m)
    c = otp_encrypt(m, k)
    c2 = malleate(c, b"0100", b"9900", 10)
    assert otp_decrypt(c2, k) == b"PAY ALICE 9900 DOLLARS"


def test_exact_perfect_secrecy() -> None:
    prior = {0: Fraction(1, 2), 1: Fraction(1, 4), 2: Fraction(1, 8), 3: Fraction(1, 8)}
    # The one-time pad on 2 bits: four keys, uniform.
    post = posterior(prior, [0, 1, 2, 3])
    assert sorted(post) == [0, 1, 2, 3]
    assert all(p == prior for p in post.values())
    assert is_perfectly_secret(prior, [0, 1, 2, 3])
    # Only the keys 00 and 11: seeing c = 00 leaves only the messages 00 and 11.
    post = posterior(prior, [0, 3])
    assert post[0] == {0: Fraction(4, 5), 1: Fraction(0), 2: Fraction(0), 3: Fraction(1, 5)}
    assert not is_perfectly_secret(prior, [0, 3])


def test_fewer_keys_than_messages_fail() -> None:
    # On 3-bit messages with every message possible, each key set smaller
    # than the message space fails, and only the full key set succeeds.
    prior = {m: Fraction(m + 1, 36) for m in range(8)}
    for size in range(1, 9):
        for keys in itertools.combinations(range(8), size):
            assert is_perfectly_secret(prior, list(keys)) == (size == 8)
