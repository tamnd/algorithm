# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chacha20/. The authors are listed in prov/79BC7C.jsonl.

import random

from chacha20 import chacha20_block, chacha20_encrypt, quarter_round


def h(s: str) -> bytes:
    return bytes.fromhex(s.replace(" ", "").replace(":", ""))


KEY = bytes(range(32))


def test_quarter_round_rfc8439_2_1_1() -> None:
    # RFC 8439, Section 2.1.1.
    x = [0x11111111, 0x01020304, 0x9B8D6F43, 0x01234567]
    quarter_round(x, 0, 1, 2, 3)
    assert x == [0xEA2A92F4, 0xCB1CF8CE, 0x4581472E, 0x5881C4BB]


def test_block_rfc8439_2_3_2() -> None:
    # RFC 8439, Section 2.3.2: key 00..1f, nonce 00:00:00:09:00:00:00:4a:00:00:00:00, counter 1.
    nonce = h("00:00:00:09:00:00:00:4a:00:00:00:00")
    want = h(
        "10 f1 e7 e4 d1 3b 59 15 50 0f dd 1f a3 20 71 c4"
        "c7 d1 f4 c7 33 c0 68 03 04 22 aa 9a c3 d4 6c 4e"
        "d2 82 64 46 07 9f aa 09 14 c2 d7 05 d9 8b 02 a2"
        "b5 12 9c d1 de 16 4e b9 cb d0 83 e8 a2 50 3c 4e"
    )
    assert chacha20_block(KEY, 1, nonce) == want


def test_encrypt_rfc8439_2_4_2() -> None:
    # RFC 8439, Section 2.4.2: key 00..1f, nonce 00:00:00:00:00:00:00:4a:00:00:00:00, counter 1.
    nonce = h("00:00:00:00:00:00:00:4a:00:00:00:00")
    pt = (
        b"Ladies and Gentlemen of the class of '99: If I could offer you only one tip"
        b" for the future, sunscreen would be it."
    )
    want = h(
        "6e2e359a2568f98041ba0728dd0d6981"
        "e97e7aec1d4360c20a27afccfd9fae0b"
        "f91b65c5524733ab8f593dabcd62b357"
        "1639d624e65152ab8f530c359f0861d8"
        "07ca0dbf500d6a6156a38e088a22b65e"
        "52bc514d16ccf806818ce91ab7793736"
        "5af90bbf74a35be6b40b8eedf2785e42"
        "874d"
    )
    assert len(pt) == 114
    assert chacha20_encrypt(KEY, 1, nonce, pt) == want
    assert chacha20_encrypt(KEY, 1, nonce, want) == pt


def test_round_trip_random() -> None:
    rng = random.Random(7)
    for _ in range(10):
        key = bytes(rng.randrange(256) for _ in range(32))
        nonce = bytes(rng.randrange(256) for _ in range(12))
        msg = bytes(rng.randrange(256) for _ in range(rng.randrange(0, 200)))
        c = chacha20_encrypt(key, 0, nonce, msg)
        assert len(c) == len(msg)
        assert chacha20_encrypt(key, 0, nonce, c) == msg


def test_block_avalanche() -> None:
    # One flipped nonce bit changes about half of the 512 output bits.
    rng = random.Random(8)
    total = 0
    for _ in range(20):
        key = bytes(rng.randrange(256) for _ in range(32))
        nonce = bytearray(rng.randrange(256) for _ in range(12))
        a = chacha20_block(key, 0, bytes(nonce))
        nonce[rng.randrange(12)] ^= 1 << rng.randrange(8)
        b = chacha20_block(key, 0, bytes(nonce))
        total += bin(int.from_bytes(a, "big") ^ int.from_bytes(b, "big")).count("1")
    assert 220 <= total / 20 <= 292


def test_nonce_reuse_two_time_pad() -> None:
    nonce = bytes(12)
    m1 = b"the meeting is at nine in room 4"
    m2 = b"wire the funds to account 55123"
    c1 = chacha20_encrypt(KEY, 1, nonce, m1)
    c2 = chacha20_encrypt(KEY, 1, nonce, m2)
    x = bytes(a ^ b for a, b in zip(c1, c2))
    assert x == bytes(a ^ b for a, b in zip(m1, m2))
    assert bytes(a ^ b for a, b in zip(x, m1)) == m2[: len(x)]


def test_bit_flip_malleability() -> None:
    nonce = bytes(range(12))
    c = bytearray(chacha20_encrypt(KEY, 1, nonce, b"amount=0010"))
    c[7] ^= ord("0") ^ ord("9")
    assert chacha20_encrypt(KEY, 1, nonce, bytes(c)) == b"amount=9010"
