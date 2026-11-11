# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deflate/. The authors are listed in prov/TDJAX5.jsonl.
# zlib and gzip from the standard library are oracles in these tests only.

import gzip
import random
import zlib

import pytest

from deflate import (
    DeflateError, adler32, canonical_codes, crc32, deflate, gzip_compress,
    gzip_decompress, inflate, inflate_raw, limited_lengths, tokenize,
    zlib_compress, zlib_decompress,
)


def _inputs():
    rng = random.Random(1951)
    words = [b"the", b"quick", b"brown", b"fox", b"jumps", b"over", b"lazy", b"dog", b"deflate"]
    text = b" ".join(rng.choice(words) for _ in range(3000))
    return {
        "empty": b"",
        "one": b"a",
        "equal": b"\x00" * 1000,
        "run": b"x" * 70000,
        "random": bytes(rng.randrange(256) for _ in range(5000)),
        "text": text,
        "mixed": b"ab" * 300 + bytes(rng.randrange(256) for _ in range(300)) + b"ab" * 300,
    }


INPUTS = _inputs()


def test_check_values():
    # CRC catalogue (Greg Cook), CRC-32/ISO-HDLC: check = 0xCBF43926.
    assert crc32(b"123456789") == 0xCBF43926
    for data in INPUTS.values():
        assert crc32(data) == zlib.crc32(data)
        assert adler32(data) == zlib.adler32(data)
    # RFC 1950 Section 8.2: three bytes a, b, c give s2 = 3a + 2b + c + 3.
    a, b, c = 10, 20, 30
    assert adler32(bytes([a, b, c])) >> 16 == 3 * a + 2 * b + c + 3


def test_canonical_example_rfc1951():
    # RFC 1951 Section 3.2.2: lengths (3, 3, 3, 3, 3, 2, 4, 4) for A to H
    # give the codes 010, 011, 100, 101, 110, 00, 1110, 1111.
    codes = canonical_codes([3, 3, 3, 3, 3, 2, 4, 4])
    assert codes == [0b010, 0b011, 0b100, 0b101, 0b110, 0b00, 0b1110, 0b1111]


@pytest.mark.parametrize("name", sorted(INPUTS))
def test_zlib_reads_our_raw_deflate(name):
    data = INPUTS[name]
    for level in (0, 1, 6, 9):
        assert zlib.decompress(deflate(data, level), -15) == data


@pytest.mark.parametrize("name", sorted(INPUTS))
def test_we_read_zlib_raw_deflate(name):
    data = INPUTS[name]
    for level in range(10):
        co = zlib.compressobj(level, zlib.DEFLATED, -15)
        raw = co.compress(data) + co.flush()
        assert inflate(raw) == data
    # Fixed Huffman blocks only (strategy Z_FIXED).
    co = zlib.compressobj(9, zlib.DEFLATED, -15, 9, zlib.Z_FIXED)
    assert inflate(co.compress(data) + co.flush()) == data


def test_round_trip_and_tokens():
    for data in INPUTS.values():
        assert inflate(deflate(data)) == data
        toks = tokenize(data, 9)
        out = bytearray()
        for t in toks:
            if isinstance(t, int):
                out.append(t)
            else:
                ln, d = t
                assert 3 <= ln <= 258 and 1 <= d <= 32768
                for _ in range(ln):
                    out.append(out[-d])
        assert bytes(out) == data


def test_zlib_wrapper_both_ways():
    for data in INPUTS.values():
        for level in (0, 1, 6, 9):
            assert zlib_decompress(zlib.compress(data, level)) == data
            ours = zlib_compress(data, level)
            assert zlib.decompress(ours) == data
            assert (ours[0] * 256 + ours[1]) % 31 == 0


def test_zlib_preset_dictionary():
    zd = b"the quick brown fox jumps over the lazy dog " * 4
    data = INPUTS["text"][:2000]
    co = zlib.compressobj(6, zlib.DEFLATED, 15, 8, zlib.Z_DEFAULT_STRATEGY, zd)
    theirs = co.compress(data) + co.flush()
    assert theirs[1] & 0x20
    assert zlib_decompress(theirs, zdict=zd) == data
    ours = zlib_compress(data, 6, zdict=zd)
    do = zlib.decompressobj(15, zd)
    assert do.decompress(ours) == data
    with pytest.raises(DeflateError):
        zlib_decompress(ours)


def test_gzip_wrapper_both_ways():
    for data in INPUTS.values():
        assert gzip_decompress(gzip.compress(data, 6, mtime=0)) == data
        assert gzip.decompress(gzip_compress(data)) == data
    two = gzip.compress(b"first ") + gzip_compress(b"second", name=b"x.txt")
    assert gzip_decompress(two) == b"first second"
    assert gzip.decompress(two) == b"first second"


def test_block_types_seen():
    # zlib level 0 gives stored blocks, Z_FIXED gives type 1, text gives type 2.
    assert zlib.compress(b"abc", 0)[2] & 6 == 0
    assert deflate(b"abc", 0)[0] & 6 == 0
    assert (deflate(b"abcabcabcabc")[0] >> 1) & 3 == 1
    assert (deflate(INPUTS["text"])[0] >> 1) & 3 == 2


def test_errors():
    with pytest.raises(DeflateError):
        inflate(b"\x07")  # BTYPE = 3 is reserved
    with pytest.raises(DeflateError):
        inflate(b"\x01\x03\x00\x00\x00")  # LEN and NLEN do not match
    with pytest.raises(DeflateError):
        inflate(deflate(INPUTS["text"])[:-5])
    bad = bytearray(zlib.compress(b"hello"))
    bad[-1] ^= 1
    with pytest.raises(DeflateError):
        zlib_decompress(bytes(bad))
    # A distance before the start of the output: fixed block, literal 'a',
    # then length 3 with distance 2 (only 1 byte exists).
    co = zlib.compressobj(1, zlib.DEFLATED, -15, 9, zlib.Z_FIXED)
    good = co.compress(b"aaaa") + co.flush()
    assert inflate(good) == b"aaaa"


def test_end_position():
    raw = deflate(b"hello hello hello")
    out, end = inflate_raw(raw + b"TRAILER")
    assert out == b"hello hello hello" and end == len(raw)


def test_package_merge():
    freqs = [1, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]
    unl = limited_lengths(freqs, 16)
    assert max(unl) == 16
    lim = limited_lengths(freqs, 7)
    assert max(lim) == 7
    assert sum(2.0 ** -ln for ln in lim) == 1.0
    rng = random.Random(7)
    for _ in range(30):
        f = [rng.randrange(0, 50) for _ in range(rng.randrange(2, 40))]
        if sum(1 for x in f if x) < 2:
            continue
        ls = limited_lengths(f, 15)
        assert abs(sum(2.0 ** -ln for ln in ls if ln) - 1.0) < 1e-12
