# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rc5/. The authors are listed in prov/NB7K96.jsonl.

import random

import pytest

from rc5 import decrypt_block, encrypt_block

# RFC 2040 Section 9.2 (inputs) and Section 9.3 (results), RC5-32/R/b in
# CBC mode without padding. Each case is one block, so C = E(IV xor P).
RFC2040_CBC = [
    (0, "00", "0000000000000000", "0000000000000000", "7a7bba4d79111d1e"),
    (0, "00", "0000000000000000", "ffffffffffffffff", "797bba4d78111d1e"),
    (0, "00", "0102030405060708", "1020304050607080", "8b9ded91ce7794a6"),
    (1, "11", "0000000000000000", "0000000000000000", "2f759fe7ad86a378"),
    (2, "00", "0000000000000000", "0000000000000000", "dca2694bf40e0788"),
    (2, "00000000", "0000000000000000", "0000000000000000", "dca2694bf40e0788"),
    (8, "00", "0000000000000000", "0000000000000000", "dcfe098577eca5ff"),
    (8, "00", "0102030405060708", "1020304050607080", "9646fb77638f9ca8"),
    (12, "00", "0102030405060708", "1020304050607080", "b2b3209db6594da4"),
    (16, "00", "0102030405060708", "1020304050607080", "545f7f32a5fc3836"),
    (8, "01020304", "0000000000000000", "ffffffffffffffff", "8285e7c1b5bc7402"),
    (12, "01020304", "0000000000000000", "ffffffffffffffff", "fc586f92f7080934"),
    (16, "01020304", "0000000000000000", "ffffffffffffffff", "cf270ef9717ff7c4"),
    (12, "0102030405060708", "0000000000000000", "ffffffffffffffff", "e493f1c1bb4d6e8c"),
    (8, "0102030405060708", "0102030405060708", "1020304050607080", "5c4c041e0f217ac3"),
    (12, "0102030405060708", "0102030405060708", "1020304050607080", "921f12485373b4f7"),
    (16, "0102030405060708", "0102030405060708", "1020304050607080", "5ba0ca6bbe7f5fad"),
    (8, "01020304050607081020304050607080", "0102030405060708", "1020304050607080", "c533771cd0110e63"),
    (12, "01020304050607081020304050607080", "0102030405060708", "1020304050607080", "294ddb46b3278d60"),
    (16, "01020304050607081020304050607080", "0102030405060708", "1020304050607080", "dad6bda9dfe8f7e8"),
    (12, "0102030405", "0000000000000000", "ffffffffffffffff", "97e0787837ed317f"),
    (8, "0102030405", "0000000000000000", "ffffffffffffffff", "7875dbf6738c6478"),
    (8, "0102030405", "7875dbf6738c6478", "0808080808080808", "8f34c3c681c99695"),
    (8, "0102030405", "0000000000000000", "0000000000000000", "7cb3f1df34f94811"),
    (8, "0102030405", "7cb3f1df34f94811", "1122334455667701", "7fd1a023a5bba217"),
]


@pytest.mark.parametrize("rounds,key,iv,pt,ct", RFC2040_CBC)
def test_rfc2040_section_9(rounds: int, key: str, iv: str, pt: str, ct: str) -> None:
    k = bytes.fromhex(key)
    x = bytes(a ^ b for a, b in zip(bytes.fromhex(iv), bytes.fromhex(pt)))
    assert encrypt_block(k, x, rounds).hex() == ct
    assert decrypt_block(k, bytes.fromhex(ct), rounds) == x


# Menezes, van Oorschot and Vanstone, Handbook of Applied Cryptography (1996),
# Example 7.118, RC5-32/12/16. The hex strings are byte strings.
def test_hac_example_7_118() -> None:
    key = bytes.fromhex("5269F149D41BA0152497574D7F153125")
    pt = bytes.fromhex("65C178B284D197CC")
    ct = bytes.fromhex("EB44E415DA319824")
    assert encrypt_block(key, pt, 12) == ct
    assert decrypt_block(key, ct, 12) == pt


def test_round_trip_word_sizes() -> None:
    rng = random.Random(8)
    for w in (16, 32, 64):
        for _ in range(5):
            key = rng.randbytes(rng.randrange(0, 33))
            m = rng.randbytes(w // 4)
            assert decrypt_block(key, encrypt_block(key, m, 12, w), 12, w) == m


def test_zero_rounds_is_key_addition() -> None:
    # With r = 0 the cipher only adds S[0] and S[1]; a one-bit change of the
    # input then changes one output word only.
    key = b"\x00"
    c0 = encrypt_block(key, bytes(8), 0)
    c1 = encrypt_block(key, bytes(7) + b"\x01", 0)
    assert c0[:4] == c1[:4]
