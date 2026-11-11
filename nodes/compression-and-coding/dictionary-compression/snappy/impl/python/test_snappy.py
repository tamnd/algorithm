# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/snappy/. The authors are listed in prov/A8ZRG6.jsonl.
# No standard library codec exists for Snappy. The vectors below are copied
# by hand from google/snappy format_description.txt, google/snappy
# snappy_unittest.cc and golang/snappy snappy_test.go (TestDecode).

import random

import pytest

from snappy import (
    SnappyError, compress, crc32c, decompress, frame_compress,
    frame_decompress, get_varint, put_varint,
)


def _inputs():
    rng = random.Random(2011)
    words = [b"snappy", b"fast", b"block", b"literal", b"copy", b"offset", b"tag"]
    return [
        b"",
        b"a",
        b"\x00" * 1000,
        b"z" * 200000,
        bytes(rng.randrange(256) for _ in range(20000)),
        b" ".join(rng.choice(words) for _ in range(5000)),
        b"xababab",
    ]


def test_varint_examples_format_description():
    # format_description.txt, section 1: 64 is 0x40, 2097150 is FE FF 7F.
    assert put_varint(64) == b"\x40"
    assert put_varint(2097150) == b"\xfe\xff\x7f"
    assert get_varint(b"\xfe\xff\x7f") == (2097150, 3)


def test_xababab_format_description():
    # format_description.txt, section 2.2: <literal "xab"> <copy offset 2 length 4>.
    stream = b"\x07" + b"\x08xab" + bytes([1 | (0 << 2), 2])
    assert decompress(stream) == b"xababab"


GOLANG_VALID = [  # golang/snappy snappy_test.go, TestDecode, valid inputs
    (b"\x00", b""),
    (b"\x03" + b"\x08\xff\xff\xff", b"\xff\xff\xff"),
    (b"\x28" + b"\x9c" + bytes(range(40)), bytes(range(40))),
    (b"\x03" + b"\xf0\x02\xff\xff\xff", b"\xff\xff\xff"),
    (b"\x03" + b"\xf4\x02\x00\xff\xff\xff", b"\xff\xff\xff"),
    (b"\x03" + b"\xf8\x02\x00\x00\xff\xff\xff", b"\xff\xff\xff"),
    (b"\x03" + b"\xfc\x02\x00\x00\x00\xff\xff\xff", b"\xff\xff\xff"),
    (b"\x04" + b"\x0cabcd", b"abcd"),
    (b"\x0d" + b"\x0cabcd" + b"\x15\x04", b"abcdabcdabcda"),
    (b"\x08" + b"\x0cabcd" + b"\x01\x04", b"abcdabcd"),
    (b"\x08" + b"\x0cabcd" + b"\x01\x02", b"abcdcdcd"),
    (b"\x08" + b"\x0cabcd" + b"\x01\x01", b"abcddddd"),
    (b"\x06" + b"\x0cabcd" + b"\x06\x03\x00", b"abcdbc"),
    (b"\x06" + b"\x0cabcd" + b"\x07\x03\x00\x00\x00", b"abcdbc"),
]

GOLANG_CORRUPT = [  # golang/snappy snappy_test.go, TestDecode, ErrCorrupt cases
    b"\x02" + b"\x08\xff\xff\xff",
    b"\x03" + b"\x08\xff\xff",
    b"\x01" + b"\xf0",
    b"\x01" + b"\xf4\x00",
    b"\x01" + b"\xf8\x00\x00",
    b"\x01" + b"\xfc\x00\x00\x00",
    b"\x01" + b"\xfc\x02\x00\x00\x00\xff\xff\xff",
    b"\x04" + b"\xfc\x02\x00\x00\x00\xff",
    b"\x04" + b"\x01",
    b"\x04" + b"\x02\x00",
    b"\x04" + b"\x03\x00\x00\x00",
    b"\x08" + b"\x0cabcd" + b"\x01\x00",
    b"\x09" + b"\x0cabcd" + b"\x01\x04",
    b"\x08" + b"\x0cabcd" + b"\x01\x05",
    b"\x07" + b"\x0cabcd" + b"\x01\x04",
    b"\x00\xfc000\x93",
]

SNAPPY_UNITTEST_CORRUPT = [  # google/snappy snappy_unittest.cc
    b"\xf0",                          # TruncatedVarint
    b"\x80\x80\x80\x80\x80\x0a",      # UnterminatedVarint
    b"\xfb\xff\xff\xff\x7f",          # OverflowingVarint
    b"\x05\x12\x00\x00",              # ZeroOffsetCopyValidation
    b"\x40\x12\x00\x00",              # ZeroOffsetCopy
]


@pytest.mark.parametrize("stream,want", GOLANG_VALID)
def test_official_valid(stream, want):
    assert decompress(stream) == want


@pytest.mark.parametrize("stream", GOLANG_CORRUPT + SNAPPY_UNITTEST_CORRUPT)
def test_official_corrupt(stream):
    with pytest.raises(SnappyError):
        decompress(stream)


def test_round_trip():
    for data in _inputs():
        c = compress(data)
        assert decompress(c) == data
        assert frame_decompress(frame_compress(data)) == data


def test_encoder_examples():
    assert compress(b"xababab") == b"\x07\x08xab\x01\x02"
    assert compress(b"") == b"\x00"
    # A run of 200000 bytes: one literal, then copies at offset 1.
    c = compress(b"z" * 200000)
    assert len(c) < 200000 // 20


def test_crc32c_check_values():
    # CRC catalogue, CRC-32/ISCSI: check = 0xE3069283.
    assert crc32c(b"123456789") == 0xE3069283
    # RFC 3720 Appendix B.4: 32 bytes of zeros, of ones, increasing, decreasing.
    assert crc32c(bytes(32)) == 0x8A9136AA
    assert crc32c(b"\xff" * 32) == 0x62A8AB43
    assert crc32c(bytes(range(32))) == 0x46DD794E
    assert crc32c(bytes(range(31, -1, -1))) == 0x113FDB5C


def test_framing_stream_identifier():
    # framing_format.txt, section 4.1: the stream starts with these 10 bytes.
    assert frame_compress(b"")[:10] == bytes.fromhex("ff060000734e61507059")
    bad = bytearray(frame_compress(b"hello hello hello"))
    bad[-1] ^= 1
    with pytest.raises(SnappyError):
        frame_decompress(bytes(bad))
