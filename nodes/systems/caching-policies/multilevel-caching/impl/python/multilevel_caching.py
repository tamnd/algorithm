# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multilevel-caching/. The authors are listed in prov/6DVKBB.jsonl.

"""A two-level cache of blocks, each level a fully associative LRU cache.

Three content policies:
  inclusive  every block in L1 is also in L2; an L2 eviction removes the block from L1
             too (back-invalidation).
  nine       non-inclusive non-exclusive: a miss fills both levels, and an L2 eviction
             does not touch L1.
  exclusive  a block is in at most one level; a miss fills only L1, an L2 hit moves the
             block up to L1, and each L1 victim moves down to L2.
L2 sees only the misses of L1, so an L1 hit does not change the LRU order of L2.
"""

from collections import OrderedDict
from typing import Hashable, Iterable

MODES = ("inclusive", "nine", "exclusive")


class TwoLevelCache:
    def __init__(self, c1: int, c2: int, mode: str = "inclusive") -> None:
        if mode not in MODES:
            raise ValueError(f"mode must be one of {MODES}")
        if c1 < 1 or c2 < 1:
            raise ValueError("capacities must be positive")
        if mode == "inclusive" and c2 < c1:
            raise ValueError("an inclusive L2 must be at least as large as L1")
        self.c1, self.c2, self.mode = c1, c2, mode
        self.l1: OrderedDict = OrderedDict()  # least recent first
        self.l2: OrderedDict = OrderedDict()
        self.l1_hits = self.l2_hits = self.memory = 0
        self.l2_stream: list = []  # the requests that L2 sees
        self.back_invalidations = 0

    def _put_l2(self, x: Hashable) -> None:
        self.l2[x] = True
        self.l2.move_to_end(x)
        if len(self.l2) > self.c2:
            v, _ = self.l2.popitem(last=False)
            if self.mode == "inclusive" and v in self.l1:
                del self.l1[v]  # back-invalidation keeps L1 a subset of L2
                self.back_invalidations += 1

    def _put_l1(self, x: Hashable) -> None:
        self.l1[x] = True
        if len(self.l1) > self.c1:
            v, _ = self.l1.popitem(last=False)
            if self.mode == "exclusive":
                self._put_l2(v)  # the victim moves down

    def access(self, x: Hashable) -> int:
        """Return the level that served x: 1, 2, or 3 for memory."""
        if x in self.l1:
            self.l1.move_to_end(x)
            self.l1_hits += 1
            return 1
        self.l2_stream.append(x)
        if x in self.l2:
            self.l2_hits += 1
            if self.mode == "exclusive":
                del self.l2[x]  # the block moves up and leaves L2
            else:
                self.l2.move_to_end(x)
            self._put_l1(x)
            return 2
        self.memory += 1
        if self.mode != "exclusive":
            self._put_l2(x)  # fill L2 first, so that its eviction cannot hit x itself
        self._put_l1(x)
        return 3

    def feed(self, trace: Iterable[Hashable]) -> "TwoLevelCache":
        for x in trace:
            self.access(x)
        return self


def amat(hit1: float, hit2: float, memory: float, local_miss1: float, local_miss2: float) -> float:
    """Average memory access time: hit time + miss rate x miss penalty, applied level by level."""
    return hit1 + local_miss1 * (hit2 + local_miss2 * memory)


def lru_hits(capacity: int, trace: Iterable[Hashable]) -> int:
    cache: OrderedDict = OrderedDict()
    hits = 0
    for x in trace:
        if x in cache:
            cache.move_to_end(x)
            hits += 1
        else:
            cache[x] = True
            if len(cache) > capacity:
                cache.popitem(last=False)
    return hits
