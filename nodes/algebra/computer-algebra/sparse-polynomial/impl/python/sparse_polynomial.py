# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-polynomial/. The authors are listed in prov/28C10S.jsonl.
"""Sparse distributed multivariate polynomials, sorted by a monomial order.

A polynomial in K[x_1, ..., x_n] is a list of terms (alpha, c), where alpha is
an exponent tuple of length n and c is a nonzero coefficient. The terms are in
strictly decreasing order for a fixed monomial order (lex, grlex or grevlex),
so the first term is the leading term. Coefficients may be int, Fraction, or
any type with +, -, * and == 0 that models a commutative ring.

Costs count ring operations and monomial operations (a comparison or a product
of two exponent tuples, each O(n) integer operations).
"""

from __future__ import annotations

import heapq
from typing import Any, Callable, Iterable

Mono = tuple[int, ...]
Term = tuple[Mono, Any]


def _lex(a: Mono) -> tuple:
    return a


def _grlex(a: Mono) -> tuple:
    return (sum(a),) + a


def _grevlex(a: Mono) -> tuple:
    return (sum(a),) + tuple(-e for e in reversed(a))


ORDERS: dict[str, Callable[[Mono], tuple]] = {"lex": _lex, "grlex": _grlex, "grevlex": _grevlex}


def _mono_mul(a: Mono, b: Mono) -> Mono:
    return tuple(x + y for x, y in zip(a, b))


class SparsePolynomial:
    """A polynomial with its terms in strictly decreasing monomial order and no zero coefficient."""

    __slots__ = ("nvars", "order", "terms", "_key")

    def __init__(self, nvars: int, order: str = "grevlex", terms: Iterable[Term] = ()) -> None:
        """Build from any terms: like terms are added and zero terms dropped. Cost: O(t log t) monomial comparisons."""
        if order not in ORDERS:
            raise ValueError("order must be lex, grlex or grevlex")
        self.nvars = nvars
        self.order = order
        self._key = ORDERS[order]
        acc: dict[Mono, Any] = {}
        for a, c in terms:
            a = tuple(a)
            if len(a) != nvars or min(a, default=0) < 0:
                raise ValueError("bad exponent tuple")
            acc[a] = acc[a] + c if a in acc else c
        self.terms: list[Term] = sorted(((a, c) for a, c in acc.items() if c != 0), key=lambda t: self._key(t[0]), reverse=True)

    def _new(self, terms: list[Term]) -> "SparsePolynomial":
        p = SparsePolynomial(self.nvars, self.order)
        p.terms = terms
        return p

    def check_invariant(self) -> bool:
        """True when the terms are strictly decreasing in the order and all coefficients are nonzero."""
        ks = [self._key(a) for a, _ in self.terms]
        return all(c != 0 for _, c in self.terms) and all(ks[i] > ks[i + 1] for i in range(len(ks) - 1))

    def is_zero(self) -> bool:
        return not self.terms

    def leading_term(self) -> Term:
        """LT as (LM, LC). Cost: O(1). The zero polynomial has no leading term."""
        if not self.terms:
            raise ValueError("the zero polynomial has no leading term")
        return self.terms[0]

    def to_dict(self) -> dict[Mono, Any]:
        return dict(self.terms)

    def add(self, other: "SparsePolynomial") -> "SparsePolynomial":
        """Sum by a merge of two sorted lists. Cost: O(s + t) monomial comparisons and additions."""
        a, b, key = self.terms, other.terms, self._key
        i, j, out = 0, 0, []  # @line A1
        while i < len(a) and j < len(b):  # @line A2
            ka, kb = key(a[i][0]), key(b[j][0])
            if ka > kb:  # @line A3
                out.append(a[i])
                i += 1
            elif ka < kb:  # @line A4
                out.append(b[j])
                j += 1
            else:
                u = a[i][1] + b[j][1]  # @line A5
                if u != 0:  # @line A6
                    out.append((a[i][0], u))
                i += 1  # @line A7
                j += 1
        out.extend(a[i:])  # @line A8
        out.extend(b[j:])
        return self._new(out)

    def neg(self) -> "SparsePolynomial":
        return self._new([(a, -c) for a, c in self.terms])

    def sub(self, other: "SparsePolynomial") -> "SparsePolynomial":
        return self.add(other.neg())

    def mul_term(self, mono: Mono, coeff: Any) -> "SparsePolynomial":
        """Product with one term. The order is kept because a monomial order is compatible with products. Cost: O(t)."""
        if coeff == 0:
            return self._new([])
        out = [(_mono_mul(a, mono), c * coeff) for a, c in self.terms]
        return self._new([(a, c) for a, c in out if c != 0])

    def mul(self, other: "SparsePolynomial") -> "SparsePolynomial":
        """Product by Johnson's heap method. Cost: O(s t log s) monomial operations and s t ring operations, s <= t."""
        f, g = self.terms, other.terms
        if not f or not g:  # @line L1
            return self._new([])
        if len(f) > len(g):
            f, g = g, f
        key = self._key
        heap: list = []
        for i in range(len(f)):  # @line L2
            m = _mono_mul(f[i][0], g[0][0])
            heap.append((tuple(-x for x in key(m)), i, 0, m))
        heapq.heapify(heap)
        h: list[list] = []  # @line L3
        while heap:  # @line L4
            _, i, j, m = heapq.heappop(heap)  # @line L5
            c = f[i][1] * g[j][1]  # @line L6
            if h and h[-1][0] == m:  # @line L7
                h[-1][1] = h[-1][1] + c
            else:
                if h and h[-1][1] == 0:  # @line L8
                    h.pop()
                h.append([m, c])
            if j + 1 < len(g):  # @line L9
                m2 = _mono_mul(f[i][0], g[j + 1][0])
                heapq.heappush(heap, (tuple(-x for x in key(m2)), i, j + 1, m2))
        if h and h[-1][1] == 0:  # @line L10
            h.pop()
        return self._new([(m, c) for m, c in h])  # @line L11

    def evaluate(self, point: Iterable[Any]) -> Any:
        """Value at a point. Cost: O(t n log d) ring operations with fast powers."""
        pt = list(point)
        total = 0
        for a, c in self.terms:
            v = c
            for x, e in zip(pt, a):
                if e:
                    v = v * x**e
            total = total + v
        return total
