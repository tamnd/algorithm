# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rice-coding/. The authors are listed in prov/3VFKPT.jsonl.

"""Rice code with parameter k >= 0 for the integers x >= 0.

This is the Golomb code with m = 2^k. The codeword of x is the quotient
q = x >> k in unary, written as q zero bits ended by a one bit (the FLAC
convention), followed by the k low bits of x.
"""

from math import ceil, log, sqrt

GOLDEN_MINUS_ONE = (sqrt(5) - 1) / 2  # 0.618..., the root of t^2 + t - 1 = 0


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


def rice_encode(x: int, k: int, w: BitWriter) -> None:
    """Write the Rice codeword of x >= 0 with parameter k >= 0."""
    if x < 0 or k < 0:
        raise ValueError("need x >= 0 and k >= 0")
    q = x >> k  # @line L1
    w.write_bits(0, q)  # @line L2
    w.write_bit(1)
    w.write_bits(x, k)  # @line L3


def rice_decode(k: int, r: BitReader) -> int:
    """Read one Rice codeword with parameter k and return x."""
    q = 0  # @line L4
    while r.read_bit() == 0:
        q += 1
    low = r.read_bits(k)  # @line L5
    return (q << k) | low  # @line L6


def rice_length(x: int, k: int) -> int:
    return (x >> k) + 1 + k


def best_k_for_theta(theta: float) -> int:
    """Best k for P(x) = (1 - theta) theta^x: the smallest k >= 0 with
    theta^(2^k) <= (sqrt(5) - 1) / 2."""
    if not 0 < theta < 1:
        raise ValueError("need 0 < theta < 1")
    if theta <= GOLDEN_MINUS_ONE:
        return 0
    return max(0, ceil(log(log(GOLDEN_MINUS_ONE) / log(theta), 2)))


def k_from_mean(mean: float) -> int:
    """Best k for the geometric source with this mean (theta = mean / (1 + mean))."""
    if mean <= 0:
        return 0
    return best_k_for_theta(mean / (1 + mean))


def jpegls_k(count: int, abs_sum: int) -> int:
    """The JPEG-LS rule (ITU-T T.87, LOCO-I): the smallest k with count * 2^k >= abs_sum."""
    k = 0
    while (count << k) < abs_sum:
        k += 1
    return k


def fold(v: int) -> int:
    """Map a signed residual to x >= 0 as FLAC does: v >= 0 -> 2v, v < 0 -> -2v - 1."""
    return 2 * v if v >= 0 else -2 * v - 1


def unfold(x: int) -> int:
    return x >> 1 if x % 2 == 0 else -((x + 1) >> 1)


def rice_codeword(x: int, k: int) -> str:
    w = BitWriter()
    rice_encode(x, k, w)
    return w.bits()


def encode_all(values: list[int], k: int) -> tuple[bytes, int]:
    w = BitWriter()
    for v in values:
        rice_encode(v, k, w)
    return w.getvalue()


def decode_all(data: bytes, nbits: int, k: int) -> list[int]:
    r = BitReader(data, nbits)
    out = []
    while not r.at_end():
        out.append(rice_decode(k, r))
    return out
