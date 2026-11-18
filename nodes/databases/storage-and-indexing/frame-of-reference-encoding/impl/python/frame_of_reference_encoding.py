# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frame-of-reference-encoding/. The authors are listed in prov/PWP268.jsonl.

"""Frame of reference encoding of an integer column, in blocks of B values.

Each block k keeps a header with its base (the minimum of the block), its
maximum and its bit width w_k, the number of bits of max - base. The values of
the block are stored as the offsets value - base, packed w_k bits each, least
significant bit first. A block of equal values has w_k = 0 and no offset bits.

get(i) reads one offset and adds the base, with no access to other values.
select(lo, hi) returns the positions with lo <= value <= hi (a bound of None
is open). It skips a block whose range [base, max] misses [lo, hi], takes a
block whose range lies inside [lo, hi] without reading it, and else compares
offsets with the translated bounds lo - base and hi - base. The counters
self.offsets_read and self.blocks_skipped let tests check this.
"""

from typing import List, Optional, Sequence

HEADER_BYTES = 8 + 8 + 1   # base, maximum, width


class Block:
    __slots__ = ("base", "max", "w", "count", "bits")

    def __init__(self, values: Sequence[int]) -> None:
        self.base = min(values)                               # @line L2
        self.max = max(values)                                # @line L2
        self.w = (self.max - self.base).bit_length()          # @line L3
        self.count = len(values)
        self.bits = bytearray((self.count * self.w + 7) // 8)
        for j, v in enumerate(values):                        # @line L4
            off, pos = v - self.base, j * self.w              # @line L4
            for b in range(self.w):
                if off >> b & 1:
                    self.bits[(pos + b) >> 3] |= 1 << ((pos + b) & 7)

    def offset(self, j: int) -> int:
        pos, x = j * self.w, 0                                # @line L5
        for b in range(self.w):                               # @line L5
            x |= (self.bits[(pos + b) >> 3] >> ((pos + b) & 7) & 1) << b  # @line L5
        return x


class FORColumn:
    def __init__(self, values: Sequence[int], B: int = 128) -> None:
        if B < 1:
            raise ValueError("block size must be at least 1")
        for v in values:
            if not isinstance(v, int) or isinstance(v, bool):
                raise TypeError("frame of reference encoding needs integers")
        self.B = B
        self.n = len(values)
        self.blocks: List[Block] = [Block(values[s:s + B])   # @line L1
                                    for s in range(0, self.n, B)]
        self.offsets_read = 0
        self.blocks_skipped = 0

    def get(self, i: int) -> int:
        if not 0 <= i < self.n:
            raise IndexError(i)
        blk = self.blocks[i // self.B]                        # @line L5
        self.offsets_read += 1
        return blk.base + blk.offset(i % self.B)              # @line L6

    def decode_all(self) -> List[int]:
        out = []
        for blk in self.blocks:
            out.extend(blk.base + blk.offset(j) for j in range(blk.count))
        return out

    def size_bytes(self) -> int:
        return sum(HEADER_BYTES + len(blk.bits) for blk in self.blocks)

    def select(self, lo: Optional[int], hi: Optional[int]) -> List[int]:
        out: List[int] = []
        for k, blk in enumerate(self.blocks):                 # @line L7
            first = k * self.B
            if (lo is not None and blk.max < lo) or (hi is not None and blk.base > hi):  # @line L8
                self.blocks_skipped += 1                      # @line L8
                continue
            if (lo is None or lo <= blk.base) and (hi is None or blk.max <= hi):  # @line L9
                out.extend(range(first, first + blk.count))   # @line L9
                continue
            s = 0 if lo is None else max(lo - blk.base, 0)    # @line L10
            e = blk.max - blk.base if hi is None else hi - blk.base  # @line L10
            for j in range(blk.count):                        # @line L11
                self.offsets_read += 1
                if s <= blk.offset(j) <= e:                   # @line L11
                    out.append(first + j)                     # @line L11
        return out

    def select_op(self, op: str, v: int) -> List[int]:
        """A comparison with a constant, as a range of integers."""
        ranges = {"=": (v, v), "<": (None, v - 1), "<=": (None, v),
                  ">": (v + 1, None), ">=": (v, None)}
        if op not in ranges:
            raise ValueError(f"unknown comparison {op}")
        return self.select(*ranges[op])
