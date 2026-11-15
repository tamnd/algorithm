# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximal-positively-invariant-set/. The authors are listed in prov/MVMQPG.jsonl.

"""Maximal positively invariant (maximal output admissible) set of x+ = A x.

The system is x_(k+1) = A x_k with the output y_k = C x_k, which must stay in
the polytope Y = {y : F y <= g} for all k >= 0. The maximal output admissible
set is

    O_inf = {x : F C A^k x <= g for all k >= 0},

the largest positively invariant set inside {x : F C x <= g}. Write O_t for
the set with the constraints k = 0, ..., t only. The algorithm of Gilbert and
Tan (1991) adds the constraints of step t + 1 one block at a time and stops
at the first t with O_t = O_(t+1); then O_t = O_inf. The test O_t = O_(t+1)
is one linear program per row of F: the row of step t + 1 is redundant if
its maximum over O_t is at most its bound.

If A is Schur, (C, A) is observable, and Y is bounded with 0 in its
interior, such a t exists (O_inf is finitely determined).

The linear programs use a dense two phase simplex method with Bland's rule.
With int and Fraction data the arithmetic is exact (tol = 0). With float
data a tolerance is used.
"""

from fractions import Fraction

from ctlmat import mat_power, mul

__all__ = ["lp_max", "mpi_set", "remove_redundant", "Unbounded", "Infeasible"]


class Unbounded(Exception):
    """The linear program is unbounded."""


class Infeasible(Exception):
    """The linear program has no feasible point."""


def _pivot(T, basis, r, c):
    piv = T[r][c]
    T[r] = [v / piv for v in T[r]]
    for i in range(len(T)):
        if i != r and T[i][c] != 0:
            f = T[i][c]
            Ti, Tr = T[i], T[r]
            T[i] = [a - f * b for a, b in zip(Ti, Tr)]
    basis[r] = c


def _simplex(T, basis, cost, ncols, tol):
    """Maximize cost^T y over the tableau T (last column is the right side)."""
    while True:
        enter = None
        for j in range(ncols):  # Bland's rule: the first improving column
            if j in basis:
                continue
            rc = cost[j] - sum(cost[basis[i]] * T[i][j] for i in range(len(T)))
            if rc > tol:
                enter = j
                break
        if enter is None:
            return
        best, leave = None, None
        for i in range(len(T)):
            if T[i][enter] > tol:
                ratio = T[i][-1] / T[i][enter]
                if best is None or ratio < best - tol or (abs(ratio - best) <= tol and basis[i] < basis[leave]):
                    best, leave = ratio, i
        if leave is None:
            raise Unbounded("the linear program is unbounded")
        _pivot(T, basis, leave, enter)


def lp_max(c, rows, b, tol=None):
    """Return (max c^T x, x) subject to rows x <= b, with x free.

    Two phase simplex on x = x_plus - x_minus with slack variables.
    """
    exact = all(isinstance(v, (int, Fraction)) for v in list(c) + list(b) + [a for r in rows for a in r])
    if tol is None:
        tol = 0 if exact else 1e-9
    conv = Fraction if exact else float
    n, mr = len(c), len(rows)
    nart = sum(1 for v in b if v < 0)
    ncols = 2 * n + mr + nart
    T, basis, art = [], [], []
    a_idx = 2 * n + mr
    for i, (row, bi) in enumerate(zip(rows, b)):
        line = [conv(v) for v in row] + [conv(-v) for v in row] + [conv(1 if j == i else 0) for j in range(mr)]
        line += [conv(0)] * nart + [conv(bi)]
        if bi < 0:
            line = [-v for v in line]
            line[a_idx] = conv(1)
            basis.append(a_idx)
            art.append(a_idx)
            a_idx += 1
        else:
            basis.append(2 * n + i)
        T.append(line)
    if art:
        cost1 = [conv(0)] * ncols
        for j in art:
            cost1[j] = conv(-1)
        _simplex(T, basis, cost1, ncols, tol)
        if sum(T[i][-1] for i in range(mr) if basis[i] in art) > tol:
            raise Infeasible("the linear program is infeasible")
        for i in range(mr):  # drive the artificial variables out of the basis
            if basis[i] in art:
                for j in range(2 * n + mr):
                    if abs(T[i][j]) > tol and j not in basis:
                        _pivot(T, basis, i, j)
                        break
        for row in T:
            for j in art:
                row[j] = conv(0)
    cost = [conv(v) for v in c] + [conv(-v) for v in c] + [conv(0)] * (mr + nart)
    _simplex(T, basis, cost, 2 * n + mr, tol)
    y = [conv(0)] * ncols
    for i, j in enumerate(basis):
        y[j] = T[i][-1]
    x = [y[j] - y[n + j] for j in range(n)]
    return sum(ci * xi for ci, xi in zip(cost[:n], x)), x


def mpi_set(A, C, F, g, kmax=200, tol=None):
    """Return (rows, bounds, t_star) with O_inf = {x : rows x <= bounds}.

    t_star is the first t with O_t = O_(t+1). Only the rows that were not
    redundant when they were added are kept, so the description may still
    contain rows that later rows made redundant; see remove_redundant.
    Raises RuntimeError if no t < kmax works, and Infeasible if O_0 is
    empty (possible only if some g_i < 0).
    """
    FC = mul(F, C)
    rows = [list(r) for r in FC]  # @line L1
    bounds = list(g)
    for t in range(kmax):  # @line L2
        FCAk = mul(FC, mat_power(A, t + 1))  # @line L3
        new = []
        for row, gi in zip(FCAk, g):  # @line L4
            try:
                v, _ = lp_max(row, rows, bounds, tol)  # @line L5
            except Unbounded:  # O_t is unbounded in this direction
                v = None
            slack = 0 if tol is None and isinstance(v, Fraction) else (1e-9 if tol is None else tol)
            if v is None or v > gi + slack:  # @line L6
                new.append((row, gi))
        if not new:  # @line L7
            return rows, bounds, t
        for row, gi in new:  # @line L8
            rows.append(row)
            bounds.append(gi)
    raise RuntimeError("mpi_set: not finitely determined within kmax steps")


def remove_redundant(rows, bounds, tol=None):
    """Return a description of the same polytope with no redundant row.

    A row is redundant if its maximum over the other rows, with its own
    bound relaxed by 1, is at most its bound.
    """
    rows, bounds = [list(r) for r in rows], list(bounds)
    i = 0
    while i < len(rows):
        others = rows[:i] + rows[i + 1:]
        ob = bounds[:i] + bounds[i + 1:]
        try:
            v, _ = lp_max(rows[i], others + [rows[i]], ob + [bounds[i] + 1], tol)
        except Unbounded:
            v = None
        slack = 0 if v is None or isinstance(v, Fraction) else (1e-9 if tol is None else tol)
        if v is not None and v <= bounds[i] + slack:
            del rows[i]
            del bounds[i]
        else:
            i += 1
    return rows, bounds
