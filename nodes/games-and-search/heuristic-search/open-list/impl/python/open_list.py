# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/open-list/. The authors are listed in prov/B9C3HD.jsonl.

"""The open list of A*: a binary heap with lazy deletion and a table of best entries.

Each state has at most one live entry, the one recorded in best. Older heap
entries of the same state are stale and are skipped when they reach the top.
The order is: least f, then larger g, then the earlier push (first in, first
out). When the heap holds more than twice as many entries as there are live
states, plus a small slack, it is rebuilt from the live entries, so the space
stays linear in the number of live states.
"""

import heapq
import itertools
from collections.abc import Hashable
from typing import Optional

SLACK = 16


class OpenList:
    """OPEN for best-first search, with insert-or-lower in O(log n) amortized time."""

    def __init__(self) -> None:
        self.heap: list = []  # entries (f, -g, stamp, state)
        self.best: dict = {}  # state -> (g, f, stamp) of its live entry
        self.stamps = itertools.count()

    def __len__(self) -> int:
        return len(self.best)

    def __contains__(self, n: Hashable) -> bool:
        return n in self.best  # @line L10

    def g(self, n: Hashable):
        """The g of the live entry of n. Precondition: n is in OPEN."""
        return self.best[n][0]

    def push(self, n: Hashable, g, f) -> bool:
        """Put n in OPEN with (g, f), or replace its entry if g is smaller.

        Returns False and changes nothing when n is in OPEN with g' <= g.
        Cost: O(log n) amortized, n the number of heap entries.
        """
        if n in self.best and self.best[n][0] <= g:  # @line L1
            return False
        t = next(self.stamps)
        self.best[n] = (g, f, t)  # @line L2
        heapq.heappush(self.heap, (f, -g, t, n))  # @line L3
        self._compact()
        return True  # @line L4

    def pop_min(self) -> Optional[tuple]:
        """Remove and return (n, g, f) of least f, ties toward larger g, then FIFO.

        Returns None when OPEN is empty. Cost: O(log n) amortized.
        """
        while self.heap:  # @line L5
            f, neg_g, t, n = heapq.heappop(self.heap)  # @line L6
            entry = self.best.get(n)
            if entry is not None and entry[2] == t:  # @line L7
                del self.best[n]  # @line L8
                self._compact()
                return n, -neg_g, f
        return None  # @line L9

    def remove(self, n: Hashable) -> None:
        """Take n out of OPEN; its heap entry becomes stale. Cost: O(1) amortized."""
        self.best.pop(n, None)  # @line L11
        self._compact()

    def _compact(self) -> None:
        """Rebuild the heap from the live entries when most entries are stale."""
        if len(self.heap) > 2 * len(self.best) + SLACK:  # @line L12
            self.heap = [(f, -g, t, n) for n, (g, f, t) in self.best.items()]  # @line L13
            heapq.heapify(self.heap)

    def check_invariant(self) -> None:
        h = self.heap
        for i in range(1, len(h)):
            assert h[(i - 1) // 2] <= h[i], "heap order"
        live = {}
        for f, neg_g, t, n in h:
            if self.best.get(n, (None, None, None))[2] == t:
                assert n not in live, "two live entries"
                live[n] = (-neg_g, f, t)
        assert live == self.best, "every state of best has its entry"
        assert len(h) <= 2 * len(self.best) + SLACK, "space"
