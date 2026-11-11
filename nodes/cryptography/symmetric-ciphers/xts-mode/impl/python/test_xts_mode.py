# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xts-mode/. The authors are listed in prov/9A46ZH.jsonl.

import random

import pytest

from aes import AES
from xts_mode import mul_alpha, tweak_from_data_unit, xts_decrypt, xts_encrypt

# IEEE Std 1619-2007, Annex B (XTS-AES test vectors), Vectors 1, 2, 3 and 15.
# Copied from the copies in the Linux kernel, crypto/testmgr.h (aes_xts_tv_template,
# "XTS-AES 1" to "XTS-AES 3") and libtomcrypt, src/modes/xts/xts_test.c (the 17-byte
# vector); the IEEE document itself was not open to us.
IEEE_VECTORS = [
    # (Key1, Key2, data unit sequence number, PTX, CTX)
    ("00" * 16, "00" * 16, 0, "00" * 32,
     "917cf69ebd68b2ec9b9fe9a3eadda692cd43d2f59598ed858c02c2652fbf922e"),
    ("11" * 16, "22" * 16, 0x3333333333, "44" * 32,
     "c454185e6a16936e39334038acef838bfb186fff7480adc4289382ecd6d394f0"),
    ("fffefdfcfbfaf9f8f7f6f5f4f3f2f1f0", "22" * 16, 0x3333333333, "44" * 32,
     "af85336b597afc1a900b2eb21ec949d292df4c047e0b21532186a5971a227a89"),
    ("fffefdfcfbfaf9f8f7f6f5f4f3f2f1f0", "bfbebdbcbbbab9b8b7b6b5b4b3b2b1b0", 0x123456789A,
     "000102030405060708090a0b0c0d0e0f10", "6c1625db4671522d3d7599601de7ca09ed"),
]


def test_aes_fips197_appendix_c() -> None:
    # FIPS 197, Appendix C.1 (AES-128).
    a = AES(bytes.fromhex("000102030405060708090a0b0c0d0e0f"))
    assert a.encrypt_block(bytes.fromhex("00112233445566778899aabbccddeeff")).hex() == "69c4e0d86a7b0430d8cdb78070b4c55a"


@pytest.mark.parametrize("k1, k2, dun, ptx, ctx", IEEE_VECTORS)
def test_ieee_1619_annex_b(k1: str, k2: str, dun: int, ptx: str, ctx: str) -> None:
    key = bytes.fromhex(k1 + k2)
    i = tweak_from_data_unit(dun)
    p, c = bytes.fromhex(ptx), bytes.fromhex(ctx)
    assert xts_encrypt(key, i, p, allow_equal_keys=True) == c
    assert xts_decrypt(key, i, c, allow_equal_keys=True) == p


def test_mul_alpha() -> None:
    one = bytes([1]) + bytes(15)
    assert mul_alpha(one) == bytes([2]) + bytes(15)
    top = bytes(15) + bytes([0x80])  # x^127
    assert mul_alpha(top) == bytes([0x87]) + bytes(15)  # x^128 = x^7 + x^2 + x + 1


def test_round_trip_with_stealing_and_bad_inputs() -> None:
    rng = random.Random(1619)
    key = bytes(rng.randrange(256) for _ in range(32))
    i = tweak_from_data_unit(77)
    for n in (16, 17, 31, 32, 33, 47, 100):
        p = bytes(rng.randrange(256) for _ in range(n))
        c = xts_encrypt(key, i, p)
        assert len(c) == n
        assert xts_decrypt(key, i, c) == p
    with pytest.raises(ValueError):
        xts_encrypt(key, i, bytes(15))
    with pytest.raises(ValueError):
        xts_encrypt(bytes(32), i, bytes(16))  # Key1 = Key2 is refused by default


def test_deterministic_per_position_and_no_authentication() -> None:
    key = bytes(range(32))
    i = tweak_from_data_unit(5)
    p = b"A" * 64
    c = xts_encrypt(key, i, p)
    # Equal blocks at different positions encrypt differently (the tweak) ...
    assert len({c[16 * j : 16 * j + 16] for j in range(4)}) == 4
    # ... but the same data at the same position and sector gives the same ciphertext.
    assert xts_encrypt(key, i, p) == c
    # A changed ciphertext bit is not detected: it garbles one 16-byte block only.
    bad = bytearray(c)
    bad[20] ^= 1
    q = xts_decrypt(key, i, bytes(bad))
    assert q[:16] == p[:16] and q[32:] == p[32:] and q[16:32] != p[16:32]


def test_block_replay_restores_old_plaintext() -> None:
    # Narrow-block malleability: an old ciphertext block put back at its place decrypts.
    key = bytes(range(1, 33))
    i = tweak_from_data_unit(9)
    old = b"balance: 0000100" + b"owner: alice    " + b"limit: 00000500 "
    new = b"balance: 0000003" + b"owner: alice    " + b"limit: 00000500 "
    c_old, c_new = xts_encrypt(key, i, old), xts_encrypt(key, i, new)
    spliced = c_old[:16] + c_new[16:]
    assert xts_decrypt(key, i, spliced) == old
