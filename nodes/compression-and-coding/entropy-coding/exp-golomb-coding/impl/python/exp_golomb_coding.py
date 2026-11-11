# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exp-golomb-coding/. The authors are listed in prov/GFRAJT.jsonl.

"""Exp-Golomb codes of order k >= 0 for the integers x >= 0.

The codeword of x is formed from y = x + 2^k: floor(log2 y) - k zero bits, then
the binary digits of y. Order 0 is the ue(v) code of H.264 (Section 9.1), and
se(v) maps signed values onto it (Section 9.1.1).
"""


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


def expgolomb_encode(x: int, k: int, w: BitWriter) -> None:
    """Write the order-k exp-Golomb codeword of x >= 0."""
    if x < 0 or k < 0:
        raise ValueError("need x >= 0 and k >= 0")
    y = x + (1 << k)  # @line L1
    n = y.bit_length() - 1  # @line L2
    w.write_bits(0, n - k)  # @line L3
    w.write_bits(y, n + 1)  # @line L4


def expgolomb_decode(k: int, r: BitReader, max_zeros: int = 1 << 16) -> int:
    """Read one order-k exp-Golomb codeword and return x."""
    z = 0  # @line L5
    while r.read_bit() == 0:
        z += 1
        if z > max_zeros:
            raise ValueError("exp-Golomb prefix too long")
    y = 1  # @line L6
    for _ in range(z + k):  # @line L7
        y = 2 * y + r.read_bit()
    return y - (1 << k)  # @line L8


def expgolomb_length(x: int, k: int) -> int:
    n = (x + (1 << k)).bit_length() - 1
    return 2 * n - k + 1


def ue_encode(code_num: int, w: BitWriter) -> None:
    """H.264 ue(v): order-0 exp-Golomb."""
    expgolomb_encode(code_num, 0, w)


def ue_decode(r: BitReader) -> int:
    return expgolomb_decode(0, r)


def se_to_code_num(v: int) -> int:
    """H.264 Table 9-3: 0, 1, -1, 2, -2, ... -> 0, 1, 2, 3, 4, ..."""
    return 2 * v - 1 if v > 0 else -2 * v


def code_num_to_se(c: int) -> int:
    """(-1)^(c+1) * Ceil(c / 2), H.264 Section 9.1.1."""
    half = (c + 1) // 2
    return half if c % 2 == 1 else -half


def se_encode(v: int, w: BitWriter) -> None:
    ue_encode(se_to_code_num(v), w)


def se_decode(r: BitReader) -> int:
    return code_num_to_se(ue_decode(r))


def expgolomb_codeword(x: int, k: int = 0) -> str:
    w = BitWriter()
    expgolomb_encode(x, k, w)
    return w.bits()


def encode_all(values: list[int], k: int) -> tuple[bytes, int]:
    w = BitWriter()
    for v in values:
        expgolomb_encode(v, k, w)
    return w.getvalue()


def decode_all(data: bytes, nbits: int, k: int) -> list[int]:
    r = BitReader(data, nbits)
    out = []
    while not r.at_end():
        out.append(expgolomb_decode(k, r))
    return out
