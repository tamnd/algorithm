# SPDX-License-Identifier: MIT
# Shared helper of the vs2 compilers pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Exact linear programming over the rationals.

lp_solve(c, a_eq, b_eq, a_ub, b_ub, free) minimizes c . x subject to
a_eq x = b_eq, a_ub x <= b_ub, and x_j >= 0 for every j not in free. The
inputs may be int or Fraction. The answer is exact. It returns one of
  ("optimal", x, value), ("infeasible", None, None), ("unbounded", None, None)
with x a list of Fraction.

The method is the two-phase simplex method with Bland's rule, which never
cycles. The tableau holds only integers: each row is kept as an integer
multiple of the true row, the pivot step is a cross multiplication, and
each row is divided by the gcd of its entries. A free variable is split
into two nonnegative ones. Cost: exponential in the worst case, as for
every simplex method; fast on the small systems of these pages.
"""

from fractions import Fraction
from math import gcd


def _int_row(vals):
    """Scale a list of rationals to integers with the same signs."""
    den = 1
    for v in vals:
        v = Fraction(v)
        den = den * v.denominator // gcd(den, v.denominator)
    return [int(Fraction(v) * den) for v in vals]


def _reduce(row):
    g = 0
    for v in row:
        if v:
            g = gcd(g, v)
            if g == 1:
                return row
    if g > 1:
        return [v // g for v in row]
    return row


def _pivot(t, basis, r, j):
    pr = t[r]
    if pr[j] < 0:
        pr = t[r] = [-v for v in pr]
    p = pr[j]
    nz = [k for k, v in enumerate(pr) if v]
    for i, row in enumerate(t):
        f = row[j]
        if i != r and f:
            new = [v * p for v in row]
            for k in nz:
                new[k] -= f * pr[k]
            t[i] = _reduce(new)
    basis[r] = j


def _simplex(t, basis, cost, allowed):
    """Minimize cost . x over the tableau t with the given basis, entering
    only columns in allowed. Return "optimal" or "unbounded"."""
    ncols = len(cost)
    while True:
        enter = -1
        inbasis = set(basis)
        priced = [(Fraction(cost[b], t[i][b]), t[i]) for i, b in enumerate(basis) if cost[b]]
        for j in range(ncols):
            if not allowed[j] or j in inbasis:
                continue
            z = Fraction(cost[j])
            for cb, row in priced:
                if row[j]:
                    z -= cb * row[j]
            if z < 0:
                enter = j
                break
        if enter < 0:
            return "optimal"
        best = -1
        for i, row in enumerate(t):
            a = row[enter]
            if a > 0:
                if best < 0:
                    best = i
                    continue
                # Compare row[-1] / a with the best ratio, then the basis index.
                lhs = row[-1] * t[best][enter]
                rhs = t[best][-1] * a
                if lhs < rhs or (lhs == rhs and basis[i] < basis[best]):
                    best = i
        if best < 0:
            return "unbounded"
        _pivot(t, basis, best, enter)


def lp_solve(c, a_eq=(), b_eq=(), a_ub=(), b_ub=(), free=()):
    """Minimize c . x subject to a_eq x = b_eq, a_ub x <= b_ub and x_j >= 0
    for j not in free. See the module docstring for the result."""
    n = len(c)
    free = set(free)
    # Column map: variable j -> list of (column, sign).
    cols = []
    ncol = 0
    for j in range(n):
        if j in free:
            cols.append([(ncol, 1), (ncol + 1, -1)])
            ncol += 2
        else:
            cols.append([(ncol, 1)])
            ncol += 1
    nslack = len(a_ub)
    rows = [(coeffs, rhs, None) for coeffs, rhs in zip(a_eq, b_eq)]
    rows += [(coeffs, rhs, ncol + k) for k, (coeffs, rhs) in enumerate(zip(a_ub, b_ub))]
    m = len(rows)
    # A row whose slack can start in the basis needs no artificial variable.
    needs = [slack is None or rhs < 0 for _, rhs, slack in rows]
    nart = sum(needs)
    width = ncol + nslack + nart
    t = []
    basis = []
    art = ncol + nslack
    for i, (coeffs, rhs, slack) in enumerate(rows):
        row = [0] * (width + 1)
        for j in range(n):
            a = coeffs[j]
            if a:
                for col, sign in cols[j]:
                    row[col] += sign * a
        if slack is not None:
            row[slack] = 1
        row[-1] = rhs
        if needs[i]:
            if rhs < 0:
                row = [-v for v in row]
            row[art] = 1
            basis.append(art)
            art += 1
        else:
            basis.append(slack)
        if not all(type(v) is int for v in row):
            row = _int_row(row)
        t.append(_reduce(row))
    # Phase 1: minimize the sum of the artificial variables.
    cost1 = [0] * (ncol + nslack) + [1] * nart
    _simplex(t, basis, cost1, [True] * width)
    if any(t[i][-1] for i in range(m) if basis[i] >= ncol + nslack):
        return ("infeasible", None, None)
    # Drive the artificial variables out of the basis, or drop their rows.
    i = 0
    while i < len(t):
        if basis[i] >= ncol + nslack:
            j = next((j for j in range(ncol + nslack) if t[i][j] != 0), None)
            if j is None:
                del t[i]
                del basis[i]
                continue
            _pivot(t, basis, i, j)
        i += 1
    # Phase 2 on the real columns.
    cost2 = [Fraction(0)] * width
    for j in range(n):
        for col, sign in cols[j]:
            cost2[col] = sign * Fraction(c[j])
    allowed = [j < ncol + nslack for j in range(width)]
    if _simplex(t, basis, cost2, allowed) == "unbounded":
        return ("unbounded", None, None)
    val = [Fraction(0)] * width
    for i, b in enumerate(basis):
        val[b] = Fraction(t[i][-1], t[i][b])
    x = [sum(sign * val[col] for col, sign in cols[j]) for j in range(n)]
    return ("optimal", x, sum(Fraction(c[j]) * x[j] for j in range(n)))


def feasible_point(a_eq=(), b_eq=(), a_ub=(), b_ub=(), n=0, free=()):
    """A point of {x : a_eq x = b_eq, a_ub x <= b_ub, x_j >= 0 for j not in
    free} with n variables, or None if the set is empty."""
    status, x, _ = lp_solve([0] * n, a_eq, b_eq, a_ub, b_ub, free)
    return x if status == "optimal" else None
