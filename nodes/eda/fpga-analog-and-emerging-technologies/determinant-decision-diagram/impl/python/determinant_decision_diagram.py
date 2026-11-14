# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/determinant-decision-diagram/. The authors are listed in prov/09FYV2.jsonl.

"""A determinant decision diagram (DDD) of a sparse symbolic matrix.

The matrix is a dict {(row, col): symbol} of its nonzero entries, with rows
and columns 0 .. n - 1. The DDD is built by Laplace expansion along the first
row of each minor, with a memo on the minor and a unique table on the vertices.
Node 0 is the 0-terminal and node 1 is the 1-terminal. An inner node is a tuple
(row, col, symbol, sign, hi, lo): hi is the DDD of the minor without this row
and column, lo is the rest of the expansion of the current row.
"""

from fractions import Fraction

ZERO, ONE = 0, 1


class DDD:
    def __init__(self, n: int, entries: dict) -> None:
        self.n = n
        self.entries = {k: v for k, v in entries.items()}
        self.nodes: list = [None, None]  # the two terminals
        self.unique: dict = {}
        self._minor: dict = {}
        self._chain: dict = {}
        self.root = self._build()

    def _mk(self, r: int, c: int, s: int, hi: int, lo: int) -> int:
        key = (r, c, s, hi, lo)
        v = self.unique.get(key)
        if v is None:
            v = len(self.nodes)
            self.nodes.append((r, c, self.entries[(r, c)], s, hi, lo))
            self.unique[key] = v
        return v

    def _build(self) -> int:
        return self._minor_of((1 << self.n) - 1)  # @line L1

    def _minor_of(self, cset: int) -> int:
        """The DDD of the minor with rows n - |C| .. n - 1 and columns C (a bit set)."""
        if cset == 0:  # @line L2
            return ONE
        if cset in self._minor:
            return self._minor[cset]
        r = self.n - bin(cset).count("1")  # @line L3
        cols = [c for c in range(self.n) if cset >> c & 1 and (r, c) in self.entries]  # @line L4
        v = self._chain_of(cset, r, cols, 0)  # @line L5
        self._minor[cset] = v
        return v

    def _chain_of(self, cset: int, r: int, cols: list, k: int) -> int:
        key = (cset, k)
        if key in self._chain:
            return self._chain[key]
        if k == len(cols):  # @line L6
            v = ZERO
        else:
            c = cols[k]  # @line L7
            s = -1 if bin(cset & ((1 << c) - 1)).count("1") % 2 else 1
            hi = self._minor_of(cset & ~(1 << c))  # @line L8
            lo = self._chain_of(cset, r, cols, k + 1)  # @line L9
            if hi == ZERO:  # @line L10: zero suppression
                v = lo
            else:
                v = self._mk(r, c, s, hi, lo)  # @line L11
        self._chain[key] = v
        return v

    def size(self) -> int:
        """The number of inner vertices."""
        return len(self.nodes) - 2

    def count_terms(self) -> int:
        """The number of 1-paths, that is, of nonzero terms of the determinant."""
        paths = [0, 1]
        for v in range(2, len(self.nodes)):
            _, _, _, _, hi, lo = self.nodes[v]
            paths.append(paths[hi] + paths[lo])  # children have smaller ids
        return paths[self.root]

    def evaluate(self, values: dict) -> Fraction:
        """The determinant for numeric values {symbol: number}, in one pass."""
        val = [Fraction(0), Fraction(1)]
        for v in range(2, len(self.nodes)):
            _, _, sym, s, hi, lo = self.nodes[v]
            val.append(s * Fraction(values[sym]) * val[hi] + val[lo])
        return val[self.root]

    def terms(self) -> list:
        """All terms as (sign, tuple of (row, col)) pairs, by a walk of the 1-paths."""
        out = []

        def walk(v: int, s: int, path: list) -> None:
            if v == ONE:
                out.append((s, tuple(path)))
                return
            if v == ZERO:
                return
            r, c, _, sv, hi, lo = self.nodes[v]
            walk(hi, s * sv, path + [(r, c)])
            walk(lo, s, path)

        walk(self.root, 1, [])
        return out
