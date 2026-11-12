# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lfu/. The authors are listed in prov/4DET4E.jsonl.

from collections import OrderedDict
from collections.abc import Hashable, Iterable


class _FreqNode:
    """One frequency f: the cached pages with count f, least recently used first."""

    __slots__ = ("freq", "items", "prev", "next")

    def __init__(self, freq: int) -> None:
        self.freq = freq
        self.items: OrderedDict[Hashable, None] = OrderedDict()
        self.prev: _FreqNode = self
        self.next: _FreqNode = self


class LFU:
    """LFU on a cache of k pages, with the O(1) structure of Shah, Mitra and Matani.

    A circular doubly linked list holds one node per frequency that some cached
    page has, in increasing order of frequency, after a sentinel. Each node keeps
    its pages in LRU order. The count of a page starts at 1 when it is loaded and
    is lost when it is evicted. A miss with a full cache evicts the least recently
    used page among the pages with the smallest count.
    """

    def __init__(self, k: int) -> None:
        if k < 1:
            raise ValueError("the cache size k must be at least 1")
        self.k = k
        self.head = _FreqNode(0)  # sentinel
        self.node: dict[Hashable, _FreqNode] = {}
        self.evicted: Hashable | None = None

    def __contains__(self, p: Hashable) -> bool:
        return p in self.node

    def __len__(self) -> int:
        return len(self.node)

    def count(self, p: Hashable) -> int:
        return self.node[p].freq

    def contents(self) -> set[Hashable]:
        return set(self.node)

    def _node_after(self, x: _FreqNode, f: int) -> _FreqNode:
        """Return the node for frequency f right after x, creating it if needed."""
        if x.next.freq == f:
            return x.next
        y = _FreqNode(f)
        y.prev, y.next = x, x.next
        x.next.prev = y
        x.next = y
        return y

    def _remove(self, p: Hashable) -> None:
        x = self.node.pop(p)
        del x.items[p]
        if not x.items:
            x.prev.next = x.next
            x.next.prev = x.prev

    def access(self, p: Hashable) -> bool:
        """Serve one request. Return True on a hit, False on a miss."""
        self.evicted = None
        if p in self.node:  # @line L1
            x = self.node[p]
            y = self._node_after(x, x.freq + 1)  # @line L2
            y.items[p] = None  # @line L3
            self._remove(p)
            self.node[p] = y
            return True  # @line L4
        if len(self.node) == self.k:  # @line L5
            low = self.head.next  # @line L6
            q = next(iter(low.items))  # @line L7
            self._remove(q)  # @line L8
            self.evicted = q
        y = self._node_after(self.head, 1)  # @line L9
        y.items[p] = None
        self.node[p] = y
        return False  # @line L10


def lfu_hits(trace: Iterable[Hashable], k: int) -> list[bool]:
    """Run LFU with k pages on the trace. Return one hit flag per request."""
    cache = LFU(k)
    return [cache.access(p) for p in trace]
