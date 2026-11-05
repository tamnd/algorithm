# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bk-tree/. The authors are listed in prov/WM7ED9.jsonl.

from collections.abc import Callable, Hashable, Iterable
from typing import Generic, TypeVar

T = TypeVar("T", bound=Hashable)


def levenshtein(a: str, b: str) -> int:
    """Edit distance with unit-cost insertion, deletion and substitution. O(|a| |b|) time."""
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


class _Node(Generic[T]):
    __slots__ = ("item", "children")

    def __init__(self, item: T) -> None:
        self.item = item
        self.children: dict[int, _Node[T]] = {}


class BKTree(Generic[T]):
    """Burkhard-Keller tree for a metric with nonnegative integer values.

    Invariant: every item in the subtree of t.children[i] is at distance exactly i from t.item.
    Insert: O(h) distance evaluations. Range and nearest: O(n) evaluations in the worst case.
    """

    def __init__(self, dist: Callable[[T, T], int] = levenshtein, items: Iterable[T] = ()) -> None:
        self.dist = dist
        self.root: _Node[T] | None = None
        self.size = 0
        for x in items:
            self.insert(x)

    def insert(self, x: T) -> bool:
        """Add x; return False if an item at distance 0 is already stored."""
        if self.root is None:  # @line L1
            self.root = _Node(x)
            self.size = 1
            return True
        t = self.root  # @line L2
        while True:
            k = self.dist(x, t.item)  # @line L3
            if k == 0:  # @line L4
                return False
            child = t.children.get(k)  # @line L5
            if child is None:
                t.children[k] = _Node(x)
                self.size += 1
                return True
            t = child

    def range(self, q: T, r: int) -> list[T]:
        """Return all stored items x with dist(q, x) <= r."""
        out: list[T] = []
        stack = [self.root]
        while stack:
            t = stack.pop()
            if t is None:  # @line L6
                continue
            k = self.dist(q, t.item)  # @line L7
            if k <= r:
                out.append(t.item)
            for i, child in t.children.items():  # @line L8
                if k - r <= i <= k + r:
                    stack.append(child)
        return out

    def nearest(self, q: T) -> tuple[int, T] | None:
        """Return (distance, item) for a stored item nearest to q, or None if the tree is empty."""
        if self.root is None:
            return None
        best: tuple[int, T] | None = None  # @line L9
        stack: list[tuple[int, _Node[T]]] = [(0, self.root)]
        while stack:  # @line L10
            lb, t = stack.pop()
            if best is not None and lb >= best[0]:
                continue
            k = self.dist(q, t.item)  # @line L11
            if best is None or k < best[0]:
                best = (k, t.item)
            for i, child in t.children.items():  # @line L12
                if abs(i - k) < best[0]:
                    stack.append((abs(i - k), child))
        return best  # @line L13
