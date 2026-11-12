# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delta-encoding/. The authors are listed in prov/MHQMGE.jsonl.

# Oracles: the worked examples of the page, the zigzag and varint examples of
# the Protocol Buffers encoding guide, an independent prefix-sum oracle
# (itertools.accumulate), and round trips of the byte delta.

import itertools
import random

from delta_encoding import (
    copy_add_decode,
    copy_add_encode,
    d_gaps,
    decode_int_sequence,
    delta_decode,
    delta_encode,
    encode_int_sequence,
    varint_decode_all,
    varint_encode,
    zigzag_decode,
    zigzag_encode,
)


def test_worked_examples() -> None:
    temps = [1000, 1002, 1003, 1003, 1001, 998, 1000]
    assert delta_encode(temps) == [1000, 2, 1, 0, -2, -3, 2]
    assert delta_decode([1000, 2, 1, 0, -2, -3, 2]) == temps
    assert d_gaps([3, 7, 11, 23, 29, 30]) == [3, 4, 4, 12, 6, 1]
    ramp = [5, 8, 11, 14, 17]
    assert delta_encode(ramp) == [5, 3, 3, 3, 3]
    assert delta_encode(ramp, order=2) == [5, -2, 0, 0, 0]
    squares = [i * i for i in range(8)]
    assert delta_encode(squares, order=3)[3:] == [0] * 5


def test_edges() -> None:
    assert delta_encode([]) == [] and delta_decode([]) == []
    assert delta_encode([7]) == [7]
    assert delta_encode([4] * 5) == [4, 0, 0, 0, 0]


def test_against_accumulate() -> None:
    rng = random.Random(3284)
    for _ in range(300):
        x = [rng.randrange(-10**6, 10**6) for _ in range(rng.randrange(0, 50))]
        for order in (1, 2, 3):
            d = delta_encode(x, order)
            y = d
            for _ in range(order):
                y = list(itertools.accumulate(y))
            assert y == x
            assert delta_decode(d, order) == x


def test_zigzag_protobuf() -> None:
    pairs = [(0, 0), (-1, 1), (1, 2), (-2, 3), (2147483647, 4294967294), (-2147483648, 4294967295)]
    for v, u in pairs:
        assert zigzag_encode(v) == u
        assert zigzag_decode(u) == v
    for v in range(-1000, 1000):
        assert zigzag_decode(zigzag_encode(v)) == v


def test_varint_protobuf() -> None:
    assert varint_encode(1) == b"\x01"
    assert varint_encode(150) == b"\x96\x01"
    assert varint_encode(0) == b"\x00"
    assert varint_decode_all(b"\x96\x01\x01") == [150, 1]


def test_int_sequence_round_trip() -> None:
    rng = random.Random(7)
    x = [0]
    for _ in range(2000):
        x.append(x[-1] + rng.randrange(-5, 6))
    data = encode_int_sequence(x)
    assert decode_int_sequence(data) == x
    assert len(data) < 2 * len(x)  # small deltas take one byte each
    assert decode_int_sequence(encode_int_sequence([])) == []


def test_copy_add_round_trips() -> None:
    rng = random.Random(1996)
    base = bytes(rng.randrange(256) for _ in range(3000))
    edited = base[:1000] + b"inserted text" + base[1000:2000] + base[2500:] + b"z" * 100
    cases = [
        (b"", b""),
        (b"abc", b""),
        (b"", b"a"),
        (b"", b"\x00" * 500),
        (b"", b"abcabcabcabcabcabc"),
        (b"hello world", b"hello, world"),
        (base, edited),
        (base, bytes(rng.randrange(256) for _ in range(500))),
        (b"the quick brown fox " * 20, b"the quick red fox " * 20),
    ]
    for _ in range(100):
        s = bytes(rng.choice(b"ab") for _ in range(rng.randrange(0, 40)))
        t = bytes(rng.choice(b"ab") for _ in range(rng.randrange(0, 40)))
        cases.append((s, t))
    for s, t in cases:
        ins = copy_add_encode(s, t)
        assert copy_add_decode(s, ins) == t


def test_copy_add_finds_shared_data() -> None:
    rng = random.Random(5)
    base = bytes(rng.randrange(256) for _ in range(3000))
    edited = base[:1000] + b"inserted text" + base[1000:]
    ins = copy_add_encode(base, edited)
    assert [i[0] for i in ins] == ["COPY", "ADD", "COPY"]
    assert ins[1] == ("ADD", b"inserted text")


def test_overlapping_copy() -> None:
    # T = "abcabcabcabc" with no source: one ADD of "abc", then a COPY of 9
    # bytes from address 0 of T, which overlaps the bytes it writes.
    ins = copy_add_encode(b"", b"abcabcabcabc", block=3)
    assert ins == [("ADD", b"abc"), ("COPY", 9, 0)]
    assert copy_add_decode(b"", ins) == b"abcabcabcabc"
