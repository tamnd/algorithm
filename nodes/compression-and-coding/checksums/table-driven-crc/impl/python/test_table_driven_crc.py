# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/table-driven-crc/. The authors are listed in prov/KSDEEZ.jsonl.

import binascii
import random

from table_driven_crc import (
    CATALOGUE, crc_combine, crc_table, crc_table_reflected, make_table, make_table_reflected, reflect,
)

RNG = random.Random(1988)


def bitwise_crc(data: bytes, p) -> int:
    """Reference: the bit-by-bit register of the cyclic-redundancy-check page."""
    top, mask, reg = 1 << (p.width - 1), (1 << p.width) - 1, p.init
    for byte in data:
        if p.refin:
            byte = reflect(byte, 8)
        for i in range(7, -1, -1):
            f = ((byte >> i) & 1) ^ ((reg & top) != 0)
            reg = (reg << 1) & mask
            if f:
                reg ^= p.poly
    if p.refout:
        reg = reflect(reg, p.width)
    return reg ^ p.xorout


def rand_bytes(n: int) -> bytes:
    return bytes(RNG.randrange(256) for _ in range(n))


def test_catalogue_check_values() -> None:
    # "check" = CRC of the ASCII bytes "123456789", from the reveng catalogue.
    for p in CATALOGUE.values():
        assert crc_table(b"123456789", p) == p.check, p.name
        if p.refin and p.refout:
            assert crc_table_reflected(b"123456789", p) == p.check, p.name


def test_known_table_entries() -> None:
    # Entries of the CRC-32 table of zlib (reflected form, poly 0xEDB88320).
    t = make_table_reflected(32, 0x04C11DB7)
    assert t[0] == 0 and t[1] == 0x77073096 and t[128] == 0xEDB88320 and t[255] == 0x2D02EF8D
    # Normal form, poly 0x04C11DB7: T[1] is poly itself, T[128] = x^7 x^32 mod G.
    n = make_table(32, 0x04C11DB7)
    assert n[1] == 0x04C11DB7
    assert all(t[v] == reflect(n[reflect(v, 8)], 32) for v in range(256))


def test_equals_bitwise() -> None:
    for p in CATALOGUE.values():
        for n in list(range(10)) + [64, 333]:
            data = rand_bytes(n)
            want = bitwise_crc(data, p)
            assert crc_table(data, p) == want, p.name
            if p.refin and p.refout:
                assert crc_table_reflected(data, p) == want, p.name


def test_against_binascii() -> None:
    iso = CATALOGUE["CRC-32/ISO-HDLC"]
    for n in list(range(40)) + [1000, 4097]:
        data = rand_bytes(n)
        assert crc_table_reflected(data, iso) == binascii.crc32(data)
        assert crc_table(data, CATALOGUE["CRC-16/XMODEM"]) == binascii.crc_hqx(data, 0)


def test_streaming_by_init() -> None:
    # For CRC-32/ISO-HDLC, binascii.crc32(b, crc32(a)) continues the register.
    iso = CATALOGUE["CRC-32/ISO-HDLC"]
    a, b = rand_bytes(37), rand_bytes(51)
    assert binascii.crc32(b, binascii.crc32(a)) == crc_table_reflected(a + b, iso)


def test_combine() -> None:
    for p in CATALOGUE.values():
        for _ in range(10):
            a, b = rand_bytes(RNG.randrange(0, 40)), rand_bytes(RNG.randrange(0, 40))
            got = crc_combine(crc_table(a, p), crc_table(b, p), len(b), p)
            assert got == crc_table(a + b, p), p.name
    iso = CATALOGUE["CRC-32/ISO-HDLC"]
    a, b = rand_bytes(5000), rand_bytes(100000)
    assert crc_combine(binascii.crc32(a), binascii.crc32(b), len(b), iso) == binascii.crc32(a + b)
