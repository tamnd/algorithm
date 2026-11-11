# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pfor-delta/. The authors are listed in prov/3ZJB2A.jsonl.

"""PForDelta: patched frame of reference on the gaps of a sorted list.

This follows the layout of Zukowski, Heman, Nes and Boncz (ICDE 2006): each
block of up to 128 values has a base and a bit width b. A value v with
v - base < 2^b is stored in a b-bit slot. Other values are exceptions, stored
as 32-bit words after the slots. The slot of an exception holds the distance
to the next exception minus 1, so the exceptions form a chain through the
slots. When two exceptions are more than 2^b apart, values in between are
made compulsory exceptions to keep the chain. The width b is chosen per
block by trying every b in 0..32 and keeping the one with the smallest block.

Block format (bytes):
  n (1), b (1), base (unsigned LEB128), first exception index (1, n if none),
  exception count (1), n slots of b bits packed MSB first and padded to a
  byte, then one 32-bit little-endian word per exception (v - base).
"""

from collections.abc import Sequence

BLOCK = 128
MAX_B = 32


def _uleb(x: int, out: bytearray) -> None:
    while True:
        b = x & 0x7F
        x >>= 7
        out.append(b | 0x80 if x else b)
        if not x:
            return


def _uleb_read(data: bytes, pos: int) -> tuple[int, int]:
    x = shift = 0
    while True:
        b = data[pos]
        pos += 1
        x |= (b & 0x7F) << shift
        shift += 7
        if b < 0x80:
            return x, pos


def exception_positions(deltas: Sequence[int], b: int) -> list[int]:
    """Positions of the true exceptions and the compulsory ones for width b."""
    limit = 1 << b
    out: list[int] = []
    for i, d in enumerate(deltas):
        if d >= limit:
            while out and i - out[-1] > limit:
                out.append(out[-1] + limit)
            out.append(i)
    return out


def _uleb_len(x: int) -> int:
    return max(1, -(-x.bit_length() // 7))


def block_size(deltas: Sequence[int], base: int, b: int) -> int:
    n = len(deltas)
    return 4 + _uleb_len(base) + (n * b + 7) // 8 + 4 * len(exception_positions(deltas, b))


def choose_b(values: Sequence[int]) -> int:
    base = min(values)
    deltas = [v - base for v in values]
    best_b, best = 0, None
    for b in range(0, MAX_B + 1):
        s = block_size(deltas, base, b)
        if best is None or s < best:
            best_b, best = b, s
    return best_b


def encode_block(values: Sequence[int], b: int | None = None) -> bytes:
    """Code one block of 1..128 values in [0, 2^32). b=None picks the best width."""
    n = len(values)
    if not 1 <= n <= BLOCK:
        raise ValueError("a block holds 1 to 128 values")
    if any(not 0 <= v < 1 << 32 for v in values):
        raise ValueError("values must be in [0, 2^32)")
    base = min(values)  # @line L1
    if b is None:
        b = choose_b(values)  # @line L2
    deltas = [v - base for v in values]
    exc = exception_positions(deltas, b)  # @line L3
    # exception_positions also adds the compulsory exceptions.
    exc_set = set(exc)  # @line L4
    codes = [0 if i in exc_set else d for i, d in enumerate(deltas)]  # @line L5
    for j in range(len(exc) - 1):  # @line L6
        codes[exc[j]] = exc[j + 1] - exc[j] - 1
    out = bytearray([n, b])  # @line L7
    _uleb(base, out)
    out += bytes([exc[0] if exc else n, len(exc)])
    acc = nacc = 0
    for c in codes:
        acc = (acc << b) | c
        nacc += b
        while nacc >= 8:
            nacc -= 8
            out.append((acc >> nacc) & 0xFF)
        acc &= (1 << nacc) - 1
    if nacc:
        out.append((acc << (8 - nacc)) & 0xFF)
    for i in exc:
        out += deltas[i].to_bytes(4, "little")
    return bytes(out)


def decode_block(data: bytes, pos: int = 0) -> tuple[list[int], int]:
    n, b = data[pos], data[pos + 1]  # @line L8
    base, pos = _uleb_read(data, pos + 2)
    first, count = data[pos], data[pos + 1]
    pos += 2
    codes = []
    acc = nacc = 0
    for _ in range(n):
        while nacc < b:
            acc = (acc << 8) | data[pos]
            pos += 1
            nacc += 8
        nacc -= b
        codes.append((acc >> nacc) & ((1 << b) - 1))
        acc &= (1 << nacc) - 1
    out = [base + c for c in codes]
    cur = first  # @line L9
    for j in range(count):
        nxt = cur + codes[cur] + 1  # @line L10
        out[cur] = base + int.from_bytes(data[pos + 4 * j : pos + 4 * j + 4], "little")
        cur = nxt
    return out, pos + 4 * count  # @line L11


def to_gaps(sorted_list: Sequence[int]) -> list[int]:
    prev = 0
    gaps = []
    for x in sorted_list:
        if x < prev:
            raise ValueError("the list must be sorted")
        gaps.append(x - prev)
        prev = x
    return gaps


def from_gaps(gaps: Sequence[int]) -> list[int]:
    out = []
    s = 0
    for g in gaps:
        s += g
        out.append(s)
    return out


def encode_list(sorted_list: Sequence[int]) -> bytes:
    """PForDelta: the gaps of a sorted list, coded in PFOR blocks of 128."""
    gaps = to_gaps(sorted_list)
    out = bytearray()
    _uleb(len(gaps), out)
    for i in range(0, len(gaps), BLOCK):
        out += encode_block(gaps[i : i + BLOCK])
    return bytes(out)


def decode_list(data: bytes) -> list[int]:
    total, pos = _uleb_read(data, 0)
    gaps: list[int] = []
    while len(gaps) < total:
        block, pos = decode_block(data, pos)
        gaps += block
    return from_gaps(gaps)
