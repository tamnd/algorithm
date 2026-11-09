# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bdd-satisfy-count/. The authors are listed in prov/SH4TH9.jsonl.

"""Counting the satisfying assignments of a reduced ordered BDD.

The variables are x_0, ..., x_{n-1}, tested in this order. Node 0 is FALSE,
node 1 is TRUE, and an inner node is the triple (var, lo, hi); a terminal
has var = n. MK keeps the store reduced through a unique table.
"""

FALSE, TRUE = 0, 1
AND, OR, XOR = 0b1000, 0b1110, 0b0110


class BDD:
    def __init__(self, n: int) -> None:
        self.n = n
        self.nodes: list[tuple[int, int, int]] = [(n, 0, 0), (n, 1, 1)]
        self.unique: dict[tuple[int, int, int], int] = {}
        self.cache: dict[tuple[int, int, int], int] = {}

    def var(self, u: int) -> int:
        return self.nodes[u][0]

    def mk(self, i: int, lo: int, hi: int) -> int:
        if lo == hi:
            return lo
        key = (i, lo, hi)
        u = self.unique.get(key)
        if u is None:
            u = len(self.nodes)
            self.nodes.append(key)
            self.unique[key] = u
        return u

    def ithvar(self, i: int) -> int:
        return self.mk(i, FALSE, TRUE)

    def apply(self, op: int, u: int, v: int) -> int:
        if u <= TRUE and v <= TRUE:
            return (op >> (2 * u + v)) & 1
        key = (op, u, v)
        r = self.cache.get(key)
        if r is None:
            i = min(self.var(u), self.var(v))
            u0, u1 = (self.nodes[u][1:] if self.var(u) == i else (u, u))
            v0, v1 = (self.nodes[v][1:] if self.var(v) == i else (v, v))
            r = self.mk(i, self.apply(op, u0, v0), self.apply(op, u1, v1))
            self.cache[key] = r
        return r

    # ---------------------------------------------------------------- counting

    def satcount(self, f: int) -> int:
        """The number of x in {0,1}^n with f(x) = 1, in time O(size of f)."""
        memo: dict[int, int] = {}

        def count(u: int) -> int:
            # The number of models of f_u over x_var(u), ..., x_{n-1}.
            if u == FALSE:  # @line L2
                return 0
            if u == TRUE:  # @line L3
                return 1
            r = memo.get(u)  # @line L4
            if r is None:
                i, lo, hi = self.nodes[u]  # @line L5
                r = (count(lo) << (self.var(lo) - i - 1)) + (count(hi) << (self.var(hi) - i - 1))  # @line L6
                memo[u] = r  # @line L7
            return r

        return count(f) << self.var(f)  # @line L1

    def satcount_bottom_up(self, f: int) -> int:
        """The same count, in one pass over the nodes in increasing id order.

        Children are made before parents, so a child has a smaller id.
        """
        c = [0] * len(self.nodes)
        c[TRUE] = 1
        for u in range(2, f + 1):
            i, lo, hi = self.nodes[u]
            c[u] = (c[lo] << (self.var(lo) - i - 1)) + (c[hi] << (self.var(hi) - i - 1))
        return c[f] << self.var(f)

    def probability(self, f: int, p: list[float]) -> float:
        """The probability that f = 1 when each x_i is 1 with probability p[i]."""
        memo: dict[int, float] = {FALSE: 0.0, TRUE: 1.0}

        def go(u: int) -> float:
            r = memo.get(u)
            if r is None:
                i, lo, hi = self.nodes[u]
                r = (1 - p[i]) * go(lo) + p[i] * go(hi)
                memo[u] = r
            return r

        return go(f)

    # ----------------------------------------------------------------- tools

    def build(self, table: list[int]) -> int:
        c = [TRUE if t else FALSE for t in table]
        for i in range(self.n - 1, -1, -1):
            for p in range(1 << i):
                c[p] = self.mk(i, c[p], c[p + (1 << i)])
        return c[0]

    def size(self, u: int) -> int:
        seen = {u}
        stack = [u]
        while stack:
            w = stack.pop()
            if w > TRUE:
                for c in self.nodes[w][1:]:
                    if c not in seen:
                        seen.add(c)
                        stack.append(c)
        return len(seen)
