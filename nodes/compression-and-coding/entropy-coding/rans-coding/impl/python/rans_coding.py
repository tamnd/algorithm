# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rans-coding/. The authors are listed in prov/08A5D1.jsonl.

"""Byte-wise rANS with two interleaved states, after rans_byte.h of ryg_rans.

The frequencies f[s] are integers that sum to M = 2^12, and c[s] are their
prefix sums. Each state lies in [L, 256 L) with L = 2^23 between symbols, so
it fits in 32 bits. The encoder works from the last symbol to the first and
writes bytes to the front of the output; the decoder reads them from the front.
Symbol i uses state i mod 2. The frequency table is static: it is built from
the counts of the whole input and must reach the decoder by other means.

Cost: O(1) word operations per symbol and per output byte, plus O(M) to build
the slot table.
"""

import heapq
import math

SCALE_BITS = 12
M = 1 << SCALE_BITS  # the total of the frequencies
L = 1 << 23  # the lower end of the state interval
STATES = 2  # the number of interleaved states


def normalize_frequencies(counts: list[int]) -> list[int]:
    """Scale counts to frequencies that sum to M, with f >= 1 for each symbol that occurs."""
    n = sum(counts)
    if n == 0:
        raise ValueError("no symbols")
    if sum(1 for c in counts if c) > M:
        raise ValueError("too many distinct symbols for M")
    freq = [max(1, round(M * c / n)) if c else 0 for c in counts]  # @line L15
    total = sum(freq)
    if total < M:  # @line L16
        freq[max(range(len(counts)), key=lambda t: counts[t])] += M - total
    # Too much: take 1 at a time from the largest frequency, with a heap.
    heap = [(-f, s) for s, f in enumerate(freq) if f > 1]
    heapq.heapify(heap)
    while total > M:
        f, s = heapq.heappop(heap)
        freq[s] -= 1
        total -= 1
        if freq[s] > 1:
            heapq.heappush(heap, (-freq[s], s))
    return freq


def cumulative(freq: list[int]) -> list[int]:
    cum = [0] * (len(freq) + 1)
    for s, f in enumerate(freq):
        cum[s + 1] = cum[s] + f  # @line L17
    return cum


def slot_table(freq: list[int], cum: list[int]) -> list[int]:
    """sym[slot] is the symbol s with c[s] <= slot < c[s] + f[s]."""
    sym = [0] * M
    for s, f in enumerate(freq):
        for k in range(cum[s], cum[s] + f):
            sym[k] = s
    return sym


def encode_put(x: int, f: int, c: int, out: list[int]) -> int:
    """Code one symbol into the state x; out collects bytes in reverse stream order."""
    x_max = ((L >> SCALE_BITS) << 8) * f  # @line L1
    while x >= x_max:  # @line L2
        out.append(x & 0xFF)
        x >>= 8
    return (x // f << SCALE_BITS) + x % f + c  # @line L3


def encode(data: bytes, freq: list[int]) -> bytes:
    cum = cumulative(freq)
    for b in data:
        if freq[b] == 0:
            raise ValueError("a symbol with frequency 0")
    x = [L] * STATES  # @line L9
    rev: list[int] = []
    for i in range(len(data) - 1, -1, -1):  # @line L10
        s = data[i]
        x[i % STATES] = encode_put(x[i % STATES], freq[s], cum[s], rev)
    for j in range(STATES - 1, -1, -1):  # @line L11
        for shift in (24, 16, 8, 0):
            rev.append((x[j] >> shift) & 0xFF)
    return bytes(reversed(rev))


class _Reader:
    def __init__(self, data: bytes) -> None:
        self.data = data
        self.pos = 0

    def byte(self) -> int:
        if self.pos >= len(self.data):
            raise ValueError("the stream is too short")
        b = self.data[self.pos]
        self.pos += 1
        return b


def decode_get(x: int, freq: list[int], cum: list[int], sym: list[int], rd: _Reader) -> tuple[int, int]:
    slot = x & (M - 1)  # @line L4
    s = sym[slot]  # @line L5
    x = freq[s] * (x >> SCALE_BITS) + slot - cum[s]  # @line L6
    while x < L:  # @line L7
        x = (x << 8) | rd.byte()
    return s, x  # @line L8


def decode(code: bytes, n: int, freq: list[int]) -> bytes:
    cum = cumulative(freq)
    sym = slot_table(freq, cum)
    rd = _Reader(code)
    x = []
    for _ in range(STATES):  # @line L12
        b = [rd.byte() for _ in range(4)]
        x.append(b[0] | b[1] << 8 | b[2] << 16 | b[3] << 24)
    out = bytearray()
    for i in range(n):  # @line L13
        s, x[i % STATES] = decode_get(x[i % STATES], freq, cum, sym, rd)
        out.append(s)
    if any(v != L for v in x) or rd.pos != len(code):  # @line L14
        raise ValueError("the stream does not end in the start states")
    return bytes(out)


def counts_of(data: bytes) -> list[int]:
    counts = [0] * 256
    for b in data:
        counts[b] += 1
    return counts


def empirical_entropy(data: bytes) -> float:
    """H_0 of data in bits per symbol."""
    n = len(data)
    return -sum(c / n * math.log2(c / n) for c in counts_of(data) if c)


def model_cost(data: bytes, freq: list[int]) -> float:
    """The sum of lg(M / f[s]) over data: the ideal length under the quantized table."""
    return sum(SCALE_BITS - math.log2(freq[b]) for b in data)


def length_bound(data: bytes, freq: list[int]) -> float:
    """The bound of the proof on the output length in bits."""
    return model_cost(data, freq) + len(data) * math.log2(1 + 2 ** -11) + 32 * STATES
