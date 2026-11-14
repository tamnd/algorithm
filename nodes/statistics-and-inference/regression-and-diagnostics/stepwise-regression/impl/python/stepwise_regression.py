# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stepwise-regression/. The authors are listed in prov/GX5W9T.jsonl.
"""Stepwise regression (forward selection, backward elimination, both) by the sweep operator.

The model is y = b0 + X_S b_S + e with an intercept that is always in the model
and a subset S of the p candidate columns of X. Each step looks at every
single-variable move (add one column, or drop one column), takes the best one
and stops when no move is good enough. Two stopping rules are given:

- a penalized criterion, AIC (c = 2) or BIC (c = log n): take the move with the
  smallest criterion and stop when no move makes it strictly smaller;
- partial F-tests (Efroymson 1960): add the column with the largest F-to-enter
  if its p-value is below alpha_enter, drop the column with the smallest
  F-to-remove if its p-value is above alpha_remove.

All fits come from one (p + 1) x (p + 1) centered cross-product matrix, kept
swept on the current subset. With the response as the last index y, after a
sweep on S the entry a[y][y] is RSS(S), and for every column j the residual sum
of squares after the move "toggle j" is a[y][y] - a[j][y]^2 / a[j][j].
The arithmetic is generic, so Fraction input gives exact results.
"""

import math
from fractions import Fraction
from typing import NamedTuple

from stdist import f_sf

COLLINEAR_TOL = 1e-10


def _total(values):
    values = list(values)
    if values and all(isinstance(v, float) for v in values):
        return math.fsum(values)
    return sum(values, Fraction(0) if values and isinstance(values[0], Fraction) else 0)


def centered_sscp(x, y):
    """The (p + 1) x (p + 1) matrix of centered sums of squares and cross products of [X, y]."""
    n = len(y)
    if n == 0 or len(x) != n:
        raise ValueError("X and y need the same positive number of rows")
    cols = [[row[j] for row in x] for j in range(len(x[0]))] + [list(y)]
    means = [_total(c) / n for c in cols]
    dev = [[v - m for v in c] for c, m in zip(cols, means)]
    m = len(cols)
    a = [[None] * m for _ in range(m)]
    for i in range(m):
        for j in range(i, m):
            a[i][j] = a[j][i] = _total(u * v for u, v in zip(dev[i], dev[j]))
    return a


def sweep(a, k, reverse=False):
    """Sweep (or reverse sweep) the symmetric matrix a on index k, in place (Goodnight 1979)."""
    d = a[k][k]
    if d == 0:
        raise ZeroDivisionError("zero pivot in sweep")
    m = len(a)
    s = -1 if reverse else 1
    col = [a[i][k] for i in range(m)]
    for i in range(m):
        if i == k:
            continue
        f = col[i] / d
        if f != 0:
            row_i = a[i]
            for j in range(m):
                if j != k:
                    row_i[j] -= f * col[j]
    for i in range(m):
        if i != k:
            a[i][k] = s * col[i] / d
            a[k][i] = s * col[i] / d
    a[k][k] = -1 / d


def gaussian_loglik(rss, n):
    """The maximized normal log-likelihood of a regression with residual sum of squares rss."""
    return -0.5 * n * (math.log(2 * math.pi * float(rss) / n) + 1)


def aic(loglik, k):
    """Akaike information criterion, -2 log L + 2k, with k estimated parameters."""
    return -2.0 * loglik + 2.0 * k


def aicc(loglik, k, n):
    """AIC with the Hurvich-Tsai small-sample correction 2k(k + 1)/(n - k - 1)."""
    if n - k - 1 <= 0:
        raise ValueError("AICc needs n > k + 1")
    return aic(loglik, k) + 2.0 * k * (k + 1) / (n - k - 1)


def bic(loglik, k, n):
    """Schwarz's Bayesian information criterion, -2 log L + k log n."""
    return -2.0 * loglik + k * math.log(n)


def criterion_value(rss, n, size, criterion):
    """AIC or BIC of the normal regression with an intercept, `size` columns and the variance: k = size + 2."""
    if rss <= 0:
        return -math.inf
    ll = gaussian_loglik(rss, n)
    k = size + 2
    if criterion == "aic":
        return aic(ll, k)
    if criterion == "bic":
        return bic(ll, k, n)
    raise ValueError("criterion must be 'aic' or 'bic'")


class StepwiseResult(NamedTuple):
    subset: tuple   # the selected column indices, sorted
    rss: object     # residual sum of squares of the selected model
    path: list      # the moves, as ("add" or "drop", column, rss after the move)
    cycled: bool    # True if the F-test rule came back to a subset it had seen


def stepwise(x, y, direction="both", criterion="aic", alpha_enter=0.05, alpha_remove=0.10, start=None):
    """Stepwise selection. direction is 'forward', 'backward' or 'both'; criterion is 'aic', 'bic' or 'f'."""
    if direction not in ("forward", "backward", "both"):
        raise ValueError("direction must be 'forward', 'backward' or 'both'")
    if criterion not in ("aic", "bic", "f"):
        raise ValueError("criterion must be 'aic', 'bic' or 'f'")
    n = len(y)
    a = centered_sscp(x, y)  # @line L1
    p = len(a) - 1
    yy = p
    d0 = [a[j][j] for j in range(p)]
    if start is None:
        start = range(p) if direction == "backward" else ()
    inside = [False] * p
    for j in sorted(set(start)):
        if a[j][j] <= COLLINEAR_TOL * d0[j]:
            raise ValueError("the start subset has collinear columns")
        sweep(a, j)  # @line L2
        inside[j] = True
    path = []
    seen = {tuple(j for j in range(p) if inside[j])}

    def rss_toggle(j):
        return a[yy][yy] - a[j][yy] * a[j][yy] / a[j][j]  # @line L7

    def can_add(j):
        return not inside[j] and a[j][j] > COLLINEAR_TOL * d0[j] and n - sum(inside) - 2 > 0  # @line L6

    def apply(j):
        new_rss = rss_toggle(j)
        path.append(("drop" if inside[j] else "add", j, new_rss))
        if not inside[j]:
            sweep(a, j)  # @line L10
        else:
            sweep(a, j, reverse=True)  # @line L11
        inside[j] = not inside[j]

    cycled = False
    while True:  # @line L3
        size = sum(inside)
        if criterion != "f":
            cur = criterion_value(a[yy][yy], n, size, criterion)  # @line L4
            best_j, best_val = None, cur
            for j in range(p):  # @line L5
                if inside[j] and direction in ("backward", "both"):
                    val = criterion_value(rss_toggle(j), n, size - 1, criterion)
                elif can_add(j) and direction in ("forward", "both"):
                    val = criterion_value(rss_toggle(j), n, size + 1, criterion)
                else:
                    continue
                if val < best_val - 1e-12 * max(1.0, abs(best_val)):  # @line L8
                    best_j, best_val = j, val
            if best_j is None:  # @line L9
                break
            apply(best_j)
            continue
        moved = False
        if direction in ("forward", "both"):
            best_j, best_f = None, -1.0
            for j in range(p):
                if can_add(j):
                    new = rss_toggle(j)
                    df2 = n - size - 2
                    f = math.inf if new <= 0 else float(a[yy][yy] - new) / (float(new) / df2)
                    if f > best_f:
                        best_j, best_f = j, f
            if best_j is not None and f_sf(best_f, 1, n - size - 2) < alpha_enter:
                apply(best_j)
                moved = True
        if direction in ("backward", "both"):
            while sum(inside) > 0:
                size = sum(inside)
                rss = a[yy][yy]
                worst_j, worst_f = None, math.inf
                for j in range(p):
                    if inside[j]:
                        f = math.inf if rss <= 0 else float(rss_toggle(j) - rss) / (float(rss) / (n - size - 1))
                        if f < worst_f:
                            worst_j, worst_f = j, f
                if f_sf(worst_f, 1, n - size - 1) > alpha_remove:
                    apply(worst_j)
                    moved = True
                    continue
                break
        if not moved:
            break
        key = tuple(j for j in range(p) if inside[j])
        if key in seen:
            cycled = True
            break
        seen.add(key)
    subset = tuple(j for j in range(p) if inside[j])
    return StepwiseResult(subset, a[yy][yy], path, cycled)
