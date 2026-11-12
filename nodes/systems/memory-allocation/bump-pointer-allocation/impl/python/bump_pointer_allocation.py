# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bump-pointer-allocation/. The authors are listed in prov/Q000WF.jsonl.

"""Bump-pointer allocation over the address range [base, limit).

The allocator keeps one pointer, top. To allocate n bytes with alignment a
(a power of two), it rounds top up to a multiple of a, checks the limit, and
moves top past the block. There is no free of single blocks: reset() frees
everything at once by moving top back to base.
"""


class BumpAllocator:
    def __init__(self, base: int, limit: int) -> None:
        if not 0 <= base <= limit:
            raise ValueError("need 0 <= base <= limit")
        self.base, self.limit = base, limit
        self.top = base

    def alloc(self, n: int, a: int = 1) -> int | None:
        """Return an a-aligned address of n free bytes, or None if they do not fit."""
        if n < 0 or a < 1 or a & (a - 1):
            raise ValueError("need n >= 0 and a a power of two")
        p = (self.top + a - 1) & ~(a - 1)  # @line L1
        if p + n > self.limit:  # @line L2
            return None
        self.top = p + n  # @line L3
        return p  # @line L4

    def reset(self) -> None:
        """Free every block at once."""
        self.top = self.base  # @line L5

    def used(self) -> int:
        return self.top - self.base
