# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-replacement/. The authors are listed in prov/TVHW25.jsonl.

import random
from collections.abc import Hashable, Iterable


class RandomReplacement:
    """Random replacement on a cache of k pages.

    The cached pages sit in an array, and a dict maps each page to its index.
    An eviction picks a uniform index, moves the last page into the hole and
    shrinks the array, so each request takes O(1) expected time.
    """

    def __init__(self, k: int, rng: random.Random) -> None:
        if k < 1:
            raise ValueError("the cache size k must be at least 1")
        self.k = k
        self.rng = rng
        self.slots: list[Hashable] = []
        self.index: dict[Hashable, int] = {}
        self.evicted: Hashable | None = None

    def __contains__(self, p: Hashable) -> bool:
        return p in self.index

    def __len__(self) -> int:
        return len(self.slots)

    def contents(self) -> set[Hashable]:
        return set(self.slots)

    def access(self, p: Hashable) -> bool:
        """Serve one request. Return True on a hit, False on a miss."""
        self.evicted = None
        if p in self.index:  # @line L1
            return True
        if len(self.slots) == self.k:  # @line L2
            i = self.rng.randrange(self.k)  # @line L3
            q = self.slots[i]
            last = self.slots.pop()  # @line L4
            if i < len(self.slots):
                self.slots[i] = last
                self.index[last] = i
            del self.index[q]
            self.evicted = q
        self.index[p] = len(self.slots)  # @line L5
        self.slots.append(p)
        return False  # @line L6


def random_hits(trace: Iterable[Hashable], k: int, rng: random.Random) -> list[bool]:
    """Run random replacement with k pages on the trace. Return one hit flag per request."""
    cache = RandomReplacement(k, rng)
    return [cache.access(p) for p in trace]
