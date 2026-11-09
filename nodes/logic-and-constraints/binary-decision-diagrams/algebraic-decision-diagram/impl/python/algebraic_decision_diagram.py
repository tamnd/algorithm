# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/algebraic-decision-diagram/. The authors are listed in prov/1TQF00.jsonl.

"""Algebraic decision diagrams (ADDs), also called multi-terminal BDDs.

An ADD represents a function f: {0,1}^n -> D for a set D of values (here any
hashable Python values, usually numbers). There is one terminal node for each
value that occurs, and an inner node u is nodes[u] = (v, lo, hi), with the
order x_0 < x_1 < ... < x_{n-1} (x_{i+1} of the page is x_i here). A terminal
has the variable n and stores its value in nodes[u] = (n, value, None).

The two reduction rules are those of BDDs: no node with lo == hi, and no two
equal nodes. With the unique table, equal functions give the same node.

apply(op, f, g) is memoized and makes O(|f| |g|) calls of mk. The recursion
depth is at most n + 1.
"""

import operator
from typing import Callable, Hashable


class ADD:
    def __init__(self, n: int) -> None:
        self.n = n
        self.nodes: list[tuple] = []
        self.unique: dict[tuple, int] = {}
        self.memo: dict[tuple, int] = {}

    def const(self, value: Hashable) -> int:
        key = (self.n, value, None)
        u = self.unique.get(key)
        if u is None:
            u = len(self.nodes)
            self.nodes.append(key)
            self.unique[key] = u
        return u

    def mk(self, v: int, lo: int, hi: int) -> int:
        if lo == hi:  # @line L1
            return lo
        key = (v, lo, hi)
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

    def value(self, u: int) -> Hashable:
        assert self.is_const(u)
        return self.nodes[u][1]

    def cof(self, u: int, v: int) -> tuple[int, int]:
        w, lo, hi = self.nodes[u]
        return (lo, hi) if w == v else (u, u)

    def from_table(self, table: list[Hashable]) -> int:
        """The node of the function with this table (bit i of the index is x_i)."""
        assert len(table) == 1 << self.n
        layer = [self.const(t) for t in table]
        for v in range(self.n - 1, -1, -1):
            half = 1 << v
            layer = [self.mk(v, layer[a], layer[a + half]) for a in range(half)]
        return layer[0]

    def evaluate(self, u: int, a: int) -> Hashable:
        while not self.is_const(u):
            v, lo, hi = self.nodes[u]
            u = hi if a >> v & 1 else lo
        return self.value(u)

    def apply(self, op: Callable[[Hashable, Hashable], Hashable], f: int, g: int) -> int:
        """The function x -> op(f(x), g(x))."""
        if self.is_const(f) and self.is_const(g):  # @line L4
            return self.const(op(self.value(f), self.value(g)))
        key = (op, f, g)
        r = self.memo.get(key)  # @line L5
        if r is None:
            v = min(self.var(f), self.var(g))  # @line L6
            f0, f1 = self.cof(f, v)
            g0, g1 = self.cof(g, v)
            r = self.mk(v, self.apply(op, f0, g0), self.apply(op, f1, g1))  # @line L7
            self.memo[key] = r  # @line L8
        return r

    def sum_out(self, f: int, v: int) -> int:
        """The function f|x_v=0 + f|x_v=1 (it does not depend on x_v)."""
        key = ("sum", f, v)
        r = self.memo.get(key)
        if r is None:
            if self.is_const(f) or self.var(f) > v:
                r = self.apply(operator.add, f, f)
            elif self.var(f) == v:
                _, lo, hi = self.nodes[f]
                r = self.apply(operator.add, lo, hi)
            else:
                w, lo, hi = self.nodes[f]
                r = self.mk(w, self.sum_out(lo, v), self.sum_out(hi, v))
            self.memo[key] = r
        return r

    def threshold(self, f: int, t: Hashable) -> int:
        """The 0-1 ADD of the predicate f(x) >= t."""
        return self.apply(lambda a, b: 1 if a >= b else 0, f, self.const(t))

    def size(self, u: int) -> int:
        seen = {u}
        stack = [u]
        while stack:
            w = stack.pop()
            if not self.is_const(w):
                for c in self.nodes[w][1:]:
                    if c not in seen:
                        seen.add(c)
                        stack.append(c)
        return len(seen)

    def check_invariant(self) -> None:
        for u, (v, lo, hi) in enumerate(self.nodes):
            assert self.unique[(v, lo, hi)] == u
            if v < self.n:
                assert lo != hi and self.var(lo) > v and self.var(hi) > v
