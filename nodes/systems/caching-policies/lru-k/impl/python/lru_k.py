# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lru-k/. The authors are listed in prov/YZK836.jsonl.

import heapq
import math
from collections.abc import Hashable, Iterable


class LRUK:
    """LRU-K of O'Neil, O'Neil and Weikum (1993) on a buffer of k pages.

    HIST[p] holds the times of the last K uncorrelated references to p, the
    newest first, with 0 for "none". LAST[p] is the time of the latest
    reference. A reference within crp (the correlated reference period) of the
    latest one is correlated and only moves LAST. A miss evicts, among the
    pages whose latest reference is older than crp, the page with the largest
    backward K-distance t - HIST[p][K-1] (infinite when HIST[p][K-1] = 0),
    the least recently used one on a tie. The history of an evicted page is
    kept for rip time units (the retained information period).
    """

    def __init__(self, k: int, K: int = 2, crp: int = 0, rip: float = math.inf) -> None:
        if k < 1 or K < 1:
            raise ValueError("the buffer size k and K must be at least 1")
        if crp < 0 or rip < 0:
            raise ValueError("crp and rip must not be negative")
        self.k, self.K, self.crp, self.rip = k, K, crp, rip
        self.t = 0
        self.hist: dict[Hashable, list[int]] = {}
        self.last: dict[Hashable, int] = {}
        self.buffer: set[Hashable] = set()
        self.retained: list[tuple[int, Hashable]] = []  # (LAST, page) of evicted pages
        self.evicted: Hashable | None = None

    def __contains__(self, p: Hashable) -> bool:
        return p in self.buffer

    def __len__(self) -> int:
        return len(self.buffer)

    def contents(self) -> set[Hashable]:
        return set(self.buffer)

    def distance(self, p: Hashable) -> float:
        """Backward K-distance of p at the current time."""
        h = self.hist[p][self.K - 1]
        return math.inf if h == 0 else self.t - h

    def _purge(self) -> None:
        """Forget the history of evicted pages not referenced for more than rip."""
        while self.retained and self.t - self.retained[0][0] > self.rip:
            last, q = heapq.heappop(self.retained)
            if q not in self.buffer and self.last.get(q) == last:
                del self.hist[q], self.last[q]

    def access(self, p: Hashable) -> bool:
        """Serve the reference to p at the next time step. Return True on a hit."""
        self.t += 1
        t, K = self.t, self.K
        self.evicted = None
        self._purge()
        if p in self.buffer:  # @line L1
            h = self.hist[p]
            if t - self.last[p] > self.crp:  # @line L2
                period = self.last[p] - h[0]  # @line L3
                for i in range(K - 1, 0, -1):  # @line L4
                    h[i] = h[i - 1] + period if h[i - 1] else 0
                h[0] = t  # @line L5
            self.last[p] = t  # @line L6
            return True  # @line L7
        if len(self.buffer) == self.k:  # @line L8
            eligible = [q for q in self.buffer if t - self.last[q] > self.crp]  # @line L9
            if not eligible:
                eligible = list(self.buffer)
            victim = min(eligible, key=lambda q: (self.hist[q][K - 1], self.last[q]))  # @line L10
            self.buffer.remove(victim)  # @line L11
            heapq.heappush(self.retained, (self.last[victim], victim))
            self.evicted = victim
        if p in self.hist:  # @line L12
            h = self.hist[p]
            for i in range(K - 1, 0, -1):  # @line L13
                h[i] = h[i - 1]
        else:
            self.hist[p] = [0] * K  # @line L14
        self.hist[p][0] = t  # @line L15
        self.last[p] = t
        self.buffer.add(p)  # @line L16
        return False  # @line L17


def lru_k_hits(trace: Iterable[Hashable], k: int, K: int = 2, crp: int = 0,
               rip: float = math.inf) -> list[bool]:
    """Run LRU-K with a buffer of k pages on the trace. Return one hit flag per request."""
    cache = LRUK(k, K, crp, rip)
    return [cache.access(p) for p in trace]
