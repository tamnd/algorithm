# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bst-floor-and-ceiling/. The authors are listed in prov/85F3S3.jsonl.

from typing import Generic, TypeVar

K = TypeVar("K")


class Node(Generic[K]):
    """A node of a binary search tree."""

    __slots__ = ("key", "left", "right")

    def __init__(self, key: K) -> None:
        self.key = key
        self.left: "Node[K] | None" = None
        self.right: "Node[K] | None" = None


def floor(x: Node[K] | None, k: K) -> K | None:
    """The largest key <= k in the BST rooted at x, or None.

    Precondition: the tree has the BST property. Keys need only "<".
    Cost: O(h + 1) comparisons for height h; O(1) extra space.
    """
    best: Node[K] | None = None  # @line L1
    while x is not None:  # @line L2
        if not (k < x.key or x.key < k):  # @line L3
            return x.key
        if k < x.key:  # @line L4
            x = x.left
        else:
            best = x  # @line L5
            x = x.right
    return None if best is None else best.key  # @line L6


def ceiling(x: Node[K] | None, k: K) -> K | None:
    """The smallest key >= k in the BST rooted at x, or None. Cost O(h + 1)."""
    best: Node[K] | None = None  # @line L7
    while x is not None:  # @line L8
        if not (k < x.key or x.key < k):  # @line L9
            return x.key
        if x.key < k:  # @line L10
            x = x.right
        else:
            best = x  # @line L11
            x = x.left
    return None if best is None else best.key  # @line L12


def insert(root: Node[K] | None, k: K) -> Node[K]:
    """Leaf insertion of k (a helper to build trees); returns the root."""
    z = Node(k)
    if root is None:
        return z
    x = root
    while True:
        if k < x.key:
            if x.left is None:
                x.left = z
                return root
            x = x.left
        elif x.key < k:
            if x.right is None:
                x.right = z
                return root
            x = x.right
        else:
            return root
