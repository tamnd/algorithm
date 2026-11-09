# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-moment-diagram/. The authors are listed in prov/NFC4FF.jsonl.

"""Binary moment diagrams (BMDs) for functions {0,1}^n -> integers.

The moment decomposition of f by x is f = f_0 + x * (f_1 - f_0), where f_0 and
f_1 are the cofactors. The constant moment is f_0 and the linear moment is
f_1 - f_0. An inner node u is nodes[u] = (v, c, l): it stands for c + x_v * l.
A terminal stores an integer: nodes[u] = (n, value, None). The order is
x_0 < x_1 < ... < x_{n-1} (x_{i+1} of the page is x_i here).

Reduction rules: no node whose linear moment is the terminal 0 (then the node
is its constant moment), and no two equal nodes. These make the BMD of f
unique. This is the plain BMD of Bryant and Chen, without edge weights.

add and mul are memoized. add makes O(|f| |g|) calls of mk. mul can take
more time, since each step calls add. The recursion depth is O(n).
"""


class BMD:
    def __init__(self, n: int) -> None:
        self.n = n
        self.nodes: list[tuple] = []
        self.unique: dict[tuple, int] = {}
        self.memo: dict[tuple, int] = {}
        self.zero = self.const(0)

    def const(self, value: int) -> int:
        key = (self.n, value, None)
        u = self.unique.get(key)
        if u is None:
            u = len(self.nodes)
            self.nodes.append(key)
            self.unique[key] = u
        return u

    def mk(self, v: int, c: int, l: int) -> int:
        if l == self.zero:  # @line L1
            return c
        key = (v, c, l)
        u = self.unique.get(key)  # @line L2
        if u is None:
            u = len(self.nodes)
            self.nodes.append(key)
            self.unique[key] = u
        return u  # @line L3

    def var(self, u: int) -> int:
        return self.nodes[u][0]

    def is_const(self, u: int) -> bool:
        return self.nodes[u][0] == self.n

    def moments(self, u: int, v: int) -> tuple[int, int]:
        """(constant moment, linear moment) of u by x_v, where v is at or above the top of u."""
        w, c, l = self.nodes[u]
        return (c, l) if w == v else (u, self.zero)

    def from_table(self, table: list[int]) -> int:
        """table[a] is f(x) with x_i = bit i of a."""
        assert len(table) == 1 << self.n
        coef = list(table)
        for i in range(self.n):  # the moment transform: coef[S] is the coefficient of prod_{i in S} x_i
            bit = 1 << i
            for a in range(1 << self.n):
                if a & bit:
                    coef[a] -= coef[a ^ bit]
        layer = [self.const(t) for t in coef]
        for v in range(self.n - 1, -1, -1):  # @line L4
            half = 1 << v
            layer = [self.mk(v, layer[a], layer[a + half]) for a in range(half)]  # @line L5
        return layer[0]

    def evaluate(self, u: int, a: int) -> int:
        """f(x) for x_i = bit i of a. All nodes are visited: O(|f|) time."""
        val: dict[int, int] = {}
        for w in sorted(self.reach(u)):  # children have smaller ids
            v, c, l = self.nodes[w]
            if v == self.n:
                val[w] = c
            else:
                val[w] = val[c] + (val[l] if a >> v & 1 else 0)  # @line L6
        return val[u]

    def add(self, f: int, g: int) -> int:
        if self.is_const(f) and self.is_const(g):  # @line L7
            return self.const(self.nodes[f][1] + self.nodes[g][1])
        key = ("+", min(f, g), max(f, g))
        r = self.memo.get(key)
        if r is None:
            v = min(self.var(f), self.var(g))
            fc, fl = self.moments(f, v)
            gc, gl = self.moments(g, v)
            r = self.mk(v, self.add(fc, gc), self.add(fl, gl))  # @line L8
            self.memo[key] = r
        return r

    def mul(self, f: int, g: int) -> int:
        """(a + x b)(c + x d) = a c + x (a d + b c + b d), since x * x = x."""
        if self.is_const(f) and self.is_const(g):  # @line L9
            return self.const(self.nodes[f][1] * self.nodes[g][1])
        key = ("*", min(f, g), max(f, g))
        r = self.memo.get(key)
        if r is None:
            v = min(self.var(f), self.var(g))
            a, b = self.moments(f, v)
            c, d = self.moments(g, v)
            lin = self.add(self.add(self.mul(a, d), self.mul(b, c)), self.mul(b, d))  # @line L10
            r = self.mk(v, self.mul(a, c), lin)  # @line L11
            self.memo[key] = r
        return r

    def reach(self, u: int) -> set[int]:
        seen = {u}
        stack = [u]
        while stack:
            w = stack.pop()
            if not self.is_const(w):
                for c in self.nodes[w][1:]:
                    if c not in seen:
                        seen.add(c)
                        stack.append(c)
        return seen

    def size(self, u: int) -> int:
        return len(self.reach(u))

    def check_invariant(self) -> None:
        for u, key in enumerate(self.nodes):
            assert self.unique[key] == u
            v, c, l = key
            if v < self.n:
                assert l != self.zero and self.var(c) > v and self.var(l) > v
