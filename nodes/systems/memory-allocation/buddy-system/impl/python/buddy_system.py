# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/buddy-system/. The authors are listed in prov/B9JWWG.jsonl.

"""The binary buddy system of Knowlton (1965), in the form of Knuth's
Algorithms R (reservation) and S (liberation), TAOCP Vol. 1, Section 2.5.

The heap has 2^m words with addresses 0 .. 2^m - 1. A block of order k has
2^k words and starts at a multiple of 2^k. AVAIL[k] holds the free blocks of
order k. Each list is a dict used as an ordered set, so that a block is
added, found and removed in O(1) time, as with Knuth's doubly linked lists.
"""


class BuddySystem:
    """A binary buddy allocator over a heap of 2^m words.

    malloc(n) takes O(m) time in the worst case and free(p) takes O(m) time.
    """

    def __init__(self, m: int) -> None:
        if m < 0:
            raise ValueError("m must be at least 0")
        self.m = m
        self.avail: list[dict[int, None]] = [{} for _ in range(m + 1)]
        self.avail[m][0] = None
        self.kval: dict[int, int] = {}  # address of an allocated block -> its order
        self.splits = 0
        self.merges = 0

    def malloc(self, n: int) -> int | None:
        """Allocate a block of at least n words. Return its address, or None."""
        if n < 1:
            raise ValueError("n must be at least 1")
        k = (n - 1).bit_length()  # @line L1
        j = k
        while j <= self.m and not self.avail[j]:  # @line L2
            j += 1
        if j > self.m:  # @line L3
            return None
        addr, _ = self.avail[j].popitem()  # @line L4
        while j > k:  # @line L5
            j -= 1  # @line L6
            self.avail[j][addr + (1 << j)] = None  # @line L7
            self.splits += 1
        self.kval[addr] = k  # @line L8
        return addr

    def free(self, p: int) -> None:
        """Free the block at address p, which malloc returned."""
        if p not in self.kval:
            raise ValueError("p is not an allocated block")
        k = self.kval.pop(p)  # @line L9
        while k < self.m:  # @line L10
            buddy = p ^ (1 << k)  # @line L11
            if buddy not in self.avail[k]:  # @line L12
                break
            del self.avail[k][buddy]  # @line L13
            p = min(p, buddy)  # @line L14
            k += 1
            self.merges += 1
        self.avail[k][p] = None  # @line L15

    def free_blocks(self) -> list[set[int]]:
        """The free lists as sets of addresses, one set per order 0 .. m."""
        return [set(a) for a in self.avail]

    def check_invariant(self) -> None:
        """Raise AssertionError unless the heap is in a legal buddy state."""
        blocks = [(a, k, False) for k in range(self.m + 1) for a in self.avail[k]]
        blocks += [(a, k, True) for a, k in self.kval.items()]
        blocks.sort()
        pos = 0
        for a, k, _ in blocks:
            assert a == pos, "blocks must tile the heap with no gap or overlap"
            assert a % (1 << k) == 0, "a block of order k starts at a multiple of 2^k"
            pos = a + (1 << k)
        assert pos == 1 << self.m, "the sizes must add up to 2^m"
        for k in range(self.m):
            for a in self.avail[k]:
                assert (a ^ (1 << k)) not in self.avail[k], "two free buddies were not merged"
