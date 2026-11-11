# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elias-delta-coding/. The authors are listed in prov/5Y2VCC.jsonl.

"""Elias delta code for the integers x >= 1.

The codeword of x is the gamma codeword of the bit length N + 1 of x, where
N = floor(log2 x), followed by the N low binary digits of x (the leading 1 is
not written). Its length is N + 2 floor(log2(N + 1)) + 1 bits.
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
    """Elias gamma: floor(log2 x) zeros, then the binary digits of x."""
    n = x.bit_length() - 1
    w.write_bits(0, n)
    w.write_bits(x, n + 1)


def gamma_decode(r: BitReader, max_zeros: int = 1 << 16) -> int:
    n = 0
    while r.read_bit() == 0:
        n += 1
        if n > max_zeros:
            raise ValueError("gamma prefix too long")
    x = 1
    for _ in range(n):
        x = 2 * x + r.read_bit()
    return x


def delta_encode(x: int, w: BitWriter) -> None:
    """Write the delta codeword of x >= 1."""
    if x < 1:
        raise ValueError("the delta code needs x >= 1; code x + 1 to include 0")
    n = x.bit_length() - 1  # @line L1
    gamma_encode(n + 1, w)  # @line L2
    # write_bits keeps the low n digits only, so the leading 1 is dropped.
    w.write_bits(x, n)  # @line L3


def delta_decode(r: BitReader) -> int:
    """Read one delta codeword and return x."""
    n = gamma_decode(r) - 1  # @line L4
    x = 1  # @line L5
    for _ in range(n):  # @line L6
        x = 2 * x + r.read_bit()
    return x  # @line L7


def delta_length(x: int) -> int:
    """Length in bits of the delta codeword of x >= 1."""
    n = x.bit_length() - 1
    return n + 2 * ((n + 1).bit_length() - 1) + 1


def gamma_length(x: int) -> int:
    return 2 * (x.bit_length() - 1) + 1


def delta_codeword(x: int) -> str:
    w = BitWriter()
    delta_encode(x, w)
    return w.bits()


def encode_all(values: list[int]) -> tuple[bytes, int]:
    w = BitWriter()
    for v in values:
        delta_encode(v, w)
    return w.getvalue()


def decode_all(data: bytes, nbits: int) -> list[int]:
    r = BitReader(data, nbits)
    out = []
    while not r.at_end():
        out.append(delta_decode(r))
    return out
