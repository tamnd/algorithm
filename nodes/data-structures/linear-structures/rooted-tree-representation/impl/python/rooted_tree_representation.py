# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rooted-tree-representation/. The authors are listed in prov/X6DGHS.jsonl.

from typing import Generic, Iterator, TypeVar

T = TypeVar("T")


class Node(Generic[T]):
    """A tree node with a key and three pointers: parent, leftmost child, next sibling."""

    __slots__ = ("key", "p", "left_child", "right_sibling")

    def __init__(self, key: T) -> None:
        self.key = key
        self.p: Node[T] | None = None
        self.left_child: Node[T] | None = None
        self.right_sibling: Node[T] | None = None


class RootedTree(Generic[T]):
    """Rooted trees of any degree in the left-child, right-sibling form.

    Each node keeps three pointers whatever its number of children, so a tree
    of n nodes takes Theta(n) space. new_node, add_child and parent cost O(1);
    children(x) costs Theta(deg x); detach(y) costs O(deg of the parent of y);
    preorder costs Theta(n) time and O(1) extra space.
    """

    def new_node(self, key: T) -> Node[T]:
        """Return a new tree that has one node. Cost O(1)."""
        return Node(key)  # @line L1

    def add_child(self, x: Node[T], y: Node[T]) -> None:
        """Make the root y the new leftmost child of x.

        Precondition: y is a root (no parent, no sibling) and x is not in the
        subtree of y. Cost O(1).
        """
        if y.p is not None or y.right_sibling is not None:
            raise ValueError("y must be a root")
        y.p = x  # @line L2
        y.right_sibling = x.left_child  # @line L3
        x.left_child = y  # @line L4

    def parent(self, x: Node[T]) -> Node[T] | None:
        """Return the parent of x, or None for a root. Cost O(1)."""
        return x.p

    def children(self, x: Node[T]) -> Iterator[Node[T]]:
        """Yield the children of x from left to right. Cost Theta(deg x)."""
        c = x.left_child  # @line L5
        while c is not None:  # @line L6
            yield c  # @line L7
            c = c.right_sibling

    def preorder(self, r: Node[T]) -> list[T]:
        """Return the keys of the subtree of r in preorder. Theta(n) time, O(1) extra space besides the output."""
        out: list[T] = []
        x: Node[T] | None = r  # @line L8
        while x is not None:  # @line L9
            out.append(x.key)  # @line L10
            if x.left_child is not None:  # @line L11
                x = x.left_child
            else:
                while x is not r and x.right_sibling is None:  # @line L12
                    x = x.p  # type: ignore[assignment]
                    assert x is not None
                x = None if x is r else x.right_sibling  # @line L13
        return out

    def postorder(self, r: Node[T]) -> list[T]:
        """Return the keys of the subtree of r in postorder (children before the parent). Theta(n)."""
        out: list[T] = []
        x: Node[T] = r
        while x.left_child is not None:
            x = x.left_child
        while True:
            out.append(x.key)
            if x is r:
                return out
            if x.right_sibling is not None:
                x = x.right_sibling
                while x.left_child is not None:
                    x = x.left_child
            else:
                assert x.p is not None
                x = x.p

    def detach(self, y: Node[T]) -> None:
        """Cut the subtree of y from its parent; y becomes a root. Cost O(deg of the parent)."""
        x = y.p
        if x is None:
            return
        if x.left_child is y:
            x.left_child = y.right_sibling
        else:
            c = x.left_child
            assert c is not None
            while c.right_sibling is not y:
                c = c.right_sibling
                assert c is not None
            c.right_sibling = y.right_sibling
        y.p = None
        y.right_sibling = None

    def check_invariant(self, r: Node[T]) -> int:
        """Check that every child of each node points back to it; return the size of the subtree."""
        count, stack = 0, [r]
        while stack:
            x = stack.pop()
            count += 1
            for c in self.children(x):
                assert c.p is x
                stack.append(c)
        return count
