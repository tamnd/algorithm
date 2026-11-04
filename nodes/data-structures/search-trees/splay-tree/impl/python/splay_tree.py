# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/splay-tree/. The authors are listed in prov/MX6QFK.jsonl.

"""Splay tree (Sleator and Tarjan 1985) with bottom-up splaying."""

from typing import Any, Iterator


class Node:
    __slots__ = ("key", "value", "left", "right", "p")

    def __init__(self, key: Any, value: Any = None) -> None:
        self.key = key
        self.value = value
        self.left: "Node | None" = None
        self.right: "Node | None" = None
        self.p: "Node | None" = None


def _rotate(x: Node) -> None:
    y = x.p
    assert y is not None
    z = y.p
    if x is y.left:
        y.left = x.right
        if x.right is not None:
            x.right.p = y
        x.right = y
    else:
        y.right = x.left
        if x.left is not None:
            x.left.p = y
        x.left = y
    y.p = x
    x.p = z
    if z is not None:
        if z.left is y:
            z.left = x
        else:
            z.right = x


def _splay(x: Node) -> int:
    """Splay x to the root of its tree; return the number of rotations."""
    rot = 0
    while x.p is not None:
        y = x.p
        z = y.p
        if z is None:
            _rotate(x)
            rot += 1
        elif (x is y.left) == (y is z.left):
            _rotate(y)
            _rotate(x)
            rot += 2
        else:
            _rotate(x)
            _rotate(x)
            rot += 2
    return rot


class SplayTree:
    """Ordered map. Every operation splays, so the amortized cost is O(log n)."""

    def __init__(self) -> None:
        self.root: Node | None = None
        self.n = 0
        self.rotations = 0  # total rotations, for experiments

    def __len__(self) -> int:
        return self.n

    def _splay(self, x: Node) -> None:
        self.rotations += _splay(x)
        self.root = x

    def access(self, key: Any) -> Node | None:
        """Splay the node of key, or the last node on its search path. Return the node of key or None."""
        x = self.root  # @line L1
        last = None
        while x is not None and (key < x.key or x.key < key):  # @line L2
            last = x
            x = x.left if key < x.key else x.right
        if x is None:  # @line L3
            x = last
        if x is not None:  # @line L4
            self._splay(x)
        r = self.root  # @line L5
        if r is not None and not (key < r.key or r.key < key):
            return r
        return None

    def search(self, key: Any) -> Any:
        x = self.access(key)
        return None if x is None else x.value

    def __contains__(self, key: Any) -> bool:
        return self.access(key) is not None

    def insert(self, key: Any, value: Any = None) -> bool:
        """Map key to value; return True if key was new."""
        if self.root is None:  # @line L6
            self.root = Node(key, value)
            self.n = 1
            return True
        found = self.access(key)  # @line L7
        if found is not None:
            found.value = value
            return False
        z = Node(key, value)  # @line L8
        r = self.root
        assert r is not None
        if key < r.key:  # @line L9
            z.left = r.left
            z.right = r
            r.left = None
        else:  # @line L10
            z.right = r.right
            z.left = r
            r.right = None
        for c in (z.left, z.right):  # @line L11
            if c is not None:
                c.p = z
        self.root = z
        self.n += 1
        return True

    def _join(self, left: Node | None, right: Node | None) -> Node | None:
        """Join two trees whose keys are all smaller in left. Return the new root."""
        if left is None:  # @line L15
            if right is not None:
                right.p = None
            return right
        left.p = None
        m = left
        while m.right is not None:  # @line L16
            m = m.right
        self.rotations += _splay(m)
        m.right = right  # @line L17
        if right is not None:
            right.p = m
        return m

    def delete(self, key: Any) -> bool:
        """Remove key; return True if it was present."""
        x = self.access(key)  # @line L12
        if x is None:
            return False
        left, right = x.left, x.right  # @line L13
        if left is not None:
            left.p = None
        if right is not None:
            right.p = None
        self.root = self._join(left, right)  # @line L14
        self.n -= 1
        return True

    def split(self, key: Any) -> "SplayTree":
        """Keep the keys <= key in self; return a new tree with the keys > key."""
        other = SplayTree()
        self.access(key)  # @line L18
        r = self.root
        if r is None:
            return other
        if not (key < r.key):  # @line L19
            rest = r.right
            r.right = None
        else:  # @line L20
            rest = r
            self.root = r.left
            r.left = None
            if self.root is not None:
                self.root.p = None
        if rest is not None:
            rest.p = None
        other.root = rest
        other.n = sum(1 for _ in other.keys())
        self.n -= other.n
        return other

    def join(self, other: "SplayTree") -> None:
        """Append all keys of other, which must all exceed the keys of self."""
        self.root = self._join(self.root, other.root)
        self.n += other.n
        other.root = None
        other.n = 0

    def minimum(self) -> Any:
        x = self.root
        if x is None:
            return None
        while x.left is not None:
            x = x.left
        self._splay(x)
        return x.key

    def floor(self, key: Any) -> Any:
        """The largest key <= key, or None. Splays."""
        self.access(key)
        r = self.root
        if r is None:
            return None
        if not (key < r.key):
            return r.key
        x = r.left
        if x is None:
            return None
        while x.right is not None:
            x = x.right
        self._splay(x)
        return x.key

    def _nodes(self) -> Iterator[Node]:
        stack: list[Node] = []
        x = self.root
        while stack or x is not None:
            while x is not None:
                stack.append(x)
                x = x.left
            x = stack.pop()
            yield x
            x = x.right

    def keys(self) -> Iterator[Any]:
        for x in self._nodes():
            yield x.key

    def items(self) -> Iterator[tuple[Any, Any]]:
        for x in self._nodes():
            yield x.key, x.value

    def height(self) -> int:
        if self.root is None:
            return -1
        best = 0
        stack = [(self.root, 0)]
        while stack:
            x, d = stack.pop()
            best = max(best, d)
            for c in (x.left, x.right):
                if c is not None:
                    stack.append((c, d + 1))
        return best

    def check_invariant(self) -> None:
        """BST order, parent links, and the size count."""
        if self.root is None:
            assert self.n == 0
            return
        assert self.root.p is None
        ks = list(self.keys())
        assert len(ks) == self.n
        assert all(a < b for a, b in zip(ks, ks[1:]))
        stack = [self.root]
        while stack:
            x = stack.pop()
            for c in (x.left, x.right):
                if c is not None:
                    assert c.p is x
                    stack.append(c)
