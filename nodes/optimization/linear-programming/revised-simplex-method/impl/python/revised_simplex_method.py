# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/revised-simplex-method/. The authors are listed in prov/0XTBN3.jsonl.

"""The revised simplex method with an explicit basis inverse, in exact rational arithmetic.

Solve: minimize c^T x subject to A x = b and x >= 0, from a given feasible basis. The
method never forms the full tableau B^-1 A. It keeps the m x m matrix B^-1 and updates it
after each pivot with one elementary (eta) matrix. Each iteration computes only the
multipliers y, the reduced costs, and the one column B^-1 A_q that the ratio test needs.
"""

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Callable, Sequence

Number = int | Fraction


@dataclass
class Result:
    """status is "optimal", "unbounded" or "cycle" (a basis repeated under Dantzig's rule).

    optimal: x, value = c^T x, and y = c_B^T B^-1 with A^T y <= c and b^T y = value.
    unbounded: the last vertex x and a ray d >= 0 with A d = 0 and c^T d < 0.
    """

    status: str
    x: list[Fraction] = field(default_factory=list)
    value: Fraction | None = None
    y: list[Fraction] = field(default_factory=list)
    ray: list[Fraction] = field(default_factory=list)
    basis: list[int] = field(default_factory=list)
    pivots: int = 0


def inverse(mat: list[list[Fraction]]) -> list[list[Fraction]]:
    """Gauss-Jordan inverse of a nonsingular square matrix."""
    k = len(mat)
    rows = [list(mat[i]) + [Fraction(int(j == i)) for j in range(k)] for i in range(k)]
    for col in range(k):
        p = next((i for i in range(col, k) if rows[i][col] != 0), None)
        if p is None:
            raise ValueError("the basis columns are linearly dependent")
        rows[col], rows[p] = rows[p], rows[col]
        pv = rows[col][col]
        rows[col] = [v / pv for v in rows[col]]
        for i in range(k):
            if i != col and rows[i][col] != 0:
                f = rows[i][col]
                rows[i] = [vi - f * vc for vi, vc in zip(rows[i], rows[col])]
    return [row[k:] for row in rows]


def revised_simplex_method(
    a: Sequence[Sequence[Number]],
    b: Sequence[Number],
    c: Sequence[Number],
    basis: Sequence[int],
    rule: str = "bland",
    on_pivot: Callable[[list[int], list[list[Fraction]]], None] | None = None,
) -> Result:
    """Phase two from a feasible basis. rule is "bland" or "dantzig".

    One iteration costs O(m^2 + m n) operations: O(m^2) for y, d and the update of B^-1,
    and O(m n) for the reduced costs. on_pivot(basis, binv) is called after each update.
    """
    m, n = len(a), len(c)
    A = [[Fraction(v) for v in row] for row in a]
    cc = [Fraction(v) for v in c]
    basis = list(basis)
    binv = inverse([[A[i][j] for j in basis] for i in range(m)])  # @line L1
    xb = [sum((binv[i][k] * b[k] for k in range(m)), Fraction(0)) for i in range(m)]
    if any(v < 0 for v in xb):
        raise ValueError("the starting basis is not feasible")
    seen, pivots = {tuple(sorted(basis))}, 0
    while True:  # @line L2
        y = [sum((cc[basis[i]] * binv[i][k] for i in range(m)), Fraction(0)) for k in range(m)]  # @line L3: y^T = c_B^T B^-1
        inb = set(basis)
        r = {j: cc[j] - sum((y[k] * A[k][j] for k in range(m)), Fraction(0)) for j in range(n) if j not in inb}  # @line L4
        cand = [j for j in sorted(r) if r[j] < 0]
        if not cand:
            x = _point(xb, basis, n)
            value = sum((cj * xj for cj, xj in zip(cc, x)), Fraction(0))
            return Result("optimal", x=x, value=value, y=y, basis=basis, pivots=pivots)
        q = cand[0] if rule == "bland" else min(cand, key=lambda j: (r[j], j))  # @line L5
        d = [sum((binv[i][k] * A[k][q] for k in range(m)), Fraction(0)) for i in range(m)]  # @line L6: d = B^-1 A_q
        if all(v <= 0 for v in d):
            ray = [Fraction(0)] * n
            ray[q] = Fraction(1)
            for i, j in enumerate(basis):
                ray[j] = -d[i]
            return Result("unbounded", x=_point(xb, basis, n), ray=ray, basis=basis, pivots=pivots)
        p = min((i for i in range(m) if d[i] > 0), key=lambda i: (xb[i] / d[i], basis[i]))  # @line L7
        theta = xb[p] / d[p]
        xb = [xb[i] - theta * d[i] for i in range(m)]  # @line L8
        xb[p] = theta
        basis[p] = q
        # @line L9: B^-1 <- E B^-1, where E is the identity with column p replaced by the eta vector
        rowp = [v / d[p] for v in binv[p]]
        binv = [rowp if i == p else [vi - d[i] * vp for vi, vp in zip(binv[i], rowp)] for i in range(m)]
        pivots += 1
        if on_pivot is not None:
            on_pivot(list(basis), binv)
        key = tuple(sorted(basis))
        if rule != "bland" and key in seen:
            return Result("cycle", x=_point(xb, basis, n), basis=basis, pivots=pivots)
        seen.add(key)


def _point(xb: list[Fraction], basis: list[int], n: int) -> list[Fraction]:
    x = [Fraction(0)] * n
    for i, j in enumerate(basis):
        x[j] = xb[i]
    return x
