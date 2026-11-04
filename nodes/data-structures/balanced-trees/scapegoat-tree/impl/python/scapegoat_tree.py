# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scapegoat-tree/. The authors are listed in prov/096NRC.jsonl.

from __future__ import annotations

from fractions import Fraction
from typing import Generic, Iterator, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


K = TypeVar("K", bound=Ordered)


class Node(Generic[K]):
    """A plain search-tree node: no size, height or color is stored."""

    __slots__ = ("key", "left", "right")

    def __init__(self, key: K) -> None:
        self.key = key
        self.left: Node[K] | None = None
        self.right: Node[K] | None = None


def size(t: Node[K] | None) -> int:
    """Count the nodes of the subtree t. O(size)."""
    count = 0
    stack = [t]
    while stack:
        x = stack.pop()
        if x is not None:
            count += 1
            stack.append(x.left)
            stack.append(x.right)
    return count


def flatten(t: Node[K] | None) -> list[Node[K]]:
    """Return the nodes of t in key order. O(size)."""
    out: list[Node[K]] = []
    stack: list[Node[K]] = []
    x = t
    while stack or x is not None:
        while x is not None:
            stack.append(x)
            x = x.left
        x = stack.pop()
        out.append(x)
        x = x.right
    return out


def build(a: list[Node[K]], lo: int, hi: int) -> Node[K] | None:
    """Link a[lo:hi] into a perfectly balanced tree. O(hi - lo)."""
    if lo >= hi:  # @line L11
        return None
    mid = (lo + hi) // 2  # @line L12
    t = a[mid]
    t.left = build(a, lo, mid)
    t.right = build(a, mid + 1, hi)
    return t


def rebuild(w: Node[K]) -> Node[K]:
    """Rebuild the subtree w into a perfectly balanced tree. O(size(w))."""
    a = flatten(w)  # @line L9
    t = build(a, 0, len(a))  # @line L10
    assert t is not None
    return t


class ScapegoatTree(Generic[K]):
    """An ordered set kept as a scapegoat tree (Galperin and Rivest 1993).

    The parameter alpha, with 1/2 < alpha < 1, is a Fraction. The depth of
    every node is at most log_{1/alpha} q, where q is an upper bound on the
    size with alpha*q <= n <= q. Search costs O(log n) in the worst case;
    insertion and deletion cost O(log n) amortized and O(n) in the worst case.
    """

    def __init__(self, alpha: Fraction = Fraction(2, 3)) -> None:
        if not Fraction(1, 2) < alpha < 1:
            raise ValueError("alpha must satisfy 1/2 < alpha < 1")
        self.alpha = alpha
        self.root: Node[K] | None = None
        self.n = 0
        self.q = 0
        self.rebuilt = 0  # nodes moved by rebuilds, for the tests

    def _too_deep(self, d: int) -> bool:
        """Return whether d > log_{1/alpha} q, in exact arithmetic."""
        a = self.alpha
        return a.denominator**d > self.q * a.numerator**d

    def contains(self, k: K) -> bool:
        """Return whether k is in the set. O(log n)."""
        t = self.root
        while t is not None:
            if k < t.key:
                t = t.left
            elif t.key < k:
                t = t.right
            else:
                return True
        return False

    def insert(self, k: K) -> bool:
        """Add k; return False if it was already present."""
        path: list[Node[K]] = []
        t = self.root
        while t is not None:  # @line L1
            path.append(t)
            if k < t.key:
                t = t.left
            elif t.key < k:
                t = t.right
            else:
                return False
        u = Node(k)
        if not path:
            self.root = u
        elif k < path[-1].key:
            path[-1].left = u
        else:
            path[-1].right = u
        self.n += 1  # @line L2
        self.q += 1
        if self._too_deep(len(path)):  # @line L3
            child, child_size = u, 1
            j = len(path) - 1
            while True:  # @line L4
                w = path[j]
                sibling = w.right if child is w.left else w.left
                w_size = child_size + 1 + size(sibling)
                if child_size * self.alpha.denominator > self.alpha.numerator * w_size:
                    break
                child, child_size = w, w_size
                j -= 1
            self.rebuilt += w_size
            new = rebuild(w)  # @line L5
            if j == 0:
                self.root = new
            elif path[j - 1].left is w:
                path[j - 1].left = new
            else:
                path[j - 1].right = new
        return True

    def delete(self, k: K) -> bool:
        """Remove k; return False if it was absent."""
        parent: Node[K] | None = None
        t = self.root
        while t is not None and (k < t.key or t.key < k):  # @line L6
            parent = t
            t = t.left if k < t.key else t.right
        if t is None:
            return False
        if t.left is not None and t.right is not None:
            parent, s = t, t.right
            while s.left is not None:
                parent, s = s, s.left
            t.key = s.key
            t = s
        child = t.left if t.left is not None else t.right
        if parent is None:
            self.root = child
        elif parent.left is t:
            parent.left = child
        else:
            parent.right = child
        self.n -= 1  # @line L7
        if self.n * self.alpha.denominator < self.alpha.numerator * self.q:  # @line L8
            if self.root is not None:
                self.rebuilt += self.n
                self.root = rebuild(self.root)
            self.q = self.n
        return True

    def __contains__(self, k: K) -> bool:
        return self.contains(k)

    def __len__(self) -> int:
        return self.n

    def __iter__(self) -> Iterator[K]:
        return (x.key for x in flatten(self.root))

    def keys(self) -> list[K]:
        return list(self)

    def height(self) -> int:
        """Height in edges; -1 for the empty tree."""
        best = -1
        stack: list[tuple[Node[K] | None, int]] = [(self.root, 0)]
        while stack:
            x, d = stack.pop()
            if x is not None:
                best = max(best, d)
                stack.append((x.left, d + 1))
                stack.append((x.right, d + 1))
        return best

    def check_invariant(self) -> None:
        """Assert search order, the counters and the depth bound."""
        ks = self.keys()
        assert all(a < b for a, b in zip(ks, ks[1:])), "order"
        assert len(ks) == self.n, "count"
        assert self.alpha * self.q <= self.n <= self.q, "alpha q <= n <= q"
        h = self.height()
        assert h < 0 or not self._too_deep(h), "depth bound"
