# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/golomb-coding/. The authors are listed in prov/MNB3EF.jsonl.

"""Golomb code with parameter m >= 1 for the integers x >= 0.

The codeword of x is the quotient q = x // m in unary (q one bits, then a zero
bit), followed by the remainder r = x % m in truncated binary: with
k = floor(log2 m) and u = 2^(k+1) - m, a remainder r < u takes k bits and a
remainder r >= u is written as r + u in k + 1 bits.
"""

from fractions import Fraction
from math import log


class BitWriter:
    """Append bits, most significant bit of each byte first."""

    def __init__(self) -> None:
        self.buf = bytearray()
        self.nbits = 0

    def write_bit(self, bit: int) -> None:
        if self.nbits % 8 == 0:
            self.buf.append(0)
        if bit:
            self.buf[-1] |= 0x80 >> (self.nbits % 8)
        self.nbits += 1

    def write_bits(self, value: int, width: int) -> None:
        for i in range(width - 1, -1, -1):
            self.write_bit((value >> i) & 1)

    def getvalue(self) -> tuple[bytes, int]:
        return bytes(self.buf), self.nbits

    def bits(self) -> str:
        return "".join(str((self.buf[i >> 3] >> (7 - (i & 7))) & 1) for i in range(self.nbits))


class BitReader:
    """Read bits written by BitWriter."""

    def __init__(self, data: bytes, nbits: int | None = None) -> None:
        self.data = data
        self.nbits = len(data) * 8 if nbits is None else nbits
        self.pos = 0

    def read_bit(self) -> int:
        if self.pos >= self.nbits:
            raise EOFError("read past the end of the bit stream")
        bit = (self.data[self.pos >> 3] >> (7 - (self.pos & 7))) & 1
        self.pos += 1
        return bit

    def read_bits(self, width: int) -> int:
        v = 0
        for _ in range(width):
            v = 2 * v + self.read_bit()
        return v

    def at_end(self) -> bool:
        return self.pos >= self.nbits


def truncated_binary_encode(r: int, m: int, w: BitWriter) -> None:
    """Write 0 <= r < m with k or k + 1 bits, k = floor(log2 m)."""
    k = m.bit_length() - 1
    u = (1 << (k + 1)) - m
    if r < u:
        w.write_bits(r, k)
    else:
        w.write_bits(r + u, k + 1)


def truncated_binary_decode(m: int, rd: BitReader) -> int:
    k = m.bit_length() - 1
    u = (1 << (k + 1)) - m
    r = rd.read_bits(k)
    if r >= u:
        r = 2 * r + rd.read_bit() - u
    return r


def golomb_encode(x: int, m: int, w: BitWriter) -> None:
    """Write the Golomb codeword of x >= 0 with parameter m >= 1."""
    if x < 0 or m < 1:
        raise ValueError("need x >= 0 and m >= 1")
    q, r = divmod(x, m)  # @line L1
    for _ in range(q):  # @line L2
        w.write_bit(1)
    w.write_bit(0)
    k = m.bit_length() - 1  # @line L3
    u = (1 << (k + 1)) - m
    if r < u:  # @line L4
        w.write_bits(r, k)
    else:  # @line L5
        w.write_bits(r + u, k + 1)


def golomb_decode(m: int, rd: BitReader) -> int:
    """Read one Golomb codeword with parameter m and return x."""
    q = 0  # @line L6
    while rd.read_bit() == 1:
        q += 1
    k = m.bit_length() - 1  # @line L7
    u = (1 << (k + 1)) - m
    r = rd.read_bits(k)  # @line L8
    if r >= u:  # @line L9
        r = 2 * r + rd.read_bit() - u
    return q * m + r  # @line L10


def golomb_length(x: int, m: int) -> int:
    q, r = divmod(x, m)
    k = m.bit_length() - 1
    return q + 1 + (k if r < (1 << (k + 1)) - m else k + 1)


def optimal_m(theta: float | Fraction) -> int:
    """Gallager and van Voorhis: the smallest m >= 1 with theta^m + theta^(m+1) <= 1,
    for the geometric source P(x) = (1 - theta) theta^x. Pass a Fraction for an
    exact test at the boundary."""
    if not 0 < theta < 1:
        raise ValueError("need 0 < theta < 1")
    m = max(1, int(log(1 + theta) / -log(theta)) - 1)
    while theta**m + theta ** (m + 1) > 1:
        m += 1
    while m > 1 and theta ** (m - 1) + theta**m <= 1:
        m -= 1
    return m


def golomb_codeword(x: int, m: int) -> str:
    w = BitWriter()
    golomb_encode(x, m, w)
    return w.bits()


def encode_all(values: list[int], m: int) -> tuple[bytes, int]:
    w = BitWriter()
    for v in values:
        golomb_encode(v, m, w)
    return w.getvalue()


def decode_all(data: bytes, nbits: int, m: int) -> list[int]:
    rd = BitReader(data, nbits)
    out = []
    while not rd.at_end():
        out.append(golomb_decode(m, rd))
    return out
