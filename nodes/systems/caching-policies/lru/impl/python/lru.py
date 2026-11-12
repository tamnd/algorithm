# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lru/. The authors are listed in prov/C24R9P.jsonl.

from collections import OrderedDict
from collections.abc import Hashable, Iterable


class LRU:
    """The LRU replacement policy on a cache of k pages.

    The recency order is kept in an OrderedDict, with the least recently
    used page first. The page lru-cache builds the same order by hand with a
    hash map and a doubly linked list.
    """

    def __init__(self, k: int) -> None:
        if k < 1:
            raise ValueError("the cache size k must be at least 1")
        self.k = k
        self.order: OrderedDict[Hashable, None] = OrderedDict()
        self.evicted: Hashable | None = None

    def __contains__(self, p: Hashable) -> bool:
        return p in self.order

    def __len__(self) -> int:
        return len(self.order)

    def contents(self) -> list[Hashable]:
        """The cached pages, from the least to the most recently used."""
        return list(self.order)

    def access(self, p: Hashable) -> bool:
        """Serve one request. Return True on a hit, False on a miss."""
        self.evicted = None
        if p in self.order:  # @line L1
            self.order.move_to_end(p)  # @line L2
            return True  # @line L3
        if len(self.order) == self.k:  # @line L4
            self.evicted, _ = self.order.popitem(last=False)  # @line L5
        self.order[p] = None  # @line L6
        return False  # @line L7


def lru_hits(trace: Iterable[Hashable], k: int) -> list[bool]:
    """Run LRU with k pages on the trace. Return one hit flag per request."""
    cache = LRU(k)
    return [cache.access(p) for p in trace]
