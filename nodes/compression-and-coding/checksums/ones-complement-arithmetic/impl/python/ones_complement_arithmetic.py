# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ones-complement-arithmetic/. The authors are listed in prov/RDWD1R.jsonl.

"""Ones' complement addition of 16-bit words on a two's complement machine.

add16 adds with an end-around carry: the carry out of bit 15 is added back
into bit 0. The result is congruent to a + b modulo 2^16 - 1, and it is
0x0000 (+0) only when a = b = 0x0000. The value 0xFFFF is the second zero (-0).

fold reduces a wider accumulator (32, 64 or more bits) to 16 bits by adding
its 16-bit pieces with end-around carries. Each step keeps the value modulo
2^16 - 1.

Cost: add16 and each fold step are O(1). A sum of m words costs O(m) additions
of 16 bits, or O(m / 2) or O(m / 4) wide additions plus an O(1) fold.
"""

MASK16 = 0xFFFF


def add16(a: int, b: int) -> int:
    """Ones' complement sum of two 16-bit words."""
    s = a + b  # @line L1
    s = (s & MASK16) + (s >> 16)  # @line L2
    return s  # @line L3


def neg16(a: int) -> int:
    """Ones' complement negation: flip all 16 bits."""
    return ~a & MASK16


def fold(x: int) -> int:
    """Fold a non-negative accumulator of any width to 16 bits with end-around carries."""
    if x < 0:
        raise ValueError("the accumulator must be non-negative")
    while x >> 16:  # @line L4
        x = (x & MASK16) + (x >> 16)  # @line L5
    return x  # @line L6


def sum16_words(words: list[int]) -> int:
    """Ones' complement sum of 16-bit words, one add16 per word (0 for the empty list)."""
    s = 0
    for w in words:
        s = add16(s, w)
    return s


def words_of(data: bytes, order: str = "big") -> list[int]:
    """Cut data into 16-bit words in the given byte order, padding an odd length with a zero byte."""
    if len(data) % 2:
        data = bytes(data) + b"\x00"
    return [int.from_bytes(data[i : i + 2], order) for i in range(0, len(data), 2)]


def sum_wide(data: bytes, chunk: int = 4) -> int:
    """Ones' complement sum of the 16-bit big-endian words of data, read chunk bytes at a time.

    chunk is 2, 4 or 8. Each chunk is added as one big-endian integer to an
    accumulator with an end-around carry at width 8 * chunk, and the result is
    folded to 16 bits. This is the parallel summation of RFC 1071, Section 2 (C).
    """
    if chunk not in (2, 4, 8):
        raise ValueError("chunk must be 2, 4 or 8 bytes")
    width = 8 * chunk
    mask = (1 << width) - 1
    if len(data) % chunk:
        data = bytes(data) + bytes(chunk - len(data) % chunk)
    acc = 0
    for i in range(0, len(data), chunk):
        acc += int.from_bytes(data[i : i + chunk], "big")
        acc = (acc & mask) + (acc >> width)  # end-around carry at the wide width
    return fold(acc)


def swap16(x: int) -> int:
    """Swap the two bytes of a 16-bit word."""
    return ((x & 0xFF) << 8) | (x >> 8)
