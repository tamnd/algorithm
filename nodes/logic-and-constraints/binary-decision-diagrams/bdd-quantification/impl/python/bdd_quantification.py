# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bdd-quantification/. The authors are listed in prov/8DCSXX.jsonl.

"""Existential and universal quantification on reduced ordered BDDs.

The variables are x_0, ..., x_{n-1}, tested in this order. Node 0 is FALSE,
node 1 is TRUE, and an inner node is the triple (var, lo, hi); a terminal
has var = n. A binary operator is a 4-bit truth table: bit 2a + b holds
op(a, b). MK keeps the store reduced through a unique table.
"""

FALSE, TRUE = 0, 1
AND, OR, XOR = 0b1000, 0b1110, 0b0110


class BDD:
    def __init__(self, n: int) -> None:
        self.n = n
        self.nodes: list[tuple[int, int, int]] = [(n, 0, 0), (n, 1, 1)]
        self.unique: dict[tuple[int, int, int], int] = {}
        self.cache: dict[tuple, int] = {}

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

    def apply(self, op: int, u: int, v: int) -> int:
        if u <= TRUE and v <= TRUE:
            return (op >> (2 * u + v)) & 1
        key = ("apply", op, u, v)
        r = self.cache.get(key)
        if r is None:
            i = min(self.var(u), self.var(v))
            u0, u1 = self._cof(u, i)
            v0, v1 = self._cof(v, i)
            r = self.mk(i, self.apply(op, u0, v0), self.apply(op, u1, v1))
            self.cache[key] = r
        return r

    def neg(self, u: int) -> int:
        return self.apply(XOR, u, TRUE)

    # ---------------------------------------------------------- quantification

    def quantify(self, op: int, f: int, xs: frozenset[int]) -> int:
        """(exists X) f for op = OR, and (forall X) f for op = AND."""
        if f <= TRUE:  # @line L1
            return f
        if self.var(f) > max(xs, default=-1):  # @line L2
            return f
        key = ("quant", op, f, xs)
        r = self.cache.get(key)  # @line L3
        if r is not None:
            return r
        i, lo, hi = self.nodes[f]  # @line L4
        l = self.quantify(op, lo, xs)  # @line L5
        h = self.quantify(op, hi, xs)  # @line L6
        if i in xs:
            r = self.apply(op, l, h)  # @line L7
        else:
            r = self.mk(i, l, h)  # @line L8
        self.cache[key] = r  # @line L9
        return r  # @line L10

    def exists(self, f: int, xs: set[int]) -> int:
        return self.quantify(OR, f, frozenset(xs))

    def forall(self, f: int, xs: set[int]) -> int:
        return self.quantify(AND, f, frozenset(xs))

    def and_exists(self, f: int, g: int, xs: frozenset[int]) -> int:
        """The relational product (exists X)(f AND g), without building f AND g."""
        if f == FALSE or g == FALSE:
            return FALSE
        if f == TRUE and g == TRUE:
            return TRUE
        if f == TRUE or f == g:
            return self.quantify(OR, g, xs)
        if g == TRUE:
            return self.quantify(OR, f, xs)
        key = ("relprod", f, g, xs)
        r = self.cache.get(key)
        if r is not None:
            return r
        i = min(self.var(f), self.var(g))
        f0, f1 = self._cof(f, i)
        g0, g1 = self._cof(g, i)
        l = self.and_exists(f0, g0, xs)
        if i in xs:
            r = TRUE if l == TRUE else self.apply(OR, l, self.and_exists(f1, g1, xs))
        else:
            r = self.mk(i, l, self.and_exists(f1, g1, xs))
        self.cache[key] = r
        return r

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
