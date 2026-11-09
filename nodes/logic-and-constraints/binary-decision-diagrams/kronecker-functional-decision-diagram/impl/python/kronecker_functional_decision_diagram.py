# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kronecker-functional-decision-diagram/. The authors are listed in prov/EDCXTM.jsonl.

"""Ordered Kronecker functional decision diagrams (OKFDDs).

Each variable x_v has a decomposition type dtl[v], one of "S", "pD", "nD".
With f_0 and f_1 the cofactors of f by x_v and f_2 = f_0 XOR f_1:
  S  (Shannon):          f = (not x) f_0 XOR x f_1,   node (v, f_0, f_1)
  pD (positive Davio):   f = f_0 XOR x f_2,           node (v, f_0, f_2)
  nD (negative Davio):   f = f_1 XOR (not x) f_2,     node (v, f_1, f_2)
Node 0 is the constant 0 and node 1 is the constant 1. The order is
x_0 < ... < x_{n-1} (x_{i+1} of the page is x_i here).

Reduction rules: an S node with lo == hi is removed (it becomes lo); a Davio
node with hi == 0 is removed (it becomes lo); equal nodes are shared. With a
fixed order and a fixed decomposition type list (DTL), these make the OKFDD
of f unique. xor makes O(|f| |g|) calls of mk; evaluate takes O(|f|).
"""

ZERO, ONE = 0, 1


class KFDD:
    def __init__(self, dtl: list[str]) -> None:
        assert all(t in ("S", "pD", "nD") for t in dtl)
        self.dtl = list(dtl)
        self.n = len(dtl)
        self.nodes: list[tuple[int, int, int]] = [(self.n, 0, 0), (self.n, 1, 1)]
        self.unique: dict[tuple[int, int, int], int] = {}
        self.memo: dict[tuple[int, int], int] = {}

    def mk(self, v: int, lo: int, hi: int) -> int:
        if self.dtl[v] == "S" and lo == hi:  # @line L1
            return lo
        if self.dtl[v] != "S" and hi == ZERO:  # @line L2
            return lo
        key = (v, lo, hi)
        u = self.unique.get(key)  # @line L3
        if u is None:
            u = len(self.nodes)
            self.nodes.append(key)
            self.unique[key] = u
        return u  # @line L4

    def var(self, u: int) -> int:
        return self.nodes[u][0]

    def from_table(self, table: list[int]) -> int:
        """table[a] is f(x) with x_i = bit i of a."""
        assert len(table) == 1 << self.n
        t = list(table)
        for v in range(self.n):  # write each coordinate in the basis of its type
            bit = 1 << v
            for a in range(1 << self.n):
                if a & bit == 0:
                    f0, f1 = t[a], t[a | bit]
                    if self.dtl[v] == "pD":  # @line L5
                        t[a], t[a | bit] = f0, f0 ^ f1
                    elif self.dtl[v] == "nD":
                        t[a], t[a | bit] = f1, f0 ^ f1
        layer = [ONE if b else ZERO for b in t]
        for v in range(self.n - 1, -1, -1):  # @line L6
            half = 1 << v
            layer = [self.mk(v, layer[a], layer[a + half]) for a in range(half)]  # @line L7
        return layer[0]

    def evaluate(self, u: int, a: int) -> int:
        """f(x) for x_i = bit i of a."""
        val: dict[int, int] = {ZERO: 0, ONE: 1}
        for w in sorted(self.reach(u)):  # children have smaller ids
            if w <= ONE:
                continue
            v, lo, hi = self.nodes[w]
            x = a >> v & 1
            if self.dtl[v] == "S":  # @line L8
                val[w] = val[hi] if x else val[lo]
            elif self.dtl[v] == "pD":
                val[w] = val[lo] ^ (x & val[hi])
            else:
                val[w] = val[lo] ^ ((1 - x) & val[hi])
        return val[u]

    def parts(self, u: int, v: int) -> tuple[int, int]:
        """(lo, hi) of u for a node of x_v, where v is at or above the top of u."""
        w, lo, hi = self.nodes[u]
        if w == v:
            return lo, hi
        return (u, u) if self.dtl[v] == "S" else (u, ZERO)

    def xor(self, f: int, g: int) -> int:
        """All three decompositions are linear over GF(2), so XOR goes child by child."""
        if f <= ONE and g <= ONE:
            return f ^ g
        if f == ZERO:
            return g
        if g == ZERO:
            return f
        if f == g:
            return ZERO
        key = (min(f, g), max(f, g))
        r = self.memo.get(key)
        if r is None:
            v = min(self.var(f), self.var(g))
            f0, f1 = self.parts(f, v)
            g0, g1 = self.parts(g, v)
            r = self.mk(v, self.xor(f0, g0), self.xor(f1, g1))
            self.memo[key] = r
        return r

    def reach(self, u: int) -> set[int]:
        seen = {u}
        stack = [u]
        while stack:
            w = stack.pop()
            if w > ONE:
                for c in self.nodes[w][1:]:
                    if c not in seen:
                        seen.add(c)
                        stack.append(c)
        return seen

    def size(self, u: int) -> int:
        return len(self.reach(u))

    def check_invariant(self) -> None:
        for u in range(2, len(self.nodes)):
            v, lo, hi = self.nodes[u]
            assert self.unique[(v, lo, hi)] == u
            assert self.var(lo) > v and self.var(hi) > v
            assert (lo != hi) if self.dtl[v] == "S" else (hi != ZERO)
