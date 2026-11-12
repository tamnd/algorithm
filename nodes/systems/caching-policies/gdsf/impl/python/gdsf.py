# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gdsf/. The authors are listed in prov/J6DJ3W.jsonl.

"""Greedy-Dual-Size-Frequency (Cherkasova 1998).

Each cached file f has the key Pr(f) = L + Fr(f) * Cost(f) / Size(f), where Fr(f) counts
the requests to f since it entered the cache and L (the "clock") is raised to the key of
each evicted file. At a miss the key of the new file is computed first, with the current
L. The new file then takes part in the choice of victims: the files with the lowest keys
are chosen until the rest fits. If the new file is among them, it is not cached and
nothing is evicted.
"""

import heapq
from fractions import Fraction
from typing import Hashable, Iterable

Number = int | Fraction


class GDSF:
    """GDSF with a binary heap and lazy deletion. frequency=False keeps Fr(f) = 1."""

    def __init__(self, capacity: int, frequency: bool = True) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self.frequency = frequency
        self.used = 0
        self.L: Fraction = Fraction(0)
        self.key: dict[Hashable, Fraction] = {}
        self.freq: dict[Hashable, int] = {}
        self.size: dict[Hashable, int] = {}
        self._stamp: dict[Hashable, int] = {}
        self._clock = 0
        self._heap: list[tuple[Fraction, int, Hashable]] = []
        self.evicted: list[Hashable] = []

    def __contains__(self, f: Hashable) -> bool:
        return f in self.key

    def _push(self, f: Hashable, key: Fraction) -> None:
        self._clock += 1
        self.key[f] = key
        self._stamp[f] = self._clock
        heapq.heappush(self._heap, (key, self._clock, f))
        if len(self._heap) > 2 * len(self.key) + 16:
            self._heap = [(self.key[q], self._stamp[q], q) for q in self.key]
            heapq.heapify(self._heap)

    def _pop_valid(self) -> tuple[Fraction, int, Hashable]:
        while True:
            entry = heapq.heappop(self._heap)
            if self._stamp.get(entry[2]) == entry[1]:
                return entry

    def request(self, f: Hashable, size: int, cost: Number) -> bool:
        """Serve one request. Return True on a hit."""
        if size <= 0 or cost < 0:
            raise ValueError("size must be positive and cost non-negative")
        self.evicted = []
        if f in self.key:  # @line L1
            if self.frequency:
                self.freq[f] += 1  # @line L2
            self._push(f, self.L + self.freq[f] * Fraction(cost) / size)  # @line L3
            return True  # @line L4
        key = self.L + Fraction(cost) / size  # @line L5
        new = (key, self._clock + 1)  # the new file is the newest, so it loses ties
        chosen: list[tuple[Fraction, int, Hashable]] = []
        excess = self.used + size - self.capacity
        while excess > 0:  # @line L6
            top = self._pop_valid() if len(chosen) < len(self.key) else None  # @line L7
            if top is None or new < top[:2]:  # @line L8
                # f has the least key among the candidates: do not cache it, evict nothing
                for entry in ([top] if top is not None else []) + chosen:
                    heapq.heappush(self._heap, entry)
                return False  # @line L9
            chosen.append(top)  # @line L10
            excess -= self.size[top[2]]
        for _, _, q in chosen:  # @line L11
            self.used -= self.size.pop(q)
            del self.key[q], self.freq[q], self._stamp[q]
            self.evicted.append(q)
        if chosen:
            self.L = chosen[-1][0]  # @line L12
        self.freq[f] = 1
        self.size[f] = size  # @line L13
        self.used += size
        self._push(f, key)
        return False  # @line L14

    def contents(self) -> set:
        return set(self.key)


def gdsf(capacity: int, requests: Iterable[tuple[Hashable, int, Number]], frequency: bool = True) -> list[bool]:
    """Run GDSF on (file, size, cost) requests; return the hit flags."""
    cache = GDSF(capacity, frequency)
    return [cache.request(f, size, cost) for f, size, cost in requests]
