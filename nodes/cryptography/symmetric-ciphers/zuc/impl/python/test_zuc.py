# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zuc/. The authors are listed in prov/MQAR4N.jsonl.

import random

from zuc import D, S0, S1, P, bit_reorganization, lfsr_clock, nonlinear_f, sbox, zuc_keystream

# ETSI/SAGE, Specification of the 3GPP Confidentiality and Integrity Algorithms
# 128-EEA3 & 128-EIA3, Document 3: Implementor's Test Data, Version 1.1, Sections 3.3 to 3.6.
VECTORS = [
    ("00" * 16, "00" * 16, [0x27BEDE74, 0x018082DA]),
    ("ff" * 16, "ff" * 16, [0x0657CFA0, 0x7096398B]),
    ("3d4c4be96a82fdaeb58f641db17b455b", "84319aa8de6915ca1f6bda6bfbd8c766", [0x14F1C272, 0x3279C419]),
]


def test_test_sets_1_to_3() -> None:
    for key, iv, z in VECTORS:
        assert zuc_keystream(bytes.fromhex(key), bytes.fromhex(iv), 2) == z


def test_test_set_4() -> None:
    z = zuc_keystream(bytes.fromhex("4d320bfad4c285bfd6b8bd00f39d8b41"), bytes.fromhex("52959daba0bf176ece2dc315049eb574"), 2000)
    assert z[0] == 0xED4400E7 and z[1] == 0x0633E5C5 and z[1999] == 0x7A574CDB


def test_first_initialization_steps_of_test_set_1() -> None:
    # Section 3.3: X0, X1, X2, X3, R1, R2, W and the new s15 for t = 0, 1.
    expected = [
        (0x008F9A00, 0xF100005E, 0xAF00006B, 0x6B000089, 0x67822141, 0x62A3A55F, 0x008F9A00, 0x4563CB1B),
        (0x8AC7AC00, 0x260000D7, 0x780000E2, 0x5E00004D, 0x474A2E7E, 0x119E94BB, 0x4FE932A0, 0x28652A0F),
    ]
    s = [D[i] << 8 for i in range(16)]
    r = [0, 0]
    for row in expected:
        x = bit_reorganization(s)
        w = nonlinear_f(x[0], x[1], x[2], r)
        lfsr_clock(s, w >> 1)
        assert (*x, r[0], r[1], w, s[15]) == row


def test_spec_examples_and_sbox_permutations() -> None:
    assert sbox(0x12345678) == 0xF9C05A4E  # Example 8
    assert sorted(S0) == list(range(256)) and sorted(S1) == list(range(256))
    assert D[0] == 0x44D7 and D[15] == 0x47AC


def test_lfsr_cells_stay_nonzero() -> None:
    rng = random.Random(6)
    s = [rng.randrange(1, P + 1) for _ in range(16)]
    for _ in range(200):
        lfsr_clock(s, rng.randrange(1 << 31) if rng.random() < 0.5 else 0)
        assert 1 <= s[15] <= P
