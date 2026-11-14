# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/taylor-expansion-diagram/. The authors are listed in prov/B790DF.jsonl.
"""Reduced ordered Taylor expansion diagrams over the rationals.

A node (v, (c_0, ..., c_d)) stands for the polynomial sum_k x_v^k f_{c_k}, where
f_{c_k} = (1/k!) d^k f / dx_v^k at x_v = 0 is the k-th Taylor coefficient. The
children are on later levels. A sink holds one Fraction. MK keeps the diagram
reduced: no trailing zero child, no node with only the 0-th child, and no two
equal nodes. Then two polynomials are equal exactly when their node ids are.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping, Sequence, Union

Expr = Union[tuple, str, int, Fraction]


class TED:
    def __init__(self, order: Sequence[str]) -> None:
        self.order = list(order)
        self.level = {name: i for i, name in enumerate(self.order)}
        self.n = len(self.order)
        self.nodes: list[tuple] = []        # id -> ("c", q) or (level, children)
        self.unique: dict[tuple, int] = {}
        self.add_cache: dict[tuple[int, int], int] = {}
        self.mul_cache: dict[tuple[int, int], int] = {}
        self.zero = self.const(0)
        self.one = self.const(1)

    # ------------------------------------------------------------------ nodes

    def const(self, q) -> int:
        key = ("c", Fraction(q))
        u = self.unique.get(key)
        if u is None:
            u = len(self.nodes)
            self.nodes.append(key)
            self.unique[key] = u
        return u

    def is_const(self, u: int) -> bool:
        return self.nodes[u][0] == "c"

    def value(self, u: int) -> Fraction:
        return self.nodes[u][1]

    def var_level(self, u: int) -> int:
        return self.n if self.is_const(u) else self.nodes[u][0]

    def children(self, u: int) -> tuple[int, ...]:
        return self.nodes[u][1]

    def mk(self, v: int, children: Sequence[int]) -> int:
        ch = list(children)
        while len(ch) > 1 and ch[-1] == self.zero:                  # @line L1
            ch.pop()
        if len(ch) == 1:                                             # @line L2
            return ch[0]
        key = (v, tuple(ch))
        u = self.unique.get(key)                                     # @line L3
        if u is None:
            u = len(self.nodes)                                      # @line L4
            self.nodes.append(key)
            self.unique[key] = u
        return u

    def var(self, name: str) -> int:
        return self.mk(self.level[name], (self.zero, self.one))

    def coef(self, u: int, v: int) -> list[int]:
        """The Taylor coefficients of u by the variable of level v <= level of u."""
        return list(self.children(u)) if self.var_level(u) == v else [u]

    # ------------------------------------------------------------- operations

    def add(self, f: int, g: int) -> int:
        if f == self.zero:
            return g
        if g == self.zero:
            return f
        if self.is_const(f) and self.is_const(g):                    # @line L5
            return self.const(self.value(f) + self.value(g))
        key = (min(f, g), max(f, g))
        r = self.add_cache.get(key)
        if r is None:
            v = min(self.var_level(f), self.var_level(g))            # @line L6
            a, b = self.coef(f, v), self.coef(g, v)
            m = max(len(a), len(b))
            a += [self.zero] * (m - len(a))
            b += [self.zero] * (m - len(b))
            r = self.mk(v, [self.add(x, y) for x, y in zip(a, b)])
            self.add_cache[key] = r
        return r

    def mul(self, f: int, g: int) -> int:
        if f == self.zero or g == self.zero:
            return self.zero
        if f == self.one:
            return g
        if g == self.one:
            return f
        if self.is_const(f) and self.is_const(g):                    # @line L7
            return self.const(self.value(f) * self.value(g))
        key = (min(f, g), max(f, g))
        r = self.mul_cache.get(key)
        if r is None:
            v = min(self.var_level(f), self.var_level(g))            # @line L8
            a, b = self.coef(f, v), self.coef(g, v)
            c = [self.zero] * (len(a) + len(b) - 1)
            for i, x in enumerate(a):
                for j, y in enumerate(b):
                    c[i + j] = self.add(c[i + j], self.mul(x, y))
            r = self.mk(v, c)                                        # @line L9
            self.mul_cache[key] = r
        return r

    def neg(self, f: int) -> int:
        return self.mul(self.const(-1), f)

    def evaluate(self, u: int, point: Mapping[str, Fraction]) -> Fraction:
        val: dict[int, Fraction] = {}

        def go(w: int) -> Fraction:
            if w in val:
                return val[w]
            if self.is_const(w):
                r = self.value(w)
            else:                                                    # @line L10
                x = Fraction(point[self.order[self.var_level(w)]])
                r = Fraction(0)
                for c in reversed(self.children(w)):                 # Horner
                    r = r * x + go(c)
            val[w] = r
            return r

        return go(u)

    def build(self, e: Expr) -> int:
        """The node of an expression: a variable name, a number, or (op, a, b)
        with op in '+', '-', '*', or ('^', a, k) for a power k >= 0."""
        if isinstance(e, str):                                       # @line L11
            return self.var(e)
        if isinstance(e, (int, Fraction)):
            return self.const(e)
        op = e[0]
        if op == "^":
            r, base = self.one, self.build(e[1])
            for _ in range(e[2]):
                r = self.mul(r, base)
            return r
        a, b = self.build(e[1]), self.build(e[2])
        if op == "+":
            return self.add(a, b)
        if op == "-":
            return self.add(a, self.neg(b))
        return self.mul(a, b)

    # ---------------------------------------------------------------- reading

    def reachable(self, u: int) -> set[int]:
        seen, todo = set(), [u]
        while todo:
            w = todo.pop()
            if w not in seen:
                seen.add(w)
                if not self.is_const(w):
                    todo.extend(self.children(w))
        return seen

    def size(self, u: int) -> int:
        return len(self.reachable(u))

    def to_poly(self, u: int) -> dict[tuple[int, ...], Fraction]:
        """Unfold u into {exponent vector: coefficient}, with nonzero coefficients."""
        if self.is_const(u):
            q = self.value(u)
            return {(0,) * self.n: q} if q else {}
        v = self.var_level(u)
        out: dict[tuple[int, ...], Fraction] = {}
        for k, c in enumerate(self.children(u)):
            for mono, q in self.to_poly(c).items():
                m = list(mono)
                m[v] += k
                out[tuple(m)] = q
        return out
