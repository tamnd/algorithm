# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fletcher-checksum/. The authors are listed in prov/4GV784.jsonl.

import random

from fletcher_checksum import (
    BLOCK16,
    BLOCK32,
    fletcher16,
    fletcher16_check_bytes,
    fletcher32,
    fletcher_plain,
)


def plain16(data: bytes) -> int:
    a, b = fletcher_plain(list(data), 255)
    return (b << 8) | a


def plain32(data: bytes, order: str = "little") -> int:
    if len(data) % 2:
        data += b"\x00"
    a, b = fletcher_plain([int.from_bytes(data[i : i + 2], order) for i in range(0, len(data), 2)], 65535)
    return (b << 16) | a


def test_published_vectors() -> None:
    # Wikipedia, "Fletcher's checksum", Test vectors (16-bit words little-endian for Fletcher-32).
    assert fletcher16(b"abcde") == 0xC8F0
    assert fletcher16(b"abcdef") == 0x2057
    assert fletcher16(b"abcdefgh") == 0x0627
    assert fletcher32(b"abcde") == 0xF04FC729
    assert fletcher32(b"abcdef") == 0x56502D2A
    assert fletcher32(b"abcdefgh") == 0xEBE19591
    # The same values from the plain definition, reduced after every word.
    for s in (b"abcde", b"abcdef", b"abcdefgh"):
        assert plain16(s) == fletcher16(s)
        assert plain32(s) == fletcher32(s)


def test_page_trace() -> None:
    # abcde: A = 97, 195, 39, 139, 240 and B = 97, 37, 76, 215, 200 (mod 255)
    a = b = 0
    trace = []
    for d in b"abcde":
        a = (a + d) % 255
        b = (b + a) % 255
        trace.append((a, b))
    assert trace == [(97, 97), (195, 37), (39, 76), (139, 215), (240, 200)]
    assert fletcher16(b"abcde") == (200 << 8) | 240


def test_edges() -> None:
    assert fletcher16(b"") == 0 and fletcher32(b"") == 0
    assert fletcher16(b"\x00" * 100) == 0
    assert fletcher16(b"\xff" * 100) == 0  # 0xFF counts as 0 mod 255
    assert fletcher32(b"\xff\xff" * 50) == 0
    assert fletcher32(b"\x01") == plain32(b"\x01\x00")


def test_random_against_plain_definition() -> None:
    rng = random.Random(7101)
    for _ in range(600):
        n = rng.randrange(0, 80)
        data = bytes(rng.choice([0, 255, rng.randrange(256)]) for _ in range(n))
        assert fletcher16(data) == plain16(data)
        assert fletcher32(data) == plain32(data)
        assert fletcher32(data, "big") == plain32(data, "big")


def test_worst_case_blocks() -> None:
    # All-0xFF input drives both sums to their largest values; the internal
    # assertion checks that B never passes 2^32 - 1 inside a block.
    long16 = b"\xff" * (3 * BLOCK16 + 17)
    assert fletcher16(long16) == plain16(long16) == 0
    long32 = b"\xff\xfe" * (5 * BLOCK32 + 3)
    assert fletcher32(long32) == plain32(long32)


def test_zero_ff_weakness_exhaustive() -> None:
    # Replacing any byte 0x00 by 0xFF (or back) never changes Fletcher-16.
    rng = random.Random(7102)
    for _ in range(100):
        data = bytearray(rng.choice([0, 255, rng.randrange(256)]) for _ in range(30))
        c = fletcher16(bytes(data))
        for i in range(30):
            if data[i] in (0, 255):
                b = bytearray(data)
                b[i] = 255 - b[i]
                assert fletcher16(bytes(b)) == c


def test_single_byte_errors_other_than_00_ff_detected() -> None:
    rng = random.Random(7103)
    data = bytes(rng.randrange(256) for _ in range(40))
    c = fletcher16(data)
    misses = 0
    for i in range(40):
        for v in range(256):
            if v != data[i]:
                b = bytearray(data)
                b[i] = v
                if fletcher16(bytes(b)) == c:
                    misses += 1
                    assert {data[i], v} == {0, 255}
    assert misses == sum(1 for x in data if x in (0, 255))


def test_swap_misses_match_the_rule() -> None:
    # Swapping bytes x at i and y at j (i < j) changes A by 0 and B by (j - i)(x - y),
    # so it is missed exactly when 255 divides (j - i)(x - y).
    rng = random.Random(7104)
    data = bytes(rng.randrange(256) for _ in range(300))
    c = fletcher16(data)
    count = 0
    for i in range(0, 300, 7):
        for j in range(i + 1, 300):
            b = bytearray(data)
            b[i], b[j] = b[j], b[i]
            missed = fletcher16(bytes(b)) == c
            assert missed == ((j - i) * (data[i] - data[j]) % 255 == 0)
            count += missed
    assert count > 0  # distance 255 swaps and equal bytes are missed


def test_adjacent_swaps_missed_only_for_00_ff() -> None:
    rng = random.Random(7105)
    for _ in range(300):
        data = bytes(rng.choice([0, 255, rng.randrange(256)]) for _ in range(20))
        c = fletcher16(data)
        for i in range(19):
            if data[i] == data[i + 1]:
                continue
            b = bytearray(data)
            b[i], b[i + 1] = b[i + 1], b[i]
            assert (fletcher16(bytes(b)) == c) == ({data[i], data[i + 1]} == {0, 255})


def test_check_bytes() -> None:
    rng = random.Random(7106)
    for _ in range(600):
        data = bytes(rng.randrange(256) for _ in range(rng.randrange(0, 50)))
        cb = fletcher16_check_bytes(data)
        a, b = fletcher_plain(list(data + cb), 255)
        assert a == 0 and b == 0
