# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/set-associative-cache/. The authors are listed in prov/Q5H7VX.jsonl.

"""A set-associative cache: S sets of W ways, blocks of B bytes.

An address splits into  tag | index | offset.  The offset (log2 B bits) picks the byte
in the block, the index (log2 S bits) picks the set, and the tag tells which of the
blocks that map to the set is stored in a way. Replacement works inside one set: LRU,
tree pseudo-LRU, or random. W = 1 is a direct-mapped cache; S = 1 is fully associative.
"""

import random
from typing import Optional


def _log2(x: int, name: str) -> int:
    if x <= 0 or x & (x - 1):
        raise ValueError(f"{name} must be a power of two")
    return x.bit_length() - 1


class SetAssociativeCache:
    def __init__(self, sets: int, ways: int, block: int = 64, policy: str = "lru", rng: Optional[random.Random] = None) -> None:
        self.offset_bits = _log2(block, "block")
        self.index_bits = _log2(sets, "sets")
        if ways <= 0:
            raise ValueError("ways must be positive")
        if policy == "plru":
            _log2(ways, "ways for PLRU")
        if policy not in ("lru", "plru", "random"):
            raise ValueError("policy must be lru, plru or random")
        if policy == "random" and rng is None:
            raise ValueError("the random policy needs an rng")
        self.sets, self.ways, self.block, self.policy, self.rng = sets, ways, block, policy, rng
        self.tags: list[list[Optional[int]]] = [[None] * ways for _ in range(sets)]
        self.stamp = [[0] * ways for _ in range(sets)]  # time of last use, for LRU
        self.bits = [[0] * max(ways - 1, 1) for _ in range(sets)]  # PLRU tree, node i has children 2i+1, 2i+2
        self.clock = 0
        self.hits = self.misses = 0

    def split(self, address: int) -> tuple[int, int, int]:
        """(tag, index, offset) of a byte address."""
        offset = address & (self.block - 1)  # @line L1
        index = (address >> self.offset_bits) & (self.sets - 1)
        tag = address >> (self.offset_bits + self.index_bits)
        return tag, index, offset

    def _touch(self, s: int, w: int) -> None:
        self.clock += 1
        self.stamp[s][w] = self.clock
        if self.policy == "plru" and self.ways > 1:
            # walk from the root to leaf w; each bit on the path points away from w
            node, lo, hi = 0, 0, self.ways
            while hi - lo > 1:
                mid = (lo + hi) // 2
                if w < mid:
                    self.bits[s][node] = 1  # 1: the victim is in the right half
                    node, hi = 2 * node + 1, mid
                else:
                    self.bits[s][node] = 0  # 0: the victim is in the left half
                    node, lo = 2 * node + 2, mid

    def _victim(self, s: int) -> int:
        line = self.tags[s]
        if None in line:
            return line.index(None)  # fill an empty way first
        if self.policy == "lru":
            return min(range(self.ways), key=lambda w: self.stamp[s][w])
        if self.policy == "random":
            return self.rng.randrange(self.ways)
        node, lo, hi = 0, 0, self.ways
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if self.bits[s][node] == 0:
                node, hi = 2 * node + 1, mid
            else:
                node, lo = 2 * node + 2, mid
        return lo

    def access(self, address: int) -> bool:
        """Read the byte at address. Return True on a hit."""
        tag, s, _ = self.split(address)
        line = self.tags[s]  # @line L2
        for w in range(self.ways):  # @line L3
            if line[w] == tag:  # @line L4
                self._touch(s, w)  # @line L5
                self.hits += 1
                return True  # @line L6
        w = self._victim(s)  # @line L7
        line[w] = tag  # @line L8
        self._touch(s, w)  # @line L9
        self.misses += 1
        return False  # @line L10

    def contents(self) -> set[int]:
        """The block numbers in the cache."""
        out = set()
        for s, line in enumerate(self.tags):
            for tag in line:
                if tag is not None:
                    out.add((tag << self.index_bits) | s)
        return out


def run(cache: SetAssociativeCache, addresses: list[int]) -> list[bool]:
    return [cache.access(a) for a in addresses]
