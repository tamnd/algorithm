# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lfu-da/. The authors are listed in prov/6K0S3T.jsonl.

import heapq
from collections.abc import Hashable, Iterable


class LFUDA:
    """LFU with dynamic aging (Arlitt et al. 2000) on a cache of k objects.

    Each cached object i has a frequency F_i and a key K_i = C_i * F_i + L,
    with the cost C_i = 1 and the cache age L taken at its latest request.
    A miss with a full cache evicts the object of smallest key, the least
    recently used one on a tie, and sets L to the key of that object.
    A binary heap with lazy deletion holds the entries (K, time, object).
    """

    def __init__(self, k: int) -> None:
        if k < 1:
            raise ValueError("the cache size k must be at least 1")
        self.k = k
        self.age = 0  # L
        self.time = 0
        self.freq: dict[Hashable, int] = {}
        self.entry: dict[Hashable, tuple[int, int, Hashable]] = {}
        self.heap: list[tuple[int, int, Hashable]] = []
        self.evicted: Hashable | None = None

    def __contains__(self, p: Hashable) -> bool:
        return p in self.freq

    def __len__(self) -> int:
        return len(self.freq)

    def key(self, p: Hashable) -> int:
        return self.entry[p][0]

    def contents(self) -> set[Hashable]:
        return set(self.freq)

    def _push(self, p: Hashable) -> None:
        e = (self.freq[p] + self.age, self.time, p)  # K = C * F + L with C = 1
        self.entry[p] = e
        heapq.heappush(self.heap, e)
        if len(self.heap) > 2 * self.k + 16:  # drop stale entries
            self.heap = list(self.entry.values())
            heapq.heapify(self.heap)

    def access(self, p: Hashable) -> bool:
        """Serve one request. Return True on a hit, False on a miss."""
        self.evicted = None
        self.time += 1
        if p in self.freq:  # @line L1
            self.freq[p] += 1  # @line L2
            self._push(p)  # @line L3
            return True  # @line L4
        if len(self.freq) == self.k:  # @line L5
            while True:
                e = heapq.heappop(self.heap)  # @line L6
                if self.entry.get(e[2]) == e:
                    break
            q = e[2]
            self.age = e[0]  # @line L7
            del self.freq[q], self.entry[q]  # @line L8
            self.evicted = q
        self.freq[p] = 1  # @line L9
        self._push(p)  # @line L10
        return False  # @line L11


def lfu_da_hits(trace: Iterable[Hashable], k: int) -> list[bool]:
    """Run LFU-DA with k objects on the trace. Return one hit flag per request."""
    cache = LFUDA(k)
    return [cache.access(p) for p in trace]
