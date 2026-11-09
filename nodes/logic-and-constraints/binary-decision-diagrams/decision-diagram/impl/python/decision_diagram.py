# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/decision-diagram/. The authors are listed in prov/YY3W21.jsonl.

"""A reduced ordered decision diagram with finite domains and any terminal values.

Variable x_i takes the values 0 .. dom[i] - 1, and the variables are tested
in the order x_0, x_1, ..., x_{n-1}. A terminal is a node with var = n and a
value (any hashable object). An inner node is (i, children) with one child
per value of x_i. MK removes a node whose children are all equal and shares
equal nodes, so the store is reduced and two nodes are equal exactly when
their functions are equal. With dom = [2] * n and the values {0, 1} this is
a reduced ordered BDD; with numbers as values it is an algebraic (multi-
terminal) decision diagram; with dom[i] > 2 and the values {0, 1} it is a
multi-valued decision diagram.
"""

from collections.abc import Callable, Hashable


class DD:
    def __init__(self, dom: list[int]) -> None:
        assert all(d >= 1 for d in dom)
        self.dom = list(dom)
        self.n = len(dom)
        self.nodes: list[tuple[int, tuple[int, ...] | Hashable]] = []
        self.unique: dict[tuple, int] = {}
        self.cache: dict[tuple, int] = {}

    def var(self, u: int) -> int:
        return self.nodes[u][0]

    def is_terminal(self, u: int) -> bool:
        return self.nodes[u][0] == self.n

    def value(self, u: int) -> Hashable:
        assert self.is_terminal(u)
        return self.nodes[u][1]

    def terminal(self, v: Hashable) -> int:
        key = (self.n, ("value", v))
        u = self.unique.get(key)
        if u is None:
            u = len(self.nodes)
            self.nodes.append((self.n, v))
            self.unique[key] = u
        return u

    def mk(self, i: int, children: tuple[int, ...]) -> int:
        assert len(children) == self.dom[i]
        if all(c == children[0] for c in children):  # @line L1
            return children[0]
        key = (i, children)
        u = self.unique.get(key)  # @line L2
        if u is None:
            u = len(self.nodes)  # @line L3
            self.nodes.append(key)
            self.unique[key] = u  # @line L4
        return u  # @line L5

    def evaluate(self, u: int, x: list[int]) -> Hashable:
        while not self.is_terminal(u):  # @line L6
            i, children = self.nodes[u]
            u = children[x[i]]  # @line L7
        return self.value(u)  # @line L8

    def _cof(self, u: int, i: int, v: int) -> int:
        """The cofactor of u by x_i = v, when var(u) >= i."""
        j, children = self.nodes[u]
        return children[v] if j == i else u

    def apply(self, op: Callable[[Hashable, Hashable], Hashable], f: int, g: int) -> int:
        """The diagram of x -> op(f(x), g(x)). The op must be a pure function."""
        if self.is_terminal(f) and self.is_terminal(g):  # @line L9
            return self.terminal(op(self.value(f), self.value(g)))
        key = (op, f, g)
        r = self.cache.get(key)  # @line L10
        if r is not None:
            return r
        i = min(self.var(f), self.var(g))  # @line L11
        children = tuple(  # @line L12
            self.apply(op, self._cof(f, i, v), self._cof(g, i, v)) for v in range(self.dom[i])  # @line L13
        )
        r = self.mk(i, children)  # @line L14
        self.cache[key] = r  # @line L15
        return r  # @line L16

    def build(self, table: list[Hashable]) -> int:
        """The diagram of a table in mixed radix: x_0 is the lowest digit."""
        size = 1
        for d in self.dom:
            size *= d
        assert len(table) == size

        def go(i: int, base: int, stride: int) -> int:
            if i == self.n:
                return self.terminal(table[base])
            return self.mk(i, tuple(go(i + 1, base + v * stride, stride * self.dom[i]) for v in range(self.dom[i])))

        return go(0, 0, 1)

    def table(self, u: int) -> list[Hashable]:
        out = []
        size = 1
        for d in self.dom:
            size *= d
        for a in range(size):
            x, r = [], a
            for d in self.dom:
                x.append(r % d)
                r //= d
            out.append(self.evaluate(u, x))
        return out

    def reachable(self, u: int) -> set[int]:
        seen = {u}
        stack = [u]
        while stack:
            w = stack.pop()
            if not self.is_terminal(w):
                for c in self.nodes[w][1]:
                    if c not in seen:
                        seen.add(c)
                        stack.append(c)
        return seen

    def size(self, u: int) -> int:
        return len(self.reachable(u))
