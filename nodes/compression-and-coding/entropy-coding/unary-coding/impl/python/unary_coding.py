# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unary-coding/. The authors are listed in prov/KAJ1DT.jsonl.

"""Unary code for the integers n >= 0.

The default convention writes n as n one bits and then one zero bit, so the
codeword of n has n + 1 bits. With ones_first=False the roles of the two bits
swap: n zero bits and then a one bit. Both conventions appear in practice.
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
        """Write the low `width` bits of value, most significant first."""
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
        value = 0
        for _ in range(width):
            value = (value << 1) | self.read_bit()
        return value

    def at_end(self) -> bool:
        return self.pos >= self.nbits


def unary_encode(n: int, w: BitWriter, ones_first: bool = True) -> None:
    """Write the unary codeword of n >= 0. Cost: n + 1 bit writes."""
    if n < 0:
        raise ValueError("unary code needs n >= 0")
    run, stop = (1, 0) if ones_first else (0, 1)
    for _ in range(n):
        w.write_bit(run)
    w.write_bit(stop)


def unary_decode(r: BitReader, ones_first: bool = True) -> int:
    """Read one unary codeword and return n. Cost: n + 1 bit reads."""
    stop = 0 if ones_first else 1
    n = 0
    while r.read_bit() != stop:
        n += 1
    return n


def unary_codeword(n: int, ones_first: bool = True) -> str:
    """The codeword of n as a string of '0' and '1'."""
    w = BitWriter()
    unary_encode(n, w, ones_first)
    return w.bits()


def encode_all(values: list[int], ones_first: bool = True) -> tuple[bytes, int]:
    """Concatenate the codewords of all values. Returns the bytes and the bit count."""
    w = BitWriter()
    for v in values:
        unary_encode(v, w, ones_first)
    return w.getvalue()


def decode_all(data: bytes, nbits: int, ones_first: bool = True) -> list[int]:
    """Decode a stream made by encode_all."""
    r = BitReader(data, nbits)
    out = []
    while not r.at_end():
        out.append(unary_decode(r, ones_first))
    return out
