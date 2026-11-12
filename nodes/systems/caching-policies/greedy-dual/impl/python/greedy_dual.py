# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-dual/. The authors are listed in prov/F080QZ.jsonl.

"""GreedyDual and GreedyDual-Size with the inflation value L.

Each cached object p has a priority H[p]. On a request p gets H[p] = L + cost/size.
To make room, the object with the smallest H is evicted and L is raised to its H.
With all sizes 1 this is Young's GreedyDual for weighted paging. Ties are broken by
the least recent setting of H, so with all sizes and costs 1 the policy is LRU.
"""

import heapq
from fractions import Fraction
from typing import Hashable, Iterable

Number = int | Fraction


class GreedyDualSize:
    """GreedyDual-Size with a global inflation value L and a binary heap with lazy deletion."""

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self.used = 0
        self.L: Fraction = Fraction(0)
        self.H: dict[Hashable, Fraction] = {}
        self.size: dict[Hashable, int] = {}
        self._stamp: dict[Hashable, int] = {}
        self._clock = 0
        self._heap: list[tuple[Fraction, int, Hashable]] = []
        self.evicted: list[Hashable] = []

    def __contains__(self, key: Hashable) -> bool:
        return key in self.H

    def _set(self, key: Hashable, cost: Number, size: int) -> None:
        self._clock += 1
        self.H[key] = self.L + Fraction(cost) / size
        self._stamp[key] = self._clock
        heapq.heappush(self._heap, (self.H[key], self._clock, key))
        if len(self._heap) > 2 * len(self.H) + 16:
            self._heap = [(self.H[q], self._stamp[q], q) for q in self.H]
            heapq.heapify(self._heap)

    def _pop_min(self) -> Hashable:
        while True:
            h, stamp, key = heapq.heappop(self._heap)
            if self._stamp.get(key) == stamp:
                return key

    def request(self, key: Hashable, size: int, cost: Number) -> bool:
        """Serve one request. Return True on a hit."""
        if size <= 0 or cost < 0:
            raise ValueError("size must be positive and cost non-negative")
        self.evicted: list[Hashable] = []
        if key in self.H:  # @line L1
            self._set(key, cost, size)  # @line L2
            return True  # @line L3
        if size > self.capacity:  # @line L4
            return False  # an object larger than the cache is served without loading it
        while self.used + size > self.capacity:  # @line L5
            victim = self._pop_min()  # @line L6
            self.evicted.append(victim)
            self.L = self.H[victim]  # @line L7
            self.used -= self.size.pop(victim)  # @line L8
            del self.H[victim]
            del self._stamp[victim]
        self.size[key] = size
        self.used += size
        self._set(key, cost, size)  # @line L9
        return False  # @line L10

    def contents(self) -> set:
        return set(self.H)


class GreedyDualSizeDecrement:
    """The original form: on each eviction subtract the smallest H from every cached object."""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.used = 0
        self.H: dict[Hashable, Fraction] = {}
        self.size: dict[Hashable, int] = {}
        self._stamp: dict[Hashable, int] = {}
        self._clock = 0

    def request(self, key: Hashable, size: int, cost: Number) -> bool:
        self._clock += 1
        if key in self.H:
            self.H[key] = Fraction(cost) / size
            self._stamp[key] = self._clock
            return True
        if size > self.capacity:
            return False
        while self.used + size > self.capacity:
            victim = min(self.H, key=lambda q: (self.H[q], self._stamp[q]))
            m = self.H[victim]
            for q in self.H:
                self.H[q] -= m
            self.used -= self.size.pop(victim)
            del self.H[victim]
            del self._stamp[victim]
        self.H[key] = Fraction(cost) / size
        self._stamp[key] = self._clock
        self.size[key] = size
        self.used += size
        return False

    def contents(self) -> set:
        return set(self.H)


def greedy_dual_size(capacity: int, requests: Iterable[tuple[Hashable, int, Number]]) -> list[bool]:
    """Run GreedyDual-Size on (key, size, cost) requests; return the hit flags."""
    cache = GreedyDualSize(capacity)
    return [cache.request(key, size, cost) for key, size, cost in requests]


def greedy_dual(k: int, requests: Iterable[tuple[Hashable, Number]]) -> list[bool]:
    """Young's GreedyDual for weighted paging: k slots, (key, cost) requests."""
    return greedy_dual_size(k, ((key, 1, cost) for key, cost in requests))


def miss_cost(capacity: int, requests: list[tuple[Hashable, int, Number]]) -> Fraction:
    """Total cost of the misses of GreedyDual-Size."""
    hits = greedy_dual_size(capacity, requests)
    return sum((Fraction(c) for (_, _, c), h in zip(requests, hits) if not h), Fraction(0))
