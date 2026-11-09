# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-phase-simplex-method/. The authors are listed in prov/AJZNEC.jsonl.

"""The two-phase simplex method in exact rational arithmetic.

Solve: minimize c^T x subject to A x = b and x >= 0, with no starting basis given and no
assumption on the rank of A. Phase one minimizes the sum of artificial variables. Phase
two starts from the basis that phase one leaves. Both phases use Bland's rule.
"""

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Sequence

Number = int | Fraction


@dataclass
class Result:
    """status is "optimal", "unbounded" or "infeasible".

    optimal: x, value = c^T x, and y with A^T y <= c and b^T y = value.
    unbounded: a feasible x and a ray d >= 0 with A d = 0 and c^T d < 0.
    infeasible: farkas, a vector y with A^T y <= 0 and b^T y > 0.
    basis lists the final basic columns, and rows the rows of A that phase one kept.
    """

    status: str
    x: list[Fraction] = field(default_factory=list)
    value: Fraction | None = None
    y: list[Fraction] = field(default_factory=list)
    ray: list[Fraction] = field(default_factory=list)
    farkas: list[Fraction] = field(default_factory=list)
    basis: list[int] = field(default_factory=list)
    rows: list[int] = field(default_factory=list)
    phase1_pivots: int = 0
    phase2_pivots: int = 0


def _pivot(t: list[list[Fraction]], r: list[Fraction], p: int, q: int) -> None:
    """One Gauss-Jordan pivot on entry (p, q) of the tableau rows t and the cost row r."""
    piv = t[p][q]
    t[p] = [v / piv for v in t[p]]
    for i in range(len(t)):
        if i != p and t[i][q] != 0:
            f = t[i][q]
            t[i] = [vi - f * vp for vi, vp in zip(t[i], t[p])]
    if r[q] != 0:
        f = r[q]
        r[:] = [rv - f * vp for rv, vp in zip(r, t[p])]


def _bland(t: list[list[Fraction]], r: list[Fraction], basis: list[int], cols: int) -> tuple[str, int]:
    """Run the simplex method with Bland's rule on columns 0..cols-1. Return the status and the pivot count."""
    pivots = 0
    while True:
        q = next((j for j in range(cols) if r[j] < 0), None)
        if q is None:
            return "optimal", pivots
        rows = [i for i in range(len(t)) if t[i][q] > 0]
        if not rows:
            return "unbounded", pivots
        p = min(rows, key=lambda i: (t[i][-1] / t[i][q], basis[i]))
        _pivot(t, r, p, q)
        basis[p] = q
        pivots += 1


def two_phase_simplex_method(a: Sequence[Sequence[Number]], b: Sequence[Number], c: Sequence[Number]) -> Result:
    """Solve min c^T x, A x = b, x >= 0. Each pivot costs O(m (n + m)) operations on fractions."""
    m, n = len(a), len(c)
    t = [[Fraction(v) for v in row] + [Fraction(int(k == i)) for k in range(m)] + [Fraction(bi)] for i, (row, bi) in enumerate(zip(a, b))]
    sign = [1] * m
    for i in range(m):  # @line L1
        if t[i][-1] < 0:
            t[i] = [-v for v in t[i]]
            t[i][n + i] = Fraction(1)
            sign[i] = -1
    basis = list(range(n, n + m))  # @line L2: the artificial columns form an identity
    r = [Fraction(0)] * n + [Fraction(1)] * m + [Fraction(0)]
    for i in range(m):  # price out the artificial basis: r = w - 1^T rows
        r = [rv - tv for rv, tv in zip(r, t[i])]
    _, piv1 = _bland(t, r, basis, n + m)  # @line L3
    if r[-1] != 0:  # @line L4: the least sum of artificials is -r[-1] > 0
        # the artificial reduced costs are 1 - z_i, where z_i is the dual of row i (sign-adjusted)
        z = [(1 - r[n + i]) * sign[i] for i in range(m)]
        return Result("infeasible", farkas=z, phase1_pivots=piv1)
    keep, dropped = [], []
    for i in range(m):
        if basis[i] >= n:  # @line L5: an artificial stays basic at level zero
            q = next((j for j in range(n) if t[i][j] != 0), None)
            if q is not None:
                _pivot(t, r, i, q)  # @line L6
                basis[i] = q
            else:
                dropped.append(basis[i] - n)  # @line L7: original row basis[i] - n is redundant
                continue
        keep.append(i)
    t = [t[i][:n] + [t[i][-1]] for i in keep]  # @line L8: drop the artificial columns
    basis = [basis[i] for i in keep]
    kept_rows = [k for k in range(m) if k not in dropped]
    cost = [Fraction(v) for v in c]
    r = cost + [Fraction(0)]
    for i, j in enumerate(basis):
        if r[j] != 0:
            f = r[j]
            r = [rv - f * tv for rv, tv in zip(r, t[i])]
    status, piv2 = _bland(t, r, basis, n)  # @line L9
    x = [Fraction(0)] * n
    for i, j in enumerate(basis):
        x[j] = t[i][-1]
    res = Result(status, x=x, basis=basis, rows=kept_rows, phase1_pivots=piv1, phase2_pivots=piv2)
    if status == "optimal":
        res.value = sum((cj * xj for cj, xj in zip(cost, x)), Fraction(0))
        res.y = _dual(a, cost, basis, kept_rows)
    else:
        q = next(j for j in range(n) if r[j] < 0 and all(row[j] <= 0 for row in t))
        res.ray = [Fraction(0)] * n
        res.ray[q] = Fraction(1)
        for i, j in enumerate(basis):
            res.ray[j] = -t[i][q]
    return res


def _dual(a: Sequence[Sequence[Number]], cost: list[Fraction], basis: list[int], keep: list[int]) -> list[Fraction]:
    """Solve y^T A_B = c_B on the kept rows; the dropped rows get y_i = 0."""
    k = len(keep)
    rows = [[Fraction(a[i][j]) for i in keep] + [cost[j]] for j in basis]
    for col in range(k):
        p = next(i for i in range(col, k) if rows[i][col] != 0)
        rows[col], rows[p] = rows[p], rows[col]
        pv = rows[col][col]
        rows[col] = [v / pv for v in rows[col]]
        for i in range(k):
            if i != col and rows[i][col] != 0:
                f = rows[i][col]
                rows[i] = [vi - f * vc for vi, vc in zip(rows[i], rows[col])]
    y = [Fraction(0)] * len(a)
    for idx, i in enumerate(keep):
        y[i] = rows[idx][k]
    return y
