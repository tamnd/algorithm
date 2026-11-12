# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mq-cache/. The authors are listed in prov/VFWZYA.jsonl.

from collections import OrderedDict
from collections.abc import Hashable, Iterable


class MQ:
    """Multi-queue replacement (Zhou, Philbin and Li 2001) on a cache of k blocks.

    There are m LRU queues Q[0..m-1], each an OrderedDict with its head (the
    LRU end) first. A block with reference count f lives in queue
    min(m - 1, floor(log2 f)). Each block has an expiry time; when the head of
    Q[j], j >= 1, has expired, it moves to the tail of Q[j-1]. Victims come
    from the head of the lowest non-empty queue, and their identifiers and
    counts go to Qout, a FIFO history of at most h entries.
    """

    def __init__(self, k: int, m: int, life: int, h: int) -> None:
        if k < 1 or m < 1 or life < 0 or h < 0:
            raise ValueError("need k >= 1, m >= 1, life >= 0 and h >= 0")
        self.k, self.m, self.life, self.h = k, m, life, h
        self.q: list[OrderedDict[Hashable, None]] = [OrderedDict() for _ in range(m)]
        self.where: dict[Hashable, int] = {}
        self.freq: dict[Hashable, int] = {}
        self.expire: dict[Hashable, int] = {}
        self.qout: OrderedDict[Hashable, int] = OrderedDict()
        self.now = 0
        self.evicted: Hashable | None = None

    def __contains__(self, x: Hashable) -> bool:
        return x in self.where

    def __len__(self) -> int:
        return len(self.where)

    def queue_of(self, f: int) -> int:
        return min(self.m - 1, f.bit_length() - 1)

    def access(self, x: Hashable) -> bool:
        """Serve one request. Return True on a hit, False on a miss."""
        self.evicted = None
        self.now += 1  # @line L1
        if x in self.where:
            del self.q[self.where[x]][x]  # @line L2
            self.freq[x] += 1
            hit = True
        else:  # @line L3
            if x in self.qout:  # @line L4
                self.freq[x] = self.qout.pop(x) + 1
            else:
                self.freq[x] = 1  # @line L5
            if len(self.where) == self.k:  # @line L6
                self._evict()
            hit = False  # @line L7
        self.expire[x] = self.now + self.life  # @line L8
        j = self.queue_of(self.freq[x])  # @line L9
        self.q[j][x] = None
        self.where[x] = j
        self._adjust()  # @line L10
        return hit

    def _evict(self) -> None:
        j = next(i for i in range(self.m) if self.q[i])  # @line L11
        v, _ = self.q[j].popitem(last=False)
        del self.where[v], self.expire[v]
        f = self.freq.pop(v)
        self.evicted = v
        if self.h > 0 and len(self.qout) == self.h:  # @line L12
            self.qout.popitem(last=False)
        if self.h > 0:  # @line L13
            self.qout[v] = f

    def _adjust(self) -> None:
        for j in range(1, self.m):  # @line L14
            if not self.q[j]:  # @line L15
                continue
            c = next(iter(self.q[j]))
            if self.expire[c] < self.now:  # @line L16
                del self.q[j][c]  # @line L17
                self.q[j - 1][c] = None
                self.where[c] = j - 1
                self.expire[c] = self.now + self.life


def mq_hits(trace: Iterable[Hashable], k: int, m: int, life: int, h: int) -> list[bool]:
    """Run MQ with k blocks, m queues, the given lifeTime and a Qout of h entries."""
    cache = MQ(k, m, life, h)
    return [cache.access(x) for x in trace]
