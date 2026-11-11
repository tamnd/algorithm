# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lzo/. The authors are listed in prov/34ZTAK.jsonl.
"""Tests for lzo.py.

There is no published LZO test vector set and no LZO1X specification; the
format is defined by the code of the LZO library. The samples below were
made with the reference library, LZO 2.10 (liblzo2, built by Homebrew as
lzo 2.10), by its functions lzo1x_1_compress and lzo1x_999_compress, and
copied here by hand. The hand-made streams follow the byte rules of the
Linux document Documentation/staging/lzo.rst, section "Byte sequences".
"""
import random

import pytest

from lzo import LzoError, compress, decompress

# (input, stream, locator)
LIBLZO_SAMPLES = [
    (b"", "110000", "LZO 2.10 lzo1x_1_compress"),
    (b"a", "1261110000", "LZO 2.10 lzo1x_1_compress"),
    (b"abc", "14616263110000", "LZO 2.10 lzo1x_1_compress"),
    (b"abcdabcdabcd", "1d616263646162636461626364110000",
     "LZO 2.10 lzo1x_1_compress"),
    (b"abcdabcdabcd", "1561626364ec00110000", "LZO 2.10 lzo1x_999_compress"),
    (b"hello hello hello hello\n", "1768656c6c6f202f15000a110000",
     "LZO 2.10 lzo1x_999_compress"),
    (b"a" * 64, "026161616161200b10000c616161616161616161616161616161110000",
     "LZO 2.10 lzo1x_1_compress"),
    (b"a" * 64, "1261201e0000110000", "LZO 2.10 lzo1x_999_compress"),
    # 0000DDSS after one literal: a 2-byte copy at distance 2 (state 1..3)
    (b"daaaacac", "1364614100630400110000", "LZO 2.10 lzo1x_999_compress"),
    (b"abdcbdcb", "15616264636800110000", "LZO 2.10 lzo1x_999_compress"),
    (b"bdbdbccba", "13626444000163636261110000", "LZO 2.10 lzo1x_999_compress"),
    (b"aabaccdcaaaddbccdcbdababdbccdcbda",
     "1f616162616363646361616164646266016264490262272c00110000",
     "LZO 2.10 lzo1x_999_compress"),
    # 0001HLLL with a length extension: distance 20010, length 10
    (b"abcdefghij" + bytes(20000) + b"abcdefghij" + b"z" * 5,
     "1c6162636465666768696a00"
     + "2000000000000000e60000" * 9
     + "20000000000000040000" "1001a9387a6000110000",
     "LZO 2.10 lzo1x_999_compress"),
]


@pytest.mark.parametrize("x,hexs,where", LIBLZO_SAMPLES,
                         ids=[str(i) for i in range(len(LIBLZO_SAMPLES))])
def test_liblzo_samples(x, hexs, where):
    assert decompress(bytes.fromhex(hexs)) == x
    assert decompress(compress(x)) == x


def test_same_bytes_as_lzo1x_999_on_small_inputs():
    # The greedy encoder happens to give the same stream as lzo1x_999 here.
    for x, hexs in [(b"hello hello hello hello\n", "1768656c6c6f202f15000a110000"),
                    (b"abcdabcdabcd", "1561626364ec00110000"),
                    (b"a" * 64, "1261201e0000110000")]:
        assert compress(x) == bytes.fromhex(hexs)


def test_hand_made_m1_after_long_literal_run():
    # lzo.rst: state 4, 0000DDSS, H -> copy 3 bytes, distance (H<<2)+D+2049.
    rng = random.Random(5)
    p = bytes(rng.randrange(256) for _ in range(2052))
    # literal run of 2052 = 3 + 15 + 255*7 + 249: bytes 00, seven 00, f9
    s = b"\x00" + b"\x00" * 7 + b"\xf9" + p
    s += bytes([(1 << 2) | 2, 0]) + b"XY" + b"\x11\x00\x00"   # D=1, S=2, H=0
    assert decompress(s) == p + p[2:5] + b"XY"


def test_first_byte_rules():
    # lzo.rst, "First byte encoding": 18..21 copy 0..3 literals, 22..255 copy 4..238.
    assert decompress(bytes([17 + 238]) + b"q" * 238 + b"\x11\x00\x00") == b"q" * 238
    assert decompress(b"\x14xyz" + b"\x11\x00\x00") == b"xyz"
    # The first byte 17 with fewer than 5 bytes is the end marker, not a version.
    assert decompress(b"\x11\x00\x00") == b""


def test_rle_hand_made_and_encoder():
    # Version 1: 0001 1LLL, LE16 with all D bits 1, X -> ((X<<3)|LLL)+4 zeros.
    s = bytes.fromhex("110112001dfcff00110000")
    assert decompress(s) == bytes(10)
    assert compress(bytes(10), rle=True) == s
    # The same bytes without the version prefix are an M4 copy that reaches
    # before the start of the output.
    with pytest.raises(LzoError):
        decompress(bytes.fromhex("12001dfcff00110000"))
    big = bytes(5000) + b"tail" + bytes(2051) + b"x"
    c = compress(big, rle=True)
    assert decompress(c) == big
    assert len(c) < 30


def test_rle_length_cap():
    # In version 1 a long M4 copy with (distance-16384) & 0x403f == 0x403f,
    # length 261..264 and S = 3 reads as a zero run; the encoder must cap it.
    rng = random.Random(9)
    d = 16384 + 0x403F
    pat = bytes(rng.randrange(256) for _ in range(262))
    filler = bytes(rng.randrange(256) for _ in range(d - 262))
    x = pat + filler + pat + b"!@#" + pat[:20]
    v0 = compress(x)
    assert decompress(v0) == x
    try:
        misread = decompress(b"\x11\x01" + v0)
    except LzoError:
        misread = None
    assert misread != x
    assert decompress(compress(x, rle=True)) == x


def _rand(rng, n, alphabet=256):
    return bytes(rng.randrange(alphabet) for _ in range(n))


def test_round_trips():
    rng = random.Random(2024)
    text = b"".join(rng.choice([b"the ", b"cat ", b"sat ", b"on ", b"a ", b"mat\n"])
                    for _ in range(6000))
    cases = [b"", b"\x00", b"\xff", b"z" * 5000, bytes(70000),
             b"ab" * 3000 + b"c" * 1000 + b"ab" * 3000,
             _rand(rng, 20000), _rand(rng, 30000, 3), text]
    cases += [_rand(rng, rng.randrange(1, 300), rng.choice([2, 3, 256])) for _ in range(200)]
    for x in cases:
        for rle in (False, True):
            c = compress(x, rle)
            assert decompress(c) == x


def test_distance_ranges():
    rng = random.Random(77)
    pat = _rand(rng, 12)
    for d, rle in [(2048, False), (2049, False), (16384, False), (16385, False),
                   (49151, False), (49152, False), (49150, True), (49151, True)]:
        x = pat + _rand(rng, d - len(pat)) + pat
        assert decompress(compress(x, rle)) == x


def test_long_literal_and_match_lengths():
    rng = random.Random(3)
    r = _rand(rng, 1000)
    for x in [r, r + r, r[:300] + r[:300] * 3, b"k" + r[:17] + r[:17], b"ab" + r[:18] + r[:18]]:
        assert decompress(compress(x)) == x


@pytest.mark.parametrize("bad", [
    b"",
    b"\x11\x00",                    # shorter than 3 bytes
    b"\x12a",                       # one literal, then nothing
    b"\x12a\x40\x05\x11\x00\x00",   # M2 copy at distance 41 after one byte
    b"\x12a\x12\x00\x00",           # end marker with length 4
    b"\x11\x00\x00\x00",            # data after the end marker
    b"\x14ab",                      # literal run past the end
    b"\x12a\x20\x00\x00",           # length extension never ends
])
def test_errors(bad):
    with pytest.raises(LzoError):
        decompress(bad)
