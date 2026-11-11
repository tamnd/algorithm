# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cfb-mode/. The authors are listed in prov/MXBPBC.jsonl.

import random

import pytest

from aes import AES
from cfb_mode import cfb_decrypt, cfb_encrypt

KEY = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
IV = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
PT = bytes.fromhex(
    "6bc1bee22e409f96e93d7e117393172a"
    "ae2d8a571e03ac9c9eb76fac45af8e51"
    "30c81c46a35ce411e5fbc1191a0a52ef"
    "f69f2445df4f9b17ad2b417be66c3710"
)


def test_aes_fips197_appendix_c() -> None:
    # FIPS 197, Appendix C.1 (AES-128).
    a = AES(bytes.fromhex("000102030405060708090a0b0c0d0e0f"))
    assert a.encrypt_block(bytes.fromhex("00112233445566778899aabbccddeeff")).hex() == "69c4e0d86a7b0430d8cdb78070b4c55a"


def test_sp800_38a_f313_cfb128_aes128() -> None:
    # SP 800-38A, Appendix F.3.13 (CFB128-AES128.Encrypt) and F.3.14 (Decrypt).
    ct = bytes.fromhex(
        "3b3fd92eb72dad20333449f8e83cfb4a"
        "c8a64537a0b3a93fcde3cdad9f1ce58b"
        "26751f67a3cbb140b1808cf187a4f4df"
        "c04b05357c5d1c0eeac4c66f9ff7f2e6"
    )
    a = AES(KEY)
    assert cfb_encrypt(a, IV, PT) == ct
    assert cfb_decrypt(a, IV, ct) == PT


def test_sp800_38a_f37_cfb8_aes128() -> None:
    # SP 800-38A, Appendix F.3.7 (CFB8-AES128.Encrypt): 18 segments of one byte.
    p = bytes.fromhex("6bc1bee22e409f96e93d7e117393172aae2d")
    c = bytes.fromhex("3b79424c9c0dd436bace9e0ed4586a4f32b9")
    a = AES(KEY)
    assert cfb_encrypt(a, IV, p, s_bytes=1) == c
    assert cfb_decrypt(a, IV, c, s_bytes=1) == p


def test_round_trip_all_segment_sizes() -> None:
    rng = random.Random(9)
    a = AES(bytes(rng.randrange(256) for _ in range(16)))
    iv = bytes(rng.randrange(256) for _ in range(16))
    for s in (1, 2, 4, 8, 16):
        p = bytes(rng.randrange(256) for _ in range(3 * 16))
        assert cfb_decrypt(a, iv, cfb_encrypt(a, iv, p, s), s) == p
    with pytest.raises(ValueError):
        cfb_encrypt(a, iv, b"abc", 2)


def test_error_propagation_cfb128() -> None:
    # A flip in C[2] flips the same bit of P[2] and garbles P[3]; P[4] is intact.
    a = AES(KEY)
    c = bytearray(cfb_encrypt(a, IV, PT))
    c[16] ^= 0x01
    p = cfb_decrypt(a, IV, bytes(c))
    assert p[:16] == PT[:16]
    assert p[16] == PT[16] ^ 0x01 and p[17:32] == PT[17:32]
    assert p[32:48] != PT[32:48]
    assert p[48:] == PT[48:]


def test_self_synchronizing_cfb8() -> None:
    # Delete one ciphertext byte: after 16 garbled bytes, CFB-8 decrypts the rest correctly.
    rng = random.Random(4)
    a = AES(KEY)
    p = bytes(rng.randrange(256) for _ in range(80))
    c = cfb_encrypt(a, IV, p, 1)
    lost = c[:30] + c[31:]
    q = cfb_decrypt(a, IV, lost, 1)
    assert q[:30] == p[:30]
    assert q[30 + 16 :] == p[31 + 16 :]
    assert q[30:46] != p[31:47]
