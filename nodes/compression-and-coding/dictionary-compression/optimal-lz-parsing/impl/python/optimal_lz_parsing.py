# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimal-lz-parsing/. The authors are listed in prov/3V4KB0.jsonl.

"""Bit-optimal LZ77 parsing for a cost model.

A phrase at position i is a literal t[i], or a copy (length l, distance d)
with min_len <= l, 1 <= d <= i (d <= window if a window is set), and
t[i - d + k] == t[i + k] for k < l. The source may overlap the phrase.

A cost model gives literal(c) and copy(l, d) in bits. The copy cost must be
non-decreasing in d, so that for each length the smallest distance is best.

- matches(t, i): for each length l, the smallest distance of a copy of
  length at least l (the "maximal" pairs: one pair each time the length grows).
- optimal_parse: right-to-left dynamic program over all (l, smallest d) edges.
- optimal_parse_maximal: the same, but only the edges of Ferragina, Nitto
  and Venturini: for each class of distance cost the longest copy, and for
  each class of length cost below it the longest length. Needs min_len = 1
  and a copy cost non-decreasing in l.
"""


def gamma(x: int) -> int:
    """Length of the Elias gamma code of x >= 1."""
    return 2 * (x.bit_length() - 1) + 1


class GammaModel:
    """A flag bit, then 8 bits for a literal or gamma(l) + gamma(d) for a copy."""

    min_len = 1

    @staticmethod
    def literal(c: int) -> int:
        return 9

    @staticmethod
    def copy(length: int, dist: int) -> int:
        return 1 + gamma(length) + gamma(dist)

    @staticmethod
    def classes(x: int) -> list[tuple[int, int]]:
        """The ranges [2^k, 2^(k+1) - 1] on which gamma is constant, up to x."""
        out, lo = [], 1
        while lo <= x:
            out.append((lo, min(2 * lo - 1, x)))
            lo *= 2
        return out


class FlagModel:
    """Fixed-width fields: a flag bit, then 8 bits, or 4 bits of length and 12 of distance."""

    min_len = 2
    max_len = 17
    window = 4096

    @staticmethod
    def literal(c: int) -> int:
        return 9

    @staticmethod
    def copy(length: int, dist: int) -> int:
        return 17


def matches(t: bytes, i: int, window: int | None = None,
            max_len: int | None = None) -> list[tuple[int, int]]:
    """Pairs (l, d): d is the smallest distance of a copy of length >= l.

    The list has one pair per length from 1 to the longest copy, so the
    caller can read the best distance for each length.
    """
    n = len(t)
    cap = n - i if max_len is None else min(max_len, n - i)
    lo = 0 if window is None else max(0, i - window)
    best, out = 0, []
    for j in range(i - 1, lo - 1, -1):  # nearest source first
        k = 0
        while k < cap and t[j + k] == t[i + k]:
            k += 1
        while best < k:  # lengths best+1 .. k get distance i - j
            best += 1
            out.append((best, i - j))
        if best == cap:
            break
    return out


def optimal_parse(t: bytes, model, window: int | None = None,
                  max_len: int | None = None) -> tuple[int, list]:
    """Return (minimum bits, phrases) over all parses of t."""
    n = len(t)
    if window is None:
        window = getattr(model, "window", None)
    if max_len is None:
        max_len = getattr(model, "max_len", None)
    cost = [0] * (n + 1)  # @line L1
    choice: list = [None] * (n + 1)
    for i in range(n - 1, -1, -1):  # @line L2
        cost[i] = model.literal(t[i]) + cost[i + 1]  # @line L3
        choice[i] = ("L", t[i])
        for length, dist in matches(t, i, window, max_len):  # @line L4
            if length < model.min_len:
                continue
            c = model.copy(length, dist) + cost[i + length]  # @line L5
            if c < cost[i]:
                cost[i], choice[i] = c, ("M", length, dist)  # @line L6
    out, i = [], 0
    while i < n:  # @line L7
        p = choice[i]
        out.append(p)
        i += 1 if p[0] == "L" else p[1]
    return cost[0], out  # @line L8


def optimal_parse_maximal(t: bytes, model, window: int | None = None) -> tuple[int, list]:
    """The same optimum, from the maximal edges only (min_len must be 1)."""
    assert model.min_len == 1
    n = len(t)
    cost = [0] * (n + 1)
    choice: list = [None] * (n + 1)
    for i in range(n - 1, -1, -1):
        cost[i] = model.literal(t[i]) + cost[i + 1]
        choice[i] = ("L", t[i])
        lo = 0 if window is None else max(0, i - window)
        for dlo, dhi in model.classes(i - lo):
            # the longest copy whose distance lies in [dlo, dhi]
            longest, at = 0, 0
            for d in range(dlo, dhi + 1):
                k = 0
                while i + k < n and t[i - d + k] == t[i + k]:
                    k += 1
                if k > longest:
                    longest, at = k, d
            for llo, lhi in model.classes(longest):
                length = lhi  # the longest length in this length class
                c = model.copy(length, at) + cost[i + length]
                if c < cost[i]:
                    cost[i], choice[i] = c, ("M", length, at)
    out, i = [], 0
    while i < n:
        p = choice[i]
        out.append(p)
        i += 1 if p[0] == "L" else p[1]
    return cost[0], out


def greedy_parse(t: bytes, model, window: int | None = None,
                 max_len: int | None = None) -> list:
    """Longest copy (smallest distance on ties) if it reaches min_len, else a literal."""
    if window is None:
        window = getattr(model, "window", None)
    if max_len is None:
        max_len = getattr(model, "max_len", None)
    out, i = [], 0
    while i < len(t):
        m = matches(t, i, window, max_len)
        if m and m[-1][0] >= model.min_len:
            out.append(("M", m[-1][0], m[-1][1]))
            i += m[-1][0]
        else:
            out.append(("L", t[i]))
            i += 1
    return out


def bits(phrases: list, model) -> int:
    return sum(model.literal(p[1]) if p[0] == "L" else model.copy(p[1], p[2]) for p in phrases)


def decode(phrases: list) -> bytes:
    out = bytearray()
    for p in phrases:
        if p[0] == "L":
            out.append(p[1])
        else:
            _, length, dist = p
            if not 1 <= dist <= len(out):
                raise ValueError("distance out of range")
            for _ in range(length):
                out.append(out[-dist])
    return bytes(out)
