# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arithmetic-coding/. The authors are listed in prov/GC5V3X.jsonl.

"""The integer arithmetic coder of Witten, Neal and Cleary (CACM, 1987).

The coder keeps two b-bit registers low and high (b = 32 here), and a count
of pending bits for the middle-half (E3) scaling. The model is adaptive: it
starts with a count of 1 for each symbol, adds 1 after each coded symbol, and
halves all counts when the total reaches MAX_TOTAL. The encoder and the
decoder run the same model, so the decoder needs no table.

The message length n is passed to the decoder instead of an end-of-file
symbol. Cost: O(n * sigma) time with the linear cumulative-count search
of this simple model, and O(sigma) space for the model.
"""

import math

CODE_BITS = 32
TOP = (1 << CODE_BITS) - 1
QTR = 1 << (CODE_BITS - 2)
HALF = 2 * QTR
THREE_QTR = 3 * QTR
MAX_TOTAL = (1 << 16) - 1  # at most 2^(CODE_BITS - 2), so each symbol keeps a non-empty range


class AdaptiveModel:
    """Counts for the symbols 0 .. sigma - 1, each count at least 1."""

    def __init__(self, sigma: int) -> None:
        if sigma < 1 or sigma > MAX_TOTAL:
            raise ValueError("bad alphabet size")
        self.freq = [1] * sigma
        self.total = sigma

    def interval(self, s: int) -> tuple[int, int, int]:
        """Return (c_lo, c_hi, total): the counts of the symbols below s, up to and with s."""
        c_lo = sum(self.freq[:s])
        return c_lo, c_lo + self.freq[s], self.total

    def find(self, t: int) -> int:
        """Return the symbol s with c_lo(s) <= t < c_hi(s)."""
        c = 0
        for s, f in enumerate(self.freq):
            c += f
            if t < c:
                return s
        raise ValueError("target out of range")

    def update(self, s: int) -> None:
        self.freq[s] += 1
        self.total += 1
        if self.total >= MAX_TOTAL:
            self.freq = [(f + 1) // 2 for f in self.freq]
            self.total = sum(self.freq)


class _BitWriter:
    def __init__(self) -> None:
        self.bits: list[int] = []
        self.pending = 0

    def emit(self, bit: int) -> None:
        self.bits.append(bit)  # @line L16
        self.bits.extend([1 - bit] * self.pending)
        self.pending = 0


def encode(symbols: list[int], sigma: int) -> tuple[bytes, int]:
    """Encode symbols from 0 .. sigma - 1. Return (code bytes, number of code bits).

    The bit string is padded with zero bits to whole bytes.
    """
    model = AdaptiveModel(sigma)
    out = _BitWriter()
    low, high = 0, TOP  # @line L1
    for s in symbols:  # @line L2
        c_lo, c_hi, total = model.interval(s)  # @line L3
        r = high - low + 1  # @line L4
        high = low + (r * c_hi) // total - 1  # @line L5
        low = low + (r * c_lo) // total  # @line L6
        while True:  # @line L7
            if high < HALF:  # @line L8
                out.emit(0)
            elif low >= HALF:  # @line L9
                out.emit(1)
                low -= HALF
                high -= HALF
            elif low >= QTR and high < THREE_QTR:  # @line L10
                out.pending += 1
                low -= QTR
                high -= QTR
            else:
                break  # @line L11
            low = 2 * low  # @line L12
            high = 2 * high + 1
        model.update(s)  # @line L13
    out.pending += 1  # @line L14
    out.emit(0 if low < QTR else 1)  # @line L15
    bits = out.bits
    nbits = len(bits)
    bits = bits + [0] * (-nbits % 8)
    data = bytes(int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8))
    return data, nbits


def decode(data: bytes, n: int, sigma: int) -> list[int]:
    """Decode n symbols from data. Bits past the end of data read as 0."""
    bits = [(byte >> (7 - k)) & 1 for byte in data for k in range(8)]
    pos = 0

    def next_bit() -> int:
        nonlocal pos
        b = bits[pos] if pos < len(bits) else 0
        pos += 1
        return b

    model = AdaptiveModel(sigma)
    low, high, value = 0, TOP, 0  # @line L17
    for _ in range(CODE_BITS):
        value = 2 * value + next_bit()
    out = []
    for _ in range(n):  # @line L18
        r = high - low + 1  # @line L19
        t = ((value - low + 1) * model.total - 1) // r  # @line L20
        s = model.find(t)  # @line L21
        c_lo, c_hi, total = model.interval(s)
        high = low + (r * c_hi) // total - 1  # @line L22
        low = low + (r * c_lo) // total
        while True:  # @line L23
            if high < HALF:
                pass
            elif low >= HALF:
                low -= HALF
                high -= HALF
                value -= HALF
            elif low >= QTR and high < THREE_QTR:
                low -= QTR
                high -= QTR
                value -= QTR
            else:
                break
            low = 2 * low  # @line L24
            high = 2 * high + 1
            value = 2 * value + next_bit()
        model.update(s)  # @line L25
        out.append(s)
    return out


def ideal_length(symbols: list[int], sigma: int) -> float:
    """The sum of -lg p over the message, with p the probability the model gives at each step."""
    model = AdaptiveModel(sigma)
    bits = 0.0
    for s in symbols:
        c_lo, c_hi, total = model.interval(s)
        bits -= math.log2((c_hi - c_lo) / total)
        model.update(s)
    return bits


def length_bound(symbols: list[int], sigma: int) -> float:
    """The proven bound on the code bits: ideal + 2 + n * (-lg(1 - MAX_TOTAL / QTR))."""
    eps = -math.log2(1 - MAX_TOTAL / QTR)
    return ideal_length(symbols, sigma) + 2 + len(symbols) * eps
