# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-sort/. The authors are listed in prov/P5E3N3.jsonl.

from typing import Generic, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


class Node(Generic[T]):
    __slots__ = ("key", "left", "right")

    def __init__(self, key: T) -> None:
        self.key = key
        self.left: "Node[T] | None" = None
        self.right: "Node[T] | None" = None


def insert(root: "Node[T] | None", x: T) -> tuple["Node[T]", int]:
    """Insert x without recursion: left if x < key, else right. Return the root and the number of comparisons."""
    node = Node(x)
    if root is None:
        return node, 0
    u = root
    count = 0
    while True:
        count += 1
        if x < u.key:
            if u.left is None:
                u.left = node
                return root, count
            u = u.left
        else:
            if u.right is None:
                u.right = node
                return root, count
            u = u.right


def inorder(root: "Node[T] | None") -> list[T]:
    """Return the keys in inorder, with an explicit stack."""
    out: list[T] = []
    stack: list[Node[T]] = []
    u = root
    while stack or u is not None:
        while u is not None:
            stack.append(u)
            u = u.left
        u = stack.pop()
        out.append(u.key)
        u = u.right
    return out


def tree_sort(a: list[T]) -> int:
    """Sort the list a in place, stably. Return the number of comparisons."""
    root: Node[T] | None = None  # @line L1
    total = 0
    for x in a:  # @line L2
        root, c = insert(root, x)  # @line L3
        total += c
    i = 0  # @line L4
    for key in inorder(root):  # @line L5
        a[i] = key  # @line L6
        i += 1
    return total
