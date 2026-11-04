# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/balanced-parentheses-representation/. The authors are listed in prov/8WYTP6.jsonl.
"""Balanced parentheses (BP) representation of an ordinal tree.

A node is named by the position of its opening parenthesis in P.
The primitives findclose, enclose and rmq are written as plain scans
over the excess, so each takes time linear in the distance; the range
min-max tree answers the same calls in O(log n), or O(1) with the
Navarro-Sadakane structure. Excess comes from a prefix-count array.
"""

from __future__ import annotations

from typing import Optional, Sequence


class BPTree:
    """A static ordinal tree stored as a balanced parenthesis sequence."""

    def __init__(self, children: Sequence[Sequence[int]], root: int = 0) -> None:
        """Build P by a depth-first traversal; ``self.order`` is the preorder."""
        p: list[int] = []
        self.order: list[int] = []
        stack: list[tuple[int, int]] = [(root, 0)]
        p.append(1)
        self.order.append(root)
        while stack:
            v, i = stack.pop()
            if i < len(children[v]):
                stack.append((v, i + 1))
                c = children[v][i]
                p.append(1)
                self.order.append(c)
                stack.append((c, 0))
            else:
                p.append(0)
        self.P = p
        self.n = len(self.order)
        self.ones = [0]
        for b in p:
            self.ones.append(self.ones[-1] + b)

    def text(self) -> str:
        """P as a string of parentheses."""
        return "".join("(" if b else ")" for b in self.P)

    def excess(self, i: int) -> int:
        """E(i): opens minus closes in P[0..i]; E(-1) = 0."""
        return 2 * self.ones[i + 1] - (i + 1)

    def findclose(self, i: int) -> int:
        """Position of the ')' matching the '(' at i."""
        target = self.excess(i) - 1
        j = i + 1
        while self.excess(j) != target:
            j += 1
        return j

    def enclose(self, i: int) -> Optional[int]:
        """Opening position of the tightest pair strictly containing i."""
        target = self.excess(i) - 2
        j = i - 1
        while j >= 0 and self.excess(j) != target:
            j -= 1
        return j + 1 if target >= 0 else None

    def rmq(self, i: int, j: int) -> int:
        """Leftmost position of the minimum excess in P[i..j]."""
        best = i
        for k in range(i + 1, j + 1):
            if self.excess(k) < self.excess(best):
                best = k
        return best

    def first_child(self, v: int) -> Optional[int]:
        """The first child of node v, or None for a leaf."""
        if self.P[v + 1] == 1:  # @line L1
            return v + 1  # @line L2
        return None

    def next_sibling(self, v: int) -> Optional[int]:
        """The next sibling of node v, or None."""
        j = self.findclose(v)  # @line L3
        if j + 1 < len(self.P) and self.P[j + 1] == 1:  # @line L4
            return j + 1  # @line L5
        return None

    def parent(self, v: int) -> Optional[int]:
        """The parent of node v, or None for the root."""
        if self.excess(v) == 1:  # @line L6
            return None
        return self.enclose(v)  # @line L7

    def subtree_size(self, v: int) -> int:
        """Number of nodes in the subtree of v, v included."""
        return (self.findclose(v) - v + 1) // 2  # @line L8

    def depth(self, v: int) -> int:
        """Depth of v, with the root at depth 0."""
        return self.excess(v) - 1  # @line L9

    def is_ancestor(self, u: int, v: int) -> bool:
        """True if u is an ancestor of v or u = v."""
        return u <= v <= self.findclose(u)  # @line L10

    def lca(self, u: int, v: int) -> int:
        """Lowest common ancestor of nodes u and v."""
        if u > v:  # @line L11
            u, v = v, u
        if self.is_ancestor(u, v):  # @line L12
            return u
        m = self.rmq(u, v)  # @line L13
        p = self.enclose(m + 1)  # @line L14
        assert p is not None
        return p

    def preorder_rank(self, v: int) -> int:
        """Preorder number of node v, from 0."""
        return self.ones[v]

    def degree(self, v: int) -> int:
        """Number of children, by walking the siblings (O(degree) calls)."""
        d, c = 0, self.first_child(v)
        while c is not None:
            d += 1
            c = self.next_sibling(c)
        return d
