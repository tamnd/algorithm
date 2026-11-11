# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lzma/. The authors are listed in prov/KBKFC6.jsonl.
# The oracle is the lzma module of the Python standard library (liblzma),
# used here only. Our module has the same name, so the test loads the
# standard library file by its path.

import importlib.util
import os
import random
import sysconfig

import pytest

from lzma import LZMAError, compress, decompress, parse_properties

_spec = importlib.util.spec_from_file_location(
    "stdlib_lzma", os.path.join(sysconfig.get_path("stdlib"), "lzma.py"))
std = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(std)


def _inputs():
    rng = random.Random(7)
    words = [b"range", b"coder", b"literal", b"state", b"rep0", b"match", b"Pavlov"]
    return [
        b"",
        b"a",
        b"\x00" * 1000,
        b"r" * 100000,
        bytes(rng.randrange(256) for _ in range(6000)),
        b" ".join(rng.choice(words) for _ in range(3000)),
        bytes(rng.choice(b"ab") for _ in range(3000)),
    ]


def _std_alone(data, **lzma1):
    filt = {"id": std.FILTER_LZMA1, "preset": 6}
    filt.update(lzma1)
    return std.compress(data, format=std.FORMAT_ALONE, filters=[filt])


def test_we_read_liblzma():
    for data in _inputs():
        assert decompress(std.compress(data, format=std.FORMAT_ALONE)) == data


@pytest.mark.parametrize("lc,lp,pb", [(0, 0, 0), (0, 2, 0), (4, 0, 4), (1, 3, 1), (3, 0, 2)])
def test_we_read_liblzma_properties(lc, lp, pb):
    rng = random.Random(lc * 100 + lp * 10 + pb)
    data = b"".join(rng.choice([b"abcd", b"0123", b"\x00\x01\x02\x03", b"xyz"]) for _ in range(2000))
    stream = _std_alone(data, lc=lc, lp=lp, pb=pb, dict_size=1 << 16)
    assert parse_properties(stream[0]) == (lc, lp, pb)
    assert decompress(stream) == data


def test_liblzma_reads_ours():
    for data in _inputs():
        ours = compress(data)
        assert std.decompress(ours, format=std.FORMAT_ALONE) == data
        assert decompress(ours) == data
        marked = compress(data, end_marker=True)
        assert std.decompress(marked, format=std.FORMAT_ALONE) == data
        assert decompress(marked) == data


@pytest.mark.parametrize("lc,lp,pb", [(0, 0, 0), (0, 4, 0), (4, 0, 4), (2, 2, 3)])
def test_liblzma_reads_ours_properties(lc, lp, pb):
    data = b" ".join(str(i * i).encode() for i in range(3000))
    ours = compress(data, lc=lc, lp=lp, pb=pb)
    assert std.decompress(ours, format=std.FORMAT_ALONE) == data


def test_header_fields():
    # lzma-specification.txt, "lzma file format": properties byte
    # (pb * 5 + lp) * 9 + lc, 4-byte dictionary size, 8-byte size.
    c = compress(b"hello", dict_size=1 << 16)
    assert c[0] == 0x5D                      # lc = 3, lp = 0, pb = 2
    assert c[1:5] == (1 << 16).to_bytes(4, "little")
    assert c[5:13] == (5).to_bytes(8, "little")
    assert c[13] == 0                        # the range coder writes 0 first
    assert parse_properties(0x5D) == (3, 0, 2)
    m = compress(b"hello", end_marker=True)
    assert m[5:13] == b"\xff" * 8


def test_page_example():
    # The example on the page: 13-byte header, then 19 range coder bytes.
    want = bytes.fromhex("5d00001000120000000000000000"
                         "391948affe998b0dbb42175638772868e000")
    assert compress(b"red fish, red dish") == want
    assert std.decompress(want, format=std.FORMAT_ALONE) == b"red fish, red dish"


def test_errors():
    good = compress(b"an example of an example of an example")
    with pytest.raises(LZMAError):
        decompress(bytes([225]) + good[1:])          # properties byte >= 225
    with pytest.raises(LZMAError):
        decompress(good[:13] + b"\x01" + good[14:])  # first range byte not 0
    with pytest.raises(LZMAError):
        decompress(good[:-3])                        # truncated
    longer = good[:5] + (100).to_bytes(8, "little") + good[13:]
    with pytest.raises(LZMAError):
        decompress(longer)                           # size claims 100 bytes
