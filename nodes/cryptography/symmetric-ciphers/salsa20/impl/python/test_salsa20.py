# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/salsa20/. The authors are listed in prov/12PMYB.jsonl.

import random

from salsa20 import (
    doubleround,
    quarterround,
    rotl32,
    rowround,
    salsa20_encrypt,
    salsa20_expand,
    salsa20_hash,
)

# All expected values below are copied by hand from D. J. Bernstein,
# "Salsa20 specification", 2005 (cr.yp.to/snuffle/spec.pdf), with the section.


def test_rotl_section_2() -> None:
    assert rotl32(0xC0A8787E, 5) == 0x150F0FD8


def test_quarterround_section_3() -> None:
    cases = [
        ((1, 0, 0, 0), (0x08008145, 0x00000080, 0x00010200, 0x20500000)),
        ((0, 1, 0, 0), (0x88000100, 0x00000001, 0x00000200, 0x00402000)),
        ((0, 0, 1, 0), (0x80040000, 0x00000000, 0x00000001, 0x00002000)),
        ((0, 0, 0, 1), (0x00048044, 0x00000080, 0x00010000, 0x20100001)),
        ((0xE7E8C006, 0xC4F9417D, 0x6479B4B2, 0x68C67137), (0xE876D72B, 0x9361DFD5, 0xF1460244, 0x948541A3)),
        ((0xD3917C5B, 0x55F1C407, 0x52A58A7A, 0x8F887A3B), (0x3E2F308C, 0xD90A8F36, 0x6AB2A923, 0x2883524C)),
    ]
    for y, z in cases:
        assert quarterround(*y) == z


def test_rowround_section_4() -> None:
    y = [1, 0, 0, 0] * 4
    assert rowround(y) == [
        0x08008145, 0x00000080, 0x00010200, 0x20500000,
        0x20100001, 0x00048044, 0x00000080, 0x00010000,
        0x00000001, 0x00002000, 0x80040000, 0x00000000,
        0x00000001, 0x00000200, 0x00402000, 0x88000100,
    ]


def test_doubleround_section_6() -> None:
    x = [1] + [0] * 15
    assert doubleround(x) == [
        0x8186A22D, 0x0040A284, 0x82479210, 0x06929051,
        0x08000090, 0x02402200, 0x00004000, 0x00800000,
        0x00010200, 0x20400000, 0x08008104, 0x00000000,
        0x20500000, 0xA0000040, 0x0008180A, 0x612A8020,
    ]
    x = [
        0xDE501066, 0x6F9EB8F7, 0xE4FBBD9B, 0x454E3F57,
        0xB75540D3, 0x43E93A4C, 0x3A6F2AA0, 0x726D6B36,
        0x9243F484, 0x9145D1E8, 0x4FA9D247, 0xDC8DEE11,
        0x054BF545, 0x254DD653, 0xD9421B6D, 0x67B276C1,
    ]
    assert doubleround(x) == [
        0xCCAAF672, 0x23D960F7, 0x9153E63A, 0xCD9A60D0,
        0x50440492, 0xF07CAD19, 0xAE344AA0, 0xDF4CFDFC,
        0xCA531C29, 0x8E7943DB, 0xAC1680CD, 0xD503CA00,
        0xA74B2AD6, 0xBC331C5C, 0x1DDA24C7, 0xEE928277,
    ]


def test_hash_section_8() -> None:
    assert salsa20_hash(bytes(64)) == bytes(64)
    inp = bytes([
        211, 159, 13, 115, 76, 55, 82, 183, 3, 117, 222, 37, 191, 187, 234, 136,
        49, 237, 179, 48, 1, 106, 178, 219, 175, 199, 166, 48, 86, 16, 179, 207,
        31, 240, 32, 63, 15, 83, 93, 161, 116, 147, 48, 113, 238, 55, 204, 36,
        79, 201, 235, 79, 3, 81, 156, 47, 203, 26, 244, 243, 88, 118, 104, 54,
    ])
    out = bytes([
        109, 42, 178, 168, 156, 240, 248, 238, 168, 196, 190, 203, 26, 110, 170, 154,
        29, 29, 150, 26, 150, 30, 235, 249, 190, 163, 251, 48, 69, 144, 51, 57,
        118, 40, 152, 157, 180, 57, 27, 94, 107, 42, 236, 35, 27, 111, 114, 114,
        219, 236, 232, 135, 111, 155, 110, 18, 24, 232, 95, 158, 179, 19, 48, 202,
    ])
    assert salsa20_hash(inp) == out


def test_expansion_section_9() -> None:
    k0 = bytes(range(1, 17))
    k1 = bytes(range(201, 217))
    n = bytes(range(101, 117))
    want32 = bytes([
        69, 37, 68, 39, 41, 15, 107, 193, 255, 139, 122, 6, 170, 233, 217, 98,
        89, 144, 182, 106, 21, 51, 200, 65, 239, 49, 222, 34, 215, 114, 40, 126,
        104, 197, 7, 225, 197, 153, 31, 2, 102, 78, 76, 176, 84, 245, 246, 184,
        177, 160, 133, 130, 6, 72, 149, 119, 192, 195, 132, 236, 234, 103, 246, 74,
    ])
    want16 = bytes([
        39, 173, 46, 248, 30, 200, 82, 17, 48, 67, 254, 239, 37, 18, 13, 247,
        241, 200, 61, 144, 10, 55, 50, 185, 6, 47, 246, 253, 143, 86, 187, 225,
        134, 85, 110, 246, 161, 163, 43, 235, 231, 94, 171, 51, 145, 214, 112, 29,
        14, 232, 5, 16, 151, 140, 183, 141, 171, 9, 122, 181, 104, 182, 177, 193,
    ])
    assert salsa20_expand(k0 + k1, n) == want32
    assert salsa20_expand(k0, n) == want16


def test_encryption_uses_the_expansion() -> None:
    # Section 10: byte i of the keystream is Salsa20_k(v, floor(i/64))[i mod 64].
    k = bytes(range(1, 17)) + bytes(range(201, 217))
    v = bytes(range(101, 109))
    ks = salsa20_encrypt(k, v, bytes(130))
    assert ks[:64] == salsa20_expand(k, v + bytes(8))
    assert ks[64:128] == salsa20_expand(k, v + (1).to_bytes(8, "little"))
    assert ks[128:] == salsa20_expand(k, v + (2).to_bytes(8, "little"))[:2]


def test_round_trip_and_avalanche() -> None:
    rng = random.Random(11)
    total = 0
    for _ in range(10):
        k = bytes(rng.randrange(256) for _ in range(32))
        v = bytes(rng.randrange(256) for _ in range(8))
        m = bytes(rng.randrange(256) for _ in range(rng.randrange(0, 150)))
        assert salsa20_encrypt(k, v, salsa20_encrypt(k, v, m)) == m
        blk = bytearray(rng.randrange(256) for _ in range(64))
        a = salsa20_hash(bytes(blk))
        blk[rng.randrange(64)] ^= 1 << rng.randrange(8)
        b = salsa20_hash(bytes(blk))
        total += bin(int.from_bytes(a, "big") ^ int.from_bytes(b, "big")).count("1")
    assert 210 <= total / 10 <= 302


def test_salsa20_8_and_12_differ() -> None:
    blk = bytes(range(64))
    assert len({salsa20_hash(blk, 8), salsa20_hash(blk, 12), salsa20_hash(blk, 20)}) == 3
