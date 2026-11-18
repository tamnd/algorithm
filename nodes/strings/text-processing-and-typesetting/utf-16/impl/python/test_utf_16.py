# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/utf-16/. The authors are listed in prov/7HJ2KD.jsonl.

# The oracle is Python's codec: str.encode("utf-16-be") and bytes.decode("utf-16-be").
# Written against Python 3.14, unicodedata.unidata_version 16.0.0. UTF-16 does not depend
# on the Unicode version.

import itertools
import random

from utf_16 import UTF16Error, decode, decode_units, encode, encode_code_point, length_in_code_units

UNITS = [0x0000, 0x0041, 0xD7FF, 0xD800, 0xDBFF, 0xDC00, 0xDFFF, 0xE000, 0xFFFD, 0xFFFF]


def oracle_strict(b: bytes):
    try:
        return b.decode("utf-16-be")
    except UnicodeDecodeError as e:
        return (e.start, e.end)


def mine_strict(b: bytes):
    try:
        return decode(b, "strict")
    except UTF16Error as e:
        return (e.start, e.end)


def check(b: bytes) -> None:
    assert decode(b) == b.decode("utf-16-be", "replace"), b.hex(" ")
    assert mine_strict(b) == oracle_strict(b), b.hex(" ")


def test_check_values() -> None:
    table = {0x41: [0x0041], 0xE9: [0x00E9], 0x20AC: [0x20AC], 0x10000: [0xD800, 0xDC00],
             0x1F600: [0xD83D, 0xDE00], 0x10FFFF: [0xDBFF, 0xDFFF]}
    for c, units in table.items():
        assert encode_code_point(c) == units
        assert decode_units(units) == [c]


def test_encode_against_codec() -> None:
    points = [0, 0x7F, 0x80, 0x7FF, 0x800, 0xD7FF, 0xE000, 0xFFFF, 0x10000, 0x10FFFF]
    rng = random.Random(1)
    points += [rng.choice([rng.randrange(0xD800), rng.randrange(0xE000, 0x110000)]) for _ in range(5000)]
    for c in points:
        assert encode(chr(c)) == chr(c).encode("utf-16-be")
        assert encode(chr(c), "little") == chr(c).encode("utf-16-le")
        assert decode(encode(chr(c))) == chr(c)
        assert decode(encode(chr(c), "little"), byteorder="little") == chr(c)


def test_surrogates_are_not_scalar_values() -> None:
    for c in (0xD800, 0xDBFF, 0xDC00, 0xDFFF, 0x110000, -1):
        try:
            encode_code_point(c)
            raise AssertionError("must reject")
        except ValueError:
            pass


def test_unpaired_surrogates() -> None:
    assert decode_units([0xD800, 0x0041]) == [0xFFFD, 0x41]
    assert decode_units([0xDC00, 0xD800]) == [0xFFFD, 0xFFFD]
    assert decode_units([0xD800, 0xD800, 0xDC00]) == [0xFFFD, 0x10000]
    # The surrogatepass handler of Python keeps lone surrogates as code points.
    assert bytes.fromhex("D800 0041").decode("utf-16-be", "surrogatepass") == "\ud800A"


def test_all_unit_sequences_up_to_three() -> None:
    for k in range(1, 4):
        for t in itertools.product(UNITS, repeat=k):
            check(b"".join(u.to_bytes(2, "big") for u in t))


def test_odd_lengths() -> None:
    for t in itertools.product(UNITS, repeat=2):
        b = b"".join(u.to_bytes(2, "big") for u in t)
        for extra in (b"\x00", b"\xdc", b"\xd8"):
            check(b + extra)
            check(b[:2] + extra)
        check(b[:1])


def test_random_bytes() -> None:
    rng = random.Random(2)
    pool = [0x00, 0x41, 0xD8, 0xDB, 0xDC, 0xDF, 0xE0, 0xFF]
    for _ in range(5000):
        check(bytes(rng.choice(pool) for _ in range(rng.randrange(1, 11))))


def test_length_in_code_units() -> None:
    s = "a€😀"
    assert len(s) == 3
    assert length_in_code_units(s) == 4 == len(s.encode("utf-16-be")) // 2


def test_unit_order_is_not_code_point_order() -> None:
    a, b = "｡", "\U00010000"
    assert ord(a) < ord(b)
    assert encode_units_list(a) > encode_units_list(b)


def encode_units_list(s: str) -> list[int]:
    out = []
    for ch in s:
        out.extend(encode_code_point(ord(ch)))
    return out
