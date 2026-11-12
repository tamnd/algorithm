# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fifo-replacement/. The authors are listed in prov/DTB1HB.jsonl.

from collections import deque
from collections.abc import Hashable, Iterable


class FIFO:
    """FIFO replacement on a cache of k pages.

    A queue holds the cached pages in load order, the oldest first, and a
    set answers membership. A hit changes nothing.
    """

    def __init__(self, k: int) -> None:
        if k < 1:
            raise ValueError("the cache size k must be at least 1")
        self.k = k
        self.queue: deque[Hashable] = deque()
        self.members: set[Hashable] = set()
        self.evicted: Hashable | None = None

    def __contains__(self, p: Hashable) -> bool:
        return p in self.members

    def __len__(self) -> int:
        return len(self.queue)

    def contents(self) -> list[Hashable]:
        """The cached pages, from the oldest to the newest load."""
        return list(self.queue)

    def access(self, p: Hashable) -> bool:
        """Serve one request. Return True on a hit, False on a miss."""
        self.evicted = None
        if p in self.members:  # @line L1
            return True  # @line L2
        if len(self.queue) == self.k:  # @line L3
            self.evicted = self.queue.popleft()  # @line L4
            self.members.remove(self.evicted)
        self.queue.append(p)  # @line L5
        self.members.add(p)
        return False  # @line L6


def fifo_hits(trace: Iterable[Hashable], k: int) -> list[bool]:
    """Run FIFO with k pages on the trace. Return one hit flag per request."""
    cache = FIFO(k)
    return [cache.access(p) for p in trace]
