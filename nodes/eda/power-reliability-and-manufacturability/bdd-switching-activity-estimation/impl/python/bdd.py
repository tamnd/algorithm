# SPDX-License-Identifier: MIT
# Shared helper of the pr1 eda pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""A small reduced ordered BDD package.

Nodes are integers. 0 and 1 are the terminals. An internal node u has a
variable index var(u) (smaller indices are nearer the root), a low child
(the variable is 0) and a high child (the variable is 1). A unique table keeps
the diagram reduced, so two equal functions have the same node.

This module holds node creation, the apply operation with a computed table,
negation, evaluation and size. It holds no estimation algorithm.
"""

from __future__ import annotations

from typing import Callable, Mapping

TERMINAL_VAR = 1 << 30


class BDD:
    def __init__(self) -> None:
        self.var_of = [TERMINAL_VAR, TERMINAL_VAR]
        self.lo = [0, 1]
        self.hi = [0, 1]
        self.unique: dict[tuple[int, int, int], int] = {}

    def mk(self, v: int, lo: int, hi: int) -> int:
        """The node (v, lo, hi), reduced and shared."""
        if lo == hi:
            return lo
        key = (v, lo, hi)
        u = self.unique.get(key)
        if u is None:
            u = len(self.var_of)
            self.var_of.append(v)
            self.lo.append(lo)
            self.hi.append(hi)
            self.unique[key] = u
        return u

    def var(self, v: int) -> int:
        """The function that is variable v."""
        return self.mk(v, 0, 1)

    def is_terminal(self, u: int) -> bool:
        return u < 2

    def apply(self, op: Callable[[int, int], int], u: int, w: int) -> int:
        """The BDD of op(f_u, f_w) for a binary Boolean operator op."""
        memo: dict[tuple[int, int], int] = {}

        def rec(a: int, b: int) -> int:
            if a < 2 and b < 2:
                return op(a, b)
            key = (a, b)
            r = memo.get(key)
            if r is not None:
                return r
            v = min(self.var_of[a], self.var_of[b])
            a0, a1 = (self.lo[a], self.hi[a]) if self.var_of[a] == v else (a, a)
            b0, b1 = (self.lo[b], self.hi[b]) if self.var_of[b] == v else (b, b)
            r = self.mk(v, rec(a0, b0), rec(a1, b1))
            memo[key] = r
            return r

        return rec(u, w)

    def AND(self, u: int, w: int) -> int:
        return self.apply(lambda a, b: a & b, u, w)

    def OR(self, u: int, w: int) -> int:
        return self.apply(lambda a, b: a | b, u, w)

    def XOR(self, u: int, w: int) -> int:
        return self.apply(lambda a, b: a ^ b, u, w)

    def NOT(self, u: int) -> int:
        return self.apply(lambda a, b: a ^ b, u, 1)

    def evaluate(self, u: int, value: Mapping[int, int]) -> int:
        """The value of f_u when variable v has value value[v]."""
        while u >= 2:
            u = self.hi[u] if value[self.var_of[u]] else self.lo[u]
        return u

    def size(self, u: int) -> int:
        """The number of nodes reachable from u, terminals included."""
        seen = set()
        stack = [u]
        while stack:
            a = stack.pop()
            if a in seen:
                continue
            seen.add(a)
            if a >= 2:
                stack.append(self.lo[a])
                stack.append(self.hi[a])
        return len(seen)
