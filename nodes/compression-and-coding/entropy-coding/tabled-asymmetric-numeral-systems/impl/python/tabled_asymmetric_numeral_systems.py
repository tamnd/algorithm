# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tabled-asymmetric-numeral-systems/. The authors are listed in prov/8ATQ56.jsonl.

"""Tabled ANS as in FSE and in Zstandard (RFC 8878, Section 4.1).

A table has L = 2^R states. A normalized distribution gives each symbol s a
count norm[s] >= 1, or -1 for a symbol with probability "less than 1", which
gets one cell at the end of the table. The counts and the -1 cells sum to L.
The table is built by the spread rule of RFC 8878 Section 4.1.1. Each cell u
of the decoding table holds a symbol, a number of bits nb and a baseline: the
next state is baseline + the next nb bits. The encoding table lists, for each
symbol, its cells in increasing order.

The bitstream is written forward, closed with a 1 bit, and read backward, as
in Zstandard. The encoder starts with a cell of the last symbol, so that the
decoder does not update the state after the last symbol.

Cost: O(L + k) to build the tables for k symbols, O(1) per symbol to code.
"""

import heapq
import math


def build_tables(norm: list[int], r: int) -> tuple[list[tuple[int, int, int]], list[list[int]]]:
    """Return the decoding table [(symbol, nb, baseline)] and the encoding table states[s]."""
    size = 1 << r
    if r < 4:
        raise ValueError("the spread step is odd only for r >= 4")
    if sum(c if c > 0 else 1 for c in norm if c != 0) != size:
        raise ValueError("the distribution does not fill the table")
    sym = [-1] * size
    high = size - 1  # @line L1
    for s, c in enumerate(norm):
        if c == -1:  # @line L2
            sym[high] = s
            high -= 1
    step = (size >> 1) + (size >> 3) + 3  # @line L3
    mask = size - 1
    pos = 0
    for s, c in enumerate(norm):
        for _ in range(max(c, 0)):  # @line L4
            sym[pos] = s  # @line L5
            pos = (pos + step) & mask  # @line L6
            while pos > high:
                pos = (pos + step) & mask
    if pos != 0:
        raise ValueError("the spread did not end at position 0")
    nxt = [max(c, 1) for c in norm]  # @line L7
    dtable: list[tuple[int, int, int]] = []
    states: list[list[int]] = [[] for _ in norm]
    for u in range(size):  # @line L8
        s = sym[u]
        t = nxt[s]  # @line L9
        nxt[s] += 1
        nb = r - (t.bit_length() - 1)  # @line L10
        dtable.append((s, nb, (t << nb) - size))
        states[s].append(u)  # @line L11
    return dtable, states


class _BitWriter:
    def __init__(self) -> None:
        self.acc = 0
        self.pos = 0

    def write(self, value: int, nb: int) -> None:
        self.acc |= (value & ((1 << nb) - 1)) << self.pos
        self.pos += nb

    def close(self) -> bytes:
        self.acc |= 1 << self.pos  # the end mark
        self.pos += 1
        return self.acc.to_bytes((self.pos + 7) // 8, "little")


class _BackwardReader:
    def __init__(self, data: bytes) -> None:
        if not data or data[-1] == 0:
            raise ValueError("the stream has no end mark")
        self.acc = int.from_bytes(data, "little")
        self.pos = self.acc.bit_length() - 1  # skip the padding and the end mark

    def read(self, nb: int) -> int:
        if nb > self.pos:
            raise ValueError("the stream is too short")
        self.pos -= nb
        return (self.acc >> self.pos) & ((1 << nb) - 1)


def encode(data: list[int], norm: list[int], r: int) -> bytes:
    _, states = build_tables(norm, r)
    size = 1 << r
    for s in data:
        if norm[s] == 0:
            raise ValueError("a symbol with probability 0")
    w = _BitWriter()
    if not data:
        return w.close()
    u = states[data[-1]][0]  # @line L12
    for i in range(len(data) - 2, -1, -1):  # @line L13
        s = data[i]
        f = max(norm[s], 1)  # @line L14
        x = size + u
        # The k with f <= x >> k < 2f, in O(1): match the bit lengths, then fix by 1.
        k = x.bit_length() - f.bit_length()  # @line L15
        if (x >> k) < f:
            k -= 1
        w.write(x, k)  # @line L16
        u = states[s][(x >> k) - f]
    w.write(u, r)  # @line L17
    return w.close()


def decode(code: bytes, n: int, norm: list[int], r: int) -> list[int]:
    dtable, _ = build_tables(norm, r)
    rd = _BackwardReader(code)
    if n == 0:
        if rd.pos != 0:
            raise ValueError("extra bits")
        return []
    u = rd.read(r)  # @line L18
    out = []
    for i in range(n):  # @line L19
        s, nb, base = dtable[u]
        out.append(s)  # @line L20
        if i < n - 1:
            u = base + rd.read(nb)  # @line L21
    if rd.pos != 0:  # @line L22
        raise ValueError("the stream has bits left over")
    return out


def normalize(counts: list[int], r: int) -> list[int]:
    """Scale counts to a sum of 2^r with each present symbol at least 1 (no -1 cells)."""
    size = 1 << r
    n = sum(counts)
    if n == 0 or sum(1 for c in counts if c) > size:
        raise ValueError("cannot normalize")
    norm = [max(1, round(size * c / n)) if c else 0 for c in counts]
    total = sum(norm)
    if total < size:
        norm[max(range(len(counts)), key=lambda t: counts[t])] += size - total
    heap = [(-f, s) for s, f in enumerate(norm) if f > 1]
    heapq.heapify(heap)
    while total > size:
        _, s = heapq.heappop(heap)
        norm[s] -= 1
        total -= 1
        if norm[s] > 1:
            heapq.heappush(heap, (-norm[s], s))
    return norm


def model_cost(data: list[int], norm: list[int], r: int) -> float:
    """The sum of lg(L / f_s) over the data: the ideal length under the table's distribution."""
    return sum(r - math.log2(max(norm[s], 1)) for s in data)


# The predefined distribution of literals length codes, RFC 8878 Section 3.1.1.3.2.2, accuracy log 6.
LL_DEFAULT_NORM = [4, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1,
                   2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 1, 1, 1, 1, 1,
                   -1, -1, -1, -1]
LL_DEFAULT_ACCURACY_LOG = 6
