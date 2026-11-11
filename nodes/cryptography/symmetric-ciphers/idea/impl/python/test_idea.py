# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/idea/. The authors are listed in prov/M2H1VD.jsonl.

import random

from idea import (
    crypt_words,
    decrypt_block,
    decryption_subkeys,
    encrypt_block,
    encryption_subkeys,
    mul,
    mul_inv,
)

# Menezes, van Oorschot and Vanstone, Handbook of Applied Cryptography (1996),
# Example 7.106 and Table 7.12: key (1, 2, ..., 8), M = (0, 1, 2, 3).
KEY = bytes.fromhex("00010002000300040005000600070008")


def test_hac_table_7_12_ciphertext() -> None:
    pt = bytes.fromhex("0000000100020003")
    ct = bytes.fromhex("11fbed2b01986de5")
    assert encrypt_block(KEY, pt) == ct
    assert decrypt_block(KEY, ct) == pt


def test_hac_table_7_12_subkeys() -> None:
    ek = encryption_subkeys(KEY)
    assert ek[0:6] == [0x0001, 0x0002, 0x0003, 0x0004, 0x0005, 0x0006]
    assert ek[6:12] == [0x0007, 0x0008, 0x0400, 0x0600, 0x0800, 0x0A00]
    assert ek[48:52] == [0x0080, 0x00C0, 0x0100, 0x0140]


def test_hac_table_7_12_round_one() -> None:
    ek = encryption_subkeys(KEY)
    # One round with the output transformation turned into the identity
    # (multiply by 1, add 0, and undo the final swap of the middle words).
    sk = ek[:6] + [0] * 42 + [1, 0, 0, 1]
    x1, x3, x2, x4 = crypt_words([0, 1, 2, 3], sk, rounds=1)
    assert [x1, x2, x3, x4] == [0x00F0, 0x00F5, 0x010A, 0x0105]


def test_hac_table_7_13_first_decryption_round() -> None:
    dk = decryption_subkeys(encryption_subkeys(KEY))
    assert dk[0:6] == [0xFE01, 0xFF40, 0xFF00, 0x659A, 0xC000, 0xE001]


def test_multiplication_group() -> None:
    assert mul(0, 0) == 1  # (-1) * (-1) = 1 modulo 2^16 + 1
    assert mul(0, 1) == 0
    for a in (0, 1, 2, 0x8000, 0xFFFF):
        assert mul(a, mul_inv(a)) == 1


def test_round_trip_random() -> None:
    rng = random.Random(11)
    for _ in range(20):
        key, m = rng.randbytes(16), rng.randbytes(8)
        assert decrypt_block(key, encrypt_block(key, m)) == m
