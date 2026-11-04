# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dfuds/. The authors are listed in prov/BT52AM.jsonl.
"""DFUDS: the depth-first unary degree sequence of an ordinal tree.

U = ( followed by, for each node in preorder, d opening parentheses and
one closing one, where d is its degree. U is balanced, of 2n symbols
counted with the leading '('. A node is named by the position where its
code starts; the root is at 1. findclose, findopen and fwdsearch are
plain scans here; the range min-max tree makes them O(log n) or O(1).
"""

from __future__ import annotations

from typing import Optional, Sequence


class DFUDS:
    """A static ordinal tree in the DFUDS encoding."""

    def __init__(self, children: Sequence[Sequence[int]], root: int = 0) -> None:
        """Build U by preorder; ``self.order`` is the preorder of the input nodes."""
        u = [1]
        self.order: list[int] = []
        stack = [root]
        while stack:
            v = stack.pop()
            self.order.append(v)
            u.extend([1] * len(children[v]))
            u.append(0)
            stack.extend(reversed(children[v]))
        self.U = u
        self.n = len(self.order)
        self.ones = [0]
        for b in u:
            self.ones.append(self.ones[-1] + b)
        self.zeros = [i for i, b in enumerate(u) if b == 0]

    def text(self) -> str:
        """U as a string of parentheses."""
        return "".join("(" if b else ")" for b in self.U)

    # --- primitives -------------------------------------------------------
    def excess(self, i: int) -> int:
        """Opens minus closes in U[0..i]; excess(-1) = 0."""
        return 2 * self.ones[i + 1] - (i + 1)

    def rank0(self, i: int) -> int:
        """Number of ')' in U[0..i-1]."""
        return i - self.ones[i]

    def select0(self, j: int) -> int:
        """Position of the j-th ')', j >= 1; select0(0) = 0 by convention."""
        return self.zeros[j - 1] if j > 0 else 0

    def fwdsearch(self, i: int, d: int) -> int:
        """Least j > i with excess(j) = excess(i) + d."""
        target = self.excess(i) + d
        j = i + 1
        while self.excess(j) != target:
            j += 1
        return j

    def findclose(self, i: int) -> int:
        """The ')' matching the '(' at i."""
        return self.fwdsearch(i, -1)

    def findopen(self, j: int) -> int:
        """The '(' matching the ')' at j."""
        target = self.excess(j)
        i = j - 1
        while self.excess(i) != target:
            i -= 1
        return i + 1

    # --- operations -------------------------------------------------------
    def root(self) -> int:
        """The root node, at position 1."""
        return 1

    def degree(self, v: int) -> int:
        """Number of children of v."""
        return self.select0(self.rank0(v) + 1) - v  # @line L1

    def child(self, v: int, i: int) -> Optional[int]:
        """The i-th child (1-based) of v, or None."""
        if i < 1 or i > self.degree(v):  # @line L2
            return None
        e = self.select0(self.rank0(v) + 1)  # @line L3
        return self.findclose(e - i) + 1  # @line L4

    def parent(self, v: int) -> Optional[int]:
        """The parent of v, or None for the root."""
        if v == 1:  # @line L5
            return None
        o = self.findopen(v - 1)  # @line L6
        return self.select0(self.rank0(o)) + 1  # @line L7

    def child_rank(self, v: int) -> int:
        """The index (1-based) of v among its siblings; v is not the root."""
        o = self.findopen(v - 1)  # @line L8
        return self.select0(self.rank0(o) + 1) - o  # @line L9

    def subtree_size(self, v: int) -> int:
        """Number of nodes in the subtree of v."""
        end = self.fwdsearch(v - 1, -1)  # @line L10
        return (end - v) // 2 + 1  # @line L11

    def next_sibling(self, v: int) -> Optional[int]:
        """The next sibling of v, or None."""
        if v == 1:
            return None
        p = self.parent(v)
        assert p is not None
        return self.child(p, self.child_rank(v) + 1)

    def is_leaf(self, v: int) -> bool:
        """True if v has no children."""
        return self.U[v] == 0

    def preorder_rank(self, v: int) -> int:
        """Preorder number of v, from 0."""
        return self.rank0(v)

    def node_at(self, k: int) -> int:
        """The node with preorder number k."""
        return 1 if k == 0 else self.select0(k) + 1
