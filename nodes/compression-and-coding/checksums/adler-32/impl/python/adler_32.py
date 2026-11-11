# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adler-32/. The authors are listed in prov/G06YQ1.jsonl.

"""Adler-32 (RFC 1950, Sections 2.2 and 8.2; Mark Adler).

Two sums over the bytes, both modulo BASE = 65521, the largest prime below
2^16: s1 starts at 1, s2 at 0, and for each byte d

    s1 <- s1 + d,    s2 <- s2 + s1.

The checksum is s2 * 65536 + s1. As in zlib, the reduction is deferred: at most
NMAX = 5552 bytes are added between two reductions, the largest n with
255 n (n + 1) / 2 + (n + 1)(BASE - 1) <= 2^32 - 1, so the sums fit in 32 bits.

adler32_combine gives the checksum of a concatenation from the checksums of
the parts and the length of the second part, as zlib's adler32_combine does.

Cost: Theta(n) additions for n bytes, two reductions per NMAX bytes; combine is O(1).
"""

BASE = 65521
NMAX = 5552
LIMIT = (1 << 32) - 1


def adler32(data: bytes, value: int = 1) -> int:
    """Adler-32 of data, continued from a previous value (1 for a fresh start)."""
    s1 = value & 0xFFFF  # @line L1
    s2 = (value >> 16) & 0xFFFF  # @line L2
    i = 0
    n = len(data)
    while i < n:  # @line L3
        end = min(i + NMAX, n)  # @line L4
        while i < end:  # @line L5
            s1 += data[i]  # @line L6
            s2 += s1  # @line L7
            i += 1
        assert s2 <= LIMIT, "NMAX keeps both sums inside 32 bits"
        s1 %= BASE  # @line L8
        s2 %= BASE  # @line L9
    return (s2 << 16) | s1  # @line L10


def adler32_plain(data: bytes) -> int:
    """The definition of RFC 1950 Section 9, reduced after every byte."""
    s1, s2 = 1, 0
    for d in data:
        s1 = (s1 + d) % BASE
        s2 = (s2 + s1) % BASE
    return (s2 << 16) | s1


def adler32_combine(adler1: int, adler2: int, len2: int) -> int:
    """Adler-32 of A + B from adler1 = Adler-32(A), adler2 = Adler-32(B) and len2 = |B|.

    s1(AB) = s1(A) + s1(B) - 1 and s2(AB) = s2(A) + s2(B) + len2 * (s1(A) - 1), mod BASE.
    """
    if len2 < 0:
        raise ValueError("the length must be non-negative")
    a1, b1 = adler1 & 0xFFFF, adler1 >> 16
    a2, b2 = adler2 & 0xFFFF, adler2 >> 16
    rem = len2 % BASE
    s1 = (a1 + a2 - 1) % BASE
    s2 = (b1 + b2 + rem * (a1 - 1)) % BASE
    return (s2 << 16) | s1
