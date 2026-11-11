# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/signcryption/. The authors are listed in prov/G5XJ7C.jsonl.
"""Tests for Zheng's signcryption on the toy group p = 2039."""

import random
from dataclasses import replace

import pytest

from signcryption import G, P, Q, Signcryptext, keygen, signcrypt, stream_xor, unsigncrypt

X_A, Y_A = keygen(random.Random(1))
X_B, Y_B = keygen(random.Random(2))
X_C, Y_C = keygen(random.Random(3))
MSGS = [b"", b"hi", b"attack at dawn", bytes(range(100))]


def test_group() -> None:
    assert P == 2 * Q + 1 and pow(G, Q, P) == 1 and G != 1


def test_stream_cipher_round_trip() -> None:
    key = b"k" * 32
    for m in MSGS:
        assert stream_xor(key, stream_xor(key, m)) == m
    assert stream_xor(key, bytes(40)) != stream_xor(b"j" * 32, bytes(40))


@pytest.mark.parametrize("variant", [1, 2])
def test_round_trip(variant: int) -> None:
    rng = random.Random(10 + variant)
    for m in MSGS:
        for _ in range(5):
            ct = signcrypt(X_A, Y_B, m, variant, rng)
            assert unsigncrypt(Y_A, X_B, ct, variant) == m
            if len(m) >= 4:
                assert ct.c != m


@pytest.mark.parametrize("variant", [1, 2])
def test_tag_rejection(variant: int) -> None:
    rng = random.Random(20 + variant)
    m = b"attack at dawn"
    ct = signcrypt(X_A, Y_B, m, variant, rng)
    flipped = bytes([ct.c[0] ^ 1]) + ct.c[1:]
    assert unsigncrypt(Y_A, X_B, replace(ct, c=flipped), variant) is None
    assert unsigncrypt(Y_A, X_B, replace(ct, r=(ct.r + 1) % Q), variant) is None
    assert unsigncrypt(Y_A, X_B, replace(ct, s=ct.s % (Q - 1) + 1), variant) is None


@pytest.mark.parametrize("variant", [1, 2])
def test_wrong_sender_or_recipient(variant: int) -> None:
    rng = random.Random(30 + variant)
    m = b"for Bob from Alice"
    ct = signcrypt(X_A, Y_B, m, variant, rng)
    assert unsigncrypt(Y_A, X_C, ct, variant) is None  # Carol cannot open it
    assert unsigncrypt(Y_C, X_B, ct, variant) is None  # it is not from Carol
    assert unsigncrypt(Y_A, X_B, ct, 3 - variant) is None  # the other variant


def test_random_forgeries_fail() -> None:
    rng = random.Random(40)
    fakes = [Signcryptext(rng.randbytes(8), rng.randrange(Q), rng.randrange(1, Q)) for _ in range(40)]
    accepted = sum(unsigncrypt(Y_A, X_B, f) is not None for f in fakes)
    assert accepted == 0
