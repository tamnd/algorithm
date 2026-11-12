# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/memory-pool/. The authors are listed in prov/K0DCNX.jsonl.

"""A memory pool of n blocks of b words each, in one array of n * b words.

The free blocks form a singly linked list whose links are stored in the first
word of each free block, so the pool needs no memory outside the array except
two words: HEAD and FRESH. Blocks that were never used are not on the list:
FRESH counts them, so creating the pool takes O(1) time.
"""

NIL = -1


class MemoryPool:
    """Fixed-size block allocator. alloc and free take O(1) time."""

    def __init__(self, n: int, b: int, check: bool = False) -> None:
        if n < 0 or b < 1:
            raise ValueError("need n >= 0 blocks of b >= 1 words")
        self.n = n
        self.b = b
        self.mem = [0] * (n * b)
        self.head = NIL
        self.fresh = 0  # blocks 0 .. fresh-1 have been handed out at least once
        self.check = check
        self.live: set[int] = set()  # used only when check is True

    def alloc(self) -> int | None:
        """Return the address of a free block, or None."""
        if self.head != NIL:  # @line L1
            p = self.head
            self.head = self.mem[p]
        elif self.fresh < self.n:  # @line L2
            p = self.fresh * self.b
            self.fresh += 1
        else:
            return None  # @line L3
        if self.check:
            self.live.add(p)
        return p

    def free(self, p: int) -> None:
        """Give back the block at address p."""
        if self.check:
            if p not in self.live:
                raise ValueError("double free or bad address")
            self.live.remove(p)
        self.mem[p] = self.head  # @line L4
        self.head = p  # @line L5

    def free_list(self) -> list[int]:
        """The addresses on the free list, from HEAD on (at most n steps)."""
        out = []
        p = self.head
        while p != NIL and len(out) <= self.n:
            out.append(p)
            p = self.mem[p]
        return out
