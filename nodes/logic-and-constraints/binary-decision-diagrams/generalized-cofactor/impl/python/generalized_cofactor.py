# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-cofactor/. The authors are listed in prov/PVN188.jsonl.

"""The generalized cofactors constrain and restrict of Coudert and Madre.

The diagrams are reduced ordered BDDs with the order x_0 < x_1 < ... < x_{n-1}
(x_0 on top; x_{i+1} of the page is x_i here). Node 0 is FALSE, node 1 is TRUE,
and an inner node u is nodes[u] = (var, lo, hi). The variable of a sink is n.

constrain(f, c) and restrict(f, c) need c != FALSE. Both return a function g
with g(x) = f(x) for each x with c(x) = 1. Each call is memoized, so the cost
is O(|f| |c|) calls of mk, plus the OR of restrict in the case where c tests
a variable above the top of f. The recursion depth is at most n + 1.
"""

FALSE, TRUE = 0, 1


class BDD:
    def __init__(self, n: int) -> None:
        self.n = n
        self.nodes: list[tuple[int, int, int]] = [(n, 0, 0), (n, 1, 1)]
        self.unique: dict[tuple[int, int, int], int] = {}
        self.ite_memo: dict[tuple[int, int, int], int] = {}
        self.con_memo: dict[tuple[int, int], int] = {}
        self.res_memo: dict[tuple[int, int], int] = {}

    def var(self, u: int) -> int:
        return self.nodes[u][0]

    def mk(self, v: int, lo: int, hi: int) -> int:
        if lo == hi:
            return lo
        key = (v, lo, hi)
        u = self.unique.get(key)
        if u is None:
            u = len(self.nodes)
            self.nodes.append(key)
            self.unique[key] = u
        return u

    def cof(self, u: int, v: int) -> tuple[int, int]:
        """The two cofactors of u by variable v, where v is at or above the top of u."""
        w, lo, hi = self.nodes[u]
        return (lo, hi) if w == v else (u, u)

    def from_table(self, table: list[int]) -> int:
        """The node of the function with this truth table (bit i of the index is x_i)."""
        assert len(table) == 1 << self.n
        layer = [TRUE if b else FALSE for b in table]
        for v in range(self.n - 1, -1, -1):
            bit = 1 << v
            # entry a is valid when bits v..n-1 of a are zero; the others are FALSE
            layer = [self.mk(v, layer[a], layer[a | bit]) if a & bit == 0 else FALSE for a in range(len(layer))]
        return layer[0]

    def evaluate(self, u: int, a: int) -> int:
        while u > TRUE:
            v, lo, hi = self.nodes[u]
            u = hi if a >> v & 1 else lo
        return u

    def table(self, u: int) -> list[int]:
        return [self.evaluate(u, a) for a in range(1 << self.n)]

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
        r = self.ite_memo.get(key)
        if r is None:
            v = min(self.var(f), self.var(g), self.var(h))
            f0, f1 = self.cof(f, v)
            g0, g1 = self.cof(g, v)
            h0, h1 = self.cof(h, v)
            r = self.mk(v, self.ite(f0, g0, h0), self.ite(f1, g1, h1))
            self.ite_memo[key] = r
        return r

    def check_invariant(self) -> None:
        for u in range(2, len(self.nodes)):
            v, lo, hi = self.nodes[u]
            assert lo != hi and self.unique[(v, lo, hi)] == u
            assert self.var(lo) > v and self.var(hi) > v


def constrain(b: BDD, f: int, c: int) -> int:
    """The generalized cofactor f down c. Precondition: c != FALSE."""
    assert c != FALSE
    if c == TRUE or f <= TRUE:  # @line L1
        return f
    if f == c:  # @line L2
        return TRUE
    key = (f, c)
    r = b.con_memo.get(key)
    if r is not None:
        return r
    v = min(b.var(f), b.var(c))  # @line L3
    f0, f1 = b.cof(f, v)
    c0, c1 = b.cof(c, v)
    if c0 == FALSE:  # @line L4
        r = constrain(b, f1, c1)
    elif c1 == FALSE:  # @line L5
        r = constrain(b, f0, c0)
    else:
        r = b.mk(v, constrain(b, f0, c0), constrain(b, f1, c1))  # @line L6
    b.con_memo[key] = r
    return r


def restrict(b: BDD, f: int, c: int) -> int:
    """Coudert and Madre's restrict. Precondition: c != FALSE."""
    assert c != FALSE
    if c == TRUE or f <= TRUE:  # @line L7
        return f
    if f == c:
        return TRUE
    key = (f, c)
    r = b.res_memo.get(key)
    if r is not None:
        return r
    if b.var(c) < b.var(f):  # @line L8
        c0, c1 = b.cof(c, b.var(c))
        r = restrict(b, f, b.ite(c0, TRUE, c1))  # c0 OR c1
    else:
        v = b.var(f)  # @line L9
        f0, f1 = b.cof(f, v)
        c0, c1 = b.cof(c, v)
        if c0 == FALSE:
            r = restrict(b, f1, c1)
        elif c1 == FALSE:
            r = restrict(b, f0, c0)
        else:
            r = b.mk(v, restrict(b, f0, c0), restrict(b, f1, c1))
    b.res_memo[key] = r
    return r
