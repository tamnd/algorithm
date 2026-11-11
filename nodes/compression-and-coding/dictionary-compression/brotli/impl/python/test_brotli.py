# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brotli/. The authors are listed in prov/EH674F.jsonl.
# The oracle is the brotli command line tool (google/brotli), used here
# only, and only if it is installed. The static dictionary is read from
# the installed libbrotlicommon, if there is one, and checked against the
# length and CRC-32 that RFC 7932 Appendix A gives.

import random
import shutil
import subprocess
import zlib
from pathlib import Path

import pytest

from brotli import (DICT_SIZE, DOFFSET, LUT0, LUT1, LUT2, TRANSFORMS,
                    BrotliError, compress, decompress, dictionary_word)


def _static_dictionary():
    exe = shutil.which("brotli")
    dirs = [Path("/usr/lib"), Path("/usr/lib/x86_64-linux-gnu"),
            Path("/usr/lib/aarch64-linux-gnu"), Path("/usr/local/lib")]
    if exe:
        dirs.insert(0, Path(exe).resolve().parent.parent / "lib")
    for d in dirs:
        for p in sorted(d.glob("libbrotlicommon*")) if d.is_dir() else []:
            blob = p.read_bytes()
            i = blob.find(b"timedownlifeleftback")
            word = blob[i:i + DICT_SIZE] if i >= 0 else b""
            if len(word) == DICT_SIZE and zlib.crc32(word) == 0x5136CB04:
                return word
    return None


DICTIONARY = _static_dictionary()
CLI = shutil.which("brotli")
needs_dictionary = pytest.mark.skipif(DICTIONARY is None, reason="no libbrotlicommon")
needs_cli = pytest.mark.skipif(CLI is None, reason="no brotli command")


def _inputs():
    rng = random.Random(7932)
    words = [b"the ", b"window ", b"context ", b"of ", b"and ", b"Brotli "]
    return [
        b"",
        b"a",
        b"\x00" * 1000,
        b"z" * 100000,
        bytes(rng.randrange(256) for _ in range(5000)),
        b"".join(rng.choice(words) for _ in range(8000)),
        bytes(rng.choice(b"ab") for _ in range(3000)),
        b"ab" * 20 + b"cd" * 20 + b"z" * 40000 + b"ab" * 20,
    ]


# google/brotli, tests/testdata/ (copied by hand): file -> (compressed, original).
TESTDATA = {
    "empty.compressed": ("06", b""),
    "empty.compressed.05": ("d101", b""),
    "empty.compressed.16": ("81160058", b""),
    "x.compressed": ("0b00805803", b"X"),
    "x.compressed.01": ("2c00580000085803", b"X"),
    "x.compressed.03": ("a1000000008115080400", b"X"),
    "xyzzy.compressed": ("0b028058797a7a7903", b"Xyzzy"),
    "10x10y.compressed": ("1b130000a4b0b2ea8147028a", b"X" * 10 + b"Y" * 10),
    "64x.compressed": ("1b3f000024b0e2998012", b"X" * 64),
    "quickfox.compressed": (
        "0b158054686520717569636b2062726f776e20666f78206a756d7073206f76657220"
        "746865206c617a7920646f6703", b"The quick brown fox jumps over the lazy dog"),
    "ukkonooa.compressed": (
        "1b760000144aac9b7abde1979d7f8ec282360e9ce09003f78b9e38e6b600abc3caa0"
        "c2da6636dccd808d2e21d76ee3ea4cb8f0d2b8c7c2704d3af0697ea1b84573abc457"
        "1e", b"ukko nooa, ukko nooa oli kunnon mies, kun han meni saunaan, "
              b"pisti laukun naulaan, ukko nooa, ukko nooa oli kunnon mies."),
}

# Output of the brotli 1.2.0 command line tool (brotli -c -q Q), kept as
# fixed data. Each of these streams uses static dictionary words.
WITH_DICTIONARY = [
    ("1f2a0000c4dc46a95e0d0b45712af29c4cfe1c4517a82a5b4956982fbcf174445e94"
     "d5c604b7da8131d5fd87c004", b"The quick brown fox jumps over the lazy dog"),
    ("1f4e004024404a1045601b6c5c47152287ebe35720165e595c2fa92aac2d07",
     b"time down life left back code data show only site city open just "
     b"like free work"),
]


@pytest.mark.parametrize("name", sorted(TESTDATA))
def test_testdata(name):
    hexdata, want = TESTDATA[name]
    assert decompress(bytes.fromhex(hexdata)) == want


def test_rfc_tables():
    # RFC 7932 Section 7.1: lengths and CRC-32 of the context tables.
    assert [len(t) for t in (LUT0, LUT1, LUT2)] == [256] * 3
    assert zlib.crc32(LUT0) == 0x8E91EFB7
    assert zlib.crc32(LUT1) == 0xD01A32F4
    assert zlib.crc32(LUT2) == 0x0DD7A0D6
    # RFC 7932 Appendix B: the 121 transforms as bytes: 648 bytes, CRC-32.
    blob = b"".join(p + b"\0" + bytes([k]) + s + b"\0" for p, k, s in TRANSFORMS)
    assert len(TRANSFORMS) == 121
    assert len(blob) == 648 and zlib.crc32(blob) == 0x3D965F81
    # RFC 7932 Section 8: the dictionary has 122,784 bytes.
    assert DICT_SIZE == 122784 and DOFFSET[4] == 0


def test_transforms():
    fake = bytearray(DICT_SIZE)
    fake[0:4] = b"time"                          # length 4, index 0
    fake[DOFFSET[5]:DOFFSET[5] + 5] = "café".encode()   # length 5, index 0
    want = {0: b"time", 9: b"Time", 44: b"TIME", 3: b"ime", 12: b"tim",
            5: b"time the ", 49: b"timing ", 73: b" the time of the ",
            54: b"", 102: b"\xc2\xa0time"}
    for t, word in want.items():
        assert dictionary_word(fake, 4, t << 10) == word
    assert dictionary_word(fake, 4, 7) == bytes(4)          # index 7
    assert dictionary_word(fake, 5, 44 << 10) == "CAFÉ".encode()
    with pytest.raises(BrotliError):
        dictionary_word(fake, 4, 121 << 10)
    with pytest.raises(BrotliError):
        dictionary_word(fake, 3, 0)


def test_dictionary_needed():
    for hexdata, _ in WITH_DICTIONARY:
        with pytest.raises(BrotliError):
            decompress(bytes.fromhex(hexdata))


@needs_dictionary
def test_dictionary_streams():
    for hexdata, want in WITH_DICTIONARY:
        assert decompress(bytes.fromhex(hexdata), DICTIONARY) == want


def test_round_trip():
    for data in _inputs():
        ours = compress(data)
        assert decompress(ours) == data
        if CLI:
            out = subprocess.run([CLI, "-d", "-c"], input=ours,
                                 capture_output=True, check=True).stdout
            assert out == data                       # the CLI reads ours
    assert compress(b"") == bytes.fromhex("06")     # the same as empty.compressed


def test_page_example():
    want = bytes.fromhex("10010000e4589858681351cd")
    assert compress(b"abcabcabcabcabcabc") == want
    assert decompress(want) == b"abcabcabcabcabcabc"


def test_large_window():
    rng = random.Random(24)
    piece = bytes(rng.randrange(256) for _ in range(20000))
    data = piece * 14                              # 280,000 bytes, 2 meta-blocks
    ours = compress(data)
    assert ours[0] & 1 and len(ours) < len(data) // 8
    assert decompress(ours) == data


def test_metadata_block():
    # ISLAST 0, MNIBBLES 0, MSKIPBYTES 1, MSKIPLEN 3, three skipped bytes,
    # then ISLAST 1, ISLASTEMPTY 1.
    assert decompress(bytes.fromhex("2c01" "616263" "03")) == b""


@needs_cli
@pytest.mark.parametrize("quality", [0, 1, 5, 9, 11])
def test_we_read_the_cli(quality):
    if DICTIONARY is None and quality >= 2:
        pytest.skip("no static dictionary")
    for data in _inputs():
        stream = subprocess.run([CLI, "-c", "-q", str(quality)], input=data,
                                capture_output=True, check=True).stdout
        assert decompress(stream, DICTIONARY) == data


@needs_cli
@pytest.mark.parametrize("lgwin", [10, 16, 17, 18, 24])
def test_window_sizes(lgwin):
    data = b"window " * 3000
    stream = subprocess.run([CLI, "-c", "-q", "1", "-w", str(lgwin)], input=data,
                            capture_output=True, check=True).stdout
    assert decompress(stream, DICTIONARY) == data


def test_errors():
    good = compress(b"hello hello hello hello")
    with pytest.raises(BrotliError):
        decompress(good[:-2])                         # truncated
    with pytest.raises(BrotliError):
        decompress(good + b"\x00")                    # data after the end
    with pytest.raises(BrotliError):
        decompress(bytes([0x11]))                     # window code 0010001
    with pytest.raises(BrotliError):
        decompress(bytes([0x86]))                     # nonzero bits after the end
    with pytest.raises(BrotliError):
        decompress(b"")
    with pytest.raises(BrotliError):
        decompress(bytes.fromhex("3c01" "616263" "03"))   # reserved bit set
