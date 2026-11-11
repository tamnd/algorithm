# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interpolative-coding/. The authors are listed in prov/TZXH8F.jsonl.

"""Binary interpolative coding (Moffat and Stuiver, 2000).

A strictly increasing list S[0..n-1] with lo <= S[0] and S[n-1] <= hi is coded
by writing the middle element relative to the range that the bounds and the
element count leave for it, then the two halves with tighter bounds. A range
with no freedom (a run of consecutive integers) costs 0 bits.

The recursion is done with an explicit stack. The left half is pushed last and
so processed first, which gives the pre-order of the recursive form and keeps
the stack at most floor(log2 n) + 1 entries deep.

Two codes for a value 0 <= v <= r are given: plain binary in ceil(log2(r+1))
bits, and a centered minimal binary code, where the c = 2^k - (r+1) values in
the middle of the range get k - 1 bits and the others k bits.
"""

from collections.abc import Sequence


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


# ---------------------------------------------------------------------------
# Codes for a value 0 <= v <= r.
# ---------------------------------------------------------------------------


def plain_width(r: int) -> int:
    return r.bit_length()  # = ceil(log2(r + 1))


def write_plain(w: BitWriter, v: int, r: int) -> None:
    w.write_bits(v, plain_width(r))


def read_plain(rd: BitReader, r: int) -> int:
    return rd.read_bits(plain_width(r))


def _centered_params(r: int) -> tuple[int, int, int]:
    """Return (k, c, s): k = ceil(log2 N) with N = r + 1, c short codewords, and
    s the first value of the centered short range."""
    n = r + 1
    k = (n - 1).bit_length()
    c = (1 << k) - n
    # The short range of Pibiri and Venturini, Section 3.5: (r_l, r_h) exclusive.
    s = r // 2 - c // 2 + (r % 2)
    return k, c, s


def minimal_length(v: int, r: int) -> int:
    if r == 0:
        return 0
    k, c, s = _centered_params(r)
    return k - 1 if (v - s) % (r + 1) < c else k


def write_minimal(w: BitWriter, v: int, r: int) -> None:
    """Centered minimal binary: rotate so the short range starts at 0, then
    use truncated binary (y < c in k - 1 bits, else y + c in k bits)."""
    if r == 0:
        return
    k, c, s = _centered_params(r)
    y = (v - s) % (r + 1)
    if y < c:
        w.write_bits(y, k - 1)
    else:
        w.write_bits(y + c, k)


def read_minimal(rd: BitReader, r: int) -> int:
    if r == 0:
        return 0
    k, c, s = _centered_params(r)
    t = rd.read_bits(k - 1)
    if t >= c:
        t = 2 * t + rd.read_bit() - c
    return (t + s) % (r + 1)


CODES = {"minimal": (write_minimal, read_minimal), "plain": (write_plain, read_plain)}


# ---------------------------------------------------------------------------
# Interpolative coding with an explicit stack.
# ---------------------------------------------------------------------------


def bic_encode(s: Sequence[int], lo: int, hi: int, w: BitWriter, code: str = "minimal") -> int:
    """Write S; return the largest stack depth used."""
    n = len(s)
    if any(s[i] >= s[i + 1] for i in range(n - 1)) or (n and not lo <= s[0] <= s[-1] <= hi):
        raise ValueError("S must be strictly increasing and inside [lo, hi]")
    write = CODES[code][0]
    stack = [(0, n - 1, lo, hi)]  # @line L1
    depth = 1
    while stack:  # @line L2
        i, j, l, h = stack.pop()
        if i > j or h - l == j - i:  # @line L3
            continue
        m = i + (j - i) // 2  # @line L4
        write(w, s[m] - l - (m - i), h - l - (j - i))  # @line L5
        stack.append((m + 1, j, s[m] + 1, h))  # @line L6
        stack.append((i, m - 1, l, s[m] - 1))
        depth = max(depth, len(stack))
    return depth


def bic_decode(n: int, lo: int, hi: int, rd: BitReader, code: str = "minimal") -> list[int]:
    read = CODES[code][1]
    s = [0] * n
    stack = [(0, n - 1, lo, hi)]  # @line L7
    while stack:  # @line L8
        i, j, l, h = stack.pop()
        if i > j:  # @line L9
            continue
        if h - l == j - i:
            for t in range(j - i + 1):
                s[i + t] = l + t
            continue
        m = i + (j - i) // 2  # @line L10
        s[m] = l + (m - i) + read(rd, h - l - (j - i))
        stack.append((m + 1, j, s[m] + 1, h))  # @line L11
        stack.append((i, m - 1, l, s[m] - 1))
    return s  # @line L12


def encode(s: Sequence[int], lo: int, hi: int, code: str = "minimal") -> tuple[bytes, int]:
    w = BitWriter()
    bic_encode(s, lo, hi, w, code)
    return w.getvalue()


def decode(n: int, lo: int, hi: int, data: bytes, nbits: int, code: str = "minimal") -> list[int]:
    return bic_decode(n, lo, hi, BitReader(data, nbits), code)


def trace(s: Sequence[int], lo: int, hi: int) -> list[tuple[int, int, int, int, int]]:
    """Pre-order list of (l, h, middle element, value written, range r) for the nodes
    that write a value."""
    out = []
    stack = [(0, len(s) - 1, lo, hi)]
    while stack:
        i, j, l, h = stack.pop()
        if i > j or h - l == j - i:
            continue
        m = i + (j - i) // 2
        out.append((l, h, s[m], s[m] - l - (m - i), h - l - (j - i)))
        stack.append((m + 1, j, s[m] + 1, h))
        stack.append((i, m - 1, l, s[m] - 1))
    return out
