# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fibonacci-buddy-system/. The authors are listed in prov/R8K8RA.jsonl.

"""The Fibonacci buddy system (Hirschberg 1973).

The block sizes are S[0] = 1, S[1] = 2 and S[k] = S[k-1] + S[k-2], that is
1, 2, 3, 5, 8, 13, ... The heap is one block of order m, with S[m] words.
A block of order k >= 2 splits into a left block of order k - 1 at the same
address and a right block of order k - 2 just after it. Each block keeps two
bits: lr (0 for a left block, 1 for a right block) and inh, the inheritance
bit. A split gives the left child inh = lr of the parent and the right child
inh = inh of the parent, so a merge can give the parent back its two bits.
"""

from dataclasses import dataclass


def fib_sizes(m: int) -> list[int]:
    """Return S[0 .. m]."""
    s = [1, 2]
    while len(s) < m + 1:
        s.append(s[-1] + s[-2])
    return s[: m + 1]


@dataclass
class Block:
    order: int
    lr: int  # 0 = left buddy, 1 = right buddy
    inh: int  # inheritance bit


class FibonacciBuddySystem:
    """Fibonacci buddy allocator over a heap of S[m] words.

    malloc and free take O(m) time, and m is about log_phi of the heap size.
    """

    def __init__(self, m: int) -> None:
        if m < 0:
            raise ValueError("m must be at least 0")
        self.m = m
        self.size = fib_sizes(m)
        self.avail: list[dict[int, None]] = [{} for _ in range(m + 1)]
        self.block: dict[int, Block] = {0: Block(m, 0, 0)}  # every block, free or not
        self.avail[m][0] = None
        self.allocated: set[int] = set()
        self.splits = 0
        self.merges = 0

    def order_for(self, n: int) -> int | None:
        """The least k with S[k] >= n, or None."""
        for k in range(self.m + 1):
            if self.size[k] >= n:
                return k
        return None

    def malloc(self, n: int) -> int | None:
        """Allocate at least n words. Return the address, or None."""
        if n < 1:
            raise ValueError("n must be at least 1")
        k = self.order_for(n)  # @line L1
        if k is None:
            return None
        j = k
        while j <= self.m and not self.avail[j]:  # @line L2
            j += 1
        if j > self.m:  # @line L3
            return None
        a, _ = self.avail[j].popitem()  # @line L4
        b = self.block[a]
        while j >= 2 and j - 1 >= k:  # @line L5
            left = Block(j - 1, 0, b.lr)  # @line L6
            right = Block(j - 2, 1, b.inh)
            ra = a + self.size[j - 1]
            self.splits += 1
            if j - 2 >= k:  # @line L7
                self.block[a] = left
                self.avail[j - 1][a] = None
                a, b, j = ra, right, j - 2
            else:  # @line L8
                self.block[ra] = right
                self.avail[j - 2][ra] = None
                b, j = left, j - 1
        self.block[a] = b  # @line L9
        self.allocated.add(a)
        return a

    def free(self, p: int) -> None:
        """Free the block at address p, which malloc returned."""
        if p not in self.allocated:
            raise ValueError("p is not an allocated block")
        self.allocated.remove(p)
        b = self.block[p]  # @line L10
        while b.order < self.m:  # @line L11
            if b.lr == 0:  # @line L12
                q, qorder = p + self.size[b.order], b.order - 1
            else:
                q, qorder = p - self.size[b.order + 1], b.order + 1
            if q not in self.avail[qorder]:  # @line L13
                break
            del self.avail[qorder][q]  # @line L14
            c = self.block[q]
            del self.block[max(p, q)]
            if b.lr == 0:  # @line L15
                left, right = b, c
            else:
                left, right = c, b
            p = min(p, q)
            b = Block(left.order + 1, left.inh, right.inh)  # @line L16
            self.block[p] = b
            self.merges += 1
        self.avail[b.order][p] = None  # @line L17

    def free_blocks(self) -> list[set[int]]:
        """The free lists as sets of addresses, one set per order."""
        return [set(a) for a in self.avail]

    def check_invariant(self) -> None:
        """Raise AssertionError unless the state is legal."""
        pos = 0
        for a in sorted(self.block):
            b = self.block[a]
            assert a == pos, "blocks must tile the heap"
            free = a in self.avail[b.order]
            assert free != (a in self.allocated), "a block is free or allocated, not both"
            pos = a + self.size[b.order]
        assert pos == self.size[self.m], "the sizes must add up to S[m]"
        assert sum(len(x) for x in self.avail) + len(self.allocated) == len(self.block)
