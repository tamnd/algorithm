# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lz77/. The authors are listed in prov/380S00.jsonl.

# There is no standard library codec for LZ77 and no official test vector.
# The tests use parses worked out by hand, round trips, and a brute-force
# check of the greedy longest-match rule.

import random

import pytest

from lz77 import lz77_decode, lz77_encode

A, B, C, D, R = (ord(ch) for ch in "abcdr")


def test_hand_examples() -> None:
    assert lz77_encode(b"abracadabra") == [
        (0, 0, A), (0, 0, B), (0, 0, R), (3, 1, C), (2, 1, D), (7, 3, A),
    ]
    # The second triple copies 6 symbols from 1 position back: it overlaps itself.
    assert lz77_encode(b"aaaaaaaa") == [(0, 0, A), (1, 6, A)]
    assert lz77_encode(b"abababab") == [(0, 0, A), (0, 0, B), (2, 5, B)]


def test_window_limits_the_offset() -> None:
    data = b"abcdefgh" + b"xyz" + b"abcdefgh"
    far = lz77_encode(data, window=64)
    near = lz77_encode(data, window=4)
    assert (11, 7, ord("h")) in far
    assert all(d <= 4 for d, _, _ in near)
    assert lz77_decode(far) == data and lz77_decode(near) == data


def test_overlapping_copy_is_decoded_byte_by_byte() -> None:
    assert lz77_decode([(0, 0, A), (0, 0, B), (2, 5, B)]) == b"abababab"
    assert lz77_decode([(0, 0, A), (1, 6, A)]) == b"a" * 8


def test_bad_offset() -> None:
    with pytest.raises(ValueError):
        lz77_decode([(0, 0, A), (3, 2, B)])


def longest_match(data: bytes, i: int, window: int, max_len: int) -> int:
    cap = min(max_len, len(data) - i - 1)
    best = 0
    for j in range(max(0, i - window), i):
        k = 0
        while k < cap and data[j + k] == data[i + k]:
            k += 1
        best = max(best, k)
    return best


def test_greedy_longest_match() -> None:
    rng = random.Random(7)
    for _ in range(200):
        n = rng.randrange(0, 40)
        data = bytes(rng.choice(b"ab") for _ in range(n))
        w, m = rng.randrange(1, 12), rng.randrange(0, 10)
        i = 0
        for d, length, c in lz77_encode(data, window=w, max_len=m):
            assert length == longest_match(data, i, w, m)
            # Also true when the copy overlaps itself (d < length).
            assert length == 0 or data[i - d:i - d + length] == data[i:i + length]
            assert c == data[i + length]
            i += length + 1
        assert i == n


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_round_trip(seed: int) -> None:
    rng = random.Random(seed)
    words = [b"the ", b"cat ", b"sat ", b"on ", b"mat ", b"\n"]
    cases = [
        b"",
        b"x",
        b"\x00" * 1000,
        b"a" * 300 + b"b" * 300 + b"a" * 300,
        bytes(rng.randrange(256) for _ in range(1500)),
        b"".join(rng.choice(words) for _ in range(500)),
        bytes(range(256)) * 4,
    ]
    for data in cases:
        for w, m in [(4096, 255), (16, 8), (1, 1), (100, 0)]:
            triples = lz77_encode(data, window=w, max_len=m)
            assert lz77_decode(triples) == data
            assert all(0 <= d <= w and 0 <= length <= m for d, length, _ in triples)


def test_repetitive_text_needs_few_triples() -> None:
    data = b"abc" * 1000
    assert len(lz77_encode(data, max_len=255)) == 3 + 12
