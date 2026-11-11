# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lz4/. The authors are listed in prov/2E3NAH.jsonl.
# No standard library codec exists for LZ4. The frames below are copied by
# hand from lz4/lz4 tests/data/goldenSamples, or are the output of the
# reference command line tool lz4 v1.10.0, as each comment says.

import random

import pytest

from lz4 import (
    LZ4Error, LAST_LITERALS, MF_LIMIT, compress_block, compress_frame,
    decompress_block, decompress_frame, xxh32,
)


def _inputs():
    rng = random.Random(4)
    words = [b"lz4", b"token", b"literal", b"match", b"offset", b"frame"]
    return [
        b"",
        b"a",
        b"\x00" * 1000,
        b"q" * 300000,
        bytes(rng.randrange(256) for _ in range(20000)),
        b" ".join(rng.choice(words) for _ in range(6000)),
        b"abcabcabcabcabc",
        bytes(range(13)),
    ]


def _sequences(block):
    """Parse a block into (literal_length, match_length, offset) triples."""
    out, pos = [], 0
    while True:
        token = block[pos]
        pos += 1
        lit = token >> 4
        if lit == 15:
            while True:
                lit += block[pos]
                pos += 1
                if block[pos - 1] != 255:
                    break
        pos += lit
        if pos == len(block):
            out.append((lit, 0, 0))
            return out
        off = block[pos] | block[pos + 1] << 8
        pos += 2
        ml = token & 15
        if ml == 15:
            while True:
                ml += block[pos]
                pos += 1
                if block[pos - 1] != 255:
                    break
        out.append((lit, ml + 4, off))


def test_xxh32_check_values():
    # Reference values of xxHash32 with seed 0 (xxhash sanity tests).
    assert xxh32(b"") == 0x02CC5D05
    # The frame header checksum of FLG 0x64, BD 0x40 is 0xA7 (see the CLI
    # sample below), that is (XXH32(64 40) >> 8) & 0xFF.
    assert (xxh32(b"\x64\x40") >> 8) & 0xFF == 0xA7


def test_golden_dictid():
    # lz4/lz4 tests/data/goldenSamples/dictID.bin: FLG 0x61 (version 01,
    # independent blocks, DictID), BD 0x40, DictID 0x0000D1C7, HC 0x69, one
    # uncompressed block of 35 bytes, EndMark.
    text = b"lz4 dictID frame regression sample\n"
    frame = bytes.fromhex("04224d18" "61" "40" "c7d10000" "69" "23000080") + text + bytes(4)
    assert decompress_frame(frame) == text


def test_golden_skippable():
    # lz4/lz4 tests/data/goldenSamples/skip.bin: magic 0x184D2A5A, size 30.
    frame = bytes.fromhex("5a2a4d18" "1e000000") + bytes(30)
    assert decompress_frame(frame) == b""


CLI_SAMPLES = [
    # Output of `lz4 -c -9` (lz4 v1.10.0) on the given input.
    (b"Hello, LZ4! Hello, LZ4! Hello, LZ4! Hello, LZ4! The end.\n",
     "04224d186440a71a000000cf48656c6c6f2c204c5a3421200c00119054686520656e642e0a00000000176517d1"),
    # Output of `lz4 -c -1` (lz4 v1.10.0) on "abc" * 10.
    (b"abc" * 10,
     "04224d186440a70d0000003f61626303000350626361626300000000c1ab873d"),
    # Output of `lz4 -c` (lz4 v1.10.0) on empty input.
    (b"", "04224d186440a700000000055dcc02"),
]


@pytest.mark.parametrize("data,hexframe", CLI_SAMPLES)
def test_reference_tool_frames(data, hexframe):
    assert decompress_frame(bytes.fromhex(hexframe)) == data


def test_reference_tool_frames_match_ours():
    # On these three short inputs our greedy encoder makes the same frame,
    # byte for byte. This is not true for all inputs: the encoder is free.
    for data, hexframe in CLI_SAMPLES:
        assert compress_frame(data) == bytes.fromhex(hexframe)


def test_round_trip_blocks_and_frames():
    for data in _inputs():
        assert decompress_block(compress_block(data)) == data
        for kw in ({}, {"independent": False, "block_checksum": True},
                   {"content_size": True, "block_max": 5}):
            assert decompress_frame(compress_frame(data, **kw)) == data


def test_linked_blocks_use_history():
    data = b"the quick brown fox jumps over the lazy dog. " * 3000
    a = compress_frame(data, independent=True)
    b = compress_frame(data, independent=False)
    assert decompress_frame(b) == data and len(b) <= len(a)


def test_end_of_block_rules():
    # lz4_Block_format.md, "End of block conditions".
    for data in _inputs():
        block = compress_block(data)
        seqs = _sequences(block)
        assert seqs[-1][1] == 0                    # the last sequence is literals only
        pos = 0
        for lit, ml, off in seqs:
            pos += lit
            if ml:
                assert ml >= 4 and 1 <= off <= 65535
                assert pos <= len(data) - MF_LIMIT     # the match starts early enough
                pos += ml
                assert pos <= len(data) - LAST_LITERALS
        assert pos == len(data)


def test_overlapping_match():
    # One literal "a", then a match at offset 1 of length 4 + 15 + 3 = 22,
    # then 5 literals. Hand-built from the token rules.
    block = bytes([0x1F]) + b"a" + b"\x01\x00" + bytes([3]) + bytes([0x50]) + b"bcdef"
    assert decompress_block(block) == b"a" * 23 + b"bcdef"


def test_errors():
    with pytest.raises(LZ4Error):
        decompress_block(b"\x10a\x00\x00\x50bcdef")      # offset 0
    with pytest.raises(LZ4Error):
        decompress_block(b"\x10a\x02\x00\x50bcdef")      # offset before the start
    with pytest.raises(LZ4Error):
        decompress_block(b"\x30ab")                      # literals past the end
    good = compress_frame(b"hello hello hello hello hello")
    bad = bytearray(good)
    bad[-1] ^= 1
    with pytest.raises(LZ4Error):
        decompress_frame(bytes(bad))                      # content checksum
    bad = bytearray(good)
    bad[6] ^= 1
    with pytest.raises(LZ4Error):
        decompress_frame(bytes(bad))                      # header checksum
