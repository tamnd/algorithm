# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/persistent-binary-search-tree/. The authors are listed in prov/F9C8A3.jsonl.

from __future__ import annotations

from typing import Generic, Iterator, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


K = TypeVar("K", bound=Ordered)


class _Node(Generic[K]):
    """A tree node. Its fields are set once, when it is made, and never change."""

    __slots__ = ("key", "left", "right")

    def __init__(self, key: K, left: _Node[K] | None, right: _Node[K] | None) -> None:
        self.key = key
        self.left = left
        self.right = right


def _descend(t: _Node[K] | None, k: K) -> tuple[list[_Node[K]], _Node[K] | None]:
    """Return the nodes passed on the search path for k, and the node of k (or None)."""
    path: list[_Node[K]] = []  # @line L15
    while t is not None and (k < t.key or t.key < k):  # @line L16
        path.append(t)  # @line L17
        t = t.left if k < t.key else t.right  # @line L18
    return path, t  # @line L19


def _rebuild(path: list[_Node[K]], k: K, c: _Node[K] | None) -> _Node[K] | None:
    """Copy the nodes of path bottom up; in each copy, c replaces the child toward k."""
    for y in reversed(path):  # @line L20
        if k < y.key:
            c = _Node(y.key, c, y.right)  # @line L21
        else:
            c = _Node(y.key, y.left, c)  # @line L22
    return c  # @line L23


class PersistentBinarySearchTree(Generic[K]):
    """An unbalanced binary search tree updated by path copying.

    Each update returns a new tree and leaves self unchanged. On a version of
    height h, contains takes O(h) time, and insert and delete take O(h) time and
    make at most h + 1 new nodes. No recursion is used, so a tall tree is safe.
    """

    __slots__ = ("_root",)

    def __init__(self, _root: _Node[K] | None = None) -> None:
        self._root = _root

    def contains(self, k: K) -> bool:
        """True when k is a key of this version. O(h)."""
        t = self._root
        while t is not None and (k < t.key or t.key < k):  # @line L1
            t = t.left if k < t.key else t.right  # @line L2
        return t is not None  # @line L3

    def insert(self, k: K) -> PersistentBinarySearchTree[K]:
        """Return the version with k added. O(h) time and new nodes."""
        path, x = _descend(self._root, k)  # @line L4
        if x is not None:  # @line L5
            return self
        return PersistentBinarySearchTree(_rebuild(path, k, _Node(k, None, None)))  # @line L6

    def delete(self, k: K) -> PersistentBinarySearchTree[K]:
        """Return the version with k removed. O(h) time and new nodes."""
        path, x = _descend(self._root, k)  # @line L7
        if x is None:  # @line L8
            return self
        if x.left is None:  # @line L9
            c = x.right
        elif x.right is None:  # @line L10
            c = x.left
        else:  # @line L11
            q: list[_Node[K]] = []  # @line L12
            y = x.right
            while y.left is not None:
                q.append(y)
                y = y.left
            c = _Node(y.key, x.left, _rebuild(q, y.key, y.right))  # @line L13
        return PersistentBinarySearchTree(_rebuild(path, k, c))  # @line L14

    def keys(self) -> Iterator[K]:
        """The keys in increasing order, by an in-order walk with an explicit stack."""
        stack: list[_Node[K]] = []
        t = self._root
        while stack or t is not None:
            while t is not None:
                stack.append(t)
                t = t.left
            t = stack.pop()
            yield t.key
            t = t.right

    def height(self) -> int:
        """The number of nodes on a longest root-to-leaf path (0 for the empty tree)."""
        best = 0
        stack: list[tuple[_Node[K], int]] = [(self._root, 1)] if self._root else []
        while stack:
            t, d = stack.pop()
            best = max(best, d)
            for ch in (t.left, t.right):
                if ch is not None:
                    stack.append((ch, d + 1))
        return best

    def check_invariant(self) -> None:
        """Check the search-tree order: the in-order keys strictly increase."""
        ks = list(self.keys())
        assert all(ks[i] < ks[i + 1] for i in range(len(ks) - 1))


def count_nodes(*versions: PersistentBinarySearchTree[K]) -> int:
    """The number of distinct nodes reachable from the given versions."""
    seen: set[int] = set()
    stack = [v._root for v in versions if v._root is not None]
    while stack:
        t = stack.pop()
        if id(t) in seen:
            continue
        seen.add(id(t))
        stack.extend(ch for ch in (t.left, t.right) if ch is not None)
    return len(seen)
