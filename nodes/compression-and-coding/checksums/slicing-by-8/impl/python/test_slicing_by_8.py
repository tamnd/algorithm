# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slicing-by-8/. The authors are listed in prov/K8JNYQ.jsonl.

import binascii
import random

from slicing_by_8 import (
    CRC32_POLY, CRC32C_POLY, Counter, crc32_bytewise, crc32_slicing4, crc32_slicing8, make_tables, reflect,
)

RNG = random.Random(2005)
T32 = make_tables(CRC32_POLY, 8)
T32C = make_tables(CRC32C_POLY, 8)


def test_check_values() -> None:
    # Check values of CRC-32/ISO-HDLC and CRC-32/ISCSI, reveng CRC catalogue.
    for f in (crc32_bytewise, crc32_slicing4, crc32_slicing8):
        assert f(b"123456789", CRC32_POLY) == 0xCBF43926
        assert f(b"123456789", CRC32C_POLY) == 0xE3069283


def test_tables_are_shifted_bytes() -> None:
    # T_k[v] is the register after byte v and k zero bytes, from zero.
    for k in range(8):
        for v in (1, 0x80, 0xFF, RNG.randrange(256)):
            reg = 0
            for byte in bytes([v]) + bytes(k):
                reg = (reg >> 8) ^ T32[0][(reg ^ byte) & 0xFF]
            assert T32[k][v] == reg
    # Normal-domain meaning: T_k[v] reversed is v(x) x^(32 + 8k) mod G(x).
    g = (1 << 32) | CRC32_POLY
    for k in range(8):
        for v in (1, 0x80, 0x5A):
            a = reflect(v, 8) << (32 + 8 * k)
            while a.bit_length() > 32:
                a ^= g << (a.bit_length() - 33)
            assert reflect(T32[k][v], 32) == a


def test_all_methods_agree() -> None:
    for n in list(range(0, 70)) + [255, 1024, 4099]:
        data = bytes(RNG.randrange(256) for _ in range(n))
        want = binascii.crc32(data)
        assert crc32_bytewise(data, CRC32_POLY, tables=T32[:1]) == want
        assert crc32_slicing4(data, CRC32_POLY, tables=T32[:4]) == want
        assert crc32_slicing8(data, CRC32_POLY, tables=T32) == want
        c = crc32_bytewise(data, CRC32C_POLY, tables=T32C[:1])
        assert crc32_slicing4(data, CRC32C_POLY, tables=T32C[:4]) == c
        assert crc32_slicing8(data, CRC32C_POLY, tables=T32C) == c


def test_operation_counts() -> None:
    # One lookup per byte in each method; the number of dependent register
    # updates drops from n to about n/4 and n/8.
    data = bytes(RNG.randrange(256) for _ in range(1003))
    counts = {}
    for name, f in (("bytewise", crc32_bytewise), ("slicing4", crc32_slicing4), ("slicing8", crc32_slicing8)):
        cnt = Counter()
        f(data, CRC32_POLY, cnt)
        counts[name] = (cnt.lookups, cnt.steps)
    assert counts == {"bytewise": (1003, 1003), "slicing4": (1003, 250 + 3), "slicing8": (1003, 125 + 3)}


def test_table_sizes() -> None:
    # 256 entries of 4 bytes each: 1, 4 and 8 KiB.
    for k, kib in ((1, 1), (4, 4), (8, 8)):
        assert len(make_tables(CRC32_POLY, k)) * 256 * 4 == kib * 1024
