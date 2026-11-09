# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kkt-conditions/. The authors are listed in prov/MERSHB.jsonl.

"""Exact KKT solver for small strictly convex quadratic programs.

Problem: minimize 1/2 x^T Q x + c^T x subject to A x <= b,
with Q symmetric positive definite. All numbers are Fractions.

For a strictly convex QP the KKT conditions are necessary and sufficient,
and the optimal x is unique. The solver guesses the active set S, solves
the linear KKT system for that guess, and accepts the first guess whose
solution is primal feasible and has nonnegative multipliers.
"""

from fractions import Fraction
from itertools import combinations

Matrix = list[list[Fraction]]
Vector = list[Fraction]


def solve_linear(M: Matrix, r: Vector) -> Vector | None:
    """Solve M z = r exactly by Gaussian elimination. Return None if M is singular."""
    n = len(M)
    a = [list(map(Fraction, row)) + [Fraction(r[i])] for i, row in enumerate(M)]
    for col in range(n):
        piv = next((i for i in range(col, n) if a[i][col] != 0), None)
        if piv is None:
            return None
        a[col], a[piv] = a[piv], a[col]
        for i in range(n):
            if i != col and a[i][col] != 0:
                f = a[i][col] / a[col][col]
                a[i] = [x - f * y for x, y in zip(a[i], a[col])]
    return [a[i][n] / a[i][i] for i in range(n)]


def kkt_violation(Q: Matrix, c: Vector, A: Matrix, b: Vector, x: Vector, lam: Vector) -> Fraction:
    """Largest violation of the four KKT conditions at (x, lam). It is 0 exactly at a KKT point."""
    n, m = len(c), len(b)
    grad = [sum((Q[i][j] * x[j] for j in range(n)), Fraction(0)) + c[i] + sum((A[k][i] * lam[k] for k in range(m)), Fraction(0)) for i in range(n)]
    slack = [b[k] - sum((A[k][j] * x[j] for j in range(n)), Fraction(0)) for k in range(m)]
    worst = Fraction(0)
    for g in grad:  # stationarity
        worst = max(worst, abs(g))
    for k in range(m):
        worst = max(worst, -slack[k])  # primal feasibility
        worst = max(worst, -lam[k])  # dual feasibility
        worst = max(worst, abs(lam[k] * slack[k]))  # complementary slackness
    return worst


def solve_qp_kkt(Q: Matrix, c: Vector, A: Matrix, b: Vector) -> tuple[Vector, Vector] | None:
    """Return (x, lam) satisfying the KKT conditions, or None if the QP is infeasible."""
    n, m = len(c), len(b)
    for size in range(0, min(n, m) + 1):
        for S in combinations(range(m), size):
            # KKT system for active set S:  [Q  A_S^T] [x  ]   [-c ]
            #                               [A_S  0  ] [l_S] = [b_S]
            M = [[Fraction(Q[i][j]) for j in range(n)] + [Fraction(A[k][i]) for k in S] for i in range(n)]
            M += [[Fraction(A[k][j]) for j in range(n)] + [Fraction(0)] * size for k in S]
            r = [-Fraction(ci) for ci in c] + [Fraction(b[k]) for k in S]
            z = solve_linear(M, r)
            if z is None:
                continue
            x, lS = z[:n], z[n:]
            if any(v < 0 for v in lS):
                continue
            if any(sum((A[k][j] * x[j] for j in range(n)), Fraction(0)) > b[k] for k in range(m)):
                continue
            lam = [Fraction(0)] * m
            for k, v in zip(S, lS):
                lam[k] = v
            return x, lam
    return None
