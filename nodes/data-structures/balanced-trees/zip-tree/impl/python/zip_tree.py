# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zip-tree/. The authors are listed in prov/4VXZ7W.jsonl.

from __future__ import annotations

import random
from typing import Generic, Iterator, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


K = TypeVar("K", bound=Ordered)


class Node(Generic[K]):
    __slots__ = ("key", "rank", "left", "right")

    def __init__(self, key: K, rank: int) -> None:
        self.key = key
        self.rank = rank
        self.left: Node[K] | None = None
        self.right: Node[K] | None = None


def random_rank(rng: random.Random) -> int:
    """Return k with probability 1 / 2^(k+1): the number of heads before
    the first tail."""
    k = 0
    while rng.random() < 0.5:
        k += 1
    return k


def unzip(t: Node[K] | None, k: K) -> tuple[Node[K] | None, Node[K] | None]:
    """Cut the search path of k in t into the nodes with keys < k and the
    nodes with keys > k (k is not in t). O(path length)."""
    p_root: Node[K] | None = None  # @line L5
    q_root: Node[K] | None = None
    p_last: Node[K] | None = None  # bottom of the right spine of P
    q_last: Node[K] | None = None  # bottom of the left spine of Q
    while t is not None:  # @line L6
        if t.key < k:
            if p_last is None:
                p_root = t
            else:
                p_last.right = t
            p_last, t = t, t.right
        else:
            if q_last is None:
                q_root = t
            else:
                q_last.left = t
            q_last, t = t, t.left
    if p_last is not None:  # @line L7
        p_last.right = None
    if q_last is not None:
        q_last.left = None
    return p_root, q_root


def zip_trees(a: Node[K] | None, b: Node[K] | None) -> Node[K] | None:
    """Join a and b, where every key of a is less than every key of b, by
    zipping the right spine of a with the left spine of b. O(spine length)."""
    root: Node[K] | None = None
    hook: Node[K] | None = None  # last node hung
    hook_right = False  # hang the next node as its right child?
    while a is not None and b is not None:  # @line L9
        if a.rank >= b.rank:  # on a tie the smaller key stays on top
            nxt, a, side = a, a.right, True
        else:
            nxt, b, side = b, b.left, False
        if hook is None:
            root = nxt
        elif hook_right:
            hook.right = nxt
        else:
            hook.left = nxt
        hook, hook_right = nxt, side
    rest = a if a is not None else b  # @line L10
    if hook is None:
        return rest
    if hook_right:
        hook.right = rest
    else:
        hook.left = rest
    return root


class ZipTree(Generic[K]):
    """An ordered set kept as a zip tree (Tarjan, Levy and Timmel 2019).

    Each node has a random geometric rank; ranks are in max-heap order, and
    a child may have its parent's rank only if it is a right child.
    Operations take O(log n) expected time.
    """

    def __init__(self, rng: random.Random | None = None) -> None:
        self.root: Node[K] | None = None
        self.rng = rng if rng is not None else random.Random()
        self.n = 0

    def contains(self, k: K) -> bool:
        t = self.root
        while t is not None:
            if k < t.key:
                t = t.left
            elif t.key < k:
                t = t.right
            else:
                return True
        return False

    def insert(self, k: K, rank: int | None = None) -> bool:
        """Add k; return False if it was already present."""
        if self.contains(k):  # @line L1
            return False
        x = Node(k, random_rank(self.rng) if rank is None else rank)
        parent: Node[K] | None = None
        cur = self.root
        while cur is not None and (  # @line L2
            cur.rank > x.rank or (cur.rank == x.rank and cur.key < k)
        ):
            parent = cur
            cur = cur.left if k < cur.key else cur.right
        x.left, x.right = unzip(cur, k)  # @line L3
        if parent is None:  # @line L4
            self.root = x
        elif k < parent.key:
            parent.left = x
        else:
            parent.right = x
        self.n += 1
        return True

    def delete(self, k: K) -> bool:
        """Remove k; return False if it was absent."""
        parent: Node[K] | None = None
        x = self.root
        while x is not None and (k < x.key or x.key < k):  # @line L8
            parent = x
            x = x.left if k < x.key else x.right
        if x is None:
            return False
        c = zip_trees(x.left, x.right)
        if parent is None:
            self.root = c
        elif parent.left is x:
            parent.left = c
        else:
            parent.right = c
        self.n -= 1
        return True

    def __contains__(self, k: K) -> bool:
        return self.contains(k)

    def __len__(self) -> int:
        return self.n

    def __iter__(self) -> Iterator[K]:
        stack: list[Node[K]] = []
        t = self.root
        while stack or t is not None:
            while t is not None:
                stack.append(t)
                t = t.left
            t = stack.pop()
            yield t.key
            t = t.right

    def keys(self) -> list[K]:
        return list(self)

    def height(self) -> int:
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
        """Assert search order and the rank rule."""
        def go(t: Node[K] | None) -> int:
            if t is None:
                return 0
            if t.left is not None:
                assert t.left.key < t.key and t.left.rank < t.rank, "left child"
            if t.right is not None:
                assert t.key < t.right.key and t.right.rank <= t.rank, "right child"
            return 1 + go(t.left) + go(t.right)
        assert go(self.root) == self.n, "count"
        ks = self.keys()
        assert all(a < b for a, b in zip(ks, ks[1:])), "order"
