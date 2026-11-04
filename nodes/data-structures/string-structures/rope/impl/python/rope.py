# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rope/. The authors are listed in prov/K8GJQ9.jsonl.

"""Rope: an immutable string kept as a height-balanced binary tree of short strings.

Leaves hold nonempty strings; an inner node holds its total length and its
height, and its text is the text of its left child followed by that of its
right child. Heights obey the AVL rule (children differ by at most 1), so the
depth is O(log n). Concatenation joins two trees down the spine of the taller
one; split, insert and delete are built from split and concatenation. All
operations return new ropes and share unchanged subtrees with the old ones.
Recursion is used only along root-to-leaf paths, whose length is O(log n).
"""

from __future__ import annotations


class _Leaf:
    __slots__ = ("s", "length", "height")

    def __init__(self, s: str) -> None:
        self.s = s
        self.length = len(s)
        self.height = 0


class _Node:
    __slots__ = ("left", "right", "length", "height")

    def __init__(self, left: _Tree, right: _Tree) -> None:
        self.left = left
        self.right = right
        self.length = left.length + right.length
        self.height = 1 + max(left.height, right.height)


_Tree = _Leaf | _Node


def _rotate_left(t: _Node) -> _Node:
    r = t.right
    assert isinstance(r, _Node)
    return _Node(_Node(t.left, r.left), r.right)


def _rotate_right(t: _Node) -> _Node:
    lft = t.left
    assert isinstance(lft, _Node)
    return _Node(lft.left, _Node(lft.right, t.right))


def _balance(t: _Node) -> _Node:
    """Fix a node whose children differ in height by at most 2."""
    lh, rh = t.left.height, t.right.height
    if lh > rh + 1:
        lft = t.left
        assert isinstance(lft, _Node)
        if lft.left.height < lft.right.height:
            t = _Node(_rotate_left(lft), t.right)
        return _rotate_right(t)
    if rh > lh + 1:
        r = t.right
        assert isinstance(r, _Node)
        if r.right.height < r.left.height:
            t = _Node(t.left, _rotate_right(r))
        return _rotate_left(t)
    return t


def _concat(a: _Tree | None, b: _Tree | None, leaf_max: int) -> _Tree | None:
    if a is None:  # @line L5
        return b
    if b is None:
        return a
    if isinstance(a, _Leaf) and isinstance(b, _Leaf) and a.length + b.length <= leaf_max:
        return _Leaf(a.s + b.s)
    if abs(a.height - b.height) <= 1:  # @line L6
        return _Node(a, b)
    if a.height > b.height:  # @line L7
        assert isinstance(a, _Node)
        c = _concat(a.right, b, leaf_max)
        assert c is not None
        return _balance(_Node(a.left, c))
    assert isinstance(b, _Node)  # @line L8
    c = _concat(a, b.left, leaf_max)
    assert c is not None
    return _balance(_Node(c, b.right))


def _split(t: _Tree | None, i: int, leaf_max: int) -> tuple[_Tree | None, _Tree | None]:
    """Split into the first i characters and the rest."""
    if t is None:
        return None, None
    if isinstance(t, _Leaf):  # @line L9
        x = _Leaf(t.s[:i]) if i > 0 else None
        y = _Leaf(t.s[i:]) if i < t.length else None
        return x, y
    if i <= t.left.length:  # @line L10
        x, y = _split(t.left, i, leaf_max)
        return x, _concat(y, t.right, leaf_max)
    x, y = _split(t.right, i - t.left.length, leaf_max)  # @line L11
    return _concat(t.left, x, leaf_max), y


def _build(s: str, leaf_max: int) -> _Tree | None:
    """Balanced tree over the chunks of s; halves differ by at most one chunk."""
    chunks = [_Leaf(s[k : k + leaf_max]) for k in range(0, len(s), leaf_max)]

    def make(lo: int, hi: int) -> _Tree:
        if hi - lo == 1:
            return chunks[lo]
        mid = (lo + hi + 1) // 2
        return _Node(make(lo, mid), make(mid, hi))

    return make(0, len(chunks)) if chunks else None


class Rope:
    """An immutable string with O(log n) index, concatenation, split, insert and delete."""

    __slots__ = ("root", "leaf_max")

    def __init__(self, s: str = "", leaf_max: int = 64) -> None:
        if leaf_max < 1:
            raise ValueError("leaf_max must be positive")
        self.leaf_max = leaf_max
        self.root: _Tree | None = _build(s, leaf_max)

    @classmethod
    def _of(cls, root: _Tree | None, leaf_max: int) -> Rope:
        r = cls.__new__(cls)
        r.root, r.leaf_max = root, leaf_max
        return r

    def __len__(self) -> int:
        return 0 if self.root is None else self.root.length

    def char_at(self, i: int) -> str:
        """Return the character at position i."""
        if not 0 <= i < len(self):
            raise IndexError("position out of range")
        t = self.root
        while isinstance(t, _Node):  # @line L1
            if i < t.left.length:  # @line L2
                t = t.left
            else:  # @line L3
                i -= t.left.length
                t = t.right
        assert isinstance(t, _Leaf)
        return t.s[i]  # @line L4

    def concat(self, other: Rope) -> Rope:
        return Rope._of(_concat(self.root, other.root, self.leaf_max), self.leaf_max)

    def split(self, i: int) -> tuple[Rope, Rope]:
        """Return the ropes of the first i characters and of the rest."""
        if not 0 <= i <= len(self):
            raise IndexError("split position out of range")
        x, y = _split(self.root, i, self.leaf_max)
        return Rope._of(x, self.leaf_max), Rope._of(y, self.leaf_max)

    def insert(self, i: int, s: str) -> Rope:
        """Return the rope with s inserted so that it starts at position i."""
        x, y = self.split(i)  # @line L12
        return x.concat(Rope(s, self.leaf_max)).concat(y)  # @line L13

    def delete(self, i: int, j: int) -> Rope:
        """Return the rope without the characters at positions i .. j - 1."""
        if not 0 <= i <= j <= len(self):
            raise IndexError("delete range out of range")
        x, y = self.split(i)  # @line L14
        _, z = y.split(j - i)
        return x.concat(z)  # @line L15

    def substring(self, i: int, j: int) -> str:
        if not 0 <= i <= j <= len(self):
            raise IndexError("range out of range")
        return self.split(j)[0].split(i)[1].to_string()

    def to_string(self) -> str:
        out: list[str] = []
        stack = [self.root]
        while stack:
            t = stack.pop()
            if t is None:
                continue
            if isinstance(t, _Leaf):
                out.append(t.s)
            else:
                stack.append(t.right)
                stack.append(t.left)
        return "".join(out)

    def height(self) -> int:
        return -1 if self.root is None else self.root.height

    def leaf_count(self) -> int:
        count, stack = 0, [self.root]
        while stack:
            t = stack.pop()
            if isinstance(t, _Leaf):
                count += 1
            elif t is not None:
                stack.extend((t.left, t.right))
        return count

    def check_invariant(self) -> None:
        stack = [self.root]
        while stack:
            t = stack.pop()
            if t is None:
                continue
            if isinstance(t, _Leaf):
                assert 0 < t.length == len(t.s) <= self.leaf_max and t.height == 0, "bad leaf"
            else:
                assert t.length == t.left.length + t.right.length, "bad length"
                assert t.height == 1 + max(t.left.height, t.right.height), "bad height"
                assert abs(t.left.height - t.right.height) <= 1, "not balanced"
                stack.extend((t.left, t.right))
