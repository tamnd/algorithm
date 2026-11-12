# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/run-length-encoding/. The authors are listed in prov/SEKR0Q.jsonl.

# Oracles: the worked example of the page, an independent run splitter
# (itertools.groupby), the PackBits example of Apple Technical Note TN1023,
# and round trips of every format.

import itertools
import random

from run_length_encoding import (
    packbits_decode,
    packbits_encode,
    pairs_decode,
    pairs_encode,
    rle1_decode,
    rle1_encode,
    rle_decode,
    rle_encode,
)


def cases() -> list[bytes]:
    rng = random.Random(1966)
    out = [
        b"",
        b"A",
        b"\x00" * 1000,
        b"AB" * 300,
        b"A" * 3 + b"B" * 4 + b"C" * 255 + b"D" * 256 + b"E" * 259 + b"F" * 1000,
        bytes(rng.randrange(256) for _ in range(4000)),
        bytes(rng.choice(b"ab") for _ in range(4000)),
        b"the quick brown fox jumps over the lazy dog " * 40,
    ]
    for _ in range(200):
        k = rng.randrange(0, 60)
        out.append(b"".join(bytes((rng.choice(b"xyz"),)) * rng.randrange(1, 9) for _ in range(k)))
    return out


def test_worked_example() -> None:
    assert rle_encode("WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW") == [
        ("W", 12),
        ("B", 1),
        ("W", 12),
        ("B", 3),
        ("W", 24),
        ("B", 1),
        ("W", 14),
    ]
    assert rle_encode("") == []
    assert rle_encode("a") == [("a", 1)]
    assert rle_encode("aaaa") == [("a", 4)]


def test_against_groupby() -> None:
    for data in cases():
        assert rle_encode(data) == [(k, len(list(g))) for k, g in itertools.groupby(data)]
        assert bytes(rle_decode(rle_encode(data))) == data


def test_canonical_form() -> None:
    for data in cases():
        pairs = rle_encode(data)
        assert all(c >= 1 for _, c in pairs)
        assert all(a != b for (a, _), (b, _) in zip(pairs, pairs[1:]))


def test_pairs_round_trip() -> None:
    for data in cases():
        assert pairs_decode(pairs_encode(data)) == data
    assert pairs_encode(b"\x07" * 600) == bytes((255, 7, 255, 7, 90, 7))


def test_packbits_tn1023() -> None:
    unpacked = bytes.fromhex("AAAAAA80002AAAAAAAAA80002A22AAAAAAAAAAAAAAAAAAAA")
    packed = bytes.fromhex("FEAA0280002AFDAA0380002A22F7AA")
    assert len(unpacked) == 24 and len(packed) == 15
    assert packbits_encode(unpacked) == packed
    assert packbits_decode(packed) == unpacked


def test_packbits_round_trip_and_bound() -> None:
    for data in cases():
        enc = packbits_encode(data)
        assert packbits_decode(enc) == data
        # Literal packets add one header byte per 128 bytes at most.
        assert len(enc) <= len(data) + (len(data) + 127) // 128
    assert packbits_decode(b"\x80") == b""  # -128 is a no-op


def test_rle1() -> None:
    assert rle1_encode(b"AAAA") == b"AAAA\x00"
    assert rle1_encode(b"AAAAAAA") == b"AAAA\x03"
    assert rle1_encode(b"AAA") == b"AAA"
    assert rle1_encode(b"A" * 255) == b"AAAA\xfb"
    assert rle1_encode(b"A" * 256) == b"AAAA\xfbA"
    for data in cases():
        assert rle1_decode(rle1_encode(data)) == data
