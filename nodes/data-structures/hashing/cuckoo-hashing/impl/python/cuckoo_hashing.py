# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cuckoo-hashing/. The authors are listed in prov/FHYWMC.jsonl.

import math
import random
from fractions import Fraction
from collections.abc import Callable, Hashable, Iterator
from typing import Any

HashFn = Callable[[Any], int]
Factory = Callable[[int, random.Random], tuple[HashFn, HashFn]]

P = (1 << 61) - 1  # a Mersenne prime


def random_pair(r: int, rng: random.Random) -> tuple[HashFn, HashFn]:
    """Two independent functions k -> ((a * hash(k) + b) mod P) mod r."""

    def make() -> HashFn:
        a, b = rng.randrange(1, P), rng.randrange(P)
        return lambda k: ((a * (hash(k) % P) + b) % P) % r

    return make(), make()


class CuckooHashing:
    """A dictionary stored by cuckoo hashing in two tables of r cells.

    Each key k is in T1[h1(k)] or in T2[h2(k)], so search and delete look at
    two cells: O(1) time in the worst case. An insert moves keys between their
    two cells for at most MaxLoop rounds, then rehashes with new functions.
    The tables keep r >= (1 + eps) * n. With random enough hash functions an
    insert takes O(1) expected amortized time.
    """

    def __init__(
        self,
        r: int = 8,
        eps: float | Fraction = Fraction(1, 10),
        factory: Factory = random_pair,
        rng: random.Random | None = None,
    ) -> None:
        self.eps = Fraction(str(eps)) if isinstance(eps, float) else Fraction(eps)
        if r < 1 or not 0 < self.eps <= 1:
            raise ValueError("need r >= 1 and 0 < eps <= 1")
        self.factory = factory
        self.rng = rng if rng is not None else random.Random()
        self.rehashes = 0
        self._reset(r)

    def _reset(self, r: int) -> None:
        self.r = r
        self.h1, self.h2 = self.factory(r, self.rng)
        self.max_loop = max(1, math.ceil(3 * math.log(r) / math.log(1 + float(self.eps))))
        self.t1: list[tuple[Any, Any] | None] = [None] * r
        self.t2: list[tuple[Any, Any] | None] = [None] * r
        self.n = 0

    def search(self, k: Hashable) -> Any:
        """Return the value of k, or None if k is not a key. Two cells."""
        c = self.t1[self.h1(k)]
        if c is not None and c[0] == k:  # @line L1
            return c[1]
        c = self.t2[self.h2(k)]
        if c is not None and c[0] == k:  # @line L2
            return c[1]
        return None  # @line L3

    def contains(self, k: Hashable) -> bool:
        c1, c2 = self.t1[self.h1(k)], self.t2[self.h2(k)]
        return (c1 is not None and c1[0] == k) or (c2 is not None and c2[0] == k)

    def _place(self, x: tuple[Any, Any]) -> tuple[Any, Any] | None:
        """The eviction walk. Return None if x found a cell, else the pair left over."""
        y: tuple[Any, Any] | None = x  # @line L6
        for _ in range(self.max_loop):  # @line L7
            i = self.h1(y[0])
            y, self.t1[i] = self.t1[i], y  # @line L8
            if y is None:  # @line L9
                self.n += 1
                return None
            j = self.h2(y[0])
            y, self.t2[j] = self.t2[j], y  # @line L10
            if y is None:  # @line L11
                self.n += 1
                return None
        return y

    def insert(self, k: Hashable, v: Any) -> None:
        """Set the value of k to v."""
        i, j = self.h1(k), self.h2(k)
        for t, p in ((self.t1, i), (self.t2, j)):
            c = t[p]
            if c is not None and c[0] == k:  # @line L4
                t[p] = (k, v)
                return
        if self.r < (1 + self.eps) * (self.n + 1):  # @line L5
            self._rehash(2 * self.r, [])
        left = self._place((k, v))
        if left is not None:
            self._rehash(self.r, [left])  # @line L12

    def delete(self, k: Hashable) -> bool:
        """Remove k. Return True if k was a key. Two cells, no tombstone."""
        i = self.h1(k)
        c = self.t1[i]
        if c is not None and c[0] == k:  # @line L13
            self.t1[i] = None
            self.n -= 1
            return True
        j = self.h2(k)
        c = self.t2[j]
        if c is not None and c[0] == k:  # @line L14
            self.t2[j] = None
            self.n -= 1
            return True
        return False

    def _rehash(self, r2: int, extra: list[tuple[Any, Any]]) -> None:
        """Put all pairs and the pairs of extra into new tables of r2 cells."""
        pairs = [c for c in self.t1 + self.t2 if c is not None] + extra  # @line L15
        while True:
            self.rehashes += 1
            self._reset(r2)  # @line L16
            if all(self._place(x) is None for x in pairs):  # @line L17
                return

    def __len__(self) -> int:
        return self.n

    def items(self) -> Iterator[tuple[Any, Any]]:
        for c in self.t1 + self.t2:
            if c is not None:
                yield c

    def check_invariant(self) -> None:
        """Assert (C1) to (C4) of the page."""
        keys = []
        for i, c in enumerate(self.t1):
            if c is not None:
                assert self.h1(c[0]) == i  # (C1)
                keys.append(c[0])
        for j, c in enumerate(self.t2):
            if c is not None:
                assert self.h2(c[0]) == j  # (C1)
                keys.append(c[0])
        assert len(keys) == len(set(keys))  # (C2)
        assert self.n == len(keys)  # (C3)
        assert self.r >= (1 + self.eps) * self.n  # (C4)
