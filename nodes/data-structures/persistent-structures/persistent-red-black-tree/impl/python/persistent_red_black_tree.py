# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/persistent-red-black-tree/. The authors are listed in prov/3F3XMG.jsonl.

from __future__ import annotations

from typing import Generic, Iterator, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


K = TypeVar("K", bound=Ordered)
RED, BLACK = True, False


class _Node(Generic[K]):
    """A tree node. Its fields are set once and never change."""

    __slots__ = ("red", "left", "key", "right")

    def __init__(self, red: bool, left: _Node[K] | None, key: K, right: _Node[K] | None) -> None:
        self.red = red
        self.left = left
        self.key = key
        self.right = right


Tree = _Node[K] | None


def _is_red(t: Tree[K]) -> bool:
    return t is not None and t.red


def _is_black(t: Tree[K]) -> bool:
    return t is not None and not t.red


def _blacken(t: Tree[K]) -> Tree[K]:
    if t is None or not t.red:
        return t
    return _Node(BLACK, t.left, t.key, t.right)


def _redden(t: _Node[K]) -> _Node[K]:
    assert not t.red, "REDDEN is applied only to a black node"
    return _Node(RED, t.left, t.key, t.right)


def _balance(a: Tree[K], x: K, b: Tree[K]) -> _Node[K]:
    """Make a node from a, x, b and repair a red node with a red child below it."""
    if a is not None and b is not None and a.red and b.red:  # @line L10
        return _Node(RED, _blacken(a), x, _blacken(b))
    if a is not None and a.red and _is_red(a.left):  # @line L11
        assert a.left is not None
        return _Node(RED, _blacken(a.left), a.key, _Node(BLACK, a.right, x, b))
    if a is not None and a.red and a.right is not None and a.right.red:  # @line L12
        m = a.right
        return _Node(RED, _Node(BLACK, a.left, a.key, m.left), m.key, _Node(BLACK, m.right, x, b))
    if b is not None and b.red and _is_red(b.right):  # @line L13
        return _Node(RED, _Node(BLACK, a, x, b.left), b.key, _blacken(b.right))
    if b is not None and b.red and b.left is not None and b.left.red:  # @line L14
        m = b.left
        return _Node(RED, _Node(BLACK, a, x, m.left), m.key, _Node(BLACK, m.right, b.key, b.right))
    return _Node(BLACK, a, x, b)  # @line L15


def _ins(t: Tree[K], k: K) -> _Node[K]:
    if t is None:  # @line L3
        return _Node(RED, None, k, None)
    if k < t.key:  # @line L4
        if not t.red:  # @line L5
            return _balance(_ins(t.left, k), t.key, t.right)
        return _Node(RED, _ins(t.left, k), t.key, t.right)  # @line L6
    if not t.red:  # @line L7 @line L8
        return _balance(t.left, t.key, _ins(t.right, k))
    return _Node(RED, t.left, t.key, _ins(t.right, k))  # @line L9


def _bal_left(l: Tree[K], x: K, r: Tree[K]) -> _Node[K]:
    """l has black height one less than r. Return a tree of the black height of r."""
    if l is not None and l.red:  # @line L25
        return _Node(RED, _blacken(l), x, r)
    assert r is not None
    if not r.red:  # @line L26
        return _balance(l, x, _redden(r))
    a = r.left  # @line L27
    assert a is not None and r.right is not None
    return _Node(RED, _Node(BLACK, l, x, a.left), a.key, _balance(a.right, r.key, _redden(r.right)))  # @line L28


def _bal_right(l: Tree[K], x: K, r: Tree[K]) -> _Node[K]:
    """The mirror image of _bal_left: r has black height one less than l."""
    if r is not None and r.red:  # @line L29
        return _Node(RED, l, x, _blacken(r))
    assert l is not None
    if not l.red:  # @line L30
        return _balance(_redden(l), x, r)
    a = l.right  # @line L31
    assert a is not None and l.left is not None
    return _Node(RED, _balance(_redden(l.left), l.key, a.left), a.key, _Node(BLACK, a.right, x, r))


def _fuse(a: Tree[K], b: Tree[K]) -> Tree[K]:
    """Join two trees of the same black height; every key of a is less than every key of b."""
    if a is None:  # @line L32
        return b
    if b is None:  # @line L33
        return a
    if a.red and b.red:  # @line L34
        c = _fuse(a.right, b.left)  # @line L35
        if c is not None and c.red:  # @line L36
            return _Node(RED, _Node(RED, a.left, a.key, c.left), c.key, _Node(RED, c.right, b.key, b.right))
        return _Node(RED, a.left, a.key, _Node(RED, c, b.key, b.right))  # @line L37
    if not a.red and not b.red:  # @line L38
        c = _fuse(a.right, b.left)  # @line L39
        if c is not None and c.red:  # @line L40
            return _Node(RED, _Node(BLACK, a.left, a.key, c.left), c.key, _Node(BLACK, c.right, b.key, b.right))
        return _bal_left(a.left, a.key, _Node(BLACK, c, b.key, b.right))  # @line L41
    if b.red:  # @line L42
        return _Node(RED, _fuse(a, b.left), b.key, b.right)
    return _Node(RED, a.left, a.key, _fuse(a.right, b))  # @line L43


def _del(t: Tree[K], k: K) -> Tree[K]:
    """Precondition: k is a key of t."""
    assert t is not None
    if k < t.key:  # @line L18
        if _is_black(t.left):  # @line L19
            return _bal_left(_del(t.left, k), t.key, t.right)
        return _Node(RED, _del(t.left, k), t.key, t.right)  # @line L20
    if t.key < k:  # @line L21
        if _is_black(t.right):  # @line L22
            return _bal_right(t.left, t.key, _del(t.right, k))
        return _Node(RED, t.left, t.key, _del(t.right, k))  # @line L23
    return _fuse(t.left, t.right)  # @line L24


class PersistentRedBlackTree(Generic[K]):
    """A red-black tree with purely functional insert and delete.

    Each update returns a new tree and leaves self unchanged. The height is at most
    2 lg(n + 1), so contains, insert and delete take O(log n) time, and an update
    makes O(log n) new nodes.
    """

    __slots__ = ("_root",)

    def __init__(self, _root: Tree[K] = None) -> None:
        self._root = _root

    def contains(self, k: K) -> bool:
        """True when k is a key of this version. O(log n)."""
        t = self._root
        while t is not None and (k < t.key or t.key < k):
            t = t.left if k < t.key else t.right
        return t is not None

    def insert(self, k: K) -> PersistentRedBlackTree[K]:
        """Return the version with k added. O(log n)."""
        if self.contains(k):  # @line L1
            return self
        return PersistentRedBlackTree(_blacken(_ins(self._root, k)))  # @line L2

    def delete(self, k: K) -> PersistentRedBlackTree[K]:
        """Return the version with k removed. O(log n)."""
        if not self.contains(k):  # @line L16
            return self
        return PersistentRedBlackTree(_blacken(_del(self._root, k)))  # @line L17

    def keys(self) -> Iterator[K]:
        """The keys in increasing order."""
        stack: list[_Node[K]] = []
        t = self._root
        while stack or t is not None:
            while t is not None:
                stack.append(t)
                t = t.left
            t = stack.pop()
            yield t.key
            t = t.right

    def check_invariant(self) -> int:
        """Check the search order and the red-black rules; return the black height."""

        def go(t: Tree[K], lo: K | None, hi: K | None) -> int:
            if t is None:
                return 0
            assert (lo is None or lo < t.key) and (hi is None or t.key < hi)
            if t.red:
                assert not _is_red(t.left) and not _is_red(t.right)
            hl, hr = go(t.left, lo, t.key), go(t.right, t.key, hi)
            assert hl == hr
            return hl + (0 if t.red else 1)

        assert not _is_red(self._root)
        return go(self._root, None, None)
