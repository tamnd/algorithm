# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gaussian-belief-propagation/. The authors are listed in prov/63EWRZ.jsonl.

"""Gaussian belief propagation in information form (Weiss and Freeman 2001).

The model is p(x) proportional to exp(-x^T J x / 2 + h^T x), with J symmetric
positive definite, given as a list of rows. Its mean is J^{-1} h and its
covariance is J^{-1}. The graph has an edge (i, j) when J[i][j] != 0.

The message from i to j is a Gaussian in x_j in information form, a pair
(P_ij, v_ij), the function exp(-P_ij x_j^2 / 2 + v_ij x_j).
"""

import math
from fractions import Fraction


def neighbors(J):
    n = len(J)
    return [[j for j in range(n) if j != i and J[i][j] != 0] for i in range(n)]


def gabp(J, h, tol=1e-12, max_iter=10000):
    """Synchronous Gaussian BP. Return (means, variances, iterations, converged).
    The run stops as not converged if a cavity precision J_{i minus j} is not positive
    or a message overflows."""
    n = len(J)
    nb = neighbors(J)
    P = {(i, j): 0.0 for i in range(n) for j in nb[i]}  # @line L1
    v = {(i, j): 0.0 for i in range(n) for j in nb[i]}
    converged = False
    it = 0
    for it in range(1, max_iter + 1):  # @line L2
        newP, newv = {}, {}
        for (i, j) in P:
            jc = J[i][i] + sum(P[(k, i)] for k in nb[i] if k != j)  # @line L3
            hc = h[i] + sum(v[(k, i)] for k in nb[i] if k != j)
            if not jc > 0 or not math.isfinite(jc) or not math.isfinite(hc):
                means, variances = _marginals(J, h, nb, P, v)
                return means, variances, it, False
            newP[(i, j)] = -J[i][j] ** 2 / jc  # @line L4
            newv[(i, j)] = -J[i][j] * hc / jc
        delta = max([abs(newP[e] - P[e]) for e in P] + [abs(newv[e] - v[e]) for e in v] + [0.0])  # @line L5
        P, v = newP, newv
        if delta < tol:  # @line L6
            converged = True
            break
    means, variances = _marginals(J, h, nb, P, v)
    return means, variances, it, converged


def _marginals(J, h, nb, P, v):
    means, variances = [], []
    for i in range(len(J)):
        jh = J[i][i] + sum(P[(k, i)] for k in nb[i])  # @line L7
        hh = h[i] + sum(v[(k, i)] for k in nb[i])
        means.append(hh / jh if jh != 0 else math.nan)  # @line L8
        variances.append(1 / jh if jh != 0 else math.nan)
    return means, variances


def exact(J, h):
    """The exact mean J^{-1} h and the diagonal of J^{-1}, by Gauss-Jordan
    elimination in exact rational arithmetic."""
    n = len(J)
    a = [[Fraction(x) for x in J[i]] + [Fraction(h[i])] + [Fraction(int(i == k)) for k in range(n)]
         for i in range(n)]
    for c in range(n):
        piv = next(r for r in range(c, n) if a[r][c] != 0)
        a[c], a[piv] = a[piv], a[c]
        p = a[c][c]
        a[c] = [x / p for x in a[c]]
        for r in range(n):
            if r != c and a[r][c] != 0:
                f = a[r][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[c])]
    return [float(a[i][n]) for i in range(n)], [float(a[i][n + 1 + i]) for i in range(n)]


def walk_summability_radius(J, iters=2000):
    """The spectral radius of |R|, where R = I - D^{-1/2} J D^{-1/2} and D is the
    diagonal of J. The model is walk-summable when it is below 1. |R| is symmetric
    and nonnegative, so power iteration on |R| + I finds 1 + rho(|R|)."""
    n = len(J)
    R = [[0.0 if i == j else abs(J[i][j]) / math.sqrt(J[i][i] * J[j][j]) for j in range(n)] for i in range(n)]
    x = [1.0] * n
    lam = 0.0
    for _ in range(iters):
        y = [x[i] + sum(R[i][j] * x[j] for j in range(n)) for i in range(n)]
        lam = math.sqrt(sum(t * t for t in y)) / math.sqrt(sum(t * t for t in x))
        s = max(y)
        x = [t / s for t in y]
    return lam - 1.0


def grid_precision(rows, cols, couplings, diag=1.0):
    """J with J_ii = diag and J_ij = couplings[(i, j)] on the edges of a grid."""
    n = rows * cols
    J = [[0.0] * n for _ in range(n)]
    for i in range(n):
        J[i][i] = diag
    for (i, j), w in couplings.items():
        J[i][j] = J[j][i] = w
    return J


def grid_edges(rows, cols):
    idx = lambda r, c: r * cols + c
    edges = [(idx(r, c), idx(r, c + 1)) for r in range(rows) for c in range(cols - 1)]
    edges += [(idx(r, c), idx(r + 1, c)) for r in range(rows - 1) for c in range(cols)]
    return edges
