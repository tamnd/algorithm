# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ctr-mode/. The authors are listed in prov/ZGS9FV.jsonl.

import random

import pytest

from aes import AES
from ctr_mode import counter_block, ctr_crypt, keystream_block

KEY = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
T1 = bytes.fromhex("f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff")
PT = bytes.fromhex(
    "6bc1bee22e409f96e93d7e117393172a"
    "ae2d8a571e03ac9c9eb76fac45af8e51"
    "30c81c46a35ce411e5fbc1191a0a52ef"
    "f69f2445df4f9b17ad2b417be66c3710"
)
CT = bytes.fromhex(
    "874d6191b620e3261bef6864990db6ce"
    "9806f66b7970fdff8617187bb9fffdff"
    "5ae4df3edbd5d35e5b4f09020db03eab"
    "1e031dda2fbe03d1792170a0f3009cee"
)


def xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def test_aes_fips197_appendix_c() -> None:
    # FIPS 197, Appendix C.1 (AES-128).
    a = AES(bytes.fromhex("000102030405060708090a0b0c0d0e0f"))
    assert a.encrypt_block(bytes.fromhex("00112233445566778899aabbccddeeff")).hex() == "69c4e0d86a7b0430d8cdb78070b4c55a"


def test_sp800_38a_f51_f52_ctr_aes128() -> None:
    # SP 800-38A, Appendix F.5.1 (CTR-AES128.Encrypt) and F.5.2 (Decrypt).
    a = AES(KEY)
    blocks = [counter_block(T1, j, 128).hex() for j in range(4)]
    assert blocks == [
        "f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff",
        "f0f1f2f3f4f5f6f7f8f9fafbfcfdff00",
        "f0f1f2f3f4f5f6f7f8f9fafbfcfdff01",
        "f0f1f2f3f4f5f6f7f8f9fafbfcfdff02",
    ]
    assert keystream_block(a, T1, 0).hex() == "ec8cdf7398607cb0f2d21675ea9ea1e4"
    assert keystream_block(a, T1, 3).hex() == "e89c399ff0f198c6d40a31db156cabfe"
    assert ctr_crypt(a, T1, PT) == CT
    assert ctr_crypt(a, T1, CT) == PT


def test_round_trip_and_partial_block() -> None:
    rng = random.Random(5)
    a = AES(bytes(rng.randrange(256) for _ in range(16)))
    for n in (0, 1, 15, 16, 17, 50):
        t1 = bytes(rng.randrange(256) for _ in range(12)) + bytes(4)
        p = bytes(rng.randrange(256) for _ in range(n))
        c = ctr_crypt(a, t1, p, m_bits=32)
        assert len(c) == n
        assert ctr_crypt(a, t1, c, m_bits=32) == p
    # A partial last block is a prefix of the full-block result.
    assert ctr_crypt(a, T1, PT[:37]) == ctr_crypt(a, T1, PT)[:37]


def test_random_access_equals_sequential() -> None:
    # Block j can be decrypted alone from T[1] and j: CTR runs in parallel.
    a = AES(KEY)
    for j in range(4):
        alone = xor(CT[16 * j : 16 * j + 16], keystream_block(a, T1, j))
        assert alone == PT[16 * j : 16 * j + 16]


def test_nonce_reuse_gives_xor_of_plaintexts() -> None:
    a = AES(KEY)
    p1 = b"attack the north gate at dawn, then hold"
    p2 = b"retreat to the river before noon, all of"
    c1, c2 = ctr_crypt(a, T1, p1), ctr_crypt(a, T1, p2)
    assert xor(c1, c2) == xor(p1, p2)
    assert xor(xor(c1, c2), p1) == p2
    # Overlap: the second message starts one counter later than the first.
    t2 = counter_block(T1, 1, 128)
    c3 = ctr_crypt(a, t2, p2)
    assert xor(c3[:16], c1[16:32]) == xor(p2[:16], p1[16:32])


def test_counter_field_wrap_is_refused() -> None:
    a = AES(KEY)
    t1 = bytes(12) + bytes.fromhex("fffffffe")
    assert len(ctr_crypt(a, t1, bytes(32), m_bits=32)) == 32
    with pytest.raises(OverflowError):
        ctr_crypt(a, t1, bytes(33), m_bits=32)
    with pytest.raises(ValueError):
        ctr_crypt(a, bytes(8), b"x")
