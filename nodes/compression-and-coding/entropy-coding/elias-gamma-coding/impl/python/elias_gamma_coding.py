# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elias-gamma-coding/. The authors are listed in prov/6VVNKC.jsonl.

"""Elias gamma code for the integers x >= 1.

The codeword of x is floor(log2 x) zero bits and then the binary digits of x,
most significant first. Its length is 2 floor(log2 x) + 1 bits. To code 0,
code x + 1 instead (gamma0_encode and gamma0_decode do this).
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

    def at_end(self) -> bool:
        return self.pos >= self.nbits


def gamma_encode(x: int, w: BitWriter) -> None:
    """Write the gamma codeword of x >= 1. Cost: 2 floor(log2 x) + 1 bit writes."""
    if x < 1:
        raise ValueError("the gamma code needs x >= 1; code x + 1 to include 0")
    n = x.bit_length() - 1  # @line L1
    for _ in range(n):  # @line L2
        w.write_bit(0)
    w.write_bits(x, n + 1)  # @line L3


def gamma_decode(r: BitReader) -> int:
    """Read one gamma codeword and return x. Cost: 2 floor(log2 x) + 1 bit reads."""
    n = 0  # @line L4
    while r.read_bit() == 0:  # @line L5
        n += 1
    x = 1  # @line L6
    for _ in range(n):  # @line L7
        x = 2 * x + r.read_bit()
    return x  # @line L8


def gamma_length(x: int) -> int:
    """Length in bits of the codeword of x >= 1."""
    return 2 * (x.bit_length() - 1) + 1


def gamma_codeword(x: int) -> str:
    w = BitWriter()
    gamma_encode(x, w)
    return w.bits()


def gamma0_encode(x: int, w: BitWriter) -> None:
    """Code x >= 0 by the gamma codeword of x + 1."""
    gamma_encode(x + 1, w)


def gamma0_decode(r: BitReader) -> int:
    return gamma_decode(r) - 1


def encode_all(values: list[int]) -> tuple[bytes, int]:
    w = BitWriter()
    for v in values:
        gamma_encode(v, w)
    return w.getvalue()


def decode_all(data: bytes, nbits: int) -> list[int]:
    r = BitReader(data, nbits)
    out = []
    while not r.at_end():
        out.append(gamma_decode(r))
    return out
