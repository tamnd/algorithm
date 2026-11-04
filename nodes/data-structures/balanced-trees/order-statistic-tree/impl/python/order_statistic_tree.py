# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/order-statistic-tree/. The authors are listed in prov/S2AJN7.jsonl.

from __future__ import annotations

from typing import Generic, Iterator, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


K = TypeVar("K", bound=Ordered)

RED = True
BLACK = False


class Node(Generic[K]):
    """A node of a left-leaning red-black tree with its subtree size."""

    __slots__ = ("key", "left", "right", "red", "size")

    def __init__(self, key: K) -> None:
        self.key = key
        self.left: Node[K] | None = None
        self.right: Node[K] | None = None
        self.red = RED
        self.size = 1


def size(x: Node[K] | None) -> int:
    """The number of nodes in the subtree of x. O(1)."""
    return 0 if x is None else x.size  # @line L13


def update(x: Node[K]) -> None:
    """Recompute x.size from its children, whose sizes are right. O(1)."""
    x.size = 1 + size(x.left) + size(x.right)  # @line L14


def is_red(h: Node[K] | None) -> bool:
    return h is not None and h.red


def rotate_left(h: Node[K]) -> Node[K]:
    """Turn the red right link of h into a left link; fix both sizes. O(1)."""
    x = h.right  # @line L15
    assert x is not None
    h.right = x.left
    x.left = h
    x.red = h.red
    h.red = RED
    update(h)  # @line L16
    update(x)
    return x


def rotate_right(h: Node[K]) -> Node[K]:
    """Turn the red left link of h into a right link; fix both sizes. O(1)."""
    x = h.left
    assert x is not None
    h.left = x.right
    x.right = h
    x.red = h.red
    h.red = RED
    update(h)
    update(x)
    return x


def flip_colors(h: Node[K]) -> None:
    assert h.left is not None and h.right is not None
    h.red = not h.red
    h.left.red = not h.left.red
    h.right.red = not h.right.red


def fix_up(h: Node[K]) -> Node[K]:
    """Restore the left-leaning shape at h and recompute its size. O(1)."""
    if is_red(h.right) and not is_red(h.left):
        h = rotate_left(h)
    if is_red(h.left) and h.left is not None and is_red(h.left.left):
        h = rotate_right(h)
    if is_red(h.left) and is_red(h.right):
        flip_colors(h)
    update(h)  # @line L17
    return h


def put(h: Node[K] | None, k: K) -> Node[K]:
    if h is None:
        return Node(k)
    if k < h.key:
        h.left = put(h.left, k)
    else:
        h.right = put(h.right, k)
    return fix_up(h)


def move_red_left(h: Node[K]) -> Node[K]:
    flip_colors(h)
    assert h.right is not None
    if is_red(h.right.left):
        h.right = rotate_right(h.right)
        h = rotate_left(h)
        flip_colors(h)
    return h


def move_red_right(h: Node[K]) -> Node[K]:
    flip_colors(h)
    assert h.left is not None
    if is_red(h.left.left):
        h = rotate_right(h)
        flip_colors(h)
    return h


def delete_min(h: Node[K]) -> Node[K] | None:
    if h.left is None:
        return None
    if not is_red(h.left) and not is_red(h.left.left):
        h = move_red_left(h)
    assert h.left is not None
    h.left = delete_min(h.left)
    return fix_up(h)


def remove(h: Node[K], k: K) -> Node[K] | None:
    """Delete the present key k below h (see left-leaning-red-black-tree)."""
    if k < h.key:
        assert h.left is not None
        if not is_red(h.left) and not is_red(h.left.left):
            h = move_red_left(h)
        assert h.left is not None
        h.left = remove(h.left, k)
    else:
        if is_red(h.left):
            h = rotate_right(h)
        if not (k < h.key) and not (h.key < k) and h.right is None:
            return None
        assert h.right is not None
        if not is_red(h.right) and not is_red(h.right.left):
            h = move_red_right(h)
        assert h.right is not None
        if not (k < h.key) and not (h.key < k):
            m = h.right
            while m.left is not None:
                m = m.left
            h.key = m.key
            h.right = delete_min(h.right)
        else:
            h.right = remove(h.right, k)
    return fix_up(h)


class OrderStatisticTree(Generic[K]):
    """An ordered set with rank and select, kept as a left-leaning red-black
    tree in which each node stores the size of its subtree.

    Keys must be totally ordered. Ranks start at 0: select(i) is the key
    with exactly i smaller keys, and rank(k) is the number of keys less than
    k. All operations cost O(log n) time in the worst case.
    """

    def __init__(self) -> None:
        self.root: Node[K] | None = None

    def __len__(self) -> int:
        return size(self.root)

    def contains(self, k: K) -> bool:
        """Return whether k is in the set. O(log n)."""
        h = self.root
        while h is not None:
            if k < h.key:
                h = h.left
            elif h.key < k:
                h = h.right
            else:
                return True
        return False

    def select(self, i: int) -> K:
        """Return the key with exactly i smaller keys. O(log n).

        Precondition: 0 <= i < len(self); else IndexError.
        """
        if not 0 <= i < size(self.root):
            raise IndexError("rank out of range")
        x = self.root  # @line L1
        while True:  # @line L2
            assert x is not None
            r = size(x.left)  # @line L3
            if i == r:  # @line L4
                return x.key
            if i < r:  # @line L5
                x = x.left
            else:  # @line L6
                i = i - r - 1
                x = x.right

    def rank(self, k: K) -> int:
        """Return the number of keys less than k; k need not be present.
        O(log n)."""
        r, x = 0, self.root  # @line L7
        while x is not None:  # @line L8
            if k < x.key:  # @line L9
                x = x.left
            elif not (x.key < k):  # @line L10
                return r + size(x.left)
            else:  # @line L11
                r += size(x.left) + 1
                x = x.right
        return r  # @line L12

    def insert(self, k: K) -> bool:
        """Add k; return False if it was already present. O(log n)."""
        if self.contains(k):
            return False
        self.root = put(self.root, k)
        self.root.red = BLACK
        return True

    def delete(self, k: K) -> bool:
        """Remove k; return False if it was absent. O(log n)."""
        if not self.contains(k):
            return False
        assert self.root is not None
        if not is_red(self.root.left) and not is_red(self.root.right):
            self.root.red = RED
        self.root = remove(self.root, k)
        if self.root is not None:
            self.root.red = BLACK
        return True

    def keys(self) -> Iterator[K]:
        """Yield the keys in increasing order. O(n)."""
        stack: list[Node[K]] = []
        h = self.root
        while stack or h is not None:
            while h is not None:
                stack.append(h)
                h = h.left
            h = stack.pop()
            yield h.key
            h = h.right

    def height(self) -> int:
        def ht(h: Node[K] | None) -> int:
            return 0 if h is None else 1 + max(ht(h.left), ht(h.right))

        return ht(self.root)

    def check_invariant(self) -> None:
        """Raise AssertionError unless the tree is a valid left-leaning
        red-black tree and every stored size is right."""
        assert not is_red(self.root), "the root is black"

        def walk(h: Node[K] | None, lo: K | None, hi: K | None) -> tuple[int, int]:
            if h is None:
                return 0, 0
            assert lo is None or lo < h.key
            assert hi is None or h.key < hi
            assert not is_red(h.right), "no red right link"
            if h.red:
                assert not is_red(h.left), "no two red links in a row"
            bl, nl = walk(h.left, lo, h.key)
            br, nr = walk(h.right, h.key, hi)
            assert bl == br, "perfect black balance"
            assert h.size == 1 + nl + nr, "size field"
            return bl + (0 if h.red else 1), h.size

        walk(self.root, None, None)
