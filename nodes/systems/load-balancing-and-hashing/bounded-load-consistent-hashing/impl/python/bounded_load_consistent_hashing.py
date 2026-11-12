# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bounded-load-consistent-hashing/. The authors are listed in prov/5BJKG5.jsonl.

"""Consistent hashing with bounded loads (Mirrokni, Thorup and Zadimoghaddam, 2018).

Bins and balls are hashed to a ring. Every bin has the capacity
ceil(c * m / n), where m is the number of balls, n the number of bins and
c = 1 + eps. A ball goes to the first bin clockwise from its hash that is
not full.

The structure keeps two invariants after every update:
  (C) no bin holds more than the capacity, and
  (I) every bin that a ball passes on its walk, before its own bin, is full.
Updates change m or n, and so the capacity. REPAIR restores the invariants:
it first moves balls forward out of bins that are over the capacity, and then
pulls balls back into bins that are not full but are passed by some ball.
The counter `moves` counts the balls that change bin, not the new ball itself.
"""

import bisect
import hashlib
from collections.abc import Callable, Hashable
from fractions import Fraction


def ring_point(name: str, person: bytes) -> int:
    d = hashlib.blake2b(name.encode(), digest_size=8, person=person).digest()
    return int.from_bytes(d, "big")


def bin_hash(name: str) -> int:
    return ring_point(name, b"bounded-bin")


def ball_hash(name: str) -> int:
    return ring_point(name, b"bounded-ball")


class BoundedLoadRing:
    def __init__(
        self,
        bins: list[str],
        eps: Fraction | int | str,
        bin_point: Callable[[str], int] = bin_hash,
        ball_point: Callable[[Hashable], int] = ball_hash,
    ) -> None:
        self.c = 1 + Fraction(eps)
        if self.c <= 1:
            raise ValueError("eps must be positive")
        self.bin_point = bin_point
        self.ball_point = ball_point
        self.points: list[int] = []  # sorted bin points
        self.order: list[str] = []  # bin names in ring order
        self.members: dict[str, set] = {}
        self.where: dict[Hashable, str] = {}
        self.h: dict[Hashable, int] = {}
        self.moves = 0
        for b in bins:
            self._place_bin(b)

    # ---- the ring -------------------------------------------------------

    def _place_bin(self, name: str) -> None:
        p = self.bin_point(name)
        i = bisect.bisect_left(self.points, p)
        if i < len(self.points) and self.points[i] == p:
            raise ValueError("two bins hash to the same point")
        self.points.insert(i, p)
        self.order.insert(i, name)
        self.members[name] = set()

    def capacity(self) -> int:
        n = len(self.order)
        v = self.c * len(self.where) / n
        return -((-v.numerator) // v.denominator)  # the ceiling

    def load(self, b: str) -> int:
        return len(self.members[b])

    def start(self, x: Hashable) -> int:
        """The index of the first bin at or after the hash of x."""
        i = bisect.bisect_left(self.points, self.h[x])
        return i % len(self.points)

    def walk_length(self, x: Hashable) -> int:
        n = len(self.order)
        return (self.order.index(self.where[x]) - self.start(x)) % n

    def passes(self, x: Hashable, i: int) -> bool:
        """True if bin number i lies on the walk of x strictly before its bin."""
        n = len(self.order)
        st = self.start(x)
        return (i - st) % n < self.walk_length(x)

    def _move(self, x: Hashable, b: str) -> None:
        self.members[self.where[x]].discard(x)
        self.members[b].add(x)
        self.where[x] = b
        self.moves += 1

    def _first_open(self, i: int, cap: int) -> int:
        n = len(self.order)
        for s in range(n):
            j = (i + s) % n
            if self.load(self.order[j]) < cap:
                return j
        raise AssertionError("no bin has room")

    # ---- updates --------------------------------------------------------

    def insert(self, x: Hashable) -> str:
        if x in self.where:
            raise KeyError("ball already present")
        self.h[x] = self.ball_point(x)
        self.where[x] = None  # @line L1
        cap = self.capacity()
        i = self.start(x)  # @line L2
        n = len(self.order)
        while self.load(self.order[i]) >= cap:  # @line L3
            i = (i + 1) % n  # @line L4
        b = self.order[i]
        self.members[b].add(x)  # @line L5
        self.where[x] = b
        self._repair()  # @line L6
        return self.where[x]

    def delete(self, x: Hashable) -> None:
        b = self.where.pop(x)  # @line L7
        self.members[b].discard(x)
        del self.h[x]
        self._repair()  # @line L8

    def add_bin(self, name: str) -> None:
        self._place_bin(name)
        self._repair()

    def remove_bin(self, name: str) -> None:
        i = self.order.index(name)
        balls = sorted(self.members[name], key=repr)
        del self.points[i], self.order[i], self.members[name]
        if not self.order:
            raise ValueError("cannot remove the last bin")
        cap = self.capacity()
        for x in balls:  # each of these balls has to move
            j = self._first_open(self.start(x), cap)
            self.where[x] = self.order[j]
            self.members[self.order[j]].add(x)
            self.moves += 1
        self._repair()

    def _repair(self) -> None:
        n = len(self.order)
        cap = self.capacity()
        for i in range(n):  # @line L9
            b = self.order[i]
            while self.load(b) > cap:  # @line L10
                x = min(self.members[b], key=repr)
                j = self._first_open((i + 1) % n, cap)
                self._move(x, self.order[j])  # @line L11
        moved = True
        while moved:  # @line L12
            moved = False  # @line L13
            for i in range(n):  # @line L14
                b = self.order[i]
                while self.load(b) < cap:
                    x = self._candidate(i, cap)  # @line L15
                    if x is None:
                        break
                    self._move(x, b)  # @line L16
                    moved = True
        # @line L17: the loop of line L12 stops after a sweep with no move

    def _candidate(self, i: int, cap: int) -> Hashable | None:
        """A ball that passes bin i, looked for up to the next bin that is not full."""
        n = len(self.order)
        for s in range(1, n):
            j = (i + s) % n
            b = self.order[j]
            for x in sorted(self.members[b], key=repr):
                if self.passes(x, i):
                    return x
            if self.load(b) < cap:
                break
        return None

    def lookup(self, x: Hashable) -> str:
        return self.where[x]

    def loads(self) -> dict[str, int]:
        return {b: len(s) for b, s in self.members.items()}
