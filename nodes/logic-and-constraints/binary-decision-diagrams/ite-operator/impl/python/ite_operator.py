# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ite-operator/. The authors are listed in prov/X6QCE3.jsonl.

"""The ITE operator on reduced ordered BDDs.

ite(f, g, h) is the function (f AND g) OR (NOT f AND h). The variables are
x_0, ..., x_{n-1}, tested in this order. Node 0 is FALSE, node 1 is TRUE, and
an inner node is the triple (var, lo, hi); a terminal has var = n. MK keeps
the store reduced through a unique table, and the computed table caches ITE.
"""

FALSE, TRUE = 0, 1


class BDD:
    def __init__(self, n: int, normalize: bool = True) -> None:
        self.n = n
        self.normalize = normalize
        self.nodes: list[tuple[int, int, int]] = [(n, 0, 0), (n, 1, 1)]
        self.unique: dict[tuple[int, int, int], int] = {}
        self.cache: dict[tuple[int, int, int], int] = {}
        self.calls = 0  # ITE calls that pass the terminal cases

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

    def _cof(self, u: int, i: int) -> tuple[int, int]:
        v, lo, hi = self.nodes[u]
        return (lo, hi) if v == i else (u, u)

    def ite(self, f: int, g: int, h: int) -> int:
        if f == TRUE:  # @line L1
            return g
        if f == FALSE:  # @line L2
            return h
        if g == h:  # @line L3
            return g
        if g == TRUE and h == FALSE:  # @line L4
            return f
        if self.normalize:
            if g == f:  # @line L5
                g = TRUE
            if h == f:
                h = FALSE
            if h == FALSE and g > TRUE and g < f:  # @line L6
                f, g = g, f  # f AND g = g AND f
            if g == TRUE and h > TRUE and h < f:  # @line L7
                f, h = h, f  # f OR h = h OR f
            if g == h or (g == TRUE and h == FALSE):
                return self.ite(f, g, h)
        key = (f, g, h)
        r = self.cache.get(key)  # @line L8
        if r is not None:
            return r
        self.calls += 1
        i = min(self.var(f), self.var(g), self.var(h))  # @line L9
        f0, f1 = self._cof(f, i)
        g0, g1 = self._cof(g, i)
        h0, h1 = self._cof(h, i)
        t = self.ite(f1, g1, h1)  # @line L10
        e = self.ite(f0, g0, h0)  # @line L11
        r = self.mk(i, e, t)  # @line L12
        self.cache[key] = r  # @line L13
        return r  # @line L14

    # ------------------------------------------------- operators through ITE

    def neg(self, f: int) -> int:
        return self.ite(f, FALSE, TRUE)

    def binop(self, op: int, f: int, g: int) -> int:
        """The operator with 4-bit table op (bit 2a + b is op(a, b)), as one ITE."""
        lo = op & 3  # the function of g when f = 0: bit b of lo is op(0, b)
        hi = (op >> 2) & 3  # the function of g when f = 1
        return self.ite(f, self._unary(hi, g), self._unary(lo, g))

    def _unary(self, t: int, g: int) -> int:
        """The function b -> bit b of t applied to g: 0, g, NOT g or 1."""
        return [FALSE, self.neg(g), g, TRUE][t]

    # ----------------------------------------------------------------- tools

    def ithvar(self, i: int) -> int:
        return self.mk(i, FALSE, TRUE)

    def build(self, table: list[int]) -> int:
        c = [TRUE if t else FALSE for t in table]
        for i in range(self.n - 1, -1, -1):
            for p in range(1 << i):
                c[p] = self.mk(i, c[p], c[p + (1 << i)])
        return c[0]

    def evaluate(self, u: int, x: list[int]) -> int:
        while u > TRUE:
            v, lo, hi = self.nodes[u]
            u = hi if x[v] else lo
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
