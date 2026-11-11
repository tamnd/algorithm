# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ofb-mode/. The authors are listed in prov/K2XCQP.jsonl.

import random

import pytest

from aes import AES
from ofb_mode import ofb_crypt, ofb_keystream

KEY = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
IV = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
PT = bytes.fromhex(
    "6bc1bee22e409f96e93d7e117393172a"
    "ae2d8a571e03ac9c9eb76fac45af8e51"
    "30c81c46a35ce411e5fbc1191a0a52ef"
    "f69f2445df4f9b17ad2b417be66c3710"
)


def xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def test_aes_fips197_appendix_c() -> None:
    # FIPS 197, Appendix C.1 (AES-128).
    a = AES(bytes.fromhex("000102030405060708090a0b0c0d0e0f"))
    assert a.encrypt_block(bytes.fromhex("00112233445566778899aabbccddeeff")).hex() == "69c4e0d86a7b0430d8cdb78070b4c55a"


def test_sp800_38a_f41_f42_ofb_aes128() -> None:
    # SP 800-38A, Appendix F.4.1 (OFB-AES128.Encrypt) and F.4.2 (Decrypt).
    a = AES(KEY)
    ks = bytes.fromhex(
        "50fe67cc996d32b6da0937e99bafec60"
        "d9a4dada0892239f6b8b3d7680e15674"
        "a78819583f0308e7a6bf36b1386abf23"
        "c6d3416d29165c6fcb8e51a227ba994e"
    )
    ct = bytes.fromhex(
        "3b3fd92eb72dad20333449f8e83cfb4a"
        "7789508d16918f03f53c52dac54ed825"
        "9740051e9c5fecf64344f7a82260edcc"
        "304c6528f659c77866a510d9c1d6ae5e"
    )
    assert ofb_keystream(a, IV, 64) == ks
    assert ofb_crypt(a, IV, PT) == ct
    assert ofb_crypt(a, IV, ct) == PT


def test_round_trip_partial_block() -> None:
    rng = random.Random(8)
    a = AES(bytes(rng.randrange(256) for _ in range(16)))
    for n in (0, 1, 15, 16, 17, 40):
        iv = bytes(rng.randrange(256) for _ in range(16))
        p = bytes(rng.randrange(256) for _ in range(n))
        assert ofb_crypt(a, iv, ofb_crypt(a, iv, p)) == p
    with pytest.raises(ValueError):
        ofb_crypt(a, bytes(8), b"x")


def test_iv_reuse_gives_xor_of_plaintexts() -> None:
    a = AES(KEY)
    p1 = b"transfer 100 USD to account 7"
    p2 = b"transfer 999 USD to account 1"
    c1, c2 = ofb_crypt(a, IV, p1), ofb_crypt(a, IV, p2)
    assert xor(c1, c2) == xor(p1, p2)
    # Knowing p1 gives p2 at once.
    assert xor(xor(c1, c2), p1) == p2


def test_iv_equal_to_an_output_block_shifts_the_keystream() -> None:
    # If IV2 = O[1] of message 1, the keystream of message 2 is that of message 1 shifted by a block.
    a = AES(KEY)
    iv2 = a.encrypt_block(IV)
    assert ofb_keystream(a, iv2, 48) == ofb_keystream(a, IV, 64)[16:]


def test_bit_errors_do_not_spread_and_bytes_lost_do_not_heal() -> None:
    a = AES(KEY)
    c = bytearray(ofb_crypt(a, IV, PT))
    c[20] ^= 0x80
    p = ofb_crypt(a, IV, bytes(c))
    assert xor(p, PT) == bytes(20) + b"\x80" + bytes(43)
    lost = ofb_crypt(a, IV, PT)[:10] + ofb_crypt(a, IV, PT)[11:]
    q = ofb_crypt(a, IV, lost)
    assert q[:10] == PT[:10]
    assert sum(q[i] == PT[i + 1] for i in range(10, 63)) < 10
