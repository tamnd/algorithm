# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/threaded-binary-tree/. The authors are listed in prov/EJENNS.jsonl.

from collections.abc import Iterator
from typing import Any, Generic, TypeVar

K = TypeVar("K")


class Node(Generic[K]):
    """A node of a fully threaded binary search tree.

    If lthread is True, left is a thread to the in-order predecessor (or
    None for the smallest key); else left is the left child. The same holds
    for rthread, right and the in-order successor.
    """

    __slots__ = ("key", "left", "right", "lthread", "rthread")

    def __init__(self, key: K) -> None:
        self.key = key
        self.left: "Node[K] | None" = None
        self.right: "Node[K] | None" = None
        self.lthread = True
        self.rthread = True


class ThreadedBinarySearchTree(Generic[K]):
    """A fully threaded binary search tree of distinct keys.

    Empty child fields hold threads to the in-order neighbours, so an
    in-order walk needs no stack and no parent pointers. Search and insert
    take O(h) time for height h; a full walk takes O(n) time and O(1) space.
    """

    def __init__(self) -> None:
        self.root: Node[K] | None = None
        self.n = 0

    def __len__(self) -> int:
        return self.n

    @staticmethod
    def successor_node(x: Node[K]) -> Node[K] | None:
        """The in-order successor of x, or None. O(h) worst, O(1) amortized in a walk."""
        if x.rthread:  # @line L1
            return x.right
        y = x.right  # @line L2
        assert y is not None
        while not y.lthread:  # @line L3
            y = y.left  # type: ignore[assignment]
        return y  # @line L4

    @staticmethod
    def predecessor_node(x: Node[K]) -> Node[K] | None:
        if x.lthread:
            return x.left
        y = x.left
        assert y is not None
        while not y.rthread:
            y = y.right  # type: ignore[assignment]
        return y

    def minimum_node(self) -> Node[K] | None:
        x = self.root
        if x is None:
            return None
        while not x.lthread:
            x = x.left  # type: ignore[assignment]
        return x

    def search(self, k: K) -> Node[K] | None:
        """The node with key k, or None. Threads end the search like NIL."""
        x = self.root
        while x is not None:
            if k < x.key:
                if x.lthread:
                    return None
                x = x.left
            elif x.key < k:
                if x.rthread:
                    return None
                x = x.right
            else:
                return x
        return None

    def insert(self, k: K) -> bool:
        """Insert k. Return False if k was already a key. O(h) time."""
        if self.root is None:  # @line L5
            self.root = Node(k)
            self.n = 1
            return True
        x = self.root  # @line L6
        while True:  # @line L7
            if not (k < x.key or x.key < k):  # @line L8
                return False
            if k < x.key:  # @line L9
                if not x.lthread:  # @line L10
                    x = x.left  # type: ignore[assignment]
                    continue
                z = Node(k)  # @line L11
                z.left, z.right = x.left, x
                x.left, x.lthread = z, False
                break
            if not x.rthread:  # @line L12
                x = x.right  # type: ignore[assignment]
                continue
            z = Node(k)  # @line L13
            z.left, z.right = x, x.right
            x.right, x.rthread = z, False
            break
        self.n += 1
        return True

    def successor(self, k: K) -> K | None:
        x = self.search(k)
        if x is None:
            raise KeyError(k)
        s = self.successor_node(x)
        return None if s is None else s.key

    def predecessor(self, k: K) -> K | None:
        x = self.search(k)
        if x is None:
            raise KeyError(k)
        s = self.predecessor_node(x)
        return None if s is None else s.key

    def __iter__(self) -> Iterator[K]:
        """In-order walk with O(1) extra space."""
        x = self.minimum_node()
        while x is not None:
            yield x.key
            x = self.successor_node(x)

    def check_invariant(self) -> None:
        """Check the BST property on child links and every thread."""
        order: list[Node[K]] = []
        stack: list[Node[K]] = []
        x = self.root
        while stack or x is not None:  # in-order walk on child links only
            while x is not None:
                stack.append(x)
                x = None if x.lthread else x.left
            x = stack.pop()
            order.append(x)
            x = None if x.rthread else x.right
        assert len(order) == self.n
        for i, node in enumerate(order):
            if i > 0:
                assert order[i - 1].key < node.key
            if node.lthread:
                assert node.left is (order[i - 1] if i > 0 else None)
            if node.rthread:
                assert node.right is (order[i + 1] if i + 1 < len(order) else None)

    def threads(self) -> dict[Any, tuple[Any, Any]]:
        """For each key, the keys its threads point to ('-' for a child link)."""
        out = {}
        stack = [self.root] if self.root else []
        while stack:
            x = stack.pop()
            lt = (x.left.key if x.left else None) if x.lthread else "-"
            rt = (x.right.key if x.right else None) if x.rthread else "-"
            out[x.key] = (lt, rt)
            if not x.lthread:
                stack.append(x.left)
            if not x.rthread:
                stack.append(x.right)
        return out
