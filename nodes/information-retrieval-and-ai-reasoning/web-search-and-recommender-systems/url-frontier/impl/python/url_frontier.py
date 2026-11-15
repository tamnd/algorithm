# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/url-frontier/. The authors are listed in prov/91KJAA.jsonl.
"""The two-stage URL frontier of Najork and Heydon (Manning, Raghavan and Schuetze, Section 20.2.3).

Front queues hold URLs by priority (index 0 is the highest). Back queues
hold URLs of one host each. A min-heap orders the nonempty back queues by
the earliest time at which their host may be contacted again. The
frontier remembers that time for every host it has served, so a host that
leaves its back queue and comes back later still gets its full gap.
"""

import heapq
import random
from collections import deque
from typing import Callable, Optional


def host_of(url: str) -> str:
    """The host part of a URL of the form scheme://host/path."""
    rest = url.split("://", 1)[-1]
    return rest.split("/", 1)[0]


class URLFrontier:
    def __init__(self, front: int, back: int, delay: Callable[[str], float], rng: Optional[random.Random] = None, host: Callable[[str], str] = host_of) -> None:
        """front and back are the numbers of queues. delay(h) is the politeness gap of host h.

        With rng None the front queue selector is strict: it always takes the
        highest priority queue that is not empty. With an rng it picks a
        nonempty queue i with weight front - i, which favours high priority
        but serves every queue.
        """
        if front < 1 or back < 1:
            raise ValueError("need at least one front queue and one back queue")
        self.front = [deque() for _ in range(front)]
        self.back: list[deque] = [deque() for _ in range(back)]
        self.owner: list[Optional[str]] = [None] * back  # host of each back queue
        self.queue_of: dict[str, int] = {}  # host -> its back queue
        self.heap: list[tuple[float, int]] = []  # (earliest fetch time, back queue)
        self.free = list(range(back - 1, -1, -1))  # empty back queues, not in the heap
        self.next_ok: dict[str, float] = {}  # host -> earliest time of its next fetch
        self.seen: set[str] = set()
        self.delay, self.rng, self.host = delay, rng, host
        self.waiting = 0  # URLs in the front queues
        self.on_pull: Optional[Callable[[str, int], None]] = None  # test hook

    def add(self, url: str, priority: int) -> bool:
        """Insert a URL with a priority in 0 .. front - 1. Return False if it was seen before."""
        if url in self.seen:  # @line L1
            return False
        self.seen.add(url)  # @line L2
        self.front[priority].append(url)
        self.waiting += 1
        return True

    def _select_front(self) -> int:
        live = [i for i, q in enumerate(self.front) if q]
        if self.rng is None:
            return live[0]
        weights = [len(self.front) - i for i in live]
        return self.rng.choices(live, weights)[0]

    def _refill(self, j: int, now: float) -> None:
        """Move URLs from the front queues to the back stage until back queue j gets a new host."""
        while self.waiting:  # @line L11
            i = self._select_front()  # @line L12
            url = self.front[i].popleft()  # @line L13
            self.waiting -= 1
            if self.on_pull:
                self.on_pull(url, i)
            h = self.host(url)
            if h in self.queue_of:  # @line L14
                self.back[self.queue_of[h]].append(url)
            else:  # @line L15
                self.owner[j] = h
                self.queue_of[h] = j
                self.back[j].append(url)
                heapq.heappush(self.heap, (max(now, self.next_ok.get(h, now)), j))
                return
        self.free.append(j)  # @line L16

    def next_url(self, now: float) -> Optional[tuple[str, float]]:
        """Return (url, start time) with start >= now, or None if the frontier is empty."""
        while self.free and self.waiting:  # @line L3
            self._refill(self.free.pop(), now)
        if not self.heap:  # @line L4
            return None
        t, j = heapq.heappop(self.heap)  # @line L5
        start = max(now, t)  # @line L6
        url = self.back[j].popleft()
        h = self.owner[j]
        assert h is not None
        self.next_ok[h] = start + self.delay(h)  # @line L7
        if self.back[j]:  # @line L8
            heapq.heappush(self.heap, (self.next_ok[h], j))
        else:  # @line L9
            del self.queue_of[h]
            self.owner[j] = None
            self._refill(j, start)
        return url, start  # @line L10

    def __len__(self) -> int:
        return self.waiting + sum(len(q) for q in self.back)
