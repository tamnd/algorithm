# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bst-insertion/. The authors are listed in prov/82JNAM.jsonl.

from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class Node(Generic[K, V]):
    """A node of a binary search tree, with a parent pointer."""

    __slots__ = ("key", "value", "left", "right", "p")

    def __init__(self, key: K, value: V = None) -> None:  # type: ignore[assignment]
        self.key = key
        self.value = value
        self.left: "Node[K, V] | None" = None
        self.right: "Node[K, V] | None" = None
        self.p: "Node[K, V] | None" = None


class Tree(Generic[K, V]):
    """A binary search tree: a root and a count of nodes."""

    def __init__(self) -> None:
        self.root: Node[K, V] | None = None
        self.n = 0


def tree_insert(t: Tree[K, V], k: K, v: V = None) -> Node[K, V]:  # type: ignore[assignment]
    """Insert key k with value v into the BST t and return its node.

    If k is already a key, its value is replaced and no node is added.
    Precondition: t has the BST property. The keys need only "<".
    Cost: O(h + 1) comparisons, where h is the height of t. Extra space O(1).
    """
    y: Node[K, V] | None = None  # @line L1
    x = t.root
    while x is not None:  # @line L2
        y = x  # @line L3
        if k < x.key:  # @line L4
            x = x.left
        elif x.key < k:  # @line L5
            x = x.right
        else:
            x.value = v  # @line L6
            return x
    z = Node(k, v)  # @line L7
    z.p = y
    if y is None:  # @line L8
        t.root = z
    elif k < y.key:  # @line L9
        y.left = z
    else:
        y.right = z  # @line L10
    t.n += 1  # @line L11
    return z


def depth(z: Node[K, V]) -> int:
    """The number of edges from the root to z."""
    d = 0
    while z.p is not None:
        z = z.p
        d += 1
    return d


def inorder(t: Tree[K, V]) -> list[K]:
    """The keys of t in in-order, with an explicit stack."""
    out, stack, x = [], [], t.root
    while stack or x is not None:
        while x is not None:
            stack.append(x)
            x = x.left
        x = stack.pop()
        out.append(x.key)
        x = x.right
    return out
