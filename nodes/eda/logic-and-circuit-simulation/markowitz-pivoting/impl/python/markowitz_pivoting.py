# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/markowitz-pivoting/. The authors are listed in prov/RPNJK6.jsonl.
"""Sparse LU factorization with Markowitz pivoting and a threshold test.

The input is a square matrix as a list of rows; a zero entry is a structural
zero. Entries are Fraction (exact) or float. At each step the pivot is the
active entry a_ij that passes the threshold test |a_ij| >= u * max_k |a_kj|
(the largest entry of its active column) and has the least Markowitz count
(r_i - 1)(c_j - 1), where r_i and c_j count the nonzeros of row i and column
j in the active submatrix. Ties go to the larger |a_ij|, then to the smaller
row and column index.

An entry that becomes zero by cancellation is kept as a stored zero, so the
pattern of the factors is the structural pattern and the fill counts are
structural counts.

markowitz_lu returns a Factor with:
- prow[k], pcol[k]: the row and the column of A that hold pivot k, so
  P A Q = L U with (P A Q)[k][m] = A[prow[k]][pcol[m]];
- lower[k]: a dict {i: l_ik} over the rows i of A eliminated later (unit
  diagonal not stored);
- upper[k]: a dict {j: u_kj} over the columns j of A, including the pivot;
- steps[k]: (count, fill) of step k, the Markowitz count of the chosen pivot
  and the number of new nonzeros that step created.
"""

from dataclasses import dataclass, field


class SingularMatrixError(ValueError):
    """An active column has no nonzero entry, so A is singular."""


@dataclass
class Factor:
    n: int
    prow: list = field(default_factory=list)
    pcol: list = field(default_factory=list)
    lower: list = field(default_factory=list)
    upper: list = field(default_factory=list)
    steps: list = field(default_factory=list)

    @property
    def fill(self):
        return sum(f for _, f in self.steps)


def markowitz_lu(a, u=1, tol=0):
    """Factor the square matrix a (a list of rows) with Markowitz pivoting.

    u is the threshold, 0 < u <= 1. tol is the magnitude at or below which a
    column maximum counts as zero (0 for exact Fraction input).
    """
    n = len(a)
    rows = {i: {j: v for j, v in enumerate(a[i]) if v != 0} for i in range(n)}  # @line L1
    cols = {j: set() for j in range(n)}
    for i, r in rows.items():
        for j in r:
            cols[j].add(i)
    f = Factor(n)
    for _ in range(n):  # @line L2
        best = None
        for j, cj in cols.items():  # @line L3
            m = max((abs(rows[i][j]) for i in cj), default=0)
            if m <= tol:
                raise SingularMatrixError(f"column {j} has no usable pivot")
            for i in cj:  # @line L4
                v = rows[i][j]
                if abs(v) >= u * m:
                    key = ((len(rows[i]) - 1) * (len(cj) - 1), -abs(v), i, j)
                    if best is None or key < best:
                        best = key
        count, _, p, q = best
        piv = rows[p][q]
        prow = rows.pop(p)  # @line L5
        f.prow.append(p)
        f.pcol.append(q)
        f.upper.append(dict(prow))
        low, made = {}, 0
        for i in cols[q] - {p}:  # @line L6
            ri = rows[i]
            l = ri.pop(q) / piv  # @line L7
            low[i] = l
            for j, v in prow.items():  # @line L8
                if j == q:
                    continue
                if j in ri:
                    ri[j] -= l * v  # @line L9
                else:
                    ri[j] = -l * v
                    cols[j].add(i)
                    made += 1
        for j in prow:  # @line L10
            cols[j].discard(p)
        del cols[q]
        f.lower.append(low)
        f.steps.append((count, made))
    return f  # @line L11


def lu_solve(f, b):
    """Solve A x = b with the factors of markowitz_lu."""
    n = f.n
    pos = {r: k for k, r in enumerate(f.prow)}
    y = [None] * n
    for k in range(n):  # forward: L y = P b, column by column
        s = b[f.prow[k]] if y[k] is None else b[f.prow[k]] - y[k]
        y[k] = s
        for i, l in f.lower[k].items():
            m = pos[i]
            y[m] = (0 if y[m] is None else y[m]) + l * s
    x = [0] * n
    for k in range(n - 1, -1, -1):  # backward: U z = y, x = Q z
        s = y[k]
        for j, v in f.upper[k].items():
            if j != f.pcol[k]:
                s -= v * x[j]
        x[f.pcol[k]] = s / f.upper[k][f.pcol[k]]
    return x


def markowitz_solve(a, b, u=1, tol=0):
    return lu_solve(markowitz_lu(a, u, tol), b)
