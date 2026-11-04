# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/louds-tree/. The authors are listed in prov/QA72X1.jsonl.
"""LOUDS tree: an ordinal tree as a level-order unary degree sequence.

Nodes are named by their level-order number k, with the root at k = 0.
The bit string is L = 10 1^d0 0 1^d1 0 ... 1^d(n-1) 0, of 2n + 1 bits.
Rank and select are answered from plain lookup arrays, which keeps the
code short; a real succinct index (see rank-select-dictionary) answers
the same calls in O(1) time with o(n) extra bits.
"""

from __future__ import annotations

from collections import deque
from typing import Optional, Sequence


class _Bits:
    """A static bit string with rank and select by lookup arrays."""

    def __init__(self, bits: Sequence[int]) -> None:
        self.bits = list(bits)
        self.ones_before = [0]
        self.pos1: list[int] = []
        self.pos0: list[int] = []
        for i, b in enumerate(self.bits):
            self.ones_before.append(self.ones_before[-1] + b)
            (self.pos1 if b else self.pos0).append(i)

    def rank1(self, i: int) -> int:
        """Number of 1s in positions 0..i-1."""
        return self.ones_before[i]

    def rank0(self, i: int) -> int:
        """Number of 0s in positions 0..i-1."""
        return i - self.ones_before[i]

    def select1(self, j: int) -> int:
        """Position of the j-th 1, j >= 1."""
        return self.pos1[j - 1]

    def select0(self, j: int) -> int:
        """Position of the j-th 0, j >= 1."""
        return self.pos0[j - 1]


class LoudsTree:
    """A static ordinal tree in the LOUDS encoding."""

    def __init__(self, children: Sequence[Sequence[int]], root: int = 0) -> None:
        """Build from child lists of any node numbering; nodes become level order.

        ``self.order[k]`` is the input node that became level-order node k.
        """
        bits = [1, 0]
        self.order: list[int] = []
        queue = deque([root])
        while queue:
            v = queue.popleft()
            self.order.append(v)
            for c in children[v]:
                bits.append(1)
                queue.append(c)
            bits.append(0)
        self.n = len(self.order)
        self.L = _Bits(bits)

    def bitstring(self) -> str:
        """The LOUDS string as text."""
        return "".join(map(str, self.L.bits))

    def child(self, k: int, i: int) -> Optional[int]:
        """The i-th child (1-based) of node k, or None."""
        s = self.L.select0(k + 1)  # @line L1
        if i < 1 or i > self.degree(k):  # @line L2
            return None
        return self.L.rank1(s) + i - 1  # @line L3

    def degree(self, k: int) -> int:
        """Number of children of node k."""
        return self.L.select0(k + 2) - self.L.select0(k + 1) - 1  # @line L4

    def is_leaf(self, k: int) -> bool:
        """True if node k has no children."""
        return self.L.bits[self.L.select0(k + 1) + 1] == 0

    def parent(self, k: int) -> Optional[int]:
        """The parent of node k, or None for the root."""
        if k == 0:  # @line L5
            return None
        p = self.L.select1(k + 1)  # @line L6
        return self.L.rank0(p) - 1  # @line L7

    def next_sibling(self, k: int) -> Optional[int]:
        """The next sibling of node k, or None."""
        p = self.L.select1(k + 1)  # @line L8
        return k + 1 if self.L.bits[p + 1] == 1 else None  # @line L9

    def prev_sibling(self, k: int) -> Optional[int]:
        """The previous sibling of node k, or None."""
        p = self.L.select1(k + 1)
        return k - 1 if self.L.bits[p - 1] == 1 and k > 0 else None

    def child_rank(self, k: int) -> int:
        """The position (1-based) of node k among its siblings; k >= 1."""
        p = self.L.select1(k + 1)  # @line L10
        return p - self.L.select0(self.L.rank0(p))  # @line L11
