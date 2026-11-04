# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/disjoint-set-forest/. The authors are listed in prov/B24A25.jsonl.

from collections.abc import Hashable
from typing import Generic, TypeVar

T = TypeVar("T", bound=Hashable)


class DisjointSetForest(Generic[T]):
    """Disjoint sets as a forest with union by rank and path compression.

    Each element has a parent and a rank. A root is its own parent and is
    the representative of its tree. make_set takes O(1) time; find and union
    take O(log n) worst-case time and O(alpha(n)) amortized time, where n is
    the number of elements. find needs no recursion: it walks up to the root,
    then walks the path again and points each node at the root.
    """

    def __init__(self) -> None:
        self.parent: dict[T, T] = {}
        self.rank: dict[T, int] = {}
        self.count = 0

    def __contains__(self, x: object) -> bool:
        return x in self.parent

    def make_set(self, x: T) -> None:
        """Add x as a set of its own. Raise ValueError if x is already present."""
        if x in self.parent:
            raise ValueError("element already present")
        self.parent[x] = x  # @line L1
        self.rank[x] = 0  # @line L2
        self.count += 1

    def find(self, x: T) -> T:
        """Return the root of the tree of x, and compress the path to it."""
        p = self.parent
        root = x
        while p[root] != root:  # @line L3
            root = p[root]
        while p[x] != root:
            p[x], x = root, p[x]  # @line L4
        return root  # @line L5

    def union(self, x: T, y: T) -> bool:
        """Merge the sets of x and y. Return False if they were already one set."""
        x, y = self.find(x), self.find(y)  # @line L6
        if x == y:  # @line L7
            return False
        if self.rank[x] > self.rank[y]:  # @line L8
            self.parent[y] = x
        else:
            self.parent[x] = y  # @line L9
            if self.rank[x] == self.rank[y]:  # @line L10
                self.rank[y] += 1
        self.count -= 1
        return True

    def connected(self, x: T, y: T) -> bool:
        """Return True if x and y are in the same set."""
        return self.find(x) == self.find(y)

    def check_invariant(self) -> None:
        """Check that the parent pointers form a forest and that ranks grow strictly upward."""
        roots = 0
        for x, px in self.parent.items():
            if px == x:
                roots += 1
            else:
                assert self.rank[x] < self.rank[px]
        assert roots == self.count
        n = len(self.parent)
        for x in self.parent:
            if self.parent[x] == x:
                size = sum(1 for y in self.parent if self._root_no_compress(y) == x)
                assert size >= 1 << self.rank[x]
                assert self.rank[x] <= n.bit_length() - 1

    def _root_no_compress(self, x: T) -> T:
        steps = 0
        while self.parent[x] != x:
            x = self.parent[x]
            steps += 1
            assert steps <= len(self.parent)
        return x
