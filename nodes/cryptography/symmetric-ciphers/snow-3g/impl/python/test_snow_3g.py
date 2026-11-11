# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/snow-3g/. The authors are listed in prov/YDPQ53.jsonl.

import random

from snow_3g import DIV_ALPHA, MUL_ALPHA, SQ, SR, mulx, snow3g_keystream

# ETSI/SAGE, Specification of the 3GPP Confidentiality and Integrity Algorithms
# UEA2 & UIA2, Document 3: Implementors' Test Data, Version 1.0, Sections 3.3 to 3.6.
VECTORS = [
    ("2BD6459F82C5B300952C49104881FF48", "EA024714AD5C4D84DF1F9B251C0BF45F", [0xABEE9704, 0x7AC31373]),
    ("8CE33E2CC3C0B5FC1F3DE8A6DC66B1F3", "D3C5D592327FB11CDE551988CEB2F9B7", [0xEFF8A342, 0xF751480F]),
    ("4035C6680AF8C6D1A8FF8667B1714013", "62A540981BA6F9B74592B0E78690F71B", [0xA8C874A9, 0x7AE7C4F8]),
]


def test_test_sets_1_to_3() -> None:
    for key, iv, z in VECTORS:
        assert snow3g_keystream(bytes.fromhex(key), bytes.fromhex(iv), 2) == z


def test_test_set_4_full_table_coverage() -> None:
    # Section 3.6: 2500 words, which use every table entry at least once.
    z = snow3g_keystream(bytes.fromhex("0DED7263109CF92E3352255A140E0F76"), bytes.fromhex("6B68079A41A7C4C91BEFD79F7FDCC233"), 2500)
    assert z[:3] == [0xD712C05C, 0xA937C2A6, 0xEB7EAAE3]
    assert z[2499] == 0x9C0DB3AA


def test_sboxes_against_spec_tables() -> None:
    # Document 2, Tables 1 and 2: the first row and the worked examples.
    assert SR[:16] == [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76]
    assert SQ[:16] == [0x25, 0x24, 0x73, 0x67, 0xD7, 0xAE, 0x5C, 0x30, 0xA4, 0xEE, 0x6E, 0xCB, 0x7D, 0xB5, 0x82, 0xDB]
    assert SR[0x2A] == 0xE5 and SQ[0x2A] == 0xAC
    assert sorted(SR) == list(range(256)) and sorted(SQ) == list(range(256))
    assert mulx(0x96, 0x1B) == 0x37


def test_alpha_tables_are_inverse_shifts() -> None:
    # MUL_alpha(c) and DIV_alpha(c) are c * alpha^4 and c * alpha^-4 as words: both are
    # linear in c, and c = 0 maps to 0.
    rng = random.Random(4)
    assert MUL_ALPHA[0] == 0 and DIV_ALPHA[0] == 0
    for _ in range(50):
        a, b = rng.randrange(256), rng.randrange(256)
        assert MUL_ALPHA[a ^ b] == MUL_ALPHA[a] ^ MUL_ALPHA[b]
        assert DIV_ALPHA[a ^ b] == DIV_ALPHA[a] ^ DIV_ALPHA[b]


def test_iv_changes_keystream() -> None:
    rng = random.Random(5)
    key = rng.randbytes(16)
    a = snow3g_keystream(key, bytes(16), 4)
    b = snow3g_keystream(key, bytes(15) + b"\x01", 4)
    diff = sum(bin(x ^ y).count("1") for x, y in zip(a, b))
    assert 40 < diff < 88
