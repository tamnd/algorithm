# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ecb-mode/. The authors are listed in prov/3HG8V8.jsonl.

import random

import pytest

from aes import AES
from ecb_mode import ecb_decrypt, ecb_encrypt

# NIST SP 800-38A, Appendix F: the four plaintext blocks shared by all examples.
PT = bytes.fromhex(
    "6bc1bee22e409f96e93d7e117393172a"
    "ae2d8a571e03ac9c9eb76fac45af8e51"
    "30c81c46a35ce411e5fbc1191a0a52ef"
    "f69f2445df4f9b17ad2b417be66c3710"
)


def test_aes_fips197_appendix_c() -> None:
    # FIPS 197, Appendix C.1 (AES-128) and C.3 (AES-256).
    pt = bytes.fromhex("00112233445566778899aabbccddeeff")
    a = AES(bytes.fromhex("000102030405060708090a0b0c0d0e0f"))
    assert a.encrypt_block(pt).hex() == "69c4e0d86a7b0430d8cdb78070b4c55a"
    assert a.decrypt_block(bytes.fromhex("69c4e0d86a7b0430d8cdb78070b4c55a")) == pt
    a = AES(bytes(range(32)))
    assert a.encrypt_block(pt).hex() == "8ea2b7ca516745bfeafc49904b496089"


def test_sp800_38a_f11_f12_ecb_aes128() -> None:
    # SP 800-38A, Appendix F.1.1 (ECB-AES128.Encrypt) and F.1.2 (Decrypt).
    a = AES(bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c"))
    ct = bytes.fromhex(
        "3ad77bb40d7a3660a89ecaf32466ef97"
        "f5d3d58503b9699de785895a96fdbaaf"
        "43b1cd7f598ece23881b00e3ed030688"
        "7b0c785e27e8ad3f8223207104725dd4"
    )
    assert ecb_encrypt(a, PT) == ct
    assert ecb_decrypt(a, ct) == PT


def test_sp800_38a_f15_ecb_aes256() -> None:
    # SP 800-38A, Appendix F.1.5 (ECB-AES256.Encrypt).
    a = AES(bytes.fromhex("603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4"))
    ct = bytes.fromhex(
        "f3eed1bdb5d2a03c064b5a7e3db181f8"
        "591ccb10d410ed26dc5ba74a31362870"
        "b6ed21b99ca6f4f9f153e7b1beafed1d"
        "23304b7a39f9f3ff067d8d8f9e24ecc7"
    )
    assert ecb_encrypt(a, PT) == ct


def test_round_trip_and_lengths() -> None:
    rng = random.Random(7)
    a = AES(bytes(rng.randrange(256) for _ in range(16)))
    assert ecb_encrypt(a, b"") == b""
    for m in range(6):
        p = bytes(rng.randrange(256) for _ in range(16 * m))
        assert ecb_decrypt(a, ecb_encrypt(a, p)) == p
    with pytest.raises(ValueError):
        ecb_encrypt(a, b"x" * 17)


def test_equal_blocks_leak() -> None:
    # The bitmap of the page: each pixel is one block, white = 00..00, black = ff..ff.
    a = AES(bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c"))
    pic = [".........", ".##...##.", "..##.##..", "...###...", "..##.##..", ".##...##.", "........."]
    for row in pic:
        ct = ecb_encrypt(a, b"".join((b"\x00" if c == "." else b"\xff") * 16 for c in row))
        heads = ["%02x" % ct[16 * i] for i in range(len(row))]
        assert heads == ["7d" if c == "." else "8a" for c in row]


def test_ind_cpa_adversary_wins_always() -> None:
    # The adversary of the page: M0 = 0^n 0^n, M1 = 0^n 1^n; guess 0 when the two blocks are equal.
    rng = random.Random(1)
    wins = 0
    for _ in range(40):
        a = AES(bytes(rng.randrange(256) for _ in range(16)))
        b = rng.randrange(2)
        m = [bytes(32), bytes(16) + b"\xff" * 16][b]
        c = ecb_encrypt(a, m)
        guess = 0 if c[:16] == c[16:] else 1
        wins += guess == b
    assert wins == 40


def test_error_stays_in_one_block() -> None:
    rng = random.Random(3)
    a = AES(bytes(16))
    p = bytes(rng.randrange(256) for _ in range(64))
    c = bytearray(ecb_encrypt(a, p))
    c[20] ^= 1
    q = ecb_decrypt(a, bytes(c))
    assert q[:16] == p[:16] and q[32:] == p[32:] and q[16:32] != p[16:32]
