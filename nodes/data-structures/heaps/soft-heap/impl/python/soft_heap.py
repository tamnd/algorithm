# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/soft-heap/. The authors are listed in prov/C1G5PQ.jsonl.

"""Soft heap in the style of Kaplan, Tarjan and Zwick (2013).

Each node of a binary tree holds a list of items, which all carry the same
current key, the ckey of the node. Items in nodes of rank above T may be
corrupted: their ckey is larger than their own key.
"""

import math
from typing import Any, List, Optional, Protocol, Tuple, TypeVar, Generic


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)


class Node(Generic[K]):
    """A node: ckey, rank, item list and two children."""

    __slots__ = ("ckey", "rank", "items", "left", "right")

    def __init__(self, key: K) -> None:
        self.ckey: K = key
        self.rank = 0
        self.items: List[K] = [key]
        self.left: Optional["Node[K]"] = None
        self.right: Optional["Node[K]"] = None

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


class SoftHeap(Generic[K]):
    """Soft heap with error rate eps: at most eps * (number of inserts) corrupted items.

    The threshold is T = ceil(lg(1/eps)) + 5, which is what the proof on the
    page needs. A value of t given directly overrides it.
    """

    def __init__(self, eps: float = 0.25, t: Optional[int] = None) -> None:
        if t is None:
            if not 0 < eps < 1:
                raise ValueError("eps must be in (0, 1)")
            t = math.ceil(math.log2(1 / eps)) + 5
        self.t = t
        self.roots: List[Node[K]] = []  # decreasing rank; the end has the smallest rank
        self.best: List[int] = []  # best[i]: index of the root of smallest ckey in roots[0..i]
        self.inserts = 0
        self.count = 0
        self.links = 0
        self.moves = 0

    def __len__(self) -> int:
        return self.count

    def size(self, rank: int) -> int:
        """Target size s_k: 1 for k <= T, then ceil(3 s_{k-1} / 2)."""
        s = 1
        for _ in range(self.t, rank):
            s = (3 * s + 1) // 2
        return s

    def _sift(self, x: Node[K]) -> None:
        """Fill the item list of x from below while it is shorter than s_rank."""
        target = self.size(x.rank)
        while len(x.items) < target and not x.is_leaf():  # @line L3
            if x.left is None or (x.right is not None and x.right.ckey < x.left.ckey):  # @line L4
                x.left, x.right = x.right, x.left
            c = x.left
            assert c is not None
            self.moves += 1
            x.items.extend(c.items)  # @line L5
            x.ckey = c.ckey
            c.items = []
            if c.is_leaf():  # @line L6
                x.left = None
            else:
                self._sift(c)

    def _link(self, x: Node[K], y: Node[K]) -> Node[K]:
        """Make a new node of rank r + 1 over two roots of rank r, and fill it."""
        self.links += 1
        z: Node[K] = Node(x.ckey)  # @line L1
        z.items = []
        z.rank = x.rank + 1
        z.left, z.right = x, y
        self._sift(z)  # @line L2
        return z

    def _fix_best(self, start: int) -> None:
        """Recompute best[start:]."""
        del self.best[start:]
        for i in range(start, len(self.roots)):
            if i == 0 or self.roots[i].ckey < self.roots[self.best[i - 1]].ckey:
                self.best.append(i)
            else:
                self.best.append(self.best[i - 1])

    def _add_root(self, x: Node[K]) -> None:
        """Add a root, linking it with a root of equal rank while there is one."""
        while True:
            i = len(self.roots)
            while i > 0 and self.roots[i - 1].rank < x.rank:
                i -= 1
            if i > 0 and self.roots[i - 1].rank == x.rank:
                x = self._link(x, self.roots.pop(i - 1))
                continue
            self.roots.insert(i, x)
            self._fix_best(min(i, len(self.best)))
            return

    def insert(self, key: K) -> None:
        """Insert key."""
        self.inserts += 1
        self.count += 1
        self._add_root(Node(key))  # @line L7

    def meld(self, other: "SoftHeap[K]") -> None:
        """Move all items of other into this heap. Both must use the same T."""
        if other.t != self.t:
            raise ValueError("the heaps have different thresholds")
        for x in reversed(other.roots):  # @line L8
            self._add_root(x)
        self.inserts += other.inserts
        self.count += other.count
        other.roots, other.best, other.count, other.inserts = [], [], 0, 0

    def find_min(self) -> Tuple[K, K]:
        """Return (item, current key) of an item of smallest current key."""
        if not self.roots:
            raise IndexError("the heap is empty")
        x = self.roots[self.best[-1]]  # @line L9
        return x.items[-1], x.ckey

    def delete_min(self) -> Tuple[K, K]:
        """Remove and return (item, current key) of an item of smallest current key."""
        if not self.roots:
            raise IndexError("the heap is empty")
        i = self.best[-1]
        x = self.roots[i]  # @line L10
        e = x.items.pop()  # @line L11
        ckey = x.ckey
        self.count -= 1
        if 2 * len(x.items) <= self.size(x.rank):  # @line L12
            if not x.is_leaf():
                self._sift(x)  # @line L13
            elif not x.items:
                self.roots.pop(i)  # @line L14
        self._fix_best(min(i, len(self.best)))  # @line L15
        return e, ckey

    # -- checking ----------------------------------------------------------

    def nodes(self) -> List[Node[K]]:
        out: List[Node[K]] = []
        stack = list(self.roots)
        while stack:
            v = stack.pop()
            out.append(v)
            stack.extend(c for c in (v.left, v.right) if c is not None)
        return out

    def corrupted(self) -> int:
        """The number of items whose current key is larger than their own key."""
        return sum(1 for v in self.nodes() for e in v.items if e < v.ckey)

    def check_invariant(self) -> None:
        """Check ranks, heap order of ckeys, item keys, the size bounds and the error bound."""
        ranks = [r.rank for r in self.roots]
        assert all(a > b for a, b in zip(ranks, ranks[1:]))
        assert len(self.best) == len(self.roots)
        for i in range(len(self.roots)):
            m = min(range(i + 1), key=lambda j: (self.roots[j].ckey, j))
            assert not self.roots[m].ckey < self.roots[self.best[i]].ckey
        total = 0
        for v in self.nodes():
            total += len(v.items)
            assert v.is_leaf() or v.items, "an internal node has an empty list"
            assert v.items or v.is_leaf()
            for e in v.items:
                assert not v.ckey < e
            if v.rank <= self.t:
                assert len(v.items) <= 1
            for c in (v.left, v.right):
                if c is not None:
                    assert c.rank == v.rank - 1
                    assert not c.ckey < v.ckey
        assert total == self.count
        assert all(r.items or not r.is_leaf() for r in self.roots)
        assert self.corrupted() * 2**self.t <= 18 * self.inserts
