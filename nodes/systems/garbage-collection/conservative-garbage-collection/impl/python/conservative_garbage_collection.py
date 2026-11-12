# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conservative-garbage-collection/. The authors are listed in prov/BZ71R7.jsonl.

"""Conservative mark-sweep collection on a heap of plain integer words.

The collector has no type information. A word is a pointer candidate if it
lies inside the heap bounds and points to the start of an allocated object
(or, with `interior=True`, anywhere inside one). Each candidate is treated as
a real pointer: its object is marked, and the words of the object are scanned
in the same way. Objects are never moved, because an ambiguous word cannot be
updated: it might be an integer.
"""

import bisect
from typing import Iterable, Optional


class ConservativeHeap:
    def __init__(self, lo: int, size: int, interior: bool = True) -> None:
        if lo <= 0 or size <= 0:
            raise ValueError("the heap must lie at positive addresses")
        self.lo, self.hi = lo, lo + size  # the heap is [lo, hi)
        self.interior = interior
        self.mem = [0] * size
        self.starts: list[int] = []  # sorted starts of the allocated objects
        self.size_of: dict[int, int] = {}
        self.free: list[tuple[int, int]] = [(lo, size)]  # sorted (start, length)
        self.collections = 0

    # ---- memory ----------------------------------------------------------
    def load(self, a: int) -> int:
        return self.mem[a - self.lo]

    def store(self, a: int, w: int) -> None:
        self.mem[a - self.lo] = w

    def words(self, o: int) -> list[int]:
        return self.mem[o - self.lo: o - self.lo + self.size_of[o]]

    def alloc(self, n: int) -> Optional[int]:
        """First fit. Return the address of n zeroed words, or None."""
        for k, (s, m) in enumerate(self.free):
            if m >= n:
                if m == n:
                    del self.free[k]
                else:
                    self.free[k] = (s + n, m - n)
                bisect.insort(self.starts, s)
                self.size_of[s] = n
                return s
        return None

    def alloc_or_collect(self, n: int, roots: list[int]) -> Optional[int]:
        a = self.alloc(n)
        if a is None:
            self.collect(roots)
            a = self.alloc(n)
        return a

    def release(self, o: int) -> None:
        n = self.size_of.pop(o)
        del self.starts[bisect.bisect_left(self.starts, o)]
        for a in range(o, o + n):
            self.store(a, 0)
        k = bisect.bisect_left(self.free, (o, 0))
        self.free.insert(k, (o, n))
        if k + 1 < len(self.free) and o + n == self.free[k + 1][0]:  # merge right
            self.free[k] = (o, n + self.free[k + 1][1])
            del self.free[k + 1]
        if k > 0 and self.free[k - 1][0] + self.free[k - 1][1] == o:  # merge left
            s, m = self.free[k - 1]
            self.free[k - 1] = (s, m + self.free[k][1])
            del self.free[k]

    # ---- the collector -----------------------------------------------------
    def object_at(self, w: int) -> Optional[int]:
        """The allocated object that the word w points to, if any."""
        if not (self.lo <= w < self.hi):  # @line L8
            return None
        k = bisect.bisect_right(self.starts, w) - 1  # @line L9
        if k < 0:
            return None
        o = self.starts[k]
        if w == o or (self.interior and w < o + self.size_of[o]):
            return o
        return None

    def collect(self, roots: Iterable[int]) -> set[int]:
        """Mark from the ambiguous roots, then sweep. Return the freed starts."""
        self.collections += 1
        marked: set[int] = set()
        stack: list[int] = []

        def mark_if_pointer(w: int) -> None:
            o = self.object_at(w)
            if o is not None and o not in marked:  # @line L10
                marked.add(o)
                stack.append(o)

        for w in roots:  # @line L1
            mark_if_pointer(w)
        while stack:  # @line L2
            o = stack.pop()  # @line L3
            for w in self.words(o):  # @line L4
                mark_if_pointer(w)
        freed = set()
        for o in list(self.starts):  # @line L5
            if o not in marked:  # @line L6
                self.release(o)
                freed.add(o)
            else:
                marked.discard(o)  # @line L7
        return freed
