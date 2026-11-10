# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plru-replacement/. The authors are listed in prov/1SHFPZ.jsonl.

from typing import Hashable, List, Optional, Sequence, Tuple

Block = Hashable


class TreePLRU:
    """One set of a cache with A ways (A a power of two) and tree pseudo-LRU replacement.

    bits[1 .. A-1] form a complete binary tree in heap order: node v has children
    2v and 2v + 1, and the leaves A .. 2A-1 stand for the ways 0 .. A-1.
    A bit 0 points to the left child and a bit 1 points to the right child.
    The bits point toward the next victim.
    """

    def __init__(self, ways: int) -> None:
        if ways < 1 or ways & (ways - 1):
            raise ValueError("the number of ways must be a power of two")
        self.ways = ways
        self.bits: List[int] = [0] * ways  # index 0 is not used
        self.lines: List[Optional[Block]] = [None] * ways

    def victim(self) -> int:
        """The way that the bits point to."""
        v = 1
        while v < self.ways:
            v = 2 * v + self.bits[v]
        return v - self.ways

    def touch(self, way: int) -> None:
        """Set each bit on the path to the way so that it points away from the way."""
        v = way + self.ways
        while v > 1:
            parent = v // 2
            self.bits[parent] = 1 if v == 2 * parent else 0
            v = parent

    def access(self, x: Block) -> Tuple[bool, Optional[Block]]:
        """Serve one access. Returns (hit, evicted block or None)."""
        evicted = None
        if x in self.lines:  # @line L3
            w = self.lines.index(x)
            hit = True
        elif None in self.lines:  # @line L4
            w = self.lines.index(None)
            hit = False
        else:
            w = self.victim()  # @line L5
            evicted = self.lines[w]
            hit = False
        self.lines[w] = x  # @line L6
        self.touch(w)  # @line L7
        return hit, evicted


def plru_replacement(requests: Sequence[Block], ways: int) -> Tuple[int, List[Tuple[Block, bool, Optional[Block]]]]:
    """Run tree PLRU on one cache set. Returns (misses, log of (block, hit, evicted)).

    Each access takes O(A) time to search the ways and O(log A) time for the bits.
    """
    cache = TreePLRU(ways)
    misses = 0  # @line L1
    log = []
    for x in requests:  # @line L2
        hit, evicted = cache.access(x)
        misses += 0 if hit else 1
        log.append((x, hit, evicted))
    return misses, log  # @line L8
