# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/front-coding/. The authors are listed in prov/NH530P.jsonl.
"""Blocked front coding of a list of strings.

The list is cut into blocks of k strings. The first string of a block is
written in full, as its length and its bytes. Each other string is written
as the length of the prefix it shares with the string before it, the length
of the rest, and the bytes of the rest. Lengths are variable byte numbers,
and the output starts with the number of strings.
"""


def lcp(a: bytes, b: bytes) -> int:
    """Return the length of the longest common prefix of a and b. Cost O(min(|a|, |b|))."""
    n = min(len(a), len(b))
    i = 0
    while i < n and a[i] == b[i]:
        i += 1
    return i


def write_number(x: int, out: bytearray) -> None:
    """Append x >= 0 as a variable byte number: 7 bits per byte, the high bit set on the last byte."""
    while x >= 128:
        out.append(x & 127)
        x >>= 7
    out.append(x | 128)


def read_number(data: bytes, pos: int) -> tuple[int, int]:
    """Read a variable byte number at pos. Return it and the position after it."""
    x, shift = 0, 0
    while True:
        b = data[pos]
        pos += 1
        x |= (b & 127) << shift
        if b & 128:
            return x, pos
        shift += 7


def encode(terms: list[str], k: int = 4) -> bytes:
    """Front code the strings with blocks of k. Any list works; a sorted list compresses well.

    Precondition: k >= 1. Cost O(total length of the strings).
    """
    if k < 1:
        raise ValueError("k must be at least 1")
    out = bytearray()  # @line L1
    write_number(len(terms), out)
    prev = b""
    for i, t in enumerate(terms):  # @line L2
        s = t.encode()
        if i % k == 0:  # @line L3
            p = 0
        else:
            p = lcp(prev, s)  # @line L4
            write_number(p, out)  # @line L5
        write_number(len(s) - p, out)  # @line L6
        out += s[p:]
        prev = s
    return bytes(out)  # @line L7


def decode(data: bytes, k: int = 4) -> list[str]:
    """Return the list of strings that encode(terms, k) wrote into data. Cost O(|data| + total length)."""
    terms: list[bytes] = []
    n, pos = read_number(data, 0)
    prev = b""
    for i in range(n):
        p = 0
        if i % k != 0:
            p, pos = read_number(data, pos)
        r, pos = read_number(data, pos)
        s = prev[:p] + data[pos : pos + r]
        pos += r
        terms.append(s)
        prev = s
    if pos != len(data):
        raise ValueError("bad data")
    return [s.decode() for s in terms]
