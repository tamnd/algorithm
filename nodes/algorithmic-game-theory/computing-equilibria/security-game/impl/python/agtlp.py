# SPDX-License-Identifier: MIT
# Shared helper of the algorithmic game theory pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Exact linear programming in Fraction, by the two-phase simplex method with Bland's rule.

lp_max(c, A_ub, b_ub, A_eq=None, b_eq=None) maximizes c x subject to A_ub x <= b_ub,
A_eq x = b_eq and x >= 0. lp_min does the same for minimization. Free variables must be
split by the caller (x = x+ - x-). Every input number is converted to Fraction, so the
result is exact: there is no tolerance anywhere.

Both functions return (status, x, value, dual). status is "optimal", "infeasible" or
"unbounded". When status is not "optimal", x, value and dual are None. dual has one entry
per constraint, the A_ub rows first and then the A_eq rows. It is the vector of shadow
prices: the value is sum_i b_i dual_i (strong duality). For lp_max, dual_i >= 0 on the
A_ub rows and A^T dual >= c. For lp_min, dual_i <= 0 on the A_ub rows and A^T dual <= c.
The entries for the A_eq rows have no sign condition.

Bland's rule (the smallest improving column enters, and among the rows with the smallest
ratio the one with the smallest basic variable leaves) makes the method finite on every
input, degenerate inputs included. There is no game algorithm in this module.
"""

from fractions import Fraction


def _frac(v):
    return v if isinstance(v, Fraction) else Fraction(v)


def _pivot(T, obj, basis, r, j):
    p = T[r][j]
    row = [v / p for v in T[r]]
    T[r] = row
    for k in range(len(T)):
        f = T[k][j]
        if k != r and f != 0:
            T[k] = [a - f * b for a, b in zip(T[k], row)]
    f = obj[j]
    if f != 0:
        obj[:] = [a - f * b for a, b in zip(obj, row)]
    basis[r] = j


def _simplex(T, obj, basis, ncols):
    """Maximize. obj[j] is the reduced cost of column j and obj[-1] is minus the value."""
    while True:
        enter = next((j for j in range(ncols) if obj[j] > 0), None)
        if enter is None:
            return "optimal"
        best = None
        for r, row in enumerate(T):
            a = row[enter]
            if a > 0:
                key = (row[-1] / a, basis[r])
                if best is None or key < best[0]:
                    best = (key, r)
        if best is None:
            return "unbounded"
        _pivot(T, obj, basis, best[1], enter)


def _objective_row(cost, T, basis):
    obj = list(cost) + [Fraction(0)]
    for r, j in enumerate(basis):
        f = obj[j]
        if f != 0:
            obj = [a - f * b for a, b in zip(obj, T[r])]
    return obj


def _any_solution(M, rhs, nvars):
    """Return one solution y of M y = rhs (a consistent system), with the free variables 0."""
    rows = [list(M[k]) + [rhs[k]] for k in range(len(M))]
    pivots = []
    r = 0
    for col in range(nvars):
        p = next((k for k in range(r, len(rows)) if rows[k][col] != 0), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        pv = rows[r][col]
        rows[r] = [v / pv for v in rows[r]]
        for k in range(len(rows)):
            f = rows[k][col]
            if k != r and f != 0:
                rows[k] = [a - f * b for a, b in zip(rows[k], rows[r])]
        pivots.append(col)
        r += 1
        if r == len(rows):
            break
    y = [Fraction(0)] * nvars
    for k, col in enumerate(pivots):
        y[col] = rows[k][-1]
    return y


def _matrix(A, width, name):
    A = [[_frac(v) for v in row] for row in (A or [])]
    if any(len(row) != width for row in A):
        raise ValueError(name + " must have one column per variable")
    return A


def lp_max(c, A_ub, b_ub, A_eq=None, b_eq=None):
    """Maximize c x subject to A_ub x <= b_ub, A_eq x = b_eq and x >= 0, exactly."""
    c = [_frac(v) for v in c]
    n = len(c)
    A_ub = _matrix(A_ub, n, "A_ub")
    A_eq = _matrix(A_eq, n, "A_eq")
    b_ub = [_frac(v) for v in (b_ub or [])]
    b_eq = [_frac(v) for v in (b_eq or [])]
    if len(b_ub) != len(A_ub) or len(b_eq) != len(A_eq):
        raise ValueError("b_ub and b_eq must have one entry per row")
    m1, m2 = len(A_ub), len(A_eq)
    m = m1 + m2
    width = n + m1
    # Rows in the original orientation, with a slack column for each A_ub row.
    orig = [A_ub[i] + [Fraction(int(k == i)) for k in range(m1)] for i in range(m1)]
    orig += [A_eq[i] + [Fraction(0)] * m1 for i in range(m2)]
    rhs = b_ub + b_eq
    # A row gets an artificial variable if it is an equation or if its right side is negative.
    need = [i >= m1 or rhs[i] < 0 for i in range(m)]
    nart = sum(need)
    T, basis = [], []
    a = 0
    for i in range(m):
        sign = -1 if rhs[i] < 0 else 1
        row = [sign * v for v in orig[i]] + [Fraction(0)] * nart + [sign * rhs[i]]
        if need[i]:
            row[width + a] = Fraction(1)
            basis.append(width + a)
            a += 1
        else:
            basis.append(n + i)
        T.append(row)
    if nart:
        # Phase 1: maximize minus the sum of the artificial variables.
        obj = _objective_row([Fraction(0)] * width + [Fraction(-1)] * nart, T, basis)
        _simplex(T, obj, basis, width + nart)
        if obj[-1] != 0:
            return "infeasible", None, None, None
        keep = []
        for r in range(m):
            if basis[r] >= width:
                j = next((j for j in range(width) if T[r][j] != 0), None)
                if j is None:
                    continue  # the row is a combination of the other rows
                _pivot(T, [Fraction(0)] * (width + nart + 1), basis, r, j)
            keep.append(r)
        T = [T[r][:width] + [T[r][-1]] for r in keep]
        basis = [basis[r] for r in keep]
    # Phase 2: the original objective, without the artificial columns.
    cost = c + [Fraction(0)] * m1
    obj = _objective_row(cost, T, basis)
    if _simplex(T, obj, basis, width) == "unbounded":
        return "unbounded", None, None, None
    x = [Fraction(0)] * n
    for r, j in enumerate(basis):
        if j < n:
            x[j] = T[r][-1]
    value = sum((ci * xi for ci, xi in zip(c, x)), Fraction(0))
    # The dual solves y^T A_B = c_B, where A_B holds the basic columns of the original rows.
    M = [[orig[i][j] for i in range(m)] for j in basis]
    dual = _any_solution(M, [cost[j] for j in basis], m)
    return "optimal", x, value, dual


def lp_min(c, A_ub, b_ub, A_eq=None, b_eq=None):
    """Minimize c x subject to A_ub x <= b_ub, A_eq x = b_eq and x >= 0, exactly."""
    status, x, value, dual = lp_max([-_frac(v) for v in c], A_ub, b_ub, A_eq, b_eq)
    if status != "optimal":
        return status, None, None, None
    return status, x, -value, [-v for v in dual]
