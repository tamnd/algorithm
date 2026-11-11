# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variable-byte-encoding/. The authors are listed in prov/JRS6JT.jsonl.

import random

import pytest

from variable_byte_encoding import (
    decode_all,
    encode_all,
    sleb128_decode,
    sleb128_encode,
    stream_vbyte_decode,
    stream_vbyte_encode,
    uleb128_decode,
    uleb128_encode,
    uleb128_length,
    zigzag_decode,
    zigzag_encode,
)

# DWARF Debugging Information Format Version 5 (2017), Section 7.6,
# Table 7.7 (examples of unsigned LEB128 encodings), copied by hand.
DWARF_TABLE_7_7 = {2: "02", 127: "7f", 128: "80 01", 129: "81 01", 12857: "b9 64"}

# DWARF 5, Section 7.6, Table 7.8 (examples of signed LEB128 encodings), copied by hand.
DWARF_TABLE_7_8 = {
    2: "02", -2: "7e", 127: "ff 00", -127: "81 7f",
    128: "80 01", -128: "80 7f", 129: "81 01", -129: "ff 7e",
}

# Protocol Buffers encoding guide (protobuf.dev/programming-guides/encoding/),
# section "Signed Integers", ZigZag table, copied by hand: signed -> encoded.
PROTOBUF_ZIGZAG = {0: 0, -1: 1, 1: 2, -2: 3, 0x7FFFFFFF: 0xFFFFFFFE, -0x80000000: 0xFFFFFFFF}

# Lemire, Kurz and Rupp, Stream VByte: Faster byte-oriented integer compression,
# Information Processing Letters 130 (2018), Figure 3, copied by hand.
STREAM_VBYTE_FIG3_VALUES = [1024, 12, 10, 1073741824, 1, 2, 3, 1024]
STREAM_VBYTE_FIG3_CONTROL = "c1 40"
STREAM_VBYTE_FIG3_DATA = "00 04 0c 0a 00 00 00 40 01 02 03 00 04"


def uleb(x: int) -> bytes:
    out = bytearray()
    uleb128_encode(x, out)
    return bytes(out)


def sleb(v: int) -> bytes:
    out = bytearray()
    sleb128_encode(v, out)
    return bytes(out)


def uleb_oracle(x: int) -> bytes:
    """Cut the binary form into 7-bit groups from the right, then flag all but the last."""
    b = format(x, "b")
    b = b.zfill(-(-len(b) // 7) * 7)
    groups = [int(b[i : i + 7], 2) for i in range(0, len(b), 7)][::-1]
    return bytes([g | 0x80 for g in groups[:-1]] + [groups[-1]])


def test_dwarf_unsigned() -> None:
    for x, hexstr in DWARF_TABLE_7_7.items():
        assert uleb(x) == bytes.fromhex(hexstr)
        assert uleb128_decode(bytes.fromhex(hexstr)) == (x, len(bytes.fromhex(hexstr)))


def test_dwarf_signed() -> None:
    for v, hexstr in DWARF_TABLE_7_8.items():
        assert sleb(v) == bytes.fromhex(hexstr)
        assert sleb128_decode(bytes.fromhex(hexstr)) == (v, len(bytes.fromhex(hexstr)))


def test_protobuf() -> None:
    # Section "Base 128 Varints": 150 is encoded as 96 01.
    assert uleb(150) == bytes.fromhex("96 01")
    assert uleb128_decode(bytes.fromhex("96 01")) == (150, 2)
    # A 64-bit value takes at most 10 bytes; -1 as int64 is 2^64 - 1.
    assert len(uleb(2**64 - 1)) == 10
    for v, z in PROTOBUF_ZIGZAG.items():
        assert zigzag_encode(v) == z
        assert zigzag_decode(z) == v


def test_stream_vbyte_figure_3() -> None:
    control, data = stream_vbyte_encode(STREAM_VBYTE_FIG3_VALUES)
    assert control == bytes.fromhex(STREAM_VBYTE_FIG3_CONTROL)
    assert data == bytes.fromhex(STREAM_VBYTE_FIG3_DATA)
    assert stream_vbyte_decode(8, control, data) == STREAM_VBYTE_FIG3_VALUES


def test_worked_example() -> None:
    # The page example: 624485 -> e5 8e 26; -123456 -> c0 bb 78.
    assert uleb(624485) == bytes.fromhex("e5 8e 26")
    assert sleb(-123456) == bytes.fromhex("c0 bb 78")
    assert encode_all([1, 300, 0]) == bytes.fromhex("01 ac 02 00")


def test_random_against_oracles() -> None:
    rng = random.Random(79)
    for _ in range(500):
        values = [rng.randrange(0, 1 << rng.randrange(1, 70)) for _ in range(rng.randrange(1, 20))]
        data = encode_all(values)
        assert data == b"".join(uleb_oracle(x) for x in values)
        assert len(data) == sum(uleb128_length(x) for x in values)
        assert decode_all(data) == values
        signed = [v - (1 << rng.randrange(0, 70)) for v in values]
        for v in signed:
            enc = sleb(v)
            assert sleb128_decode(enc) == (v, len(enc))
            # Two's complement in 7 * len bits holds v; one byte fewer would not.
            n = 7 * len(enc)
            assert -(1 << (n - 1)) <= v < 1 << (n - 1)
            if len(enc) > 1:
                assert not -(1 << (n - 8)) <= v < 1 << (n - 8)
            assert zigzag_decode(zigzag_encode(v)) == v
        u32 = [rng.randrange(0, 1 << rng.choice((8, 16, 24, 32))) for _ in range(rng.randrange(0, 30))]
        control, sdata = stream_vbyte_encode(u32)
        assert len(control) == (len(u32) + 3) // 4
        assert stream_vbyte_decode(len(u32), control, sdata) == u32


def test_zigzag_order() -> None:
    order = sorted(range(-50, 51), key=zigzag_encode)
    assert order[:5] == [0, -1, 1, -2, 2]
    assert [zigzag_encode(v) for v in order] == list(range(101))


def test_edge_cases() -> None:
    assert uleb(0) == b"\x00"
    assert sleb(0) == b"\x00" and sleb(-1) == b"\x7f" and sleb(63) == b"\x3f" and sleb(64) == b"\xc0\x00"
    assert decode_all(b"") == []
    # An overlong but valid encoding of 0.
    assert uleb128_decode(b"\x80\x80\x00") == (0, 3)
    with pytest.raises(ValueError):
        uleb128_decode(b"\x80" * 10 + b"\x00", max_bytes=10)
    with pytest.raises(EOFError):
        uleb128_decode(b"\x80\x80")
    with pytest.raises(ValueError):
        uleb(-1)
    with pytest.raises(ValueError):
        stream_vbyte_encode([1 << 32])
