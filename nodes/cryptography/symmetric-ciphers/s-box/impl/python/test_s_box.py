# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/s-box/. The authors are listed in prov/FXRB76.jsonl.

import random

from s_box import (
    HEYS_SBOX,
    aes_sbox,
    ddt,
    differential_uniformity,
    gf_inv,
    gf_mul,
    lat,
    nonlinearity,
    sac_matrix,
)

# FIPS 197 (2023 update), Table 4, SBOX(): substitution values for the byte xy. Copied by hand, row x = 0 to f.
FIPS197_TABLE4 = """
63 7c 77 7b f2 6b 6f c5 30 01 67 2b fe d7 ab 76
ca 82 c9 7d fa 59 47 f0 ad d4 a2 af 9c a4 72 c0
b7 fd 93 26 36 3f f7 cc 34 a5 e5 f1 71 d8 31 15
04 c7 23 c3 18 96 05 9a 07 12 80 e2 eb 27 b2 75
09 83 2c 1a 1b 6e 5a a0 52 3b d6 b3 29 e3 2f 84
53 d1 00 ed 20 fc b1 5b 6a cb be 39 4a 4c 58 cf
d0 ef aa fb 43 4d 33 85 45 f9 02 7f 50 3c 9f a8
51 a3 40 8f 92 9d 38 f5 bc b6 da 21 10 ff f3 d2
cd 0c 13 ec 5f 97 44 17 c4 a7 7e 3d 64 5d 19 73
60 81 4f dc 22 2a 90 88 46 ee b8 14 de 5e 0b db
e0 32 3a 0a 49 06 24 5c c2 d3 ac 62 91 95 e4 79
e7 c8 37 6d 8d d5 4e a9 6c 56 f4 ea 65 7a ae 08
ba 78 25 2e 1c a6 b4 c6 e8 dd 74 1f 4b bd 8b 8a
70 3e b5 66 48 03 f6 0e 61 35 57 b9 86 c1 1d 9e
e1 f8 98 11 69 d9 8e 94 9b 1e 87 e9 ce 55 28 df
8c a1 89 0d bf e6 42 68 41 99 2d 0f b0 54 bb 16
"""


def test_aes_sbox_matches_fips197_table4() -> None:
    table = [int(v, 16) for v in FIPS197_TABLE4.split()]
    assert len(table) == 256
    assert aes_sbox() == table


def test_gf_inverse() -> None:
    for a in range(1, 256):
        assert gf_mul(a, gf_inv(a)) == 1
    assert gf_inv(0) == 0
    # FIPS 197 Section 4.2: {57} . {83} = {c1}.
    assert gf_mul(0x57, 0x83) == 0xC1


def test_aes_differential_uniformity_is_4() -> None:
    s = aes_sbox()
    d = ddt(s)
    assert differential_uniformity(s) == 4
    for a in range(1, 256):
        row = d[a]
        assert row.count(4) == 1 and row.count(2) == 126 and row.count(0) == 129


def test_aes_nonlinearity_is_112() -> None:
    s = aes_sbox()
    assert nonlinearity(s) == 112
    big = max(abs(v) for row in lat(s)[1:] for v in row[1:])
    assert big == 16


def test_heys_tables() -> None:
    d = ddt(HEYS_SBOX)
    # Heys (2002), the difference distribution table: the entries used in the differential characteristic.
    assert d[0xB][0x2] == 8 and d[0x4][0x6] == 6 and d[0x2][0x5] == 6
    assert differential_uniformity(HEYS_SBOX) == 8
    t = lat(HEYS_SBOX)
    # Heys (2002), the linear approximation table: X1 + X3 + X4 = Y2 has bias +1/4, X2 = Y2 + Y4 has bias -1/4.
    assert t[0xB][0x4] == 4 and t[0x4][0x5] == -4
    assert nonlinearity(HEYS_SBOX) == 2


def test_ddt_rows_sum() -> None:
    rng = random.Random(8)
    for _ in range(20):
        s = list(range(16))
        rng.shuffle(s)
        d = ddt(s)
        assert d[0][0] == 16
        assert all(sum(row) == 16 and row[0] == 0 for row in d[1:])
        assert all(v % 2 == 0 for row in d for v in row)
        # The LAT and the nonlinearity agree.
        t = lat(s)
        assert nonlinearity(s) == 8 - max(abs(v) for row in t for v in row[1:])


def test_identity_is_linear() -> None:
    s = list(range(16))
    assert nonlinearity(s) == 0
    assert differential_uniformity(s) == 16


def test_sac_near_half() -> None:
    m = sac_matrix(aes_sbox(), 8)
    assert all(0.45 <= v <= 0.57 for row in m for v in row)
