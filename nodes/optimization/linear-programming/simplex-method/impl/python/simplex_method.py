# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simplex-method/. The authors are listed in prov/1FHAJA.jsonl.

"""The primal simplex method on a dense tableau, in exact rational arithmetic.

The linear program is in standard form: minimize c^T x subject to A x = b and x >= 0,
where A has m rows and n columns. All numbers become fractions.Fraction, so ties in
the pivot rules and degenerate steps are decided exactly.
"""

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Sequence

Number = int | Fraction
RULES = ("dantzig", "bland", "steepest-edge")


@dataclass
class Result:
    """The outcome of a run.

    status is "optimal", "unbounded", "infeasible" or "cycle". For "optimal", x is an
    optimal basic feasible solution, value is c^T x, and y is a dual solution with
    A^T y <= c and b^T y = value. For "unbounded", x is the last vertex and ray is a
    direction d >= 0 with A d = 0 and c^T d < 0. pivots counts the pivots of phase two.
    """

    status: str
    x: list[Fraction] = field(default_factory=list)
    value: Fraction | None = None
    y: list[Fraction] = field(default_factory=list)
    basis: list[int] = field(default_factory=list)
    ray: list[Fraction] = field(default_factory=list)
    pivots: int = 0


class Tableau:
    """Row i holds B^-1 A | B^-1 b. The cost row r holds r_j = c_j - c_B^T B^-1 A_j and, last, -c_B^T B^-1 b."""

    def __init__(self, a: Sequence[Sequence[Number]], b: Sequence[Number], c: Sequence[Number], basis: Sequence[int]):
        self.m, self.n = len(a), len(c)
        self.t = [[Fraction(v) for v in row] + [Fraction(bi)] for row, bi in zip(a, b)]
        self.c = [Fraction(v) for v in c]
        self.basis = list(basis)
        if len(self.basis) != self.m or len(set(self.basis)) != self.m:
            raise ValueError("a basis needs m distinct columns")
        for i, j in enumerate(self.basis):
            p = next((k for k in range(i, self.m) if self.t[k][j] != 0), None)
            if p is None:
                raise ValueError("the basis columns are linearly dependent")
            self.t[i], self.t[p] = self.t[p], self.t[i]
            self._eliminate(i, j)
        self.r = self.c + [Fraction(0)]
        for i, j in enumerate(self.basis):
            f = self.r[j]
            if f:
                self.r = [rv - f * tv for rv, tv in zip(self.r, self.t[i])]

    def _eliminate(self, p: int, q: int) -> None:
        """Gauss-Jordan step: make column q the unit vector e_p in the rows."""
        piv = self.t[p][q]
        self.t[p] = [v / piv for v in self.t[p]]
        for i in range(self.m):
            if i != p and self.t[i][q] != 0:
                f = self.t[i][q]
                self.t[i] = [vi - f * vp for vi, vp in zip(self.t[i], self.t[p])]

    def pivot(self, p: int, q: int) -> None:
        """Column q enters the basis and the variable of row p leaves."""
        self._eliminate(p, q)
        f = self.r[q]
        if f:
            self.r = [rv - f * tv for rv, tv in zip(self.r, self.t[p])]
        self.basis[p] = q

    def x(self) -> list[Fraction]:
        x = [Fraction(0)] * self.n
        for i, j in enumerate(self.basis):
            x[j] = self.t[i][self.n]
        return x

    def entering(self, rule: str) -> int:
        """The entering column among those with a negative reduced cost (there is one)."""
        cand = [j for j in range(self.n) if self.r[j] < 0]
        if rule == "bland":
            return cand[0]
        if rule == "dantzig":
            return min(cand, key=lambda j: (self.r[j], j))
        # steepest edge: the edge of column j has squared length 1 + |B^-1 A_j|^2
        return max(cand, key=lambda j: (self.r[j] ** 2 / (1 + sum(row[j] ** 2 for row in self.t)), -j))

    def leaving(self, q: int) -> int:
        """The row chosen by the minimum ratio test (column q has a positive entry).

        Ties go to the row whose basic variable has the smallest index."""
        rows = [i for i in range(self.m) if self.t[i][q] > 0]
        return min(rows, key=lambda i: (self.t[i][self.n] / self.t[i][q], self.basis[i]))


def simplex_method(
    a: Sequence[Sequence[Number]],
    b: Sequence[Number],
    c: Sequence[Number],
    basis: Sequence[int],
    rule: str = "bland",
    max_pivots: int | None = None,
) -> Result:
    """Phase two of the simplex method from a feasible basis.

    Precondition: basis lists m columns of A that form a nonsingular matrix B with
    B^-1 b >= 0. Each pivot costs O(m n) operations on fractions. With rule "bland" the
    method always stops. With "dantzig" or "steepest-edge" it can cycle on a degenerate
    program; the run then stops with status "cycle" as soon as a basis repeats.
    """
    if rule not in RULES:
        raise ValueError(f"unknown rule {rule!r}")
    tab = Tableau(a, b, c, basis)
    if any(row[tab.n] < 0 for row in tab.t):
        raise ValueError("the starting basis is not feasible")
    seen = {tuple(sorted(tab.basis))}
    pivots = 0
    while True:  # @line L1
        reduced = tab.r[: tab.n]  # @line L2: each pivot keeps the cost row current
        if all(v >= 0 for v in reduced):  # @line L3
            x = tab.x()
            value = sum((cj * xj for cj, xj in zip(tab.c, x)), Fraction(0))
            y = dual_solution(a, c, tab.basis)
            return Result("optimal", x=x, value=value, y=y, basis=list(tab.basis), pivots=pivots)
        q = tab.entering(rule)  # @line L4
        d = [row[q] for row in tab.t]  # @line L5: d = B^-1 A_q
        if all(v <= 0 for v in d):  # @line L6
            ray = [Fraction(0)] * tab.n
            ray[q] = Fraction(1)
            for i, j in enumerate(tab.basis):
                ray[j] = -d[i]
            return Result("unbounded", x=tab.x(), basis=list(tab.basis), ray=ray, pivots=pivots)
        p = tab.leaving(q)  # @line L7
        tab.pivot(p, q)  # @line L8
        pivots += 1
        key = tuple(sorted(tab.basis))
        if (rule != "bland" and key in seen) or (max_pivots is not None and pivots >= max_pivots):
            return Result("cycle", x=tab.x(), basis=list(tab.basis), pivots=pivots)
        seen.add(key)


def dual_solution(a: Sequence[Sequence[Number]], c: Sequence[Number], basis: Sequence[int]) -> list[Fraction]:
    """A vector y with y^T A_j = c_j for each j in basis (rows of A may be redundant)."""
    m = len(a)
    rows = [[Fraction(a[i][j]) for i in range(m)] + [Fraction(c[j])] for j in basis]
    pivots, r = [], 0
    for col in range(m):
        p = next((k for k in range(r, len(rows)) if rows[k][col] != 0), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        pv = rows[r][col]
        rows[r] = [v / pv for v in rows[r]]
        for k in range(len(rows)):
            if k != r and rows[k][col] != 0:
                f = rows[k][col]
                rows[k] = [vk - f * vr for vk, vr in zip(rows[k], rows[r])]
        pivots.append(col)
        r += 1
    y = [Fraction(0)] * m
    for k, col in enumerate(pivots):
        y[col] = rows[k][m]
    return y


def solve(a: Sequence[Sequence[Number]], b: Sequence[Number], c: Sequence[Number], rule: str = "bland") -> Result:
    """Solve min c^T x, A x = b, x >= 0 from scratch, with a phase one for the start.

    Phase one minimizes the sum of m artificial variables by Bland's rule. Rows that it
    shows to be redundant are dropped, so A need not have full row rank.
    """
    m, n = len(a), len(c)
    rows = [[Fraction(v) for v in row] for row in a]
    rhs = [Fraction(v) for v in b]
    for i in range(m):
        if rhs[i] < 0:
            rows[i], rhs[i] = [-v for v in rows[i]], -rhs[i]
    aux = [row + [Fraction(int(k == i)) for k in range(m)] for i, row in enumerate(rows)]
    tab = Tableau(aux, rhs, [0] * n + [1] * m, list(range(n, n + m)))
    while any(v < 0 for v in tab.r[: n + m]):
        q = tab.entering("bland")
        tab.pivot(tab.leaving(q), q)
    if tab.r[n + m] != 0:  # the least sum of the artificials is -r[n+m] > 0
        return Result("infeasible")
    keep = []
    for i in range(m):
        if tab.basis[i] >= n:  # an artificial at level zero: pivot it out, or the row is redundant
            q = next((j for j in range(n) if tab.t[i][j] != 0), None)
            if q is None:
                continue
            tab.pivot(i, q)
        keep.append(i)
    res = simplex_method([tab.t[i][:n] for i in keep], [tab.t[i][n + m] for i in keep], c, [tab.basis[i] for i in keep], rule)
    if res.status == "optimal":
        res.y = dual_solution(a, c, res.basis)
    return res
