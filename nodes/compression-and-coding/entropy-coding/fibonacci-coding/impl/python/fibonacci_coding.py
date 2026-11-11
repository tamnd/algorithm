# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fibonacci-coding/. The authors are listed in prov/1ZZ3YB.jsonl.

"""Fibonacci code (Apostolico and Fraenkel, 1987) for the integers x >= 1.

With the Fibonacci numbers F_2 = 1, F_3 = 2, F_4 = 3, F_5 = 5, ..., every x >= 1
is a sum of distinct, non-consecutive F_i (the Zeckendorf representation). The
codeword lists the digits d_2, d_3, ..., d_k of that sum, lowest first, and then
one more 1. The top digit d_k is 1, and no two digits in a row are 1, so the
pair 11 appears only at the end of each codeword.
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


class Fib:
    """The table F[i] for i >= 2, with F[2] = 1 and F[3] = 2, grown on demand."""

    def __init__(self) -> None:
        self.f = [0, 1, 1, 2]  # F_0 .. F_3

    def __getitem__(self, i: int) -> int:
        while len(self.f) <= i:
            self.f.append(self.f[-1] + self.f[-2])
        return self.f[i]


FIB = Fib()


def fib_encode(x: int, w: BitWriter) -> None:
    """Write the Fibonacci codeword of x >= 1."""
    if x < 1:
        raise ValueError("the Fibonacci code needs x >= 1; code x + 1 to include 0")
    k = 2  # @line L1
    while FIB[k + 1] <= x:
        k += 1
    d = [0] * (k + 1)  # @line L2
    for i in range(k, 1, -1):  # @line L3
        if FIB[i] <= x:  # @line L4
            d[i] = 1
            x -= FIB[i]
    for i in range(2, k + 1):  # @line L5
        w.write_bit(d[i])
    w.write_bit(1)


def fib_decode(r: BitReader) -> int:
    """Read bits up to and including the first pair 11, and return x."""
    x, i, prev = 0, 2, 0  # @line L6
    while True:
        b = r.read_bit()  # @line L7
        if b == 1 and prev == 1:  # @line L8
            return x
        if b == 1:  # @line L9
            x += FIB[i]
        prev = b  # @line L10
        i += 1


def fib_length(x: int) -> int:
    """Codeword length: the k with F_k <= x < F_(k+1)."""
    k = 2
    while FIB[k + 1] <= x:
        k += 1
    return k


def fib_codeword(x: int) -> str:
    w = BitWriter()
    fib_encode(x, w)
    return w.bits()


def encode_all(values: list[int]) -> tuple[bytes, int]:
    w = BitWriter()
    for v in values:
        fib_encode(v, w)
    return w.getvalue()


def decode_all(data: bytes, nbits: int) -> list[int]:
    """Decode a whole stream. Bits after the last pair 11 (a cut codeword) are ignored."""
    r = BitReader(data, nbits)
    out = []
    while not r.at_end():
        start = r.pos
        try:
            out.append(fib_decode(r))
        except EOFError:
            r.pos = start
            break
    return out
