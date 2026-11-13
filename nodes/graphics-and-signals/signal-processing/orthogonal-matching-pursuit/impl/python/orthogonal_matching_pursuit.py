# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/orthogonal-matching-pursuit/. The authors are listed in prov/DHYVW6.jsonl.

"""Orthogonal matching pursuit (OMP) for y = A x with a sparse x.

At each step OMP picks the column that is most correlated with the residual,
then fits y by least squares on all the columns picked so far. The residual
is then orthogonal to every picked column, so no column is picked twice.

With int or Fraction entries every step is exact. The column score is
<a_j, r>^2 / ||a_j||^2, which is the squared normalised correlation without a
square root, and ties go to the smallest index.
"""

from fractions import Fraction
from typing import Optional


def _dot(u: list, v: list) -> Fraction:
    return sum((Fraction(a) * b for a, b in zip(u, v)), Fraction(0))


def solve(M: list[list], b: list) -> list[Fraction]:
    """Solve the square system M z = b by Gaussian elimination with exact pivots."""
    n = len(M)
    T = [[Fraction(v) for v in M[i]] + [Fraction(b[i])] for i in range(n)]
    for c in range(n):
        p = next((r for r in range(c, n) if T[r][c] != 0), None)
        if p is None:
            raise ZeroDivisionError("the chosen columns are linearly dependent")
        T[c], T[p] = T[p], T[c]
        for r in range(n):
            if r != c and T[r][c] != 0:
                f = T[r][c] / T[c][c]
                T[r] = [a - f * e for a, e in zip(T[r], T[c])]
    return [T[i][n] / T[i][i] for i in range(n)]


def least_squares(A: list[list], cols: list[int], y: list) -> list[Fraction]:
    """Coefficients z that minimise ||y - A[:, cols] z||, from the normal equations."""
    C = [[row[j] for row in A] for j in cols]
    G = [[_dot(ci, cj) for cj in C] for ci in C]
    return solve(G, [_dot(ci, y) for ci in C])


def omp(A: list[list], y: list, s: int, tol: Fraction = Fraction(0)) -> tuple[list[Fraction], list[int]]:
    """Run at most s steps of OMP. Returns (x, support in the order picked).

    The loop stops early when ||r||^2 <= tol (exact zero by default)."""
    m, n = len(A), len(A[0])
    cols = [[A[i][j] for i in range(m)] for j in range(n)]
    norms = [_dot(c, c) for c in cols]
    r = [Fraction(v) for v in y]  # @line L1
    support: list[int] = []
    z: list[Fraction] = []
    for _ in range(s):  # @line L2
        if _dot(r, r) <= tol:
            break
        best: Optional[int] = None
        best_score = Fraction(-1)
        for j in range(n):  # @line L3
            if j in support or norms[j] == 0:
                continue
            c = _dot(cols[j], r)
            score = c * c / norms[j]
            if score > best_score:
                best, best_score = j, score
        if best is None:
            break
        support.append(best)  # @line L4
        z = least_squares(A, support, y)  # @line L5
        r = [Fraction(y[i]) - sum((A[i][j] * zj for j, zj in zip(support, z)), Fraction(0)) for i in range(m)]  # @line L6
    x = [Fraction(0)] * n
    for j, zj in zip(support, z):
        x[j] = zj
    return x, support  # @line L7


def coherence_squared(A: list[list]) -> Fraction:
    """Exact mu(A)^2 = max over i != j of <a_i, a_j>^2 / (||a_i||^2 ||a_j||^2)."""
    m, n = len(A), len(A[0])
    cols = [[A[i][j] for i in range(m)] for j in range(n)]
    norms = [_dot(c, c) for c in cols]
    best = Fraction(0)
    for i in range(n):
        for j in range(i + 1, n):
            g = _dot(cols[i], cols[j])
            best = max(best, g * g / (norms[i] * norms[j]))
    return best
