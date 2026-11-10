# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kmv-sketch/. The authors are listed in prov/CKX5V3.jsonl.
"""The k minimum values sketch (Bar-Yossef et al. 2002; Beyer et al. 2007)."""

import heapq
from typing import Callable, Hashable, Iterable

HASH_BITS = 64
SCALE = float(1 << HASH_BITS)


def unit(y: int) -> float:
    """Map a 64-bit hash value y to the point (y + 1) / 2^64 in (0, 1]."""
    return (y + 1) / SCALE


class KMV:
    """Keep the k smallest distinct hash values seen so far.

    h maps an item to a 64-bit integer and is assumed to be fully random.
    The state is k hash values of 64 bits plus the seed of h. An update
    costs one hash and O(log k) time; a query costs O(1) (O(k) for set
    operations between two sketches).
    """

    def __init__(self, k: int, h: Callable[[Hashable], int]) -> None:
        if k < 2:
            raise ValueError("k must be at least 2")
        self.k = k
        self.h = h
        self.heap: list[int] = []  # @line L1
        self.members: set[int] = set()

    def add(self, x: Hashable) -> None:
        y = self.h(x)  # @line L3
        if y in self.members or (len(self.heap) == self.k and y >= -self.heap[0]):  # @line L4
            return
        heapq.heappush(self.heap, -y)
        self.members.add(y)
        if len(self.heap) > self.k:  # @line L5
            self.members.discard(-heapq.heappop(self.heap))

    def add_all(self, stream: Iterable[Hashable]) -> None:
        for x in stream:  # @line L2
            self.add(x)

    def values(self) -> list[int]:
        """The kept hash values in increasing order."""
        return sorted(self.members)

    def estimate(self) -> float:
        if len(self.heap) < self.k:  # @line L6
            return float(len(self.heap))
        return (self.k - 1) / unit(-self.heap[0])  # @line L7

    def merge(self, other: "KMV") -> "KMV":
        """The sketch of the union: the k smallest values of both sketches together."""
        if other.k != self.k or other.h is not self.h:
            raise ValueError("sketches are not compatible")
        out = KMV(self.k, self.h)
        for y in heapq.nsmallest(self.k, self.members | other.members):
            out.members.add(y)
            out.heap.append(-y)
        heapq.heapify(out.heap)
        return out


def intersection_estimate(a: KMV, b: KMV) -> float:
    """Beyer et al.: (K / k) (k - 1) / v_k, with L the k smallest values of the union
    and K the number of values of L that are in both sketches."""
    u = a.merge(b)
    both = sum(1 for y in u.members if y in a.members and y in b.members)
    if len(u.members) < u.k:
        return float(both)
    return both / u.k * u.estimate()


def jaccard_estimate(a: KMV, b: KMV) -> float:
    """The fraction K / |L| of the union sample that lies in both sets."""
    u = a.merge(b)
    if not u.members:
        return 0.0
    both = sum(1 for y in u.members if y in a.members and y in b.members)
    return both / len(u.members)
