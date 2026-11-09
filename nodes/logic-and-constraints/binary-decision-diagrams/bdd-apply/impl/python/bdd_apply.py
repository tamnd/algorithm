# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bdd-apply/. The authors are listed in prov/5A7H4K.jsonl.

"""Bryant's APPLY on reduced ordered BDDs.

The variables are x_0, ..., x_{n-1}, tested in this order. Node 0 is FALSE,
node 1 is TRUE, and an inner node is the triple (var, lo, hi); a terminal
has var = n. A binary operator is a 4-bit truth table: bit 2a + b holds
op(a, b). MK keeps the store reduced through a unique table.
"""

FALSE, TRUE = 0, 1
AND, OR, XOR, NAND, NOR, XNOR = 0b1000, 0b1110, 0b0110, 0b0111, 0b0001, 0b1001
IMPLIES = 0b1011  # a -> b is 0 only for a = 1, b = 0 (bit 2)


class BDD:
    def __init__(self, n: int, use_cache: bool = True, use_short: bool = True) -> None:
        self.n = n
        self.use_cache = use_cache
        self.use_short = use_short  # stop early on a controlling value
        self.nodes: list[tuple[int, int, int]] = [(n, 0, 0), (n, 1, 1)]
        self.unique: dict[tuple[int, int, int], int] = {}
        self.cache: dict[tuple[int, int, int], int] = {}
        self.calls = 0  # all calls of apply
        self.misses = 0  # calls that reach the recursive case

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

    def _short(self, op: int, u: int, v: int) -> int | None:
        """A result without recursion when one argument is a terminal and decides it."""
        if u <= TRUE:
            row = (op >> (2 * u)) & 3  # b -> op(u, b)
            if row in (0, 3):
                return row >> 1  # a constant: a controlling value
            if row == 2:
                return v  # op(u, b) = b
        if v <= TRUE:
            col = ((op >> v) & 1) | (((op >> (2 + v)) & 1) << 1)  # a -> op(a, v)
            if col in (0, 3):
                return col >> 1
            if col == 2:
                return u
        return None

    def apply(self, op: int, u: int, v: int) -> int:
        self.calls += 1
        if u <= TRUE and v <= TRUE:  # @line L1
            return (op >> (2 * u + v)) & 1
        r = self._short(op, u, v) if self.use_short else None  # @line L2
        if r is not None:
            return r
        key = (op, u, v)
        if self.use_cache:
            r = self.cache.get(key)  # @line L3
            if r is not None:
                return r
        self.misses += 1
        i = min(self.var(u), self.var(v))  # @line L4
        u0, u1 = self._cof(u, i)  # @line L5
        v0, v1 = self._cof(v, i)  # @line L6
        r = self.mk(i, self.apply(op, u0, v0), self.apply(op, u1, v1))  # @line L7
        if self.use_cache:
            self.cache[key] = r  # @line L8
        return r  # @line L9

    def _cof(self, u: int, i: int) -> tuple[int, int]:
        w, lo, hi = self.nodes[u]
        return (lo, hi) if w == i else (u, u)

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
