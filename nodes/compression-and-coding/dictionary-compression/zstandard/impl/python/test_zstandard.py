# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zstandard/. The authors are listed in prov/E9Q3EG.jsonl.
# The oracle is compression.zstd of the Python 3.14 standard library
# (libzstd), used here only.

import random

import pytest

from zstandard import (BLOCK_MAX, PREDEFINED_OF, ZstdError, _resolve_offset,
                       compress, decompress, xxh64)

zstd = pytest.importorskip("compression.zstd")


def _inputs():
    rng = random.Random(8878)
    words = [b"frame", b"block", b"literal", b"sequence", b"offset", b"Collet"]
    return [
        b"",
        b"a",
        b"\x00" * 1000,
        b"z" * 100000,
        bytes(rng.randrange(256) for _ in range(5000)),
        b" ".join(rng.choice(words) for _ in range(30000)),   # two blocks
        bytes(rng.choice(b"ab") for _ in range(3000)),
        b"ab" * 20 + b"cd" * 20 + b"z" * 40000 + b"ab" * 20,
    ]


# facebook/zstd, tests/golden-decompression/ (copied by hand).
GOLDEN = {
    "empty-block.zst": ("28b52ffd00001500000000", b""),
    "zeroSeq_2B.zst": ("28b52ffd00008500006848656c6c6f20576f726c64210a8000",
                       b"Hello World!\n"),
    "rle-first-block.zst": (
        "28b52ffda4000010000200100002001000020010000200100002001000020010"
        "000200100003001000f13e16e1", bytes(1 << 20)),
}

# facebook/zstd, tests/golden-decompression-errors/ (copied by hand).
GOLDEN_ERRORS = {
    "off0.bin.zst": "28b52ffd0000450000080002002f430bae",
    "truncated_huff_state.zst": "28b52ffd000055000072800104207e1f02aa00",
    "zeroSeq_extraneous.zst": "28b52ffd00009500006848656c6c6f20576f726c64210a80000000",
}


@pytest.mark.parametrize("name", sorted(GOLDEN))
def test_golden(name):
    hexdata, want = GOLDEN[name]
    assert decompress(bytes.fromhex(hexdata)) == want


@pytest.mark.parametrize("name", sorted(GOLDEN_ERRORS))
def test_golden_errors(name):
    with pytest.raises(ZstdError):
        decompress(bytes.fromhex(GOLDEN_ERRORS[name]))


def test_predefined_offset_table():
    # RFC 8878 Appendix A.3, "Offset Code Table": (symbol, bits, base) by state.
    want = [(0, 5, 0), (6, 4, 0), (9, 5, 0), (15, 5, 0), (21, 5, 0),
            (3, 5, 0), (7, 4, 0), (12, 5, 0), (18, 5, 0), (23, 5, 0),
            (5, 5, 0), (8, 4, 0), (14, 5, 0), (20, 5, 0), (2, 5, 0),
            (7, 4, 16), (11, 5, 0), (17, 5, 0), (22, 5, 0), (4, 5, 0),
            (8, 4, 16), (13, 5, 0), (19, 5, 0), (1, 5, 0), (6, 4, 16),
            (10, 5, 0), (16, 5, 0), (28, 5, 0), (27, 5, 0), (26, 5, 0),
            (25, 5, 0), (24, 5, 0)]
    assert PREDEFINED_OF[0] == want


def test_repeat_offsets_table():
    # facebook/zstd doc/zstd_compression_format.md (version 0.4.5), the
    # Repeated_Offsets table in "Repeat offsets". RFC 8878 Table 18 has
    # the same rows except the last two, which it prints differently.
    rows = [(1114, 11, (1111, 1, 4)), (1, 22, (1111, 1, 4)),
            (2225, 22, (2222, 1111, 1)), (1114, 111, (1111, 2222, 1111)),
            (3336, 33, (3333, 1111, 2222)), (2, 22, (1111, 3333, 2222)),
            (3, 33, (2222, 1111, 3333)), (3, 0, (2221, 2222, 1111)),
            (1, 0, (2222, 2221, 1111))]
    rep = [1, 4, 8]
    for value, ll, want in rows:
        _resolve_offset(value, ll, rep)
        assert tuple(rep) == want


def test_xxh64():
    # The XXH64 check value of the empty input, seed 0 (xxHash).
    assert xxh64(b"") == 0xEF46DB3751D8E999
    rng = random.Random(64)
    for n in (1, 3, 4, 7, 8, 31, 32, 33, 100, 1000):
        data = bytes(rng.randrange(256) for _ in range(n))
        frame = zstd.compress(data, options={zstd.CompressionParameter.checksum_flag: 1})
        assert frame[-4:] == (xxh64(data) & 0xFFFFFFFF).to_bytes(4, "little")


@pytest.mark.parametrize("level", [-5, 1, 3, 9, 19])
def test_we_read_libzstd(level):
    for data in _inputs():
        assert decompress(zstd.compress(data, level=level)) == data


def test_we_read_streamed_frames():
    # No content size, a window descriptor and several blocks.
    data = _inputs()[5]
    p = zstd.CompressionParameter
    c = zstd.ZstdCompressor(options={p.compression_level: 3, p.checksum_flag: 1,
                                     p.window_log: 17})
    frame = c.compress(data[:70000]) + c.compress(data[70000:], mode=c.FLUSH_FRAME)
    assert frame[4] & 0x20 == 0                  # not single segment
    assert decompress(frame) == data


def test_libzstd_reads_ours():
    for data in _inputs():
        ours = compress(data)
        assert zstd.decompress(ours) == data
        assert decompress(ours) == data
        assert decompress(compress(data, checksum=False)) == data


def test_blocks_and_history():
    # Several 128 KiB blocks; matches reach back into earlier blocks.
    rng = random.Random(3)
    piece = bytes(rng.randrange(256) for _ in range(20000))
    data = piece * 15
    ours = compress(data)
    assert len(data) > 2 * BLOCK_MAX
    assert len(ours) < len(data) // 5
    assert zstd.decompress(ours) == data
    assert decompress(ours) == data


def test_page_example():
    # The example on the page: 18 bytes become one compressed block.
    want = bytes.fromhex("28b52ffd" "2412" "4d0000" "18616263" "0100" "766e08" "ebfe1327")
    assert compress(b"abcabcabcabcabcabc") == want
    assert zstd.decompress(want) == b"abcabcabcabcabcabc"


def test_frames_and_skippable_frames():
    skip = (0x184D2A53).to_bytes(4, "little") + (3).to_bytes(4, "little") + b"xyz"
    stream = zstd.compress(b"abc") + skip + compress(b"defdefdef")
    assert decompress(stream) == b"abcdefdefdef"


def test_errors():
    good = compress(b"hello hello hello hello")
    bad = bytearray(good)
    bad[-1] ^= 1
    with pytest.raises(ZstdError):
        decompress(bytes(bad))                       # checksum
    with pytest.raises(ZstdError):
        decompress(good[:-6])                        # truncated
    with pytest.raises(ZstdError):
        decompress(b"\x00" + good[1:])               # magic number
    with pytest.raises(ZstdError):
        decompress(b"")
    reserved = bytearray(good)
    reserved[4] |= 8
    with pytest.raises(ZstdError):
        decompress(bytes(reserved))                  # reserved bit
    with pytest.raises(ZstdError):
        decompress(bytes.fromhex("28b52ffd" "01" "00" "07" "010000"))   # Dictionary_ID 7
    with pytest.raises(ZstdError):
        decompress(bytes.fromhex("28b52ffd" "20" "03" "070000"))        # reserved block type
