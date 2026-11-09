# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bdd-compose/. The authors are listed in prov/SRJKH7.jsonl.

"""Functional composition f[x_i := g] on reduced ordered BDDs.

The variables are x_0, ..., x_{n-1}, tested in this order. Node 0 is FALSE,
node 1 is TRUE, and an inner node is the triple (var, lo, hi); a terminal
has var = n. MK keeps the store reduced through a unique table.
"""

FALSE, TRUE = 0, 1


class BDD:
    def __init__(self, n: int) -> None:
        self.n = n
        self.nodes: list[tuple[int, int, int]] = [(n, 0, 0), (n, 1, 1)]
        self.unique: dict[tuple[int, int, int], int] = {}
        self.cache: dict[tuple[int, int, int], int] = {}
        self.ite_misses = 0

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

    def _cof(self, u: int, i: int) -> tuple[int, int]:
        w, lo, hi = self.nodes[u]
        return (lo, hi) if w == i else (u, u)

    def ite(self, f: int, g: int, h: int) -> int:
        if f == TRUE:
            return g
        if f == FALSE:
            return h
        if g == h:
            return g
        if g == TRUE and h == FALSE:
            return f
        key = (f, g, h)
        r = self.cache.get(key)
        if r is None:
            self.ite_misses += 1
            i = min(self.var(f), self.var(g), self.var(h))
            f0, f1 = self._cof(f, i)
            g0, g1 = self._cof(g, i)
            h0, h1 = self._cof(h, i)
            r = self.mk(i, self.ite(f0, g0, h0), self.ite(f1, g1, h1))
            self.cache[key] = r
        return r

    def restrict(self, f: int, i: int, b: int) -> int:
        """f with x_i set to b, in time linear in the size of f."""
        memo: dict[int, int] = {}

        def go(u: int) -> int:
            v, lo, hi = self.nodes[u]
            if v > i:  # @line L4
                return u
            r = memo.get(u)  # @line L5
            if r is None:
                if v == i:
                    r = hi if b else lo  # @line L6
                else:
                    r = self.mk(v, go(lo), go(hi))  # @line L7
                memo[u] = r  # @line L8
            return r

        return go(f)

    def compose(self, f: int, i: int, g: int) -> int:
        """The function f with g put in place of x_i."""
        f0 = self.restrict(f, i, 0)  # @line L1
        f1 = self.restrict(f, i, 1)  # @line L2
        return self.ite(g, f1, f0)  # @line L3

    # ----------------------------------------------------------------- tools

    def build(self, table: list[int]) -> int:
        c = [TRUE if t else FALSE for t in table]
        for i in range(self.n - 1, -1, -1):
            for p in range(1 << i):
                c[p] = self.mk(i, c[p], c[p + (1 << i)])
        return c[0]

    def evaluate(self, u: int, x: list[int]) -> int:
        while u > TRUE:
            w, lo, hi = self.nodes[u]
            u = hi if x[w] else lo
        return u

    def truth_table(self, u: int) -> list[int]:
        return [self.evaluate(u, [(a >> j) & 1 for j in range(self.n)]) for a in range(1 << self.n)]

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
