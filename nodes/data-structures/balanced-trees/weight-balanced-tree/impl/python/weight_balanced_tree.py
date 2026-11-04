# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weight-balanced-tree/. The authors are listed in prov/0YHN5A.jsonl.

from __future__ import annotations

from typing import Generic, Iterator, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


K = TypeVar("K", bound=Ordered)

DELTA = 3  # a child may weigh at most DELTA times its sibling
GAMMA = 2  # single rotation if inner weight < GAMMA * outer weight


class Node(Generic[K]):
    """An immutable node; size is the number of keys in the subtree."""

    __slots__ = ("key", "left", "right", "size")

    def __init__(self, left: Node[K] | None, key: K, right: Node[K] | None) -> None:
        self.key = key
        self.left = left
        self.right = right
        self.size = size(left) + size(right) + 1


def size(t: Node[K] | None) -> int:
    return 0 if t is None else t.size


def weight(t: Node[K] | None) -> int:
    return size(t) + 1


def balance(l: Node[K] | None, k: K, r: Node[K] | None) -> Node[K]:
    """Join l < k < r, where l and r are weight-balanced and their weights
    were in balance before one key was added to or removed from one side."""
    if DELTA * weight(l) < weight(r):  # @line L1
        assert r is not None
        return rotate_left(l, k, r)
    if DELTA * weight(r) < weight(l):  # @line L2
        assert l is not None
        return rotate_right(l, k, r)
    return Node(l, k, r)  # @line L3


def rotate_left(l: Node[K] | None, k: K, r: Node[K]) -> Node[K]:
    rl, rr = r.left, r.right
    if weight(rl) < GAMMA * weight(rr):  # @line L4
        return Node(Node(l, k, rl), r.key, rr)
    assert rl is not None  # @line L5
    return Node(Node(l, k, rl.left), rl.key, Node(rl.right, r.key, rr))


def rotate_right(l: Node[K], k: K, r: Node[K] | None) -> Node[K]:
    ll, lr = l.left, l.right
    if weight(lr) < GAMMA * weight(ll):
        return Node(ll, l.key, Node(lr, k, r))
    assert lr is not None
    return Node(Node(ll, l.key, lr.left), lr.key, Node(lr.right, k, r))


def insert(t: Node[K] | None, k: K) -> Node[K]:
    """Return t with k added. O(log n)."""
    if t is None:  # @line L6
        return Node(None, k, None)
    if k < t.key:  # @line L7
        return balance(insert(t.left, k), t.key, t.right)
    if t.key < k:  # @line L8
        return balance(t.left, t.key, insert(t.right, k))
    return t


def delete_min(t: Node[K]) -> tuple[K, Node[K] | None]:
    if t.left is None:
        return t.key, t.right
    m, l = delete_min(t.left)
    return m, balance(l, t.key, t.right)


def delete_max(t: Node[K]) -> tuple[K, Node[K] | None]:
    if t.right is None:
        return t.key, t.left
    m, r = delete_max(t.right)
    return m, balance(t.left, t.key, r)


def glue(l: Node[K] | None, r: Node[K] | None) -> Node[K] | None:
    """Join two subtrees of one balanced node, without the key between."""
    if l is None:  # @line L11
        return r
    if r is None:
        return l
    if size(l) > size(r):  # @line L12
        m, l2 = delete_max(l)
        return balance(l2, m, r)
    m, r2 = delete_min(r)
    return balance(l, m, r2)


def delete(t: Node[K] | None, k: K) -> Node[K] | None:
    """Return t with k removed. O(log n)."""
    if t is None:
        return None
    if k < t.key:  # @line L9
        return balance(delete(t.left, k), t.key, t.right)
    if t.key < k:
        return balance(t.left, t.key, delete(t.right, k))
    return glue(t.left, t.right)  # @line L10


class WeightBalancedTree(Generic[K]):
    """An ordered set kept as a weight-balanced tree with (delta, gamma) =
    (3, 2), as in Adams (1993) and Hirai and Yamamoto (2011).

    Nodes are immutable, so old versions stay valid. Search, insertion,
    deletion, rank and select cost O(log n) in the worst case.
    """

    def __init__(self) -> None:
        self.root: Node[K] | None = None

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

    def insert(self, k: K) -> bool:
        """Add k; return False if it was already present."""
        n = size(self.root)
        self.root = insert(self.root, k)
        return size(self.root) > n

    def delete(self, k: K) -> bool:
        """Remove k; return False if it was absent."""
        n = size(self.root)
        self.root = delete(self.root, k)
        return size(self.root) < n

    def select(self, i: int) -> K:
        """Return the key of rank i (0-based). O(log n)."""
        if not 0 <= i < size(self.root):
            raise IndexError(i)
        t = self.root
        while t is not None:
            s = size(t.left)
            if i < s:
                t = t.left
            elif i > s:
                i -= s + 1
                t = t.right
            else:
                return t.key
        raise AssertionError("unreachable")

    def rank(self, k: K) -> int:
        """Return the number of keys less than k. O(log n)."""
        r, t = 0, self.root
        while t is not None:
            if k < t.key:
                t = t.left
            elif t.key < k:
                r += size(t.left) + 1
                t = t.right
            else:
                return r + size(t.left)
        return r

    def __contains__(self, k: K) -> bool:
        return self.contains(k)

    def __len__(self) -> int:
        return size(self.root)

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
        """Height in edges; -1 for the empty tree."""
        def h(t: Node[K] | None) -> int:
            return -1 if t is None else 1 + max(h(t.left), h(t.right))
        return h(self.root)

    def check_invariant(self) -> None:
        """Assert order, sizes and the weight rule at every node."""
        def go(t: Node[K] | None) -> None:
            if t is None:
                return
            assert t.size == size(t.left) + size(t.right) + 1, "size"
            assert weight(t.left) <= DELTA * weight(t.right), "left too heavy"
            assert weight(t.right) <= DELTA * weight(t.left), "right too heavy"
            go(t.left)
            go(t.right)
        go(self.root)
        ks = self.keys()
        assert all(a < b for a, b in zip(ks, ks[1:])), "order"
