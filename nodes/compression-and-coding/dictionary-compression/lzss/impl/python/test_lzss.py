# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lzss/. The authors are listed in prov/M0JP2V.jsonl.

# There is no standard library codec for LZSS and no official test vector.
# The tests use parses and bit counts worked out by hand, round trips, and the
# rule that a pair is used only when it is shorter than the literals.

import random

import pytest

from lzss import lzss_decode, lzss_encode, lzss_tokens, lzss_untokens, min_match


def test_min_match() -> None:
    assert min_match(12, 4) == 2  # 17 bits < 2 * 9 bits
    assert min_match(16, 8) == 3  # 25 bits < 3 * 9, but not < 2 * 9
    assert min_match(4, 3) == 1  # 8 bits < 9 bits


def test_hand_examples() -> None:
    a, b, c, d, r = (ord(ch) for ch in "abcdr")
    assert lzss_tokens(b"abracadabra") == [a, b, r, a, c, a, d, (7, 4)]
    assert lzss_tokens(b"aaaaaaaa") == [a, (1, 7)]
    assert lzss_tokens(b"abababab") == [a, b, (2, 6)]
    # 7 literals of 9 bits and one pair of 17 bits: 80 bits, 10 bytes.
    assert len(lzss_encode(b"abracadabra")) == 10
    # 0 01100001 | 1 000000000000 0101 | 000000: 9 + 17 = 26 bits, padded to 4 bytes.
    assert lzss_encode(b"aaaaaaaa") == bytes([0x30, 0xC0, 0x01, 0x40])


def test_short_final_pair() -> None:
    # With 4 offset bits and 3 length bits a pair has 8 bits and m = 1. Eight
    # literals and one pair fill exactly 80 bits, so the last token is a pair
    # of fewer than 9 bits with no padding after it.
    data = b"abcdefghh"
    assert lzss_tokens(data, 4, 3)[-1] == (1, 1)
    blob = lzss_encode(data, 4, 3)
    assert len(blob) == 10
    assert lzss_decode(blob, 4, 3) == data


def test_short_match_stays_literal() -> None:
    # With 16 offset bits and 8 length bits, m = 3: the two-byte repeat "ab" stays literal.
    toks = lzss_tokens(b"abxab", offset_bits=16, length_bits=8)
    assert toks == list(b"abxab")
    assert lzss_tokens(b"abcxabc", offset_bits=16, length_bits=8)[-1] == (4, 3)


def test_bad_distance() -> None:
    with pytest.raises(ValueError):
        lzss_untokens([97, (2, 3)])


@pytest.mark.parametrize("seed", [11, 12])
def test_round_trip(seed: int) -> None:
    rng = random.Random(seed)
    words = [b"lorem ", b"ipsum ", b"dolor ", b"sit ", b"amet\n"]
    cases = [
        b"",
        b"q",
        b"\xff" * 999,
        b"x" * 50 + b"y" * 70 + b"x" * 50,
        bytes(rng.randrange(256) for _ in range(1200)),
        b"".join(rng.choice(words) for _ in range(400)),
    ]
    for data in cases:
        for ob, lb in [(12, 4), (16, 8), (4, 3), (8, 2)]:
            toks = lzss_tokens(data, ob, lb)
            assert lzss_untokens(toks) == data
            assert lzss_decode(lzss_encode(data, ob, lb), ob, lb) == data
            m = min_match(ob, lb)
            for t in toks:
                if isinstance(t, tuple):
                    assert m <= t[1] <= m + (1 << lb) - 1 and 1 <= t[0] <= 1 << ob


def test_never_longer_than_flagged_literals() -> None:
    rng = random.Random(5)
    for _ in range(50):
        data = bytes(rng.choice(b"abc") for _ in range(rng.randrange(200)))
        assert len(lzss_encode(data)) <= (9 * len(data) + 7) // 8
