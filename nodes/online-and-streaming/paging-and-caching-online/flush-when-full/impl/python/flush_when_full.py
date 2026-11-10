# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flush-when-full/. The authors are listed in prov/9TFRYX.jsonl.

from collections.abc import Hashable, Iterable


class FlushWhenFull:
    """An online FWF cache of size k.

    Cost per request: O(1) expected time, with the flush paid by the loads
    that filled the cache. Space: O(k).
    """

    def __init__(self, k: int) -> None:
        if k < 1:
            raise ValueError("k must be at least 1")
        self.k = k
        self.cache: set[Hashable] = set()  # @line L1
        self.faults = 0
        self.flushes = 0

    def request(self, p: Hashable) -> set[Hashable]:
        """Serve a request for p. Return the set of evicted pages."""
        evicted: set[Hashable] = set()
        if p not in self.cache:  # @line L4
            self.faults += 1  # @line L5
            if len(self.cache) == self.k:  # @line L6
                evicted, self.cache = self.cache, set()  # @line L7
                self.flushes += 1
            self.cache.add(p)  # @line L8
        return evicted


def flush_when_full(sigma: Iterable[Hashable], k: int) -> int:
    """Return the number of faults of FWF on sigma, from an empty cache of size k.

    Precondition: k >= 1 and the pages are hashable.
    Cost: O(n) expected time and O(k) space, with n requests.
    """
    cache = FlushWhenFull(k)
    for p in sigma:  # @line L2
        cache.request(p)  # @line L3
    return cache.faults  # @line L9
