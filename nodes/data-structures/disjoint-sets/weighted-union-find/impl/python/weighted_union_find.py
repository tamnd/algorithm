# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-union-find/. The authors are listed in prov/N5NH9D.jsonl.

import operator
from collections.abc import Callable, Hashable
from typing import Generic, TypeVar

T = TypeVar("T", bound=Hashable)
V = TypeVar("V")


class WeightedUnionFind(Generic[T, V]):
    """Union-find with a value of an abelian group on each edge to the parent.

    The potential of x is the sum of the values on its path to the root. The
    structure keeps facts val(x) - val(y) = d, checks each new fact, and
    answers val(x) - val(y) for two elements of one set. It uses union by
    size and path compression, so each operation takes O(log n) time in the
    worst case and O(alpha(n)) amortized.
    """

    def __init__(
        self,
        add: Callable[[V, V], V] = operator.add,
        neg: Callable[[V], V] = operator.neg,
        zero: V = 0,  # type: ignore[assignment]
    ) -> None:
        self.add = add
        self.neg = neg
        self.zero = zero
        self.parent: dict[T, T] = {}
        self.w: dict[T, V] = {}
        self.size: dict[T, int] = {}

    def __contains__(self, x: object) -> bool:
        return x in self.parent

    def make_set(self, x: T) -> None:
        """Add x as a set of its own. Raise ValueError if x is already present."""
        if x in self.parent:
            raise ValueError("element already present")
        self.parent[x] = x  # @line L1
        self.size[x] = 1
        self.w[x] = self.zero  # @line L2

    def find(self, x: T) -> T:
        """Return the root of x. Afterwards w[x] is the potential of x."""
        p, w = self.parent, self.w
        path = []
        while p[x] != x:  # @line L3
            path.append(x)
            x = p[x]
        root = x  # @line L4
        acc = self.zero
        for v in reversed(path):
            acc = self.add(w[v], acc)  # @line L5
            w[v] = acc
            p[v] = root  # @line L6
        return root  # @line L7

    def diff(self, x: T, y: T) -> V | None:
        """Return val(x) - val(y) if the facts fix it, else None."""
        if self.find(x) != self.find(y):  # @line L8
            return None
        return self.add(self.w[x], self.neg(self.w[y]))  # @line L9

    def union(self, x: T, y: T, d: V) -> bool:
        """Add the fact val(x) - val(y) = d. Return False if it contradicts the earlier facts."""
        rx, ry = self.find(x), self.find(y)  # @line L10
        w = self.w
        if rx == ry:  # @line L11
            return self.add(w[x], self.neg(w[y])) == d
        if self.size[rx] > self.size[ry]:  # @line L12
            x, y, rx, ry, d = y, x, ry, rx, self.neg(d)
        self.parent[rx] = ry  # @line L13
        w[rx] = self.add(self.add(d, w[y]), self.neg(w[x]))
        self.size[ry] += self.size.pop(rx)  # @line L14
        return True

    def connected(self, x: T, y: T) -> bool:
        """Return True if x and y are in the same set."""
        return self.find(x) == self.find(y)

    def potential(self, x: T) -> V:
        """Return the potential of x, its value relative to its root."""
        self.find(x)
        return self.w[x] if self.parent[x] != x else self.zero

    def check_invariant(self) -> None:
        """Check the forest, the sizes at the roots, and the zero value at each root."""
        n = len(self.parent)
        count: dict[T, int] = {}
        for x in self.parent:
            y, steps = x, 0
            while self.parent[y] != y:
                y = self.parent[y]
                steps += 1
                assert steps < n
            count[y] = count.get(y, 0) + 1
        assert count == self.size
        for r in self.size:
            assert self.parent[r] == r and self.w[r] == self.zero
