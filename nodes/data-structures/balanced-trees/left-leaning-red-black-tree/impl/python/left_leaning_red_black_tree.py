# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/left-leaning-red-black-tree/. The authors are listed in prov/1ZQX62.jsonl.

from __future__ import annotations

from typing import Generic, Iterator, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


K = TypeVar("K", bound=Ordered)

RED = True
BLACK = False


class Node(Generic[K]):
    """A node; `red` is the color of the link from its parent."""

    __slots__ = ("key", "left", "right", "red")

    def __init__(self, key: K) -> None:
        self.key = key
        self.left: Node[K] | None = None
        self.right: Node[K] | None = None
        self.red = RED


def is_red(h: Node[K] | None) -> bool:
    return h is not None and h.red


def rotate_left(h: Node[K]) -> Node[K]:
    """Turn the red right link of h into a left link. O(1)."""
    x = h.right
    assert x is not None
    h.right = x.left
    x.left = h
    x.red = h.red
    h.red = RED
    return x


def rotate_right(h: Node[K]) -> Node[K]:
    """Turn the red left link of h into a right link. O(1)."""
    x = h.left
    assert x is not None
    h.left = x.right
    x.right = h
    x.red = h.red
    h.red = RED
    return x


def flip_colors(h: Node[K]) -> None:
    """Invert the colors of h and its two children. O(1)."""
    assert h.left is not None and h.right is not None
    h.red = not h.red
    h.left.red = not h.left.red
    h.right.red = not h.right.red


def fix_up(h: Node[K]) -> Node[K]:
    """Restore the left-leaning shape at h on the way up. O(1)."""
    if is_red(h.right) and not is_red(h.left):  # @line L6
        h = rotate_left(h)
    if is_red(h.left) and h.left is not None and is_red(h.left.left):  # @line L7
        h = rotate_right(h)
    if is_red(h.left) and is_red(h.right):  # @line L8
        flip_colors(h)
    return h  # @line L9


def put(h: Node[K] | None, k: K) -> Node[K]:
    """Insert k below h and return the new root of the subtree."""
    if h is None:  # @line L1
        return Node(k)
    if k < h.key:  # @line L2
        h.left = put(h.left, k)
    elif h.key < k:  # @line L3
        h.right = put(h.right, k)
    else:  # @line L4
        return h
    return fix_up(h)  # @line L5


def move_red_left(h: Node[K]) -> Node[K]:
    """h is red and h.left, h.left.left are black: make h.left or one of its
    children red, borrowing from the right sibling when it can. O(1)."""
    flip_colors(h)  # @line L16
    assert h.right is not None
    if is_red(h.right.left):  # @line L17
        h.right = rotate_right(h.right)
        h = rotate_left(h)
        flip_colors(h)
    return h


def move_red_right(h: Node[K]) -> Node[K]:
    """h is red and h.right, h.right.left are black: make h.right or one of
    its children red. O(1)."""
    flip_colors(h)  # @line L18
    assert h.left is not None
    if is_red(h.left.left):  # @line L19
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
    """Delete k from the subtree of h and return its new root. O(log n).

    Precondition: k is in the subtree, and h is red, or h.left is red, or
    h.right is red with k >= h.key (h is not a 2-node).
    """
    if k < h.key:  # @line L20
        assert h.left is not None
        if not is_red(h.left) and not is_red(h.left.left):  # @line L21
            h = move_red_left(h)
        assert h.left is not None
        h.left = remove(h.left, k)  # @line L22
    else:
        if is_red(h.left):  # @line L23
            h = rotate_right(h)
        if not (k < h.key) and not (h.key < k) and h.right is None:  # @line L24
            return None
        assert h.right is not None
        if not is_red(h.right) and not is_red(h.right.left):  # @line L25
            h = move_red_right(h)
        assert h.right is not None
        if not (k < h.key) and not (h.key < k):  # @line L26
            m = h.right
            while m.left is not None:
                m = m.left
            h.key = m.key
            h.right = delete_min(h.right)
        else:
            h.right = remove(h.right, k)  # @line L27
    return fix_up(h)  # @line L28


class LeftLeaningRedBlackTree(Generic[K]):
    """An ordered set kept as a left-leaning red-black tree (the 2-3 form).

    Keys must be totally ordered. Search, insertion and deletion cost
    O(log n) time in the worst case; the height is at most 2 lg(n + 1).
    """

    def __init__(self) -> None:
        self.root: Node[K] | None = None
        self.size = 0

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

    def insert(self, k: K) -> bool:
        """Add k; return False if it was already present. O(log n)."""
        if self.contains(k):
            return False
        self.root = put(self.root, k)
        self.root.red = BLACK  # @line L10
        self.size += 1
        return True

    def delete(self, k: K) -> bool:
        """Remove k; return False if it was absent. O(log n)."""
        if not self.contains(k):  # @line L11
            return False
        assert self.root is not None
        if not is_red(self.root.left) and not is_red(self.root.right):  # @line L12
            self.root.red = RED
        self.root = remove(self.root, k)  # @line L13
        if self.root is not None:  # @line L14
            self.root.red = BLACK
        self.size -= 1  # @line L15
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
        """The number of nodes on the longest downward path."""

        def ht(h: Node[K] | None) -> int:
            return 0 if h is None else 1 + max(ht(h.left), ht(h.right))

        return ht(self.root)

    def __len__(self) -> int:
        return self.size

    def check_invariant(self) -> None:
        """Raise AssertionError unless the tree is a valid left-leaning
        red-black tree: search order, black root, no red right link, no two
        red links in a row, and the same number of black links on every
        path from the root to nil."""
        assert not is_red(self.root), "the root is black"
        count = 0

        def walk(h: Node[K] | None, lo: K | None, hi: K | None) -> int:
            nonlocal count
            if h is None:
                return 0
            count += 1
            assert lo is None or lo < h.key
            assert hi is None or h.key < hi
            assert not is_red(h.right), "no red right link"
            if h.red:
                assert not is_red(h.left), "no two red links in a row"
            bl = walk(h.left, lo, h.key)
            br = walk(h.right, h.key, hi)
            assert bl == br, "perfect black balance"
            return bl + (0 if h.red else 1)

        walk(self.root, None, None)
        assert count == self.size
