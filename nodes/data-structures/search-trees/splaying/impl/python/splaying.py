# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/splaying/. The authors are listed in prov/AA2JCV.jsonl.

"""Bottom-up splaying (Sleator and Tarjan 1985) on nodes with parent pointers."""

from typing import Any, Iterator


class Node:
    """A BST node with a parent pointer."""

    __slots__ = ("key", "left", "right", "p")

    def __init__(self, key: Any) -> None:
        self.key = key
        self.left: "Node | None" = None
        self.right: "Node | None" = None
        self.p: "Node | None" = None


def rotate(x: Node) -> None:
    """Rotate x above its parent. x must have a parent. O(1) time."""
    y = x.p  # @line L7
    assert y is not None
    z = y.p
    if x is y.left:  # @line L8
        y.left = x.right
        if x.right is not None:
            x.right.p = y
        x.right = y
    else:  # @line L9
        y.right = x.left
        if x.left is not None:
            x.left.p = y
        x.left = y
    y.p = x  # @line L10
    x.p = z
    if z is not None:  # @line L11
        if z.left is y:
            z.left = x
        else:
            z.right = x


def splay(x: Node) -> tuple[Node, int]:
    """Splay x to the root of its tree. Return (new root, number of rotations)."""
    rotations = 0
    while x.p is not None:  # @line L1
        y = x.p  # @line L2
        z = y.p
        if z is None:  # @line L3
            rotate(x)  # zig
            rotations += 1
        elif (x is y.left) == (y is z.left):  # @line L4
            rotate(y)  # zig-zig: the parent first
            rotate(x)
            rotations += 2
        else:  # @line L5
            rotate(x)  # zig-zag: x twice
            rotate(x)
            rotations += 2
    return x, rotations  # @line L6


def insert(root: Node | None, key: Any) -> tuple[Node, Node]:
    """Plain leaf insertion (no splay); returns (root, node of key)."""
    z = Node(key)
    if root is None:
        return z, z
    x = root
    while True:
        if key < x.key:
            if x.left is None:
                x.left = z
                z.p = x
                return root, z
            x = x.left
        elif x.key < key:
            if x.right is None:
                x.right = z
                z.p = x
                return root, z
            x = x.right
        else:
            return root, x


def find(root: Node | None, key: Any) -> Node | None:
    x = root
    while x is not None and (key < x.key or x.key < key):
        x = x.left if key < x.key else x.right
    return x


def inorder(root: Node | None) -> Iterator[Any]:
    stack: list[Node] = []
    x = root
    while stack or x is not None:
        while x is not None:
            stack.append(x)
            x = x.left
        x = stack.pop()
        yield x.key
        x = x.right


def depth(x: Node) -> int:
    d = 0
    while x.p is not None:
        x = x.p
        d += 1
    return d


def check_tree(root: Node | None) -> None:
    """Raise AssertionError unless parent pointers and the BST order are right."""
    if root is None:
        return
    assert root.p is None
    keys = list(inorder(root))
    assert all(a < b for a, b in zip(keys, keys[1:]))
    stack = [root]
    while stack:
        x = stack.pop()
        for c in (x.left, x.right):
            if c is not None:
                assert c.p is x
                stack.append(c)
