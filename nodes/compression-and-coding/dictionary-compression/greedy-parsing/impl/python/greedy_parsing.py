# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-parsing/. The authors are listed in prov/08SJN4.jsonl.

"""Greedy parsing: at each position take the longest phrase that the dictionary allows.

Three dictionaries are covered.

- greedy_parse: LZ77 style copies with literals. A phrase is a literal
  ("L", c) or a copy ("M", length, distance) with min_len <= length and,
  if a window w is given, distance <= w. The source may overlap the phrase.
- greedy_parse_lz77: the original LZ77 phrase, a copy of length 0 or more
  followed by one explicit symbol, written ("T", length, distance, c).
- greedy_parse_static: a fixed set of strings; every phrase is a member.

The match search here is exhaustive, so each step finds a longest phrase.
"""

Phrase = tuple


def longest_match(t: bytes, i: int, window: int | None = None,
                  max_len: int | None = None) -> tuple[int, int]:
    """Longest (length, distance) with the source starting before i; smallest distance on ties."""
    n = len(t)
    cap = n - i if max_len is None else min(max_len, n - i)
    lo = 0 if window is None else max(0, i - window)
    best, dist = 0, 0
    for j in range(i - 1, lo - 1, -1):
        k = 0
        while k < cap and t[j + k] == t[i + k]:
            k += 1
        if k > best:
            best, dist = k, i - j
            if k == cap:
                break
    return best, dist


def greedy_parse(t: bytes, window: int | None = None, min_len: int = 1,
                 max_len: int | None = None) -> list[Phrase]:
    """Greedy parse into literals and copies of length at least min_len."""
    i, out = 0, []  # @line L1
    while i < len(t):  # @line L2
        length, dist = longest_match(t, i, window, max_len)  # @line L3
        if length >= min_len:  # @line L4
            out.append(("M", length, dist))  # @line L5
            i += length
        else:  # @line L6
            out.append(("L", t[i]))  # @line L7
            i += 1
    return out  # @line L8


def greedy_parse_lz77(t: bytes, window: int | None = None) -> list[Phrase]:
    """Greedy LZ77 triples: the longest copy that leaves room for one explicit symbol."""
    i, out = 0, []
    n = len(t)
    while i < n:
        length, dist = longest_match(t, i, window, n - i - 1)
        out.append(("T", length, dist, t[i + length]))
        i += length + 1
    return out


def greedy_parse_static(t: bytes, dictionary: set[bytes]) -> list[bytes] | None:
    """Greedy parse with a static dictionary; None if greedy gets stuck."""
    longest = max((len(w) for w in dictionary), default=0)
    i, out = 0, []
    while i < len(t):
        for k in range(min(longest, len(t) - i), 0, -1):
            if t[i:i + k] in dictionary:
                out.append(t[i:i + k])
                i += k
                break
        else:
            return None
    return out


def decode(phrases: list[Phrase]) -> bytes:
    """Rebuild the text from literals, copies and LZ77 triples."""
    out = bytearray()
    for p in phrases:
        if p[0] == "L":
            out.append(p[1])
            continue
        length, dist = p[1], p[2]
        if length and not 1 <= dist <= len(out):
            raise ValueError("distance out of range")
        for _ in range(length):
            out.append(out[-dist])
        if p[0] == "T":
            out.append(p[3])
    return bytes(out)


def bit_cost(phrases: list[Phrase], literal: int = 9, match=None) -> int:
    """Cost in bits: literal bits per literal, match(length, distance) bits per copy.

    The default copy cost is 1 + gamma(length) + gamma(distance), with the
    Elias gamma code length 2 floor(log2 x) + 1.
    """
    if match is None:
        def match(length: int, dist: int) -> int:
            return 1 + gamma(length) + gamma(dist)
    return sum(literal if p[0] == "L" else match(p[1], p[2]) for p in phrases)


def gamma(x: int) -> int:
    """Length of the Elias gamma code of x >= 1."""
    return 2 * (x.bit_length() - 1) + 1
