# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bst-search/. The authors are listed in prov/EJR7Z3.jsonl.

from typing import Any, Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class Node(Generic[K, V]):
    """A node of a binary search tree."""

    __slots__ = ("key", "value", "left", "right")

    def __init__(self, key: K, value: V = None) -> None:  # type: ignore[assignment]
        self.key = key
        self.value = value
        self.left: "Node[K, V] | None" = None
        self.right: "Node[K, V] | None" = None


def tree_search(x: Node[K, V] | None, k: K) -> Node[K, V] | None:
    """Return the node with key k in the BST rooted at x, or None.

    Precondition: the tree rooted at x has the BST property. The keys need
    only "<"; two keys are equal when neither is less than the other.
    Cost: O(d + 1) comparisons, where d is the depth where the search stops;
    O(h + 1) in the worst case. Extra space: O(1).
    """
    while x is not None:  # @line L1
        if not (k < x.key or x.key < k):  # @line L2
            return x
        if k < x.key:  # @line L3
            x = x.left
        else:
            x = x.right  # @line L4
    return None  # @line L5


def tree_search_path(x: Node[K, V] | None, k: K) -> list[Any]:
    """The keys compared by tree_search(x, k), in order."""
    path = []
    while x is not None:
        path.append(x.key)
        if not (k < x.key or x.key < k):
            break
        x = x.left if k < x.key else x.right
    return path


def insert(root: Node[K, V] | None, k: K, v: V = None) -> Node[K, V]:  # type: ignore[assignment]
    """Insert k into the BST rooted at root and return the root (a helper)."""
    z = Node(k, v)
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
            x.value = v
            return root
