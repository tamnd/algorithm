# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bst-deletion/. The authors are listed in prov/RSMQKE.jsonl.

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

    def insert(self, k: K, v: V = None) -> None:  # type: ignore[assignment]
        """Leaf insertion, used to build trees for deletion."""
        y, x = None, self.root
        while x is not None:
            y = x
            if k < x.key:
                x = x.left
            elif x.key < k:
                x = x.right
            else:
                x.value = v
                return
        z = Node(k, v)
        z.p = y
        if y is None:
            self.root = z
        elif k < y.key:
            y.left = z
        else:
            y.right = z
        self.n += 1


def tree_delete(t: Tree[K, V], k: K) -> bool:
    """Remove key k and its value from the BST t. Return True if k was a key.

    A node with two children takes the key and value of its successor, and
    the successor node, which has no left child, is spliced out.
    Precondition: t has the BST property. Cost: O(h + 1) for height h.
    """
    z = t.root  # @line L1
    while z is not None and (k < z.key or z.key < k):
        z = z.left if k < z.key else z.right
    if z is None:  # @line L2
        return False
    if z.left is not None and z.right is not None:  # @line L3
        y = z.right  # @line L4
        while y.left is not None:
            y = y.left
        z.key, z.value = y.key, y.value  # @line L5
        z = y  # @line L6
    c = z.left if z.left is not None else z.right  # @line L7
    if c is not None:  # @line L8
        c.p = z.p
    if z.p is None:  # @line L9
        t.root = c
    elif z is z.p.left:  # @line L10
        z.p.left = c
    else:
        z.p.right = c  # @line L11
    t.n -= 1  # @line L12
    return True


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
