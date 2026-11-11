# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/crc-generator-polynomial/. The authors are listed in prov/TY4M8X.jsonl.

from functools import reduce

from crc_generator_polynomial import (
    deg, factor, from_koopman, from_normal, from_reversed, hd_profile, is_primitive, min_distance_brute,
    min_distance_by_length, order_of_x, pmod, pmul, reciprocal, to_koopman, to_normal, to_reversed,
)


def is_irreducible_brute(f: int) -> bool:
    return all(pmod(f, g) for g in range(2, 1 << (deg(f) // 2 + 1)))


def test_notations() -> None:
    # (normal, reversed, Koopman) for well-known generators.
    table = [
        (32, 0x04C11DB7, 0xEDB88320, 0x82608EDB),  # CRC-32 (IEEE 802.3)
        (32, 0x1EDC6F41, 0x82F63B78, 0x8F6E37A0),  # CRC-32C (Castagnoli)
        (16, 0x8005, 0xA001, 0xC002),  # CRC-16 (ARC, Modbus)
        (16, 0x1021, 0x8408, 0x8810),  # CRC-16 of ITU-T V.41
        (8, 0x07, 0xE0, 0x83),  # CRC-8/SMBUS
    ]
    for r, normal, rev, koop in table:
        g = from_normal(normal, r)
        assert from_reversed(rev, r) == g and from_koopman(koop, r) == g
        assert (to_normal(g), to_reversed(g), to_koopman(g)) == (normal, rev, koop)
        # The reversed notation of G is the Koopman notation of its reciprocal.
        assert to_koopman(reciprocal(g)) == rev


def test_koopman_reciprocal_pairs() -> None:
    # Koopman, CRC zoo, 8-bit page: "(0x83; 0x107) <=> (0xe0; 0x1c1)".
    g = from_koopman(0x83, 8)
    assert g == 0x107 and reciprocal(g) == 0x1C1 and to_koopman(reciprocal(g)) == 0xE0


def test_factorizations() -> None:
    known = {
        0x104C11DB7: [0x104C11DB7],  # CRC-32: irreducible
        0x11EDC6F41: [0x3, 0xF5B4253F],  # CRC-32C: (x + 1) times degree 31
        0x18005: [0x3, 0x8003],  # CRC-16: (x + 1)(x^15 + x + 1)
        0x11021: [0x3, 0xF01F],  # V.41: (x + 1)(x^15 + x^14 + x^13 + x^12 + x^4 + x^3 + x^2 + x + 1)
        0x107: [0x3, 0xFD],  # CRC-8/SMBUS
        0x101: [0x3] * 8,  # x^8 + 1 = (x + 1)^8
    }
    for g, fs in known.items():
        got = factor(g)
        assert got == fs, hex(g)
        assert reduce(pmul, got, 1) == g
    for g in range(0x100, 0x200):
        fs = factor(g)
        assert reduce(pmul, fs, 1) == g
        assert all(deg(f) <= 9 and is_irreducible_brute(f) for f in fs if deg(f) > 1)


def test_primitive_parts() -> None:
    assert is_primitive(0x104C11DB7) and order_of_x(0x104C11DB7) == 2**32 - 1
    assert is_primitive(0xF5B4253F) and order_of_x(0xF5B4253F) == 2**31 - 1
    assert is_primitive(0x8003) and is_primitive(0xF01F) and is_primitive(0xFD)


def test_hd_profile_against_koopman_crc8_zoo() -> None:
    # Philip Koopman, CRC polynomial zoo, 8-bit page (users.ece.cmu.edu/~koopman/crc/crc8.html),
    # copied by hand: Koopman notation and the list of maximum data lengths
    # in bits for HD = 3, 4, 5, ...
    zoo = {
        0x83: [119, 119],
        0x97: [119, 119, 3, 3],
        0x9B: [118, 118, 4, 4],
        0xA6: [247, 15, 6],
        0xE7: [247, 19, 1, 1, 1],
        0xEA: [85, 85, 2, 2],
        0x80: [],
        0x8E: [247, 13, 6],
    }
    for k, want in zoo.items():
        assert hd_profile(from_koopman(k, 8), 260) == want, hex(k)


def test_min_distance_against_all_multiples() -> None:
    for g in (0x107, 0x12F, 0x137, 0x14D, 0x1CF, 0x1D5, 0x11D, 0x1021 | 0x10000):
        d = min_distance_by_length(g, 13)
        for L in range(1, 14):
            assert d[L] == min_distance_brute(g, L), (hex(g), L)
