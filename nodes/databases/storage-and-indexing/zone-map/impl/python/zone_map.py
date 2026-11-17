# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zone-map/. The authors are listed in prov/BKMHC8.jsonl.

"""A zone map: the minimum and maximum of a column in each block of rows.

Rows are stored in blocks of b consecutive rows. A range scan reads only the
blocks whose [min, max] interval meets the query interval. The bounds may be
loose after updates (they only widen), and the scan stays correct.
"""

from typing import List, Tuple


class ZoneMap:
    def __init__(self, block_size: int) -> None:
        if block_size < 1:
            raise ValueError("block_size must be at least 1")
        self.b = block_size
        self.column: List[int] = []
        self.lo: List[int] = []      # min of each block
        self.hi: List[int] = []      # max of each block
        self.blocks_read = 0
        self.blocks_skipped = 0

    @classmethod
    def build(cls, column: List[int], block_size: int) -> "ZoneMap":
        """One pass over the column: O(n) time, O(n / b) extra space."""
        z = cls(block_size)
        for v in column:
            z.append(v)
        return z

    def num_blocks(self) -> int:
        return len(self.lo)

    def append(self, v: int) -> None:
        r = len(self.column)
        self.column.append(v)
        if r % self.b == 0:
            self.lo.append(v)
            self.hi.append(v)
        else:
            k = r // self.b
            self.lo[k] = min(self.lo[k], v)
            self.hi[k] = max(self.hi[k], v)

    def update(self, r: int, x: int) -> None:
        """Set row r to x. The bounds widen; they never shrink here."""
        k = r // self.b                                  # @line L10
        self.column[r] = x                               # @line L11
        self.lo[k] = min(self.lo[k], x)                  # @line L12
        self.hi[k] = max(self.hi[k], x)                  # @line L12

    def scan(self, lo: int, hi: int) -> List[int]:
        """Rows r with lo <= A(r) <= hi, in row order. Counts blocks read and skipped."""
        self.blocks_read = 0
        self.blocks_skipped = 0
        result: List[int] = []                           # @line L1
        for k in range(len(self.lo)):                    # @line L2
            if self.hi[k] < lo or self.lo[k] > hi:       # @line L3
                self.blocks_skipped += 1                 # @line L4
                continue                                 # @line L4
            self.blocks_read += 1                        # @line L5
            start = k * self.b                           # @line L6
            for r in range(start, min(start + self.b, len(self.column))):  # @line L7
                if lo <= self.column[r] <= hi:           # @line L8
                    result.append(r)                     # @line L8
        return result                                    # @line L9

    def recompute(self, k: int) -> None:
        """Make the bounds of block k tight again (one read of the block)."""
        part = self.column[k * self.b:(k + 1) * self.b]
        self.lo[k], self.hi[k] = min(part), max(part)

    def check_invariant(self) -> None:
        """Every value lies inside the bounds of its block."""
        assert len(self.lo) == len(self.hi) == -(-len(self.column) // self.b)
        for r, v in enumerate(self.column):
            k = r // self.b
            assert self.lo[k] <= v <= self.hi[k]


def skip_probability(below: int, above: int, total: int, b: int) -> Tuple[int, int]:
    """P(block skipped) for b values drawn independently and uniformly from `total`
    equally likely values, of which `below` are < lo and `above` are > hi.
    Returned as an exact fraction (numerator, denominator)."""
    return below ** b + above ** b, total ** b
