# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gomory-cutting-plane-algorithm/. The authors are listed in prov/BP9Q4E.jsonl.

"""Gomory's fractional cutting-plane algorithm for pure integer programs.

The problem is max c^T x subject to A x <= b, x >= 0, x integer, with
integer data A, b, c. The algorithm solves the LP relaxation with an exact
simplex method (fractions.Fraction), takes the lexicographically largest
optimal vertex of (c^T x, x_1, ..., x_n), and adds the Gomory fractional cut
of the first fractional component. It stops when the LP vertex is integral
or the LP is infeasible.

Precondition: the polytope {x >= 0 : A x <= b} is bounded. Under it the
method stops after finitely many rounds (Gomory 1958). There is no
polynomial bound on the number of rounds.
"""

from dataclasses import dataclass, field
from fractions import Fraction
from math import floor

Vector = list[Fraction]


@dataclass
class Result:
    status: str  # "optimal" or "infeasible"
    x: list[int] | None = None
    value: int | None = None
    cuts: list[tuple[list[int], int]] = field(default_factory=list)
    points: list[Vector] = field(default_factory=list)  # LP vertex of each round


class _Tableau:
    """Rows x_B[r] = T[r][-1] - sum_h T[r][h] x_h over the nonbasic x_h."""

    def __init__(self, A: list[list[int]], b: list[int]) -> None:
        m, n = len(A), len(A[0])
        self.n, self.nv = n, n + m
        self.T = [[Fraction(v) for v in A[r]] + [Fraction(int(r == k)) for k in range(m)] + [Fraction(b[r])] for r in range(m)]
        self.basis = [n + r for r in range(m)]

    def pivot(self, r: int, e: int) -> None:
        T = self.T
        p = T[r][e]
        T[r] = [v / p for v in T[r]]
        for i in range(len(T)):
            if i != r and T[i][e] != 0:
                f = T[i][e]
                T[i] = [a - f * c for a, c in zip(T[i], T[r])]
        self.basis[r] = e

    def reduced(self, w: dict[int, Fraction]) -> tuple[Fraction, dict[int, Fraction]]:
        """Write sum_v w_v x_v as d0 - sum_h d_h x_h over the nonbasic x_h."""
        nb = [h for h in range(self.nv) if h not in self.basis]
        d0 = sum((w.get(self.basis[r], 0) * self.T[r][-1] for r in range(len(self.T))), Fraction(0))
        d = {h: sum((w.get(self.basis[r], 0) * self.T[r][h] for r in range(len(self.T))), Fraction(0)) - w.get(h, 0) for h in nb}
        return d0, d

    def maximize(self, w: dict[int, Fraction], allowed) -> None:
        """Primal simplex with Bland's rule; enter only columns in allowed(h)."""
        while True:
            _, d = self.reduced(w)
            enter = [h for h in sorted(d) if d[h] < 0 and allowed(h)]
            if not enter:
                return
            e = enter[0]
            rows = [r for r in range(len(self.T)) if self.T[r][e] > 0]
            if not rows:
                raise ValueError("the LP relaxation is unbounded")
            r = min(rows, key=lambda i: (self.T[i][-1] / self.T[i][e], self.basis[i]))
            self.pivot(r, e)

    def value(self, v: int) -> Fraction:
        return self.T[self.basis.index(v)][-1] if v in self.basis else Fraction(0)


def _phase_one(tab: _Tableau) -> bool:
    """Make the tableau primal feasible. Return False if the LP is infeasible."""
    T = tab.T
    if all(row[-1] >= 0 for row in T):
        return True
    a = tab.nv  # artificial variable, column -1 in each row
    for row in T:
        row.insert(a, Fraction(-1))
    tab.nv += 1
    r = min(range(len(T)), key=lambda i: T[i][-1])
    tab.pivot(r, a)
    tab.maximize({a: Fraction(-1)}, lambda h: True)
    if tab.value(a) > 0:
        return False
    if a in tab.basis:
        r = tab.basis.index(a)
        e = next((h for h in range(a) if T[r][h] != 0), None)
        if e is None:
            del T[r], tab.basis[r]
        else:
            tab.pivot(r, e)
    for row in T:
        del row[a]
    tab.nv -= 1
    return True


def lex_max_lp(A: list[list[int]], b: list[int], c: list[int]):
    """Lexicographically maximize (c^T x, x_1, ..., x_n) over {x >= 0 : Ax <= b}.

    Return None if the LP is infeasible, else (v, rows): v is the vector of
    the components at the optimal vertex, and rows[k] maps each nonbasic
    column h to d_h, where component k = v[k] - sum_h d_h t_h.
    """
    tab = _Tableau(A, b)
    if not _phase_one(tab):
        return None
    n = len(c)
    comps = [{j: Fraction(c[j]) for j in range(n)}] + [{j: Fraction(1)} for j in range(n)]
    fixed: set[int] = set()  # nonbasic columns with a positive reduced cost in an earlier stage
    for w in comps:
        tab.maximize(w, lambda h: h not in fixed)
        _, d = tab.reduced(w)
        fixed |= {h for h, dh in d.items() if dh > 0}
    v, rows = [], []
    for w in comps:
        d0, d = tab.reduced(w)
        v.append(d0)
        rows.append(d)
    return v, rows


def frac(q: Fraction) -> Fraction:
    return q - floor(q)


def gomory(A: list[list[int]], b: list[int], c: list[int], max_rounds: int = 100000) -> Result:
    """Solve max c^T x, A x <= b, x >= 0, x integer, with Gomory's fractional cuts.

    A, b, c are integer. The LP relaxation must be bounded. Each round costs
    one exact LP solve. The cuts are returned in the original variables.
    """
    A = [list(row) for row in A]
    b = list(b)
    n = len(c)
    res = Result(status="infeasible")
    for _ in range(max_rounds):  # @line L1
        sol = lex_max_lp(A, b, c)  # @line L2
        if sol is None:  # @line L3
            return res
        v, rows = sol
        res.points.append(v[1:])  # @line L4: v = (c^T x, x_1, ..., x_n)
        if all(q.denominator == 1 for q in v):  # @line L5
            res.status, res.x, res.value = "optimal", [int(q) for q in v[1:]], int(v[0])
            return res
        j = next(k for k in range(n + 1) if v[k].denominator != 1)  # @line L6
        d = rows[j]
        # @line L7: the cut sum_h frac(d_h) t_h >= frac(v_j), written in CG form
        # component_j + sum_h floor(d_h) t_h <= floor(v_j)
        g = [Fraction(c[k]) for k in range(n)] if j == 0 else [Fraction(int(k == j - 1)) for k in range(n)]
        g0 = Fraction(floor(v[j]))
        for h, dh in d.items():
            q = floor(dh)
            if h < n:  # @line L8: t_h is an original variable
                g[h] += q
            else:  # t_h is the slack b_r - A_r x of row r
                r = h - n
                g = [g[k] - q * A[r][k] for k in range(n)]
                g0 -= q * b[r]
        cut = [int(gk) for gk in g]
        A.append(cut)
        b.append(int(g0))
        res.cuts.append((cut, int(g0)))
    raise RuntimeError("round limit reached")
