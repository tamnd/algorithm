# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/union-find-with-rollback/. The authors are listed in prov/CSRV45.jsonl.

from collections.abc import Hashable
from typing import Generic, TypeVar

T = TypeVar("T", bound=Hashable)


class UnionFindWithRollback(Generic[T]):
    """Union-find with union by size, no path compression, and undo of the latest unions.

    Each union pushes one record on a stack: the pair (child, root) of its
    link, or None for a union inside one set. undo pops a record and
    restores the two fields. find and union take O(log n) time in the worst
    case; undo takes O(1).
    """

    def __init__(self) -> None:
        self.parent: dict[T, T] = {}
        self.size: dict[T, int] = {}
        self.history: list[tuple[T, T] | None] = []
        self.count = 0

    def __contains__(self, x: object) -> bool:
        return x in self.parent

    def make_set(self, x: T) -> None:
        """Add x as a set of its own. Raise ValueError if x is already present."""
        if x in self.parent:
            raise ValueError("element already present")
        self.parent[x] = x  # @line L1
        self.size[x] = 1
        self.count += 1

    def find(self, x: T) -> T:
        """Return the root of x without changing the forest."""
        p = self.parent
        while p[x] != x:  # @line L2
            x = p[x]
        return x  # @line L3

    def union(self, x: T, y: T) -> bool:
        """Merge the sets of x and y and record the change. Return False if they were one set."""
        x, y = self.find(x), self.find(y)  # @line L4
        if x == y:  # @line L5
            self.history.append(None)
            return False
        if self.size[x] > self.size[y]:  # @line L6
            x, y = y, x
        self.history.append((x, y))  # @line L7
        self.parent[x] = y  # @line L8
        self.size[y] += self.size[x]
        self.count -= 1
        return True  # @line L9

    def undo(self) -> None:
        """Undo the most recent union. Raise IndexError if there is none."""
        e = self.history.pop()  # @line L10
        if e is None:  # @line L11
            return
        x, y = e  # @line L12
        self.size[y] -= self.size[x]  # @line L13
        self.parent[x] = x
        self.count += 1

    def snapshot(self) -> int:
        """Return the number of unions on the stack, to pass to rollback later."""
        return len(self.history)

    def rollback(self, t: int) -> None:
        """Undo unions until only the first t remain."""
        if not 0 <= t <= len(self.history):
            raise ValueError("no such snapshot")
        while len(self.history) > t:
            self.undo()

    def connected(self, x: T, y: T) -> bool:
        """Return True if x and y are in the same set."""
        return self.find(x) == self.find(y)

    def check_invariant(self) -> None:
        """Check the forest, the sizes, the size rule on each edge, and the records."""
        n = len(self.parent)
        sub = {x: 1 for x in self.parent}
        depth: dict[T, int] = {}
        for x in self.parent:
            y, d = x, 0
            while self.parent[y] != y:
                y = self.parent[y]
                d += 1
                assert d < max(n, 1)
                sub[y] += 1
            depth[x] = d
            assert (1 << d) <= n
        roots = [x for x in self.parent if self.parent[x] == x]
        assert len(roots) == self.count
        for r in roots:
            assert self.size[r] == sub[r]
        for x in self.parent:
            if self.parent[x] != x:
                assert 2 * sub[x] <= sub[self.parent[x]]
        for e in self.history:
            if e is not None:
                assert self.parent[e[0]] == e[1]
