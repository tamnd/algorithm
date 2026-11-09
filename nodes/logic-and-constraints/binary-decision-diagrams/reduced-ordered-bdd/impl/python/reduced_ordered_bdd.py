# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reduced-ordered-bdd/. The authors are listed in prov/4A6P2D.jsonl.

"""A small reduced ordered BDD package.

The variables are x_0, ..., x_{n-1}, tested in this order (x_0 at the top).
A node is an int. Node 0 is the terminal FALSE and node 1 is the terminal
TRUE. Each node u has the triple nodes[u] = (var, lo, hi); a terminal has
var = n. The unique table maps each triple to its node, so two nodes never
have the same triple, and MK never makes a node with lo = hi. A child is
always made before its parent, so a child has a smaller id than its parent.

The recursions below go down one level of the order at each call, so their
depth is at most n + 1.
"""

FALSE, TRUE = 0, 1

# A binary operator is a 4-bit truth table: bit 2a + b holds op(a, b).
AND, OR, XOR, NAND, NOR, XNOR = 0b1000, 0b1110, 0b0110, 0b0111, 0b0001, 0b1001
IMPLIES = 0b1011  # a -> b is false only for a = 1, b = 0 (bit 2)


class BDD:
    def __init__(self, n: int) -> None:
        self.n = n
        self.nodes: list[tuple[int, int, int]] = [(n, 0, 0), (n, 1, 1)]
        self.unique: dict[tuple[int, int, int], int] = {}
        self.cache: dict[tuple, int] = {}

    # ---------------------------------------------------------------- access

    def var(self, u: int) -> int:
        return self.nodes[u][0]

    def low(self, u: int) -> int:
        return self.nodes[u][1]

    def high(self, u: int) -> int:
        return self.nodes[u][2]

    def mk(self, i: int, lo: int, hi: int) -> int:
        """Return the node (x_i ? hi : lo), with both reduction rules."""
        if lo == hi:  # @line L1
            return lo
        key = (i, lo, hi)
        u = self.unique.get(key)  # @line L2
        if u is None:
            u = len(self.nodes)  # @line L3
            self.nodes.append(key)
            self.unique[key] = u  # @line L4
        return u  # @line L5

    def ithvar(self, i: int) -> int:
        return self.mk(i, FALSE, TRUE)

    def build(self, table: list[int]) -> int:
        """Return the node of the function with truth table `table`.

        table[a] is f(x) where x_j is bit j of a, and len(table) == 2**n.
        """
        assert len(table) == 1 << self.n
        c = [TRUE if t else FALSE for t in table]  # @line L6
        for i in range(self.n - 1, -1, -1):  # @line L7
            for p in range(1 << i):  # @line L8
                c[p] = self.mk(i, c[p], c[p + (1 << i)])  # @line L9
        return c[0]  # @line L10

    def evaluate(self, u: int, x: list[int]) -> int:
        while u > TRUE:  # @line L11
            u = self.high(u) if x[self.var(u)] else self.low(u)  # @line L12
        return u  # @line L13

    def truth_table(self, u: int) -> list[int]:
        n = self.n
        return [self.evaluate(u, [(a >> j) & 1 for j in range(n)]) for a in range(1 << n)]

    def size(self, u: int) -> int:
        """The number of nodes reachable from u, terminals included."""
        seen = {u}
        stack = [u]
        while stack:
            w = stack.pop()
            if w > TRUE:
                for c in (self.low(w), self.high(w)):
                    if c not in seen:
                        seen.add(c)
                        stack.append(c)
        return len(seen)

    def equal(self, f: int, g: int) -> bool:
        """Equivalence test: by canonicity it is a compare of two ints."""
        return f == g  # @line L20

    # ------------------------------------------------------------ operations

    def _cof(self, u: int, i: int) -> tuple[int, int]:
        """The two cofactors of u by x_i, when var(u) >= i."""
        v, lo, hi = self.nodes[u]
        return (lo, hi) if v == i else (u, u)

    def ite(self, f: int, g: int, h: int) -> int:
        if f == TRUE:
            return g
        if f == FALSE:
            return h
        if g == h:
            return g
        if g == TRUE and h == FALSE:
            return f
        key = ("ite", f, g, h)
        r = self.cache.get(key)
        if r is not None:
            return r
        i = min(self.var(f), self.var(g), self.var(h))
        f0, f1 = self._cof(f, i)
        g0, g1 = self._cof(g, i)
        h0, h1 = self._cof(h, i)
        r = self.mk(i, self.ite(f0, g0, h0), self.ite(f1, g1, h1))
        self.cache[key] = r
        return r

    def neg(self, f: int) -> int:
        return self.ite(f, FALSE, TRUE)

    def apply(self, op: int, f: int, g: int) -> int:
        if f <= TRUE and g <= TRUE:
            return (op >> (2 * f + g)) & 1
        key = (op, f, g)
        r = self.cache.get(key)
        if r is not None:
            return r
        i = min(self.var(f), self.var(g))
        f0, f1 = self._cof(f, i)
        g0, g1 = self._cof(g, i)
        r = self.mk(i, self.apply(op, f0, g0), self.apply(op, f1, g1))
        self.cache[key] = r
        return r

    def restrict(self, f: int, i: int, b: int) -> int:
        """The cofactor f|x_i=b, in time linear in the size of f."""
        memo: dict[int, int] = {}

        def go(u: int) -> int:
            v = self.var(u)
            if v > i:  # @line L14
                return u
            if v == i:  # @line L15
                return self.high(u) if b else self.low(u)
            r = memo.get(u)  # @line L16
            if r is None:
                r = self.mk(v, go(self.low(u)), go(self.high(u)))  # @line L17
                memo[u] = r  # @line L18
            return r

        return go(f)  # @line L19

    def exists(self, f: int, xs: set[int]) -> int:
        """The function (exists x_i for i in xs) f."""
        memo: dict[int, int] = {}
        last = max(xs, default=-1)

        def go(u: int) -> int:
            v = self.var(u)
            if v > last:
                return u
            r = memo.get(u)
            if r is None:
                lo, hi = go(self.low(u)), go(self.high(u))
                r = self.apply(OR, lo, hi) if v in xs else self.mk(v, lo, hi)
                memo[u] = r
            return r

        return go(f)

    def forall(self, f: int, xs: set[int]) -> int:
        memo: dict[int, int] = {}
        last = max(xs, default=-1)

        def go(u: int) -> int:
            v = self.var(u)
            if v > last:
                return u
            r = memo.get(u)
            if r is None:
                lo, hi = go(self.low(u)), go(self.high(u))
                r = self.apply(AND, lo, hi) if v in xs else self.mk(v, lo, hi)
                memo[u] = r
            return r

        return go(f)

    def compose(self, f: int, i: int, g: int) -> int:
        """The function f with g put in place of x_i."""
        return self.ite(g, self.restrict(f, i, 1), self.restrict(f, i, 0))

    def satcount(self, f: int) -> int:
        """The number of x in {0,1}^n with f(x) = 1, in time O(size of f)."""
        n = self.n
        count = {FALSE: 0, TRUE: 1}
        stack = [f]
        while stack:
            u = stack[-1]
            if u in count:
                stack.pop()
                continue
            v, lo, hi = self.nodes[u]
            if lo in count and hi in count:
                stack.pop()
                count[u] = (count[lo] << (self.var(lo) - v - 1)) + (count[hi] << (self.var(hi) - v - 1))
            else:
                stack.extend(c for c in (lo, hi) if c not in count)
        return count[f] << min(self.var(f), n)

    # ---------------------------------------------------------------- checks

    def check_invariants(self) -> None:
        """Raise AssertionError if the node store is not a reduced ordered BDD."""
        seen = set()
        for u in range(2, len(self.nodes)):
            v, lo, hi = self.nodes[u]
            assert lo != hi, "a node has two equal children"
            assert (v, lo, hi) not in seen, "two nodes have the same triple"
            seen.add((v, lo, hi))
            assert self.unique[(v, lo, hi)] == u
            assert v < self.var(lo) and v < self.var(hi), "the order is broken"
            assert lo < u and hi < u
        assert len(self.unique) == len(self.nodes) - 2
