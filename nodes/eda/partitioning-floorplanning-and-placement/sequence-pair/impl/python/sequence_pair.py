# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sequence-pair/. The authors are listed in prov/9NWMQZ.jsonl.

"""The sequence pair of Murata, Fujiyoshi, Nakatake and Kajitani (1995).

A sequence pair is two orders (plus, minus) of the same blocks. The convention
of this module, for two blocks a and b:

- a before b in both orders: a is to the left of b;
- b before a in plus and a before b in minus: a is below b.

The packing puts each block as far to the left and as low as these relations
allow. pack() computes it in O(n log n) time with a Fenwick tree of prefix
maxima, which is the weighted longest common subsequence method of Tang, Tian
and Wong; pack_by_graphs() computes it in O(n^2) time with the horizontal and
vertical constraint graphs.
"""

from typing import Hashable

Block = Hashable


class _PrefixMax:
    """Fenwick tree over positions 1..n that keeps the maximum of a prefix."""

    def __init__(self, n: int) -> None:
        self.t = [0] * (n + 1)

    def update(self, i: int, v: int) -> None:
        while i < len(self.t):
            if self.t[i] < v:
                self.t[i] = v
            i += i & -i

    def query(self, i: int) -> int:
        """Return the maximum over positions 1..i (0 if i = 0)."""
        r = 0
        while i > 0:
            if self.t[i] > r:
                r = self.t[i]
            i -= i & -i
        return r


class SequencePair:
    """A pair of orders of the same blocks."""

    def __init__(self, plus: list[Block], minus: list[Block]) -> None:
        """Store the two orders. Raise ValueError if they are not orders of the same blocks."""
        if len(plus) != len(minus) or set(plus) != set(minus) or len(set(plus)) != len(plus):
            raise ValueError("the two sequences must be orders of the same blocks")
        self.plus = list(plus)
        self.minus = list(minus)
        self._index()

    def _index(self) -> None:
        self.pos_plus = {b: i for i, b in enumerate(self.plus)}
        self.pos_minus = {b: i for i, b in enumerate(self.minus)}

    def check_invariant(self) -> None:
        """Raise AssertionError if the orders or the position maps are broken."""
        assert set(self.plus) == set(self.minus) and len(set(self.plus)) == len(self.plus)
        assert all(self.plus[i] == b for b, i in self.pos_plus.items())
        assert all(self.minus[i] == b for b, i in self.pos_minus.items())

    def relation(self, a: Block, b: Block) -> str:
        """Return "left", "right", "below" or "above": where a is with respect to b. O(1)."""
        p = self.pos_plus[a] < self.pos_plus[b]
        m = self.pos_minus[a] < self.pos_minus[b]
        if p and m:
            return "left"
        if not p and not m:
            return "right"
        return "below" if m else "above"

    def pack(
        self, w: dict[Block, int], h: dict[Block, int]
    ) -> tuple[int, int, dict[Block, int], dict[Block, int]]:
        """Return (W, H, x, y), the lower-left packing of the sequence pair. O(n log n)."""
        n = len(self.plus)
        x: dict[Block, int] = {}
        y: dict[Block, int] = {}
        fx = _PrefixMax(n)  # @line L1
        for b in self.plus:  # @line L2
            p = self.pos_minus[b] + 1
            x[b] = fx.query(p - 1)  # @line L3
            fx.update(p, x[b] + w[b])  # @line L4
        fy = _PrefixMax(n)  # @line L5
        for b in reversed(self.plus):  # @line L6
            p = self.pos_minus[b] + 1
            y[b] = fy.query(p - 1)  # @line L7
            fy.update(p, y[b] + h[b])  # @line L8
        width = fx.query(n)  # @line L9
        height = fy.query(n)
        return width, height, x, y

    def pack_by_graphs(
        self, w: dict[Block, int], h: dict[Block, int]
    ) -> tuple[int, int, dict[Block, int], dict[Block, int]]:
        """The same packing by longest paths in the two constraint graphs. O(n^2)."""
        x = {b: 0 for b in self.plus}  # @line L10
        y = {b: 0 for b in self.plus}
        for b in self.plus:  # plus is a topological order of the horizontal graph  # @line L11
            for a in self.plus[: self.pos_plus[b]]:
                if self.pos_minus[a] < self.pos_minus[b]:  # edge a -> b: a left of b
                    x[b] = max(x[b], x[a] + w[a])  # @line L12
        for b in self.minus:  # minus is a topological order of the vertical graph  # @line L13
            for a in self.minus[: self.pos_minus[b]]:
                if self.pos_plus[a] > self.pos_plus[b]:  # edge a -> b: a below b
                    y[b] = max(y[b], y[a] + h[a])  # @line L14
        width = max((x[b] + w[b] for b in self.plus), default=0)  # @line L15
        height = max((y[b] + h[b] for b in self.plus), default=0)
        return width, height, x, y

    def swap_in_plus(self, a: Block, b: Block) -> None:
        """Swap blocks a and b in the plus order only. O(1)."""
        i, j = self.pos_plus[a], self.pos_plus[b]  # @line L16
        self.plus[i], self.plus[j] = b, a
        self.pos_plus[a], self.pos_plus[b] = j, i

    def swap_in_both(self, a: Block, b: Block) -> None:
        """Swap blocks a and b in both orders. O(1)."""
        self.swap_in_plus(a, b)  # @line L17
        i, j = self.pos_minus[a], self.pos_minus[b]
        self.minus[i], self.minus[j] = b, a
        self.pos_minus[a], self.pos_minus[b] = j, i
