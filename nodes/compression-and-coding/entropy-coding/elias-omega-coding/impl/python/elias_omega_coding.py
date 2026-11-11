# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elias-omega-coding/. The authors are listed in prov/7AJD58.jsonl.

"""Elias omega code for the integers x >= 1.

The codeword of x is a chain of groups followed by a single 0 bit. The last group
is the binary form of x, the group before it is the binary form of floor(log2 x),
and so on, until a group would be the value 1. Each group starts with a 1 bit, so
the final 0 marks the end. The encoder builds the chain from the right.
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


def omega_encode(x: int, w: BitWriter) -> None:
    """Write the omega codeword of x >= 1."""
    if x < 1:
        raise ValueError("the omega code needs x >= 1; code x + 1 to include 0")
    # The chain S is kept as a list of groups, last group first; the final 0 of S
    # is written after the groups at L5.
    groups: list[int] = []  # @line L1
    while x > 1:  # @line L2
        groups.append(x)  # @line L3
        x = x.bit_length() - 1  # @line L4
    for g in reversed(groups):  # @line L5
        w.write_bits(g, g.bit_length())
    w.write_bit(0)


def omega_decode(r: BitReader, max_bits: int = 1 << 20) -> int:
    """Read one omega codeword and return x."""
    x = 1  # @line L6
    while r.read_bit() == 1:  # @line L7
        if x > max_bits:
            raise ValueError("omega group longer than max_bits")
        v = 1
        for _ in range(x):  # @line L8
            v = 2 * v + r.read_bit()
        x = v
    return x  # @line L9


def omega_length(x: int) -> int:
    """Length in bits of the omega codeword of x >= 1, by the recurrence
    L(1) = 1 and L(x) = (floor(log2 x) + 1) + L(floor(log2 x))."""
    total = 1
    while x > 1:
        total += x.bit_length()
        x = x.bit_length() - 1
    return total


def omega_codeword(x: int) -> str:
    w = BitWriter()
    omega_encode(x, w)
    return w.bits()


def encode_all(values: list[int]) -> tuple[bytes, int]:
    w = BitWriter()
    for v in values:
        omega_encode(v, w)
    return w.getvalue()


def decode_all(data: bytes, nbits: int) -> list[int]:
    r = BitReader(data, nbits)
    out = []
    while not r.at_end():
        out.append(omega_decode(r))
    return out
