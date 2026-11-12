# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hash-ring/. The authors are listed in prov/XP6DXP.jsonl.

"""A hash ring: points on the circle {0, ..., R - 1}, each with an owner.

The points are kept in a sorted Python list, so successor queries are a
binary search. Inserts and removes shift the list, which is O(N) time but
fast in practice; a balanced search tree gives O(log N).
"""

import bisect
from typing import Generic, Hashable, TypeVar

T = TypeVar("T", bound=Hashable)


class HashRing(Generic[T]):
    def __init__(self, size: int = 1 << 64) -> None:
        if size < 1:
            raise ValueError("the ring needs at least one position")
        self.size = size
        self.pos: list[int] = []
        self.owner: list[T] = []

    def __len__(self) -> int:
        return len(self.pos)

    def _index(self, x: int) -> int:
        return bisect.bisect_left(self.pos, x)

    def successor(self, x: int) -> tuple[int, T]:
        """The first point at or after x, clockwise."""
        if not self.pos:
            raise LookupError("empty ring")
        i = self._index(x % self.size)  # @line L1
        if i == len(self.pos):  # @line L2
            i = 0
        return self.pos[i], self.owner[i]  # @line L3

    def insert(self, p: int, owner: T) -> None:
        if not 0 <= p < self.size:
            raise ValueError("position outside the ring")
        i = self._index(p)  # @line L4
        if i < len(self.pos) and self.pos[i] == p:  # @line L5
            raise KeyError(f"position {p} is taken")
        self.pos.insert(i, p)  # @line L6
        self.owner.insert(i, owner)

    def remove(self, p: int) -> T:
        i = self._index(p)  # @line L7
        if i == len(self.pos) or self.pos[i] != p:
            raise KeyError(f"no point at {p}")
        del self.pos[i]  # @line L8
        return self.owner.pop(i)

    def arc(self, p: int) -> tuple[int, int]:
        """The arc (a, p] that the point p owns, as a pair (a, p) with
        a = predecessor of p, or p itself if p is the only point (the whole ring)."""
        i = self._index(p)
        if i == len(self.pos) or self.pos[i] != p:
            raise KeyError(f"no point at {p}")
        return self.pos[i - 1], p  # @line L9

    def arc_length(self, p: int) -> int:
        a, b = self.arc(p)
        return (b - a) % self.size or self.size

    def shares(self) -> dict[T, int]:
        """The number of ring positions that each owner owns."""
        out: dict[T, int] = {}
        for p, s in zip(self.pos, self.owner):
            out[s] = out.get(s, 0) + self.arc_length(p)
        return out

    def items(self) -> list[tuple[int, T]]:
        return list(zip(self.pos, self.owner))
