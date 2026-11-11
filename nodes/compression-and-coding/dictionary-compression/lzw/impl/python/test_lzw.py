# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lzw/. The authors are listed in prov/2BH6WA.jsonl.

# There is no standard library codec for LZW. The tests use code streams worked
# out by hand (including the KwKwK case), a packed stream worked out by hand,
# the bit count of the code width rule, and round trips.

import random

import pytest

from lzw import lzw_compress, lzw_decode_codes, lzw_decompress, lzw_encode_codes

dec = lzw_decode_codes


def test_hand_examples() -> None:
    # a b r a c a d ab ra; new entries 256 = ab, 257 = br, 258 = ra, ...
    assert lzw_encode_codes(b"abracadabra") == [97, 98, 114, 97, 99, 97, 100, 256, 258]
    # a b ab aba b; the code 258 = aba is sent before the decoder knows it
    assert lzw_encode_codes(b"abababab") == [97, 98, 256, 258, 98]
    # a aa aaa aa; codes 256 and 257 are each used one step after they are made
    assert lzw_encode_codes(b"aaaaaaaa") == [97, 256, 257, 256]


def test_kwkwk_case() -> None:
    # Code 258 arrives when the decoder has entries only up to 257.
    assert dec([97, 98, 256, 258, 98]) == b"abababab"
    # Each new run code is used at once: 256 = aa, 257 = aaa.
    assert dec([97, 256, 257, 256]) == b"aaaaaaaa"
    with pytest.raises(ValueError):
        dec([97, 98, 300])


def test_packed_hand_example() -> None:
    # Code 256 is CLEAR, so the new entries start at 257: ab = 257, ba = 258, aba = 259.
    # Five 9-bit codes 97, 98, 257, 259, 98, least significant bit first: 45 bits, 6 bytes.
    assert lzw_compress(b"abababab") == bytes([0x61, 0xC4, 0x04, 0x1C, 0x28, 0x06])
    assert lzw_decompress(bytes([0x61, 0xC4, 0x04, 0x1C, 0x28, 0x06])) == b"abababab"


def test_code_width_grows_after_code_511() -> None:
    # No byte pair repeats, so each of the 300 codes is a single byte and each adds an entry.
    data = bytes(range(256)) + bytes(range(0, 88, 2))
    assert len(lzw_encode_codes(data)) == 300
    # Codes 1 to 256 are written with 9 bits, codes 257 to 300 with 10 bits.
    assert len(lzw_compress(data)) == (256 * 9 + 44 * 10 + 7) // 8
    assert lzw_decompress(lzw_compress(data)) == data


@pytest.mark.parametrize("seed", [31, 32])
def test_round_trip(seed: int) -> None:
    rng = random.Random(seed)
    words = [b"to ", b"be ", b"or ", b"not ", b"\n"]
    cases = [
        b"",
        b"k",
        b"\x00" * 3000,
        b"a" * 500 + b"b" * 500 + b"a" * 500,
        bytes(rng.randrange(256) for _ in range(3000)),
        b"".join(rng.choice(words) for _ in range(1500)),
    ]
    for data in cases:
        assert lzw_decode_codes(lzw_encode_codes(data)) == data
        for bits in (9, 10, 12, 16):
            assert lzw_decompress(lzw_compress(data, bits), bits) == data


def test_reset_keeps_codes_in_range() -> None:
    # With 9-bit codes the table fills after 255 new entries and is reset with CLEAR.
    rng = random.Random(4)
    data = bytes(rng.randrange(256) for _ in range(4000))
    blob = lzw_compress(data, 9)
    assert len(blob) * 8 < 9 * len(data) + 9 * (len(data) // 255 + 2)
    assert lzw_decompress(blob, 9) == data
