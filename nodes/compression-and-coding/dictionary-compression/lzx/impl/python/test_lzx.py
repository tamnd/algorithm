# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lzx/. The authors are listed in prov/Y9A12Q.jsonl.
# No LZX tool or library is installed here, and the Python standard
# library has none, so the oracles are two official samples copied by
# hand: an LZX folder of a CAB test file of libmspack, and the example
# stream of the Microsoft [MS-PATCH] specification.

import random
import struct

import pytest

from lzx import (BASE, EXTRA, SLOTS, LZXError, _e8_forward, _e8_reverse,
                 compress, decompress)

# libmspack, libmspack/test/test_files/cabd/mszip_lzx_qtm.cab (copied by
# hand). Folder 1 has CFFOLDER bytes C9000000 0100 0312 at file offset
# 0x2C: one CFDATA block at 0xC9, typeCompress 0x1203 (LZX, window 2^18).
# The CFDATA block holds cbData = 114 and cbUncomp = 187; its data starts
# at 0xD1. The folder is the file lzx.txt.
CAB_FOLDER = bytes.fromhex("c90000000100" "0312")
CAB_LZX = bytes.fromhex(
    "5b80808d0010b20b00000000220000550e43c052f23e8c8b7341f0085e9111a697bc47"
    "a87f7f202c00000000300203007820318d8d605f137ebf401000000000000086088a21"
    "2fe373d1beef979d979ad10139d814b3bc2659573f26190461a6e3e48fdf21da76d0f5"
    "3953da0a8e97b900b6")
DASHES = b"-" * 65 + b"\n"
CAB_TEXT = DASHES + b"If you can read this, the LZX decompressor is working!\n" + DASHES

# [MS-PATCH] v20250819, Section 3 (Structure Examples): "abc" in one
# uncompressed block. The first two bytes, 14 00, are the chunk size of
# LZX DELTA; CAB LZX has no chunk size, so the test drops them.
MS_PATCH_ABC = bytes.fromhex("1400" "0030300001000000010000000100000061626300")[2:]


def _window(n):
    return next((b for b in range(15, 22) if 1 << b >= n), 21)


def _inputs():
    rng = random.Random(1997)
    words = [b"the ", b"window ", b"frame ", b"of ", b"and ", b"LZX "]
    return [
        b"",
        b"a",
        b"\x00" * 1000,
        b"z" * 70000,
        bytes(rng.randrange(256) for _ in range(5000)),
        b"".join(rng.choice(words) for _ in range(8000)),
        bytes(rng.choice(b"ab") for _ in range(3000)),
        bytes(rng.randrange(256) for _ in range(40000)) + b"ab" * 20000,
    ]


def test_cab_sample():
    start, ndata, typ = struct.unpack("<IHH", CAB_FOLDER)
    assert (start, ndata, typ & 15, typ >> 8) == (0xC9, 1, 3, 18)
    assert len(CAB_LZX) == 114
    assert decompress(CAB_LZX, typ >> 8, 187) == CAB_TEXT


def test_ms_patch_example():
    assert decompress(MS_PATCH_ABC, 17, 3) == b"abc"
    assert compress(b"abc") == MS_PATCH_ABC          # our encoder writes the same


def test_tables():
    # [MS-PATCH] Section 2.6.2: bases and footer bits of the position slots.
    assert BASE[:12] == [0, 1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48]
    assert (BASE[24], EXTRA[24], BASE[37], EXTRA[37], BASE[42]) == (4096, 11, 393216, 17, 1048576)
    # The slots of a window 2^w end exactly at the largest formatted offset.
    for w, slots in SLOTS.items():
        assert BASE[slots - 1] + (1 << EXTRA[slots - 1]) == 1 << w


@pytest.mark.parametrize("block_type", [None, 1, 2, 3])
def test_round_trip(block_type):
    for data in _inputs():
        ours = compress(data, block_type=block_type)
        assert decompress(ours, _window(len(data)), len(data)) == data


def test_frames_and_windows():
    rng = random.Random(32768)
    text = bytes(rng.choice(b"abcd ") for _ in range(66000))
    for n in (32767, 32768, 32769, 65536):
        assert decompress(compress(text[:n]), _window(n), n) == text[:n]
    text = text[:36000]                         # longer than the 2^15 window
    for w in range(15, 22):                     # every CAB window size
        assert decompress(compress(text, window_bits=w), w, len(text)) == text


def test_page_example():
    x = b"abcabcabcabcabcabc"
    raw = compress(x)
    assert raw[:4] == bytes.fromhex("00302001") and raw[16:] == x   # uncompressed, 18 bytes
    verbatim = bytes.fromhex(
        "0010220100000000000020000701fddadff700a800000000000000043743ffff00d8"
        "00000000000010018c85effb90be00de")
    assert compress(x, block_type=1) == verbatim
    assert decompress(verbatim, 15, 18) == x


def _x86_like(n, seed):
    rng = random.Random(seed)
    targets = [rng.randrange(1000, 60000) for _ in range(50)]
    code = bytearray()
    while len(code) < n:
        rel = rng.choice(targets) - len(code)
        code += b"\xe8" + (rel & 0xFFFFFFFF).to_bytes(4, "little")
        code += rng.choice([b"\x90", b"\x8b\x45\x08", b"\x50", b"\xc3"])
    return bytes(code)


def test_e8_translation():
    code = _x86_like(60000, 8086)
    with_e8 = compress(code, e8_size=60000)
    assert with_e8[:2] == bytes.fromhex("0080")         # the E8 bit is set
    assert decompress(with_e8, 16, len(code)) == code
    assert len(with_e8) < len(compress(code))            # calls to equal targets now repeat
    for e8 in (1, 1000, 30000, 2**31 - 1):
        data = _x86_like(5000, e8)
        assert decompress(compress(data, e8_size=e8), 15, len(data)) == data


def test_e8_functions_are_inverse():
    rng = random.Random(0xE8)
    for e8 in (1, 77, 5000, 2**31 - 1):
        buf = bytearray(rng.choice(b"\xe8\x00\xff\x13") for _ in range(4000))
        for start in (0, 32768 * 3):
            frame = bytearray(start) + buf
            before = bytes(frame)
            _e8_forward(frame, start, len(buf), e8)
            _e8_reverse(frame, start, len(buf), e8)
            assert bytes(frame) == before


def test_errors():
    data = b"hello hello hello hello, LZX"
    good = compress(data, block_type=1)
    with pytest.raises(LZXError):
        decompress(good[:-2], 15, len(data))           # truncated
    with pytest.raises(LZXError):
        decompress(good + b"\x00\x00", 15, len(data))  # data after the end
    with pytest.raises(LZXError):
        decompress(good, 15, len(data) - 1)            # the block is longer
    with pytest.raises(LZXError):
        decompress(good, 15, len(data) + 1)
    with pytest.raises(LZXError):
        decompress(bytes(4), 15, 1)                    # block type 0
    with pytest.raises(LZXError):
        bad = bytearray(MS_PATCH_ABC)
        bad[2] |= 1                                    # a padding bit is 1
        decompress(bytes(bad), 15, 3)
    with pytest.raises(LZXError):
        decompress(b"\x00", 15, 0)
    with pytest.raises(ValueError):
        decompress(good, 22, len(data))
    with pytest.raises(ValueError):
        compress(data, window_bits=14)
    assert decompress(b"", 15, 0) == b"" and compress(b"") == b""
