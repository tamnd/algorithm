# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-search-tree/. The authors are listed in prov/MBF8HP.jsonl.

from collections.abc import Iterator
from typing import Any, Generic, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)
V = TypeVar("V")


class Node(Generic[K, V]):
    """A node with a key, a value, two children and a parent pointer."""

    __slots__ = ("key", "value", "left", "right", "p")

    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value
        self.left: "Node[K, V] | None" = None
        self.right: "Node[K, V] | None" = None
        self.p: "Node[K, V] | None" = None


class BinarySearchTree(Generic[K, V]):
    """An unbalanced binary search tree that maps distinct keys to values.

    Each operation takes O(h) time, where h is the height of the tree. The
    height is between floor(lg n) and n - 1. All loops are iterative, so a
    tall tree does not overflow the Python stack. Keys need only "<".
    """

    def __init__(self) -> None:
        self.root: Node[K, V] | None = None
        self.n = 0

    def __len__(self) -> int:
        return self.n

    def search_node(self, k: K) -> Node[K, V] | None:
        """Return the node with key k, or None."""
        x = self.root  # @line L1
        while x is not None and (k < x.key or x.key < k):  # @line L2
            x = x.left if k < x.key else x.right  # @line L3
        return x  # @line L4

    def search(self, k: K) -> V | None:
        """Return the value of k, or None if k is not a key."""
        x = self.search_node(k)
        return None if x is None else x.value

    def contains(self, k: K) -> bool:
        return self.search_node(k) is not None

    @staticmethod
    def minimum_node(x: Node[K, V]) -> Node[K, V]:
        """Return the node with the smallest key in the subtree of x."""
        while x.left is not None:  # @line L5
            x = x.left
        return x  # @line L6

    @staticmethod
    def maximum_node(x: Node[K, V]) -> Node[K, V]:
        while x.right is not None:
            x = x.right
        return x

    def minimum(self) -> K | None:
        return None if self.root is None else self.minimum_node(self.root).key

    def maximum(self) -> K | None:
        return None if self.root is None else self.maximum_node(self.root).key

    def successor_node(self, x: Node[K, V]) -> Node[K, V] | None:
        """Return the node with the next larger key, or None."""
        if x.right is not None:  # @line L7
            return self.minimum_node(x.right)
        y = x.p  # @line L8
        while y is not None and x is y.right:  # @line L9
            x, y = y, y.p
        return y  # @line L10

    def predecessor_node(self, x: Node[K, V]) -> Node[K, V] | None:
        if x.left is not None:
            return self.maximum_node(x.left)
        y = x.p
        while y is not None and x is y.left:
            x, y = y, y.p
        return y

    def successor(self, k: K) -> K | None:
        """The next larger key after the key k of the tree, or None."""
        x = self.search_node(k)
        if x is None:
            raise KeyError(k)
        s = self.successor_node(x)
        return None if s is None else s.key

    def predecessor(self, k: K) -> K | None:
        x = self.search_node(k)
        if x is None:
            raise KeyError(k)
        s = self.predecessor_node(x)
        return None if s is None else s.key

    def insert(self, k: K, v: V = None) -> None:  # type: ignore[assignment]
        """Map k to v. If k is a key, replace its value."""
        y, x = None, self.root  # @line L11
        while x is not None:  # @line L12
            y = x  # @line L13
            if k < x.key:  # @line L14
                x = x.left
            elif x.key < k:
                x = x.right
            else:
                x.value = v  # @line L15
                return
        z = Node(k, v)
        z.p = y  # @line L16
        if y is None:  # @line L17
            self.root = z
        elif k < y.key:  # @line L18
            y.left = z
        else:
            y.right = z  # @line L19
        self.n += 1

    def _transplant(self, u: Node[K, V], v: Node[K, V] | None) -> None:
        """Put the subtree of v in the place of the subtree of u."""
        if u.p is None:  # @line L20
            self.root = v
        elif u is u.p.left:  # @line L21
            u.p.left = v
        else:
            u.p.right = v  # @line L22
        if v is not None:  # @line L23
            v.p = u.p

    def delete(self, k: K) -> bool:
        """Remove k and its value. Return True if k was a key."""
        z = self.search_node(k)
        if z is None:
            return False
        if z.left is None:  # @line L24
            self._transplant(z, z.right)
        elif z.right is None:  # @line L25
            self._transplant(z, z.left)
        else:
            y = self.minimum_node(z.right)  # @line L26
            if y is not z.right:  # @line L27
                self._transplant(y, y.right)
                y.right = z.right
                y.right.p = y
            self._transplant(z, y)  # @line L28
            y.left = z.left
            y.left.p = y
        self.n -= 1
        return True

    def items(self) -> Iterator[tuple[K, V]]:
        """The pairs in increasing order of key (in-order walk with a stack)."""
        stack: list[Node[K, V]] = []
        x = self.root
        while stack or x is not None:
            while x is not None:
                stack.append(x)
                x = x.left
            x = stack.pop()
            yield x.key, x.value
            x = x.right

    def keys(self) -> list[K]:
        return [k for k, _ in self.items()]

    def height(self) -> int:
        """The number of edges on a longest root-to-leaf path; -1 if empty."""
        if self.root is None:
            return -1
        best, stack = 0, [(self.root, 0)]
        while stack:
            x, d = stack.pop()
            best = max(best, d)
            for c in (x.left, x.right):
                if c is not None:
                    stack.append((c, d + 1))
        return best

    def check_invariant(self) -> None:
        """Check the BST property, the parent pointers and the count."""
        count = 0
        stack: list[tuple[Node[K, V], Any, Any]] = []
        if self.root is not None:
            assert self.root.p is None
            stack.append((self.root, None, None))
        while stack:
            x, lo, hi = stack.pop()
            count += 1
            assert lo is None or lo < x.key
            assert hi is None or x.key < hi
            if x.left is not None:
                assert x.left.p is x
                stack.append((x.left, lo, x.key))
            if x.right is not None:
                assert x.right.p is x
                stack.append((x.right, x.key, hi))
        assert count == self.n
