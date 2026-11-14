# SPDX-License-Identifier: MIT
# Shared helper of the hv1 eda pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""A small reduced ordered BDD package with a unique table and an operation cache.

A node is an integer. The terminals are 0 and 1. A variable is a non-negative
integer; a smaller variable is nearer to the root. Every Boolean function has
exactly one node for a fixed order, so two functions are equal if and only if
their nodes are equal. The recursion depth of every operation is at most the
number of variables plus one.
"""

from __future__ import annotations

from typing import Mapping, Optional

TERMINAL_LEVEL = 1 << 30


class BDD:
    """A manager that owns all nodes. Functions of different managers must not be mixed."""

    def __init__(self) -> None:
        self._level: list[int] = [TERMINAL_LEVEL, TERMINAL_LEVEL]
        self._lo: list[int] = [0, 1]
        self._hi: list[int] = [0, 1]
        self._unique: dict[tuple[int, int, int], int] = {}
        self._cache: dict[tuple, int] = {}

    # Structure.

    def level(self, u: int) -> int:
        """The variable of the root of u, or TERMINAL_LEVEL for a terminal."""
        return self._level[u]

    def low(self, u: int) -> int:
        """The child of u for the value 0 of its root variable."""
        return self._lo[u]

    def high(self, u: int) -> int:
        """The child of u for the value 1 of its root variable."""
        return self._hi[u]

    def mk(self, v: int, lo: int, hi: int) -> int:
        """The unique node (v, lo, hi), with the reduction rule lo = hi."""
        if lo == hi:
            return lo
        key = (v, lo, hi)
        u = self._unique.get(key)
        if u is None:
            u = len(self._level)
            self._level.append(v)
            self._lo.append(lo)
            self._hi.append(hi)
            self._unique[key] = u
        return u

    def var(self, v: int) -> int:
        """The function that is the variable v."""
        return self.mk(v, 0, 1)

    def cofactors(self, u: int, v: int) -> tuple[int, int]:
        """The two cofactors of u by v, when v is at or above the root of u."""
        if self._level[u] == v:
            return self._lo[u], self._hi[u]
        return u, u

    # Boolean operations.

    def apply(self, op: str, u: int, w: int) -> int:
        """op(u, w) for op in and, or, xor. Cost O(|u| |w|) with the cache."""
        if op == "and":
            if u == 0 or w == 0:
                return 0
            if u == 1 or u == w:
                return w
            if w == 1:
                return u
        elif op == "or":
            if u == 1 or w == 1:
                return 1
            if u == 0 or u == w:
                return w
            if w == 0:
                return u
        elif op == "xor":
            if u == w:
                return 0
            if u == 0:
                return w
            if w == 0:
                return u
        else:
            raise ValueError(op)
        if u > w:
            u, w = w, u
        key = (op, u, w)
        r = self._cache.get(key)
        if r is None:
            v = min(self._level[u], self._level[w])
            u0, u1 = self.cofactors(u, v)
            w0, w1 = self.cofactors(w, v)
            r = self.mk(v, self.apply(op, u0, w0), self.apply(op, u1, w1))
            self._cache[key] = r
        return r

    def conj(self, u: int, w: int) -> int:
        return self.apply("and", u, w)

    def disj(self, u: int, w: int) -> int:
        return self.apply("or", u, w)

    def xor(self, u: int, w: int) -> int:
        return self.apply("xor", u, w)

    def neg(self, u: int) -> int:
        return self.apply("xor", u, 1)

    def xnor(self, u: int, w: int) -> int:
        return self.neg(self.xor(u, w))

    def ite(self, f: int, g: int, h: int) -> int:
        """If f then g else h."""
        return self.disj(self.conj(f, g), self.conj(self.neg(f), h))

    # Substitution and quantification.

    def restrict(self, u: int, v: int, b: int) -> int:
        """The cofactor of u with variable v fixed to b."""
        if self._level[u] > v:
            return u
        if self._level[u] == v:
            return self._hi[u] if b else self._lo[u]
        key = ("restrict", u, v, b)
        r = self._cache.get(key)
        if r is None:
            r = self.mk(self._level[u], self.restrict(self._lo[u], v, b), self.restrict(self._hi[u], v, b))
            self._cache[key] = r
        return r

    def compose(self, u: int, v: int, g: int) -> int:
        """u with variable v replaced by the function g."""
        return self.ite(g, self.restrict(u, v, 1), self.restrict(u, v, 0))

    def exists(self, u: int, vs: frozenset[int]) -> int:
        """The existential quantification of u over the variables vs."""
        if u <= 1 or not vs:
            return u
        key = ("exists", u, vs)
        r = self._cache.get(key)
        if r is None:
            v = self._level[u]
            lo = self.exists(self._lo[u], vs)
            hi = self.exists(self._hi[u], vs)
            r = self.disj(lo, hi) if v in vs else self.mk(v, lo, hi)
            self._cache[key] = r
        return r

    # Queries.

    def support(self, u: int) -> set[int]:
        """The variables that u depends on."""
        seen: set[int] = set()
        out: set[int] = set()
        stack = [u]
        while stack:
            w = stack.pop()
            if w <= 1 or w in seen:
                continue
            seen.add(w)
            out.add(self._level[w])
            stack.append(self._lo[w])
            stack.append(self._hi[w])
        return out

    def size(self, u: int) -> int:
        """The number of nodes of u, terminals included."""
        seen: set[int] = set()
        stack = [u]
        while stack:
            w = stack.pop()
            if w in seen:
                continue
            seen.add(w)
            if w > 1:
                stack.append(self._lo[w])
                stack.append(self._hi[w])
        return len(seen)

    def sat_one(self, u: int) -> Optional[dict[int, int]]:
        """One assignment to some variables that makes u true, or None if u is 0."""
        if u == 0:
            return None
        point: dict[int, int] = {}
        while u != 1:
            if self._lo[u] != 0:
                point[self._level[u]] = 0
                u = self._lo[u]
            else:
                point[self._level[u]] = 1
                u = self._hi[u]
        return point

    def evaluate(self, u: int, point: Mapping[int, int]) -> int:
        """The value of u at the point; a variable not in the point has the value 0."""
        while u > 1:
            u = self._hi[u] if point.get(self._level[u], 0) else self._lo[u]
        return u
