# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantile-regression/. The authors are listed in prov/HBFAEF.jsonl.

from fractions import Fraction
from typing import Sequence

Number = int | Fraction


def pinball(r: Fraction, tau: Fraction) -> Fraction:
    """The check loss rho_tau(r) = r * (tau - [r < 0])."""
    return r * tau if r >= 0 else r * (tau - 1)


def objective(X: Sequence[Sequence[Number]], y: Sequence[Number], tau: Number, w: Sequence[Fraction]) -> Fraction:
    """The sum of the check losses of the residuals y_i - x_i . w."""
    t = Fraction(tau)
    return sum((pinball(Fraction(yi) - sum(Fraction(a) * b for a, b in zip(xi, w)), t) for xi, yi in zip(X, y)), Fraction(0))


def quantile_regression(X: Sequence[Sequence[Number]], y: Sequence[Number], tau: Number) -> list[Fraction]:
    """Return an exact minimizer w of sum_i rho_tau(y_i - x_i . w), by the simplex method.

    The linear program is: minimize tau * sum(u) + (1 - tau) * sum(v) subject to
    X w+ - X w- + u - v = y and w+, w-, u, v >= 0. The columns are numbered
    w+ (0 .. d-1), w- (d .. 2d-1), u (2d .. 2d+n-1), v (2d+n .. 2d+2n-1).
    Precondition: 0 <= tau <= 1, the entries are int or Fraction, n >= 1.
    Bland's rule makes the method stop. Each pivot costs O(n (n + d))
    exact operations; the number of pivots is finite but not bounded by a
    polynomial in the worst case.
    """
    n, d = len(X), len(X[0])
    t = Fraction(tau)
    N = 2 * d + 2 * n
    cost = [Fraction(0)] * (2 * d) + [t] * n + [1 - t] * n
    # L1: the tableau rows [A | b]; L2: a sign flip makes b >= 0, and u_i or v_i is basic.
    T: list[list[Fraction]] = []  # @line L1
    basis: list[int] = []
    for i in range(n):  # @line L2
        row = [Fraction(a) for a in X[i]] + [-Fraction(a) for a in X[i]] + [Fraction(0)] * (2 * n) + [Fraction(y[i])]
        row[2 * d + i] = Fraction(1)
        row[2 * d + n + i] = Fraction(-1)
        if row[-1] < 0:
            row = [-a for a in row]
            basis.append(2 * d + n + i)
        else:
            basis.append(2 * d + i)
        T.append(row)
    while True:  # @line L3
        # Reduced costs c_j - c_B^T B^{-1} a_j, computed from the current tableau.
        red = [cost[j] - sum(cost[basis[i]] * T[i][j] for i in range(n)) for j in range(N)]  # @line L4
        if all(r >= 0 for r in red):  # @line L5
            break
        e = min(j for j in range(N) if red[j] < 0)  # @line L6
        rows = [i for i in range(n) if T[i][e] > 0]  # @line L7
        if not rows:
            raise ArithmeticError("unbounded; impossible for 0 <= tau <= 1")
        r = min(rows, key=lambda i: (T[i][-1] / T[i][e], basis[i]))  # @line L8
        p = T[r][e]  # @line L9
        T[r] = [a / p for a in T[r]]
        for i in range(n):
            if i != r and T[i][e] != 0:
                f = T[i][e]
                T[i] = [a - f * b for a, b in zip(T[i], T[r])]
        basis[r] = e
    value = [Fraction(0)] * N  # @line L10
    for i in range(n):
        value[basis[i]] = T[i][-1]
    return [value[j] - value[d + j] for j in range(d)]  # @line L11


def _null_vector(rows: list[list[Fraction]], d: int) -> list[Fraction] | None:
    """A nonzero vector delta with rows . delta = 0, or None when the rows have rank d."""
    M = [list(r) for r in rows]
    pivots: list[int] = []
    k = 0
    for c in range(d):
        p = next((i for i in range(k, len(M)) if M[i][c] != 0), None)
        if p is None:
            continue
        M[k], M[p] = M[p], M[k]
        M[k] = [a / M[k][c] for a in M[k]]
        for i in range(len(M)):
            if i != k and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[k])]
        pivots.append(c)
        k += 1
    free = [c for c in range(d) if c not in pivots]
    if not free:
        return None
    delta = [Fraction(0)] * d
    delta[free[0]] = Fraction(1)
    for i, c in enumerate(pivots):
        delta[c] = -M[i][free[0]]
    return delta


def interpolating_solution(X: Sequence[Sequence[Number]], y: Sequence[Number], w: Sequence[Fraction]) -> list[Fraction]:
    """Move an optimal w, at the same objective value, to one whose zero residuals have rank d.

    Precondition: w is optimal and X has rank d. This is the step of the
    Koenker and Bassett argument: along a direction delta with x_i . delta = 0
    on the zero set Z, the objective is linear near w with slope 0, so moving
    until a new residual becomes 0 keeps w optimal and raises the rank of Z.
    """
    d = len(X[0])
    w = list(w)
    Xf = [[Fraction(a) for a in xi] for xi in X]
    while True:
        res = [Fraction(yi) - sum(a * b for a, b in zip(xi, w)) for xi, yi in zip(Xf, y)]
        zero = [Xf[i] for i in range(len(Xf)) if res[i] == 0]
        delta = _null_vector(zero, d)
        if delta is None:
            return w
        steps = []
        for i in range(len(Xf)):
            a = sum(p * q for p, q in zip(Xf[i], delta))
            if res[i] != 0 and a != 0:
                steps.append(res[i] / a)
        if not steps:
            raise ValueError("X does not have rank d")
        s = min(steps, key=abs)
        w = [a + s * b for a, b in zip(w, delta)]
