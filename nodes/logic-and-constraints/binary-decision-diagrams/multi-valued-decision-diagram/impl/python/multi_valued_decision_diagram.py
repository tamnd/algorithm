# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-valued-decision-diagram/. The authors are listed in prov/C9XT2M.jsonl.

"""Multi-valued decision diagrams (MDDs) with a fixed variable order.

Variable i (0-based; x_{i+1} of the page) takes the values 0..d[i]-1. The
order is x_0 < x_1 < ... < x_{n-1}. A terminal node stores a value in
nodes[u] = (n, value); an inner node is nodes[u] = (v, children), where
children is a tuple of d[v] node ids, one for each value of x_v.

Reduction rules: no node whose children are all equal, and no two equal
nodes. With the unique table, equal functions give the same node.

apply(op, f, g) is memoized and makes O(|f| |g|) calls of mk, each of cost
O(d) for d = max(d[i]). The recursion depth is at most n + 1.
"""

from typing import Callable, Hashable


class MDD:
    def __init__(self, domains: list[int]) -> None:
        assert all(k >= 1 for k in domains)
        self.d = list(domains)
        self.n = len(domains)
        self.nodes: list[tuple] = []
        self.unique: dict[tuple, int] = {}
        self.memo: dict[tuple, int] = {}

    def const(self, value: Hashable) -> int:
        key = (self.n, value)
        u = self.unique.get(key)
        if u is None:
            u = len(self.nodes)
            self.nodes.append(key)
            self.unique[key] = u
        return u

    def mk(self, v: int, children: tuple[int, ...]) -> int:
        assert len(children) == self.d[v]
        if all(c == children[0] for c in children):  # @line L1
            return children[0]
        key = (v, children)
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

    def child(self, u: int, v: int, j: int) -> int:
        """The cofactor of u by x_v = j, where v is at or above the top of u."""
        return self.nodes[u][1][j] if self.var(u) == v else u

    def index(self, x: list[int]) -> int:
        """The mixed-radix index of x, with x_0 the least significant digit."""
        a = 0
        for v in range(self.n - 1, -1, -1):
            a = a * self.d[v] + x[v]
        return a

    def from_table(self, table: list[Hashable]) -> int:
        """table[index(x)] is f(x)."""
        total = 1
        for k in self.d:
            total *= k
        assert len(table) == total
        layer = [self.const(t) for t in table]
        for v in range(self.n - 1, -1, -1):  # x_v is the most significant digit left
            block = len(layer) // self.d[v]
            layer = [self.mk(v, tuple(layer[j * block + a] for j in range(self.d[v]))) for a in range(block)]
        return layer[0]

    def evaluate(self, u: int, x: list[int]) -> Hashable:
        while not self.is_const(u):  # @line L4
            v, children = self.nodes[u]
            u = children[x[v]]  # @line L5
        return self.nodes[u][1]  # @line L6

    def apply(self, op: Callable[[Hashable, Hashable], Hashable], f: int, g: int) -> int:
        if self.is_const(f) and self.is_const(g):  # @line L7
            return self.const(op(self.nodes[f][1], self.nodes[g][1]))
        key = (op, f, g)
        r = self.memo.get(key)
        if r is None:
            v = min(self.var(f), self.var(g))  # @line L8
            kids = tuple(self.apply(op, self.child(f, v, j), self.child(g, v, j)) for j in range(self.d[v]))  # @line L9
            r = self.mk(v, kids)  # @line L10
            self.memo[key] = r
        return r

    def count(self, u: int, value: Hashable = 1) -> int:
        """The number of x with f(x) == value."""
        order = sorted(self.reach(u))  # children have smaller ids
        c: dict[int, int] = {}
        for w in order:
            if self.is_const(w):
                below = 1
                for k in self.d:
                    below *= k
                c[w] = below if self.nodes[w][1] == value else 0
            else:
                v, children = self.nodes[w]
                c[w] = sum(c[x] for x in children) // self.d[v]
        return c[u]

    def reach(self, u: int) -> set[int]:
        seen = {u}
        stack = [u]
        while stack:
            w = stack.pop()
            if not self.is_const(w):
                for c in self.nodes[w][1]:
                    if c not in seen:
                        seen.add(c)
                        stack.append(c)
        return seen

    def size(self, u: int) -> int:
        return len(self.reach(u))

    def check_invariant(self) -> None:
        for u, key in enumerate(self.nodes):
            assert self.unique[key] == u
            if key[0] < self.n:
                v, children = key
                assert len(children) == self.d[v] and len(set(children)) > 1
                assert all(self.var(c) > v for c in children)
