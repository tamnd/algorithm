# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sm4/. The authors are listed in prov/9DN8TB.jsonl.

import random

from sm4 import CK, SBOX, decrypt_block, encrypt_block, round_keys


# draft-ribose-cfrg-sm4-10, Section 6.2.3: S(EF) = 84.
def test_sbox_example() -> None:
    assert SBOX[0xEF] == 0x84
    assert sorted(SBOX) == list(range(256))


# draft-ribose-cfrg-sm4-10, Section 7.3.2, the table of CK_i.
def test_ck_table() -> None:
    assert CK[0] == 0x00070E15
    assert CK[9] == 0xFC030A11
    assert CK[31] == 0x646B7279


# draft-ribose-cfrg-sm4-10, Appendix A.1.1 (GB/T 32907-2016 Example 1).
def test_example_1() -> None:
    key = bytes.fromhex("0123456789abcdeffedcba9876543210")
    pt = bytes.fromhex("0123456789abcdeffedcba9876543210")
    ct = bytes.fromhex("681edf34d206965e86b3e94f536e4246")
    rk = round_keys(key)
    assert rk[0] == 0xF12186F9
    assert rk[1] == 0x41662B61
    assert rk[31] == 0x9124A012
    assert encrypt_block(key, pt) == ct
    # Appendix A.1.2: decryption of Example 1.
    assert decrypt_block(key, ct) == pt


# draft-ribose-cfrg-sm4-10, Appendix A.1.4 (Example 4) and A.1.5 (its decryption).
def test_example_4() -> None:
    key = bytes.fromhex("fedcba98765432100123456789abcdef")
    pt = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    ct = bytes.fromhex("f766678f13f01adeac1b3ea955adb594")
    assert round_keys(key)[31] == 0x711138B7
    assert encrypt_block(key, pt) == ct
    assert decrypt_block(key, ct) == pt


def test_round_trip_random() -> None:
    rng = random.Random(6)
    for _ in range(20):
        key, m = rng.randbytes(16), rng.randbytes(16)
        assert decrypt_block(key, encrypt_block(key, m)) == m
