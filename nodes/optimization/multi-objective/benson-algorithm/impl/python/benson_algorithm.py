# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/benson-algorithm/. The authors are listed in prov/V38187.jsonl.

"""Benson's outer approximation algorithm for multi-objective linear programs.

All objectives are minimized. The problem is

    minimize C x  subject to  x in X = {x in R^n : A x >= b},

with p objectives (the rows of C). X must be nonempty and each objective must
be bounded below on X. The algorithm computes the upper image
P = C[X] + R^p_+ by cutting an outer approximation T, which starts as the
ideal point plus R^p_+. For each vertex t of T it solves the linear program

    D2(t):  maximize b^T v - t^T u
            subject to A^T v = C^T u,  sum(u) = 1,  u >= 0,  v >= 0.

Its value is the least z with t + z (1, ..., 1) in P. If the value is
positive, an optimal (u, v) gives the supporting half-space u^T y >= b^T v
of P, which cuts t off. When no vertex is cut off, T = P.

All arithmetic is exact, with Fraction. The vertices of T are found by brute
force over all p-subsets of the inequalities, so the code is meant for small
instances.
"""

from fractions import Fraction
from itertools import combinations
from typing import List, Optional, Sequence, Tuple

Fr = Fraction
Vec = Tuple[Fraction, ...]


# ---------------------------------------------------------------------------
# A two-phase simplex method with Bland's rule, in exact arithmetic.


def _solve_tableau(T, basis, cost, allowed) -> str:
    """Maximize cost^T w on the tableau, entering only allowed columns."""
    ncol = len(T[0]) - 1
    while True:
        enter = -1
        for j in range(ncol):
            if not allowed[j] or j in basis:
                continue
            d = cost[j] - sum(cost[basis[i]] * T[i][j] for i in range(len(T)))
            if d > 0:
                enter = j
                break
        if enter < 0:
            return "optimal"
        leave, best = -1, None
        for i in range(len(T)):
            if T[i][enter] > 0:
                ratio = T[i][-1] / T[i][enter]
                if best is None or ratio < best or (ratio == best and basis[i] < basis[leave]):
                    leave, best = i, ratio
        if leave < 0:
            return "unbounded"
        _pivot(T, basis, leave, enter)


def _pivot(T, basis, r, c) -> None:
    piv = T[r][c]
    T[r] = [x / piv for x in T[r]]
    for i in range(len(T)):
        if i != r and T[i][c] != 0:
            f = T[i][c]
            T[i] = [x - f * y for x, y in zip(T[i], T[r])]
    basis[r] = c


def simplex_max(M: Sequence[Sequence], r: Sequence, c: Sequence):
    """Maximize c^T w subject to M w = r and w >= 0.

    Return ("optimal", value, w), ("infeasible", None, None) or
    ("unbounded", None, None). The w returned is a basic solution."""
    m, n = len(M), len(c)
    rows = []
    for i in range(m):
        row = [Fr(x) for x in M[i]]
        rhs = Fr(r[i])
        if rhs < 0:
            row, rhs = [-x for x in row], -rhs
        rows.append(row + [Fr(int(k == i)) for k in range(m)] + [rhs])
    basis = [n + i for i in range(m)]
    ncol = n + m
    cost1 = [Fr(0)] * n + [Fr(-1)] * m
    _solve_tableau(rows, basis, cost1, [True] * ncol)
    if sum(rows[i][-1] for i in range(m) if basis[i] >= n) > 0:
        return "infeasible", None, None
    # Drive the artificial variables out of the basis, or drop their rows.
    i = 0
    while i < len(rows):
        if basis[i] >= n:
            j = next((j for j in range(n) if rows[i][j] != 0), -1)
            if j < 0:
                del rows[i]
                del basis[i]
                continue
            _pivot(rows, basis, i, j)
        i += 1
    cost2 = [Fr(x) for x in c] + [Fr(0)] * m
    allowed = [True] * n + [False] * m
    if _solve_tableau(rows, basis, cost2, allowed) == "unbounded":
        return "unbounded", None, None
    w = [Fr(0)] * n
    for i, j in enumerate(basis):
        if j < n:
            w[j] = rows[i][-1]
    return "optimal", sum(Fr(a) * b for a, b in zip(c, w)), w


# ---------------------------------------------------------------------------
# Small exact linear algebra.


def solve_square(M: List[List[Fraction]], rhs: List[Fraction]) -> Optional[List[Fraction]]:
    """Solve M y = rhs by Gauss-Jordan elimination; None if M is singular."""
    k = len(M)
    aug = [list(M[i]) + [rhs[i]] for i in range(k)]
    for col in range(k):
        piv = next((i for i in range(col, k) if aug[i][col] != 0), -1)
        if piv < 0:
            return None
        aug[col], aug[piv] = aug[piv], aug[col]
        pv = aug[col][col]
        aug[col] = [x / pv for x in aug[col]]
        for i in range(k):
            if i != col and aug[i][col] != 0:
                f = aug[i][col]
                aug[i] = [x - f * y for x, y in zip(aug[i], aug[col])]
    return [aug[i][k] for i in range(k)]


def vertices(cuts: List[Tuple[Vec, Fraction]], p: int) -> List[Vec]:
    """The vertices of {y : h^T y >= beta for each (h, beta) in cuts}, by
    trying every p-subset of the inequalities."""
    found = set()
    for sub in combinations(cuts, p):
        y = solve_square([list(h) for h, _ in sub], [beta for _, beta in sub])
        if y is None:
            continue
        if all(sum(a * b for a, b in zip(h, y)) >= beta for h, beta in cuts):
            found.add(tuple(y))
    return sorted(found)


# ---------------------------------------------------------------------------
# Benson's algorithm.


def benson(A: Sequence[Sequence], b: Sequence, C: Sequence[Sequence]):
    """Return (V, cuts): the vertices of the upper image C[X] + R^p_+, sorted,
    and inequalities (h, beta), meaning h^T y >= beta, that describe it."""
    m, n, p = len(A), len(A[0]), len(C)
    A = [[Fr(x) for x in row] for row in A]
    b = [Fr(x) for x in b]
    C = [[Fr(x) for x in row] for row in C]
    # X must be nonempty: x = x1 - x2, A x1 - A x2 - s = b, all >= 0.
    M = [A[i] + [-x for x in A[i]] + [Fr(-int(k == i)) for k in range(m)] for i in range(m)]
    if simplex_max(M, b, [0] * (2 * n + m))[0] != "optimal":
        raise ValueError("X is empty")
    At = [[A[i][j] for i in range(m)] for j in range(n)]
    ideal = []
    for k in range(p):  # @line L1
        st, val, _ = simplex_max(At, C[k], b)  # @line L1
        if st != "optimal":  # @line L1
            raise ValueError("objective %d is unbounded below on X" % k)  # @line L1
        ideal.append(val)  # @line L1
    unit = [tuple(Fr(int(i == k)) for i in range(p)) for k in range(p)]  # @line L2
    cuts: List[Tuple[Vec, Fraction]] = [(unit[k], ideal[k]) for k in range(p)]  # @line L2
    # D2(t): variables (v, u); rows A^T v - C^T u = 0 and sum(u) = 1.
    D = [At[j] + [-C[k][j] for k in range(p)] for j in range(n)]
    D.append([Fr(0)] * m + [Fr(1)] * p)
    rhs = [Fr(0)] * n + [Fr(1)]
    while True:  # @line L3
        V = vertices(cuts, p)  # @line L4
        added = False
        for t in V:  # @line L5
            st, z, w = simplex_max(D, rhs, b + [-x for x in t])  # @line L6
            if z > 0:  # @line L7
                v, u = w[:m], w[m:]  # @line L7
                cuts.append((tuple(u), sum(x * y for x, y in zip(b, v))))  # @line L7
                added = True  # @line L7
                break  # @line L7
        if not added:  # @line L8
            return V, cuts  # @line L8
