# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-likelihood-parameter-generation/. The authors are listed in prov/5JS7A5.jsonl.

"""Maximum likelihood parameter generation (MLPG), after Tokuda et al. (2000).

One feature dimension. For frames t = 0 .. T-1 the model gives a Gaussian with
mean mu[t][d] and variance var[t][d] for each window d = 0 .. D-1 (the static
feature, its delta, its delta-delta and so on). A window is a dict
{offset: coefficient}; the d-th observed feature at frame t is

    o[t][d] = sum over (tau, w) in windows[d] of w * c[t + tau],

and a frame t + tau outside 0 .. T-1 is replaced by the nearest end frame
(edge = "clamp", the default) or the term is dropped (edge = "zero").
So o = W c for a (D T) x T matrix W. MLPG returns the static trajectory c that
maximizes log N(W c; mu, U) with U = diag(var), which is the solution of

    (W^T U^-1 W) c = W^T U^-1 mu.

The matrix P = W^T U^-1 W is symmetric and banded with half-bandwidth
b = 2 L, where L is the largest |offset| of any window. It is solved by a
banded LDL^T factorization (Cholesky without square roots), in O(T b^2) time,
so the code runs on Fraction for exact checks and on float.

For several feature dimensions with a diagonal covariance, call it once per
dimension.
"""

from typing import Dict, List, Sequence

Window = Dict[int, object]

STATIC: Window = {0: 1}
DELTA: Window = {-1: -0.5, 1: 0.5}
DELTA2: Window = {-1: 1, 0: -2, 1: 1}


def half_bandwidth(windows: Sequence[Window]) -> int:
    reach = max((abs(k) for w in windows for k in w), default=0)
    return 2 * reach


def window_rows(T: int, windows: Sequence[Window], edge: str = "clamp"):
    """The rows of W as lists of (column, coefficient), in the order (t, d).

    edge = "clamp": a frame t + tau outside 0 .. T-1 is replaced by the nearest
    end frame (the trajectory is held constant beyond its ends).
    edge = "zero": such a term is dropped (the trajectory is 0 beyond its ends).
    """
    if edge not in ("clamp", "zero"):
        raise ValueError("edge must be 'clamp' or 'zero'")
    rows = []
    for t in range(T):
        for d, w in enumerate(windows):
            acc = {}
            for tau, coef in sorted(w.items()):
                u = t + tau
                if not 0 <= u < T:
                    if edge == "zero":
                        continue
                    u = min(max(u, 0), T - 1)
                acc[u] = acc.get(u, 0) + coef
            rows.append((t, d, sorted(acc.items())))
    return rows


def normal_equations(mu, var, windows: Sequence[Window], edge: str = "clamp"):
    """Return (P, r, b): P as a dict {(i, j): value} for i >= j within the band,
    r as a list, b the half-bandwidth."""
    T = len(mu)
    b = half_bandwidth(windows)
    P = {}
    r = [0 * mu[0][0] for _ in range(T)] if T else []  # @line L1
    for t, d, row in window_rows(T, windows, edge):  # @line L2
        inv = 1 / var[t][d]
        for u, a in row:  # @line L3
            for v, c in row:
                if u >= v:
                    P[(u, v)] = P.get((u, v), 0) + a * c * inv  # @line L4
            r[u] += a * mu[t][d] * inv  # @line L5
    return P, r, b


def banded_ldl_solve(P, r, b: int):
    """Solve P c = r for symmetric positive definite P with half-bandwidth b.

    P is a dict {(i, j): value} for i >= j. Raises ValueError if a pivot is not
    positive (P is singular or not positive definite)."""
    T = len(r)
    L = {}
    D = [None] * T
    for j in range(T):  # @line L6
        s = P.get((j, j), 0)
        for k in range(max(0, j - b), j):
            s -= L[(j, k)] * L[(j, k)] * D[k]
        if not s > 0:
            raise ValueError("the matrix W^T U^-1 W is not positive definite")
        D[j] = s  # @line L7
        for i in range(j + 1, min(T, j + b + 1)):  # @line L8
            s = P.get((i, j), 0)
            for k in range(max(0, i - b), j):
                s -= L[(i, k)] * L[(j, k)] * D[k]
            L[(i, j)] = s / D[j]
    y = list(r)
    for i in range(T):  # @line L9
        for k in range(max(0, i - b), i):
            y[i] -= L[(i, k)] * y[k]
    z = [y[i] / D[i] for i in range(T)]  # @line L10
    c = list(z)
    for i in range(T - 1, -1, -1):  # @line L11
        for k in range(i + 1, min(T, i + b + 1)):
            c[i] -= L[(k, i)] * c[k]
    return c


def mlpg(mu, var, windows: Sequence[Window] = (STATIC, DELTA, DELTA2), edge: str = "clamp") -> List:
    """The static trajectory c that maximizes log N(W c; mu, diag(var)).

    mu and var are T x D lists (D = len(windows)); every variance must be positive.
    edge is the rule for window terms beyond the ends, as in window_rows.
    """
    T = len(mu)
    if T == 0:
        return []
    if any(len(row) != len(windows) for row in list(mu) + list(var)):
        raise ValueError("each frame needs one mean and one variance per window")
    if any(not v > 0 for row in var for v in row):
        raise ValueError("variances must be positive")
    P, r, b = normal_equations(mu, var, windows, edge)
    return banded_ldl_solve(P, r, b)  # @line L12


def log_likelihood_quadratic(c, mu, var, windows: Sequence[Window], edge: str = "clamp"):
    """-1/2 (W c - mu)^T U^-1 (W c - mu), the part of log N(W c; mu, U) that depends on c."""
    q = 0
    for t, d, row in window_rows(len(mu), windows, edge):
        o = sum(a * c[u] for u, a in row)
        q += (o - mu[t][d]) * (o - mu[t][d]) / var[t][d]
    return -q / 2


def expand_states(means, variances, durations):
    """Repeat the per-state means and variances (each a list of D values) by the
    state durations, giving the T x D frame lists that mlpg takes."""
    mu, var = [], []
    for m, v, n in zip(means, variances, durations):
        if n < 0:
            raise ValueError("durations must be non-negative")
        for _ in range(n):
            mu.append(list(m))
            var.append(list(v))
    return mu, var
