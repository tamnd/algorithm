# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/camellia/. The authors are listed in prov/JV176X.jsonl.

import random

from camellia import SBOX1, SBOX4, decrypt_block, encrypt_block, fl, fl_inv

PT = bytes.fromhex("0123456789abcdeffedcba9876543210")


# RFC 3713 Appendix A, 128-bit key.
def test_rfc3713_appendix_a_128() -> None:
    key = bytes.fromhex("0123456789abcdeffedcba9876543210")
    ct = bytes.fromhex("67673138549669730857065648eabe43")
    assert encrypt_block(key, PT) == ct
    assert decrypt_block(key, ct) == PT


# RFC 3713 Appendix A, 192-bit key.
def test_rfc3713_appendix_a_192() -> None:
    key = bytes.fromhex("0123456789abcdeffedcba98765432100011223344556677")
    ct = bytes.fromhex("b4993401b3e996f84ee5cee7d79b09b9")
    assert encrypt_block(key, PT) == ct
    assert decrypt_block(key, ct) == PT


# RFC 3713 Appendix A, 256-bit key.
def test_rfc3713_appendix_a_256() -> None:
    key = bytes.fromhex("0123456789abcdeffedcba987654321000112233445566778899aabbccddeeff")
    ct = bytes.fromhex("9acc237dff16d76c20ef7c919e3a7509")
    assert encrypt_block(key, PT) == ct
    assert decrypt_block(key, ct) == PT


# RFC 3713 Section 2.4.4 gives SBOX1[0x3d] = 86 as its example.
def test_sbox_example() -> None:
    assert SBOX1[0x3D] == 86
    assert sorted(SBOX1) == list(range(256))
    assert sorted(SBOX4) == list(range(256))


def test_fl_inverse() -> None:
    rng = random.Random(1)
    for _ in range(200):
        x, k = rng.getrandbits(64), rng.getrandbits(64)
        assert fl_inv(fl(x, k), k) == x


def test_round_trip_random() -> None:
    rng = random.Random(2)
    for n in (16, 24, 32):
        for _ in range(5):
            key = rng.randbytes(n)
            m = rng.randbytes(16)
            assert decrypt_block(key, encrypt_block(key, m)) == m


def test_avalanche() -> None:
    key = bytes(16)
    c0 = int.from_bytes(encrypt_block(key, bytes(16)), "big")
    flips = 0
    for i in range(128):
        m = (1 << i).to_bytes(16, "big")
        flips += bin(c0 ^ int.from_bytes(encrypt_block(key, m), "big")).count("1")
    assert 56 < flips / 128 < 72
