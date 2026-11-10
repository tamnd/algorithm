# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/q-digest/. The authors are listed in prov/A0RJGY.jsonl.
"""The q-digest of Shrivastava, Buragohain, Agrawal and Suri, for integers in [0, 2^L).

A node is a dyadic interval (j, i) = [i 2^j, (i + 1) 2^j - 1] with a count.
Property 1: a node above the leaves has count at most floor(n / k).
Property 2 (after a compress): for each node v other than the root,
count(v) + count(sibling) + count(parent) > floor(n / k).
"""

from __future__ import annotations

Node = tuple[int, int]  # (level, index)


class QDigest:
    """A deterministic, mergeable quantile summary over an integer universe."""

    def __init__(self, levels: int, k: int) -> None:
        if levels < 0 or k < 1:
            raise ValueError("need levels >= 0 and k >= 1")
        self.levels = levels
        self.k = k
        self.n = 0
        self.count: dict[Node, int] = {}

    def __len__(self) -> int:
        return len(self.count)

    def insert(self, x: int, auto_compress: bool = True) -> None:
        """Add one copy of x, for 0 <= x < 2^levels."""
        if not 0 <= x < (1 << self.levels):
            raise ValueError("item out of the universe")
        self.n += 1  # @line L1
        leaf = (0, x)
        self.count[leaf] = self.count.get(leaf, 0) + 1
        if auto_compress and len(self.count) > 4 * self.k:  # @line L2
            self.compress()

    def compress(self) -> None:
        """Merge small families bottom up until Property 2 holds everywhere."""
        cap = self.n // self.k
        merged = True
        while merged:  # @line L3
            merged = False
            for j in range(self.levels):  # @line L4
                nodes = sorted(i for (lv, i) in self.count if lv == j)
                for i in nodes:
                    v = (j, i)
                    if v not in self.count:
                        continue  # removed as the sibling of an earlier node
                    sib = (j, i ^ 1)
                    par = (j + 1, i >> 1)
                    total = self.count[v] + self.count.get(sib, 0) + self.count.get(par, 0)
                    if total <= cap:  # @line L5
                        self.count[par] = total  # @line L6
                        del self.count[v]
                        self.count.pop(sib, None)
                        merged = True
        # @line L7

    def merge(self, other: "QDigest") -> None:
        """Add the counts of another q-digest with the same levels and k."""
        if (other.levels, other.k) != (self.levels, self.k):
            raise ValueError("parameters differ")
        for v, c in other.count.items():  # @line L10
            self.count[v] = self.count.get(v, 0) + c
        self.n += other.n
        self.compress()  # @line L11

    def rank(self, x: int) -> int:
        """Lower estimate of the number of items <= x, within L floor(n/k)."""
        return sum(c for (j, i), c in self.count.items() if ((i + 1) << j) - 1 <= x)

    def query(self, r: int) -> int:
        """Return x with R(x - 1) < r + L floor(n/k) and R(x) >= r."""
        if not 1 <= r <= self.n:
            raise ValueError("rank out of range")
        order = sorted(self.count.items(), key=lambda p: (((p[0][1] + 1) << p[0][0]) - 1, p[0][0]))  # @line L8
        s = 0
        for (j, i), c in order:  # @line L9
            s += c
            if s >= r:
                return ((i + 1) << j) - 1
        raise AssertionError("counts do not add up to n")

    def check_invariant(self, compressed: bool = False) -> None:
        """Check Property 1 always, and Property 2 and the size bound after a compress."""
        assert sum(self.count.values()) == self.n
        cap = self.n // self.k
        for (j, i), c in self.count.items():
            assert c >= 1
            assert 0 <= i < (1 << (self.levels - j))
            if j > 0:
                assert c <= cap
        if compressed:
            for (j, i), c in self.count.items():
                if j < self.levels:
                    fam = c + self.count.get((j, i ^ 1), 0) + self.count.get((j + 1, i >> 1), 0)
                    assert fam > cap
            assert len(self.count) <= 4 * self.k
