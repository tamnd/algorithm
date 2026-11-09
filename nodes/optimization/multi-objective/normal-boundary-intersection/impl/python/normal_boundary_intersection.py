# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/normal-boundary-intersection/. The authors are listed in prov/QJW02J.jsonl.

"""Normal boundary intersection (Das and Dennis) for multi-objective linear programs.

All objectives are minimized. The problem is

    minimize F(x) = C x  subject to  x in X = {x in R^n : A x >= b},

with p objectives (the rows of C). X must be nonempty and each objective
must be bounded below on X.

The method finds the anchor points x_i* (a Pareto optimal minimizer of f_i),
the ideal point F*, and the pay-off matrix Phi whose column i is
F(x_i*) - F*. For each weight vector beta on a regular grid of the simplex
it solves the linear program

    NBI(beta):  maximize t  subject to  F(x) = F* + Phi beta + t n,  x in X,

where n = -Phi e is the quasi-normal direction, and returns F(x). For p = 2
each such point is Pareto optimal. For p >= 3 some of them can be dominated.

All arithmetic is exact, with Fraction.
"""

from fractions import Fraction
from itertools import combinations
from typing import List, Optional, Sequence, Tuple

Fr = Fraction


# ---------------------------------------------------------------------------
# A two-phase simplex method with Bland's rule, in exact arithmetic.


def _pivot(T, basis, r, c) -> None:
    piv = T[r][c]
    T[r] = [x / piv for x in T[r]]
    for i in range(len(T)):
        if i != r and T[i][c] != 0:
            f = T[i][c]
            T[i] = [x - f * y for x, y in zip(T[i], T[r])]
    basis[r] = c


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


def simplex_max(M: Sequence[Sequence], r: Sequence, c: Sequence):
    """Maximize c^T w subject to M w = r and w >= 0.

    Return ("optimal", value, w), ("infeasible", None, None) or
    ("unbounded", None, None)."""
    m, n = len(M), len(c)
    rows = []
    for i in range(m):
        row = [Fr(x) for x in M[i]]
        rhs = Fr(r[i])
        if rhs < 0:
            row, rhs = [-x for x in row], -rhs
        rows.append(row + [Fr(int(k == i)) for k in range(m)] + [rhs])
    basis = [n + i for i in range(m)]
    _solve_tableau(rows, basis, [Fr(0)] * n + [Fr(-1)] * m, [True] * (n + m))
    if sum(rows[i][-1] for i in range(m) if basis[i] >= n) > 0:
        return "infeasible", None, None
    i = 0
    while i < len(rows):  # drive artificial variables out, or drop their rows
        if basis[i] >= n:
            j = next((j for j in range(n) if rows[i][j] != 0), -1)
            if j < 0:
                del rows[i]
                del basis[i]
                continue
            _pivot(rows, basis, i, j)
        i += 1
    cost = [Fr(x) for x in c] + [Fr(0)] * m
    if _solve_tableau(rows, basis, cost, [True] * n + [False] * m) == "unbounded":
        return "unbounded", None, None
    w = [Fr(0)] * n
    for i, j in enumerate(basis):
        if j < n:
            w[j] = rows[i][-1]
    return "optimal", sum(Fr(a) * b for a, b in zip(c, w)), w


def lp_min(A, b, E, d, cost) -> Tuple[str, Optional[Fraction], Optional[List[Fraction]]]:
    """Minimize cost^T z over free z subject to A z >= b and E z = d."""
    k = len(cost)
    m = len(A)
    M, r = [], []
    for i in range(m):  # A z+ - A z- - s = b
        M.append(list(A[i]) + [-x for x in A[i]] + [Fr(-int(j == i)) for j in range(m)])
        r.append(b[i])
    for i in range(len(E)):  # E z+ - E z- = d
        M.append(list(E[i]) + [-x for x in E[i]] + [Fr(0)] * m)
        r.append(d[i])
    st, val, w = simplex_max(M, r, [-x for x in cost] + [x for x in cost] + [Fr(0)] * m)
    if st != "optimal":
        return st, None, None
    return st, -val, [w[j] - w[k + j] for j in range(k)]


# ---------------------------------------------------------------------------
# Normal boundary intersection.


def simplex_grid(p: int, H: int) -> List[Tuple[Fraction, ...]]:
    """All beta >= 0 with sum(beta) = 1 and H * beta integer, in
    lexicographically decreasing order."""
    out = []
    for cut in combinations(range(H + p - 1), p - 1):  # stars and bars
        parts, prev = [], -1
        for c in cut + (H + p - 1,):
            parts.append(c - prev - 1)
            prev = c
        out.append(tuple(Fr(x, H) for x in parts))
    return sorted(out, reverse=True)


def anchors(A, b, C):
    """Pareto optimal minimizers of each objective: minimize f_i, then the
    sum of the other objectives with f_i fixed at its minimum."""
    p, n = len(C), len(C[0])
    xs = []
    for i in range(p):
        st, fi, _ = lp_min(A, b, [], [], C[i])
        if st != "optimal":
            raise ValueError("objective %d is unbounded below or X is empty" % i)
        rest = [sum(C[j][k] for j in range(p) if j != i) for k in range(n)]
        st, _, x = lp_min(A, b, [C[i]], [fi], rest)
        if st != "optimal":  # the other objectives are bounded below, so this is optimal
            raise ValueError("lexicographic step failed")
        xs.append(x)
    return xs


def nbi(A: Sequence[Sequence], b: Sequence, C: Sequence[Sequence], H: int):
    """Return (Fstar, Phi, points), where points is a list of (beta, t, y)
    with y = F(x) for an optimal x of NBI(beta), one for each grid beta."""
    A = [[Fr(x) for x in row] for row in A]
    b = [Fr(x) for x in b]
    C = [[Fr(x) for x in row] for row in C]
    p, n = len(C), len(A[0])
    F = lambda x: tuple(sum(c * v for c, v in zip(row, x)) for row in C)
    xs = anchors(A, b, C)  # @line L1
    Fstar = [F(xs[i])[i] for i in range(p)]  # @line L2
    Phi = [[F(xs[j])[i] - Fstar[i] for j in range(p)] for i in range(p)]  # @line L2
    normal = [-sum(row) for row in Phi]  # @line L3
    if all(v == 0 for v in normal):
        return Fstar, Phi, [(beta, Fr(0), tuple(Fstar)) for beta in simplex_grid(p, H)]
    # Variables z = (x, t). Rows: A x >= b and C x - t n = F* + Phi beta.
    Az = [row + [Fr(0)] for row in A]
    Ez = [C[i] + [-normal[i]] for i in range(p)]
    cost = [Fr(0)] * n + [Fr(-1)]
    points = []
    for beta in simplex_grid(p, H):  # @line L4
        rhs = [Fstar[i] + sum(Phi[i][j] * beta[j] for j in range(p)) for i in range(p)]  # @line L5
        st, val, z = lp_min(Az, b, Ez, rhs, cost)  # @line L5
        points.append((beta, -val, F(z[:n])))  # @line L6
    return Fstar, Phi, points  # @line L7
