# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/basis-pursuit/. The authors are listed in prov/M3TQK5.jsonl.

"""Basis pursuit: minimize ||x||_1 subject to A x = y, solved as a linear program.

Write x = u - v with u, v >= 0. Then basis pursuit is the linear program

    minimize sum(u) + sum(v)  subject to  A u - A v = y,  u >= 0, v >= 0,

which this module solves exactly over the rationals with a two-phase tableau
simplex method and Bland's rule (so it never cycles). Use Fraction or int
entries to get exact answers.
"""

from fractions import Fraction
from typing import Optional


def _pivot(T: list[list[Fraction]], basis: list[int], r: int, c: int) -> None:
    piv = T[r][c]
    T[r] = [v / piv for v in T[r]]
    for i in range(len(T)):
        if i != r and T[i][c] != 0:
            f = T[i][c]
            T[i] = [a - f * b for a, b in zip(T[i], T[r])]
    basis[r] = c


def _optimize(T: list[list[Fraction]], basis: list[int], cost: list[Fraction], allowed: int) -> None:
    """Primal simplex with Bland's rule on columns 0 .. allowed - 1."""
    while True:
        enter = -1
        for j in range(allowed):  # smallest index with a negative reduced cost
            if j in basis:
                continue
            rc = cost[j] - sum((cost[basis[i]] * T[i][j] for i in range(len(T))), Fraction(0))
            if rc < 0:
                enter = j
                break
        if enter < 0:
            return
        best, leave = None, -1
        for i in range(len(T)):
            if T[i][enter] > 0:
                ratio = T[i][-1] / T[i][enter]
                if best is None or ratio < best or (ratio == best and basis[i] < basis[leave]):
                    best, leave = ratio, i
        if leave < 0:
            raise ArithmeticError("the linear program is unbounded")
        _pivot(T, basis, leave, enter)


def linprog_eq(c: list, M: list[list], b: list) -> Optional[tuple[list[Fraction], Fraction]]:
    """Minimize c.z subject to M z = b, z >= 0. Returns (z, value), or None if infeasible."""
    m, N = len(M), len(c)
    T = []
    for i in range(m):
        row = [Fraction(v) for v in M[i]] + [Fraction(b[i])]
        if row[-1] < 0:
            row = [-v for v in row]
        T.append(row[:N] + [Fraction(int(k == i)) for k in range(m)] + [row[-1]])
    basis = [N + i for i in range(m)]
    phase1 = [Fraction(0)] * N + [Fraction(1)] * m
    _optimize(T, basis, phase1, N + m)  # @line L3
    if sum((T[i][-1] for i in range(m) if basis[i] >= N), Fraction(0)) != 0:
        return None
    for i in range(m):  # drive the artificial columns out of the basis
        if basis[i] >= N:
            j = next((j for j in range(N) if T[i][j] != 0 and j not in basis), -1)
            if j >= 0:
                _pivot(T, basis, i, j)
    keep = [i for i in range(m) if basis[i] < N]  # rows left with artificials are redundant
    T = [T[i] for i in keep]
    basis = [basis[i] for i in keep]
    cost = [Fraction(v) for v in c] + [Fraction(0)] * m
    _optimize(T, basis, cost, N)  # @line L4
    z = [Fraction(0)] * N
    for i, j in enumerate(basis):
        z[j] = T[i][-1]
    return z, sum((Fraction(c[j]) * z[j] for j in range(N)), Fraction(0))


def basis_pursuit(A: list[list], y: list) -> Optional[list[Fraction]]:
    """Return a minimizer of ||x||_1 subject to A x = y (a vertex of the LP), or None if A x = y has no solution."""
    n = len(A[0])
    M = [list(row) + [-v for v in row] for row in A]  # @line L1
    c = [1] * (2 * n)  # @line L2
    res = linprog_eq(c, M, y)
    if res is None:
        return None
    z, _ = res
    return [z[j] - z[n + j] for j in range(n)]  # @line L5
