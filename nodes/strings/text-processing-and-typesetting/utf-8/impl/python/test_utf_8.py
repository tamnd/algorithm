# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/utf-8/. The authors are listed in prov/59B85A.jsonl.

# The oracle is Python's own codec: str.encode("utf-8") and bytes.decode("utf-8").
# Written against Python 3.14, unicodedata.unidata_version 16.0.0. The UTF-8 rules do not
# depend on the Unicode version.

import itertools
import random

from utf_8 import UTF8Error, code_point_start, decode, decode_code_points, encode, encode_code_point, is_valid

BOUNDARY = [0x00, 0x7F, 0x80, 0x8F, 0x90, 0x9F, 0xA0, 0xBF, 0xC0, 0xC1, 0xC2, 0xDF,
            0xE0, 0xED, 0xEF, 0xF0, 0xF4, 0xF5, 0xFF]


def strict_oracle(b: bytes):
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError as e:
        return (e.start, e.end)


def mine_strict(b: bytes):
    try:
        return decode(b, "strict")
    except UTF8Error as e:
        return (e.start, e.end)


def check(b: bytes) -> None:
    assert mine_strict(b) == strict_oracle(b), b.hex(" ")
    assert decode(b) == b.decode("utf-8", "replace"), b.hex(" ")
    assert is_valid(b) == (not isinstance(strict_oracle(b), tuple))


def test_check_values() -> None:
    table = {0x41: "41", 0xE9: "C3 A9", 0x20AC: "E2 82 AC", 0x800: "E0 A0 80", 0xFFFF: "EF BF BF",
             0x10000: "F0 90 80 80", 0x1F600: "F0 9F 98 80", 0x10FFFF: "F4 8F BF BF"}
    for c, h in table.items():
        assert encode_code_point(c) == bytes.fromhex(h)
        assert decode_code_points(bytes.fromhex(h)) == [c]


def test_replacement_check_values() -> None:
    counts = {"ED A0 80": 3, "C0 AF": 2, "F4 90 80 80": 4, "E0 80 80": 3, "F0 9F 98": 1, "E2 82": 1, "80": 1}
    for h, k in counts.items():
        assert decode(bytes.fromhex(h)) == "�" * k
    assert decode(bytes.fromhex("E1 80 41")) == "�A"


def test_encode_boundaries_and_sample() -> None:
    points = [0, 0x7F, 0x80, 0x7FF, 0x800, 0xD7FF, 0xE000, 0xFFFF, 0x10000, 0x10FFFF]
    rng = random.Random(1)
    points += [rng.choice([rng.randrange(0xD800), rng.randrange(0xE000, 0x110000)]) for _ in range(3000)]
    for c in points:
        assert encode_code_point(c) == chr(c).encode("utf-8")
        assert decode(encode_code_point(c)) == chr(c)
    lengths = [len(encode_code_point(c)) for c in (0x7F, 0x80, 0x7FF, 0x800, 0xFFFF, 0x10000)]
    assert lengths == [1, 2, 2, 3, 3, 4]


def test_surrogates_rejected_or_passed() -> None:
    for c in (0xD800, 0xDBFF, 0xDC00, 0xDFFF):
        try:
            encode_code_point(c)
            raise AssertionError("a surrogate must not encode")
        except ValueError:
            pass
        assert encode_code_point(c, allow_surrogates=True) == chr(c).encode("utf-8", "surrogatepass")
        assert not is_valid(chr(c).encode("utf-8", "surrogatepass"))


def test_all_short_sequences_over_boundary_bytes() -> None:
    for k in range(1, 4):
        for t in itertools.product(BOUNDARY, repeat=k):
            check(bytes(t))


def test_all_byte_strings_of_length_at_most_two() -> None:
    for a in range(256):
        check(bytes([a]))
        for b in range(256):
            check(bytes([a, b]))


def test_random_byte_strings() -> None:
    rng = random.Random(2)
    pool = BOUNDARY + list(range(0x20, 0x7F, 7))
    for _ in range(3000):
        check(bytes(rng.choice(pool) for _ in range(rng.randrange(1, 12))))


def test_valid_text_with_one_byte_changed() -> None:
    rng = random.Random(3)
    for _ in range(1000):
        s = "".join(chr(rng.choice([rng.randrange(0x80), rng.randrange(0x80, 0x800), rng.randrange(0xE000, 0x10000),
                                    rng.randrange(0x10000, 0x110000)])) for _ in range(6))
        b = bytearray(encode(s))
        assert bytes(b) == s.encode("utf-8") and decode(bytes(b), "strict") == s
        b[rng.randrange(len(b))] = rng.randrange(256)
        check(bytes(b))


def test_code_point_start() -> None:
    s = "aé€😀"
    b = encode(s)
    starts = [code_point_start(b, i) for i in range(len(b))]
    assert starts == [0, 1, 1, 3, 3, 3, 6, 6, 6, 6]


def test_byte_order_is_code_point_order() -> None:
    rng = random.Random(4)
    for _ in range(2000):
        x = "".join(chr(rng.choice([rng.randrange(0xD800), rng.randrange(0xE000, 0x110000)])) for _ in range(2))
        y = "".join(chr(rng.choice([rng.randrange(0xD800), rng.randrange(0xE000, 0x110000)])) for _ in range(2))
        assert (encode(x) < encode(y)) == ([ord(c) for c in x] < [ord(c) for c in y])
