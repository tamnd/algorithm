# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/left-child-right-sibling/. The authors are listed in prov/NWHW83.jsonl.

from typing import Iterator

NIL = -1


class LCRSTree:
    """A rooted ordered tree on the nodes 0, 1, 2, ... with three arrays.

    child[x] is the leftmost child of x, sibling[x] the next sibling of x to
    the right, and parent[x] the parent of x. NIL (-1) marks a missing link.
    Node 0 is the root.
    """

    def __init__(self) -> None:
        self.child: list[int] = [NIL]
        self.sibling: list[int] = [NIL]
        self.parent: list[int] = [NIL]

    def size(self) -> int:
        return len(self.child)

    def add_child(self, p: int) -> int:
        """Add a new node as the leftmost child of p and return it."""
        x = len(self.child)
        self.child.append(NIL)
        self.parent.append(p)  # @line L1
        self.sibling.append(self.child[p])  # @line L2
        self.child[p] = x  # @line L3
        return x

    def children(self, p: int) -> Iterator[int]:
        c = self.child[p]  # @line L4
        while c != NIL:  # @line L5
            yield c  # @line L6
            c = self.sibling[c]  # @line L7

    def degree(self, p: int) -> int:
        return sum(1 for _ in self.children(p))

    def preorder(self, r: int = 0) -> list[int]:
        out: list[int] = []
        stack = [r]  # @line L8
        while stack:  # @line L9
            x = stack.pop()  # @line L10
            out.append(x)  # @line L11
            if x != r and self.sibling[x] != NIL:  # @line L12
                stack.append(self.sibling[x])
            if self.child[x] != NIL:  # @line L13
                stack.append(self.child[x])
        return out

    def postorder(self, r: int = 0) -> list[int]:
        """Children before parents: the inorder of the binary tree (child = left, sibling = right)."""
        out: list[int] = []
        stack: list[tuple[int, bool]] = [(r, False)]
        while stack:
            x, done = stack.pop()
            if done:
                out.append(x)
                continue
            if x != r and self.sibling[x] != NIL:
                stack.append((self.sibling[x], False))
            stack.append((x, True))
            if self.child[x] != NIL:
                stack.append((self.child[x], False))
        return out

    def depth(self, x: int) -> int:
        d = 0
        while self.parent[x] != NIL:
            x = self.parent[x]
            d += 1
        return d


def from_parent_array(parent: list[int]) -> LCRSTree:
    """Build the tree of a parent array (root 0, parent[0] = -1); children in increasing order.

    Node i of the result is node i of the input.
    """
    n = len(parent)
    t = LCRSTree()
    t.child = [NIL] * n
    t.sibling = [NIL] * n
    t.parent = list(parent)
    for x in range(n - 1, 0, -1):
        p = parent[x]
        t.sibling[x] = t.child[p]
        t.child[p] = x
    return t
