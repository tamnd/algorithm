# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dual-simplex-method/. The authors are listed in prov/M8KGT9.jsonl.

"""The dual simplex method on a dense tableau, in exact rational arithmetic.

Solve: minimize c^T x subject to A x = b and x >= 0, from a basis that is dual
feasible (all reduced costs r_j >= 0) but whose basic solution may have negative
entries. Each pivot keeps r >= 0 and removes one negative basic variable from the basis.
"""

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Sequence

Number = int | Fraction
RULES = ("most-negative", "least-index")


@dataclass
class Result:
    """status is "optimal", "infeasible" or "cycle".

    optimal: x, value = c^T x and y with A^T y <= c and b^T y = value.
    infeasible: farkas, a vector z with A^T z <= 0 and b^T z > 0.
    y is the dual solution of the last basis; b^T y never decreases from pivot to pivot.
    """

    status: str
    x: list[Fraction] = field(default_factory=list)
    value: Fraction | None = None
    y: list[Fraction] = field(default_factory=list)
    farkas: list[Fraction] = field(default_factory=list)
    basis: list[int] = field(default_factory=list)
    pivots: int = 0
    dual_values: list[Fraction] = field(default_factory=list)


def dual_simplex_method(
    a: Sequence[Sequence[Number]],
    b: Sequence[Number],
    c: Sequence[Number],
    basis: Sequence[int],
    rule: str = "least-index",
) -> Result:
    """Each pivot costs O(m (n + m)) operations on fractions.

    The tableau carries B^-1 next to B^-1 A, so the certificates come out directly.
    rule "least-index" takes the leaving row whose basic variable has the least index; rule
    "most-negative" takes the most negative basic variable and can cycle (status "cycle").
    """
    if rule not in RULES:
        raise ValueError(f"unknown rule {rule!r}")
    m, n = len(a), len(c)
    cc = [Fraction(v) for v in c]
    # row i: (B^-1 A)_i | (B^-1)_i | (B^-1 b)_i
    t = [[Fraction(v) for v in a[i]] + [Fraction(int(k == i)) for k in range(m)] + [Fraction(b[i])] for i in range(m)]
    basis = list(basis)
    for i, j in enumerate(basis):  # bring the basis columns to unit vectors
        p = next((k for k in range(i, m) if t[k][j] != 0), None)
        if p is None:
            raise ValueError("the basis columns are linearly dependent")
        t[i], t[p] = t[p], t[i]
        _pivot(t, i, j)
    seen, pivots, dual_values = {tuple(sorted(basis))}, 0, []
    while True:  # @line L1
        y = [sum((cc[basis[i]] * t[i][n + k] for i in range(m)), Fraction(0)) for k in range(m)]  # @line L2
        r = [cc[j] - sum((y[k] * a[k][j] for k in range(m)), Fraction(0)) for j in range(n)]
        if any(v < 0 for v in r):
            raise ValueError("the basis is not dual feasible")
        dual_values.append(sum((Fraction(bk) * yk for bk, yk in zip(b, y)), Fraction(0)))
        neg = [i for i in range(m) if t[i][-1] < 0]
        if not neg:  # @line L3: x_B >= 0, so the basis is also primal feasible
            x = [Fraction(0)] * n
            for i, j in enumerate(basis):
                x[j] = t[i][-1]
            value = sum((cj * xj for cj, xj in zip(cc, x)), Fraction(0))
            return Result("optimal", x=x, value=value, y=y, basis=basis, pivots=pivots, dual_values=dual_values)
        if rule == "least-index":  # @line L4: the leaving row
            p = min(neg, key=lambda i: basis[i])
        else:
            p = min(neg, key=lambda i: (t[i][-1], basis[i]))
        alpha = t[p][:n]  # @line L5: row p of B^-1 A
        cols = [j for j in range(n) if alpha[j] < 0]
        if not cols:  # @line L6: row p reads alpha x = x_B(p) < 0 with alpha >= 0
            z = [-v for v in t[p][n : n + m]]
            return Result("infeasible", farkas=z, y=y, basis=basis, pivots=pivots, dual_values=dual_values)
        q = min(cols, key=lambda j: (r[j] / -alpha[j], j))  # @line L7: the dual ratio test
        _pivot(t, p, q)  # @line L8
        basis[p] = q
        pivots += 1
        key = tuple(sorted(basis))
        if key in seen:
            return Result("cycle", basis=basis, pivots=pivots, dual_values=dual_values)
        seen.add(key)


def _pivot(t: list[list[Fraction]], p: int, q: int) -> None:
    piv = t[p][q]
    t[p] = [v / piv for v in t[p]]
    for i in range(len(t)):
        if i != p and t[i][q] != 0:
            f = t[i][q]
            t[i] = [vi - f * vp for vi, vp in zip(t[i], t[p])]
