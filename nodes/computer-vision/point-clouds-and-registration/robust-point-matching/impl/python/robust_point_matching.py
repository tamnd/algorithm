# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/robust-point-matching/. The authors are listed in prov/P020QC.jsonl.
"""Robust point matching (RPM) with softassign, after Gold, Rangarajan, Lu,
Pappu and Mjolsness (Pattern Recognition, 1998), for a 2D affine map.

X has n points x_j, Y has m points y_k. The map is y -> A y + t. The match
matrix M (n x m) has an extra slack column (a point of X with no partner)
and an extra slack row (a point of Y with no partner). At the inverse
temperature beta the code lowers

  E(M, A, t) = sum_jk M_jk (|x_j - A y_k - t|^2 - alpha) + lam |A - I|_F^2
               + (1/beta) sum over all entries, slacks included, of M (log M - 1)

subject to: every row j of X sums to 1 over the m columns and the slack
column, and every column k of Y sums to 1 over the n rows and the slack row.
alpha is the squared distance below which a match pays off.

The M step is softassign: M_jk = exp(beta (alpha - d_jk)), slack entries
start at exp(0) = 1, then Sinkhorn normalizes the rows and the columns in
turn. The (A, t) step is a weighted least squares fit with the penalty
lam |A - I|^2, which keeps the affine part near the identity at the start.
This penalty, and its weight that shrinks as beta grows, are simple choices
of this code. beta grows by a fixed factor: deterministic annealing.
"""

from __future__ import annotations

import math
from typing import Dict, List, Sequence, Tuple

Point = Sequence[float]
Matrix = List[List[float]]


def apply(A: Matrix, t: Sequence[float], y: Point) -> List[float]:
    return [A[0][0] * y[0] + A[0][1] * y[1] + t[0], A[1][0] * y[0] + A[1][1] * y[1] + t[1]]


def sq_dists(X: Sequence[Point], Y: Sequence[Point], A: Matrix, t: Sequence[float]) -> Matrix:
    Ty = [apply(A, t, y) for y in Y]
    return [[(x[0] - z[0]) ** 2 + (x[1] - z[1]) ** 2 for z in Ty] for x in X]


def sinkhorn(M: Matrix, sc: List[float], sr: List[float], iters: int,
             tol: float = 1e-9) -> int:
    """Normalize in place: rows j (with the slack column entry sc[j]) and
    columns k (with the slack row entry sr[k]) to sum 1, in turn. Stops when
    every row and column sum is within tol of 1. Returns the number of
    sweeps."""
    n, m = len(M), len(sr)
    for sweep in range(1, iters + 1):
        for j in range(n):  # @line L6
            s = sum(M[j]) + sc[j]
            M[j] = [v / s for v in M[j]]
            sc[j] /= s
        worst = 0.0
        for k in range(m):  # @line L7
            s = sum(M[j][k] for j in range(n)) + sr[k]
            for j in range(n):
                M[j][k] /= s
            sr[k] /= s
        for j in range(n):
            worst = max(worst, abs(sum(M[j]) + sc[j] - 1.0))
        if worst <= tol:
            return sweep
    return iters


def softassign(X, Y, A, t, beta: float, alpha: float, iters: int,
               tol: float = 1e-9) -> Tuple[Matrix, List[float], List[float]]:
    D = sq_dists(X, Y, A, t)
    # Subtract the largest exponent of each row: a common factor of a row
    # cancels in the row step, and avoids overflow at large beta.
    M = []
    sc = []
    for row in D:
        top = max(0.0, max(beta * (alpha - d) for d in row))
        M.append([math.exp(beta * (alpha - d) - top) for d in row])  # @line L5
        sc.append(math.exp(-top))
    sr = [1.0] * len(Y)
    sinkhorn(M, sc, sr, iters, tol)
    return M, sc, sr


def _solve(S: Matrix, r: Sequence[float]) -> List[float]:
    """Gaussian elimination with partial pivoting for a small system."""
    k = len(r)
    a = [list(S[i]) + [r[i]] for i in range(k)]
    for c in range(k):
        p = max(range(c, k), key=lambda i: abs(a[i][c]))
        a[c], a[p] = a[p], a[c]
        for i in range(c + 1, k):
            f = a[i][c] / a[c][c]
            for j in range(c, k + 1):
                a[i][j] -= f * a[c][j]
    out = [0.0] * k
    for i in reversed(range(k)):
        out[i] = (a[i][k] - sum(a[i][j] * out[j] for j in range(i + 1, k))) / a[i][i]
    return out


def pose_step(X, Y, M: Matrix, lam: float) -> Tuple[Matrix, List[float]]:
    """The A and t that minimize sum M_jk |x_j - A y_k - t|^2 + lam |A - I|^2.
    Each output coordinate r gives a 3 x 3 system in (A[r][0], A[r][1], t[r])."""
    n, m = len(X), len(Y)
    sw = swy0 = swy1 = s00 = s01 = s11 = 0.0
    sx = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]  # per r: sum w x_r y0, sum w x_r y1, sum w x_r
    for j in range(n):
        x = X[j]
        for k in range(m):
            w = M[j][k]
            y = Y[k]
            sw += w
            swy0 += w * y[0]
            swy1 += w * y[1]
            s00 += w * y[0] * y[0]
            s01 += w * y[0] * y[1]
            s11 += w * y[1] * y[1]
            for r in range(2):
                sx[r][0] += w * x[r] * y[0]
                sx[r][1] += w * x[r] * y[1]
                sx[r][2] += w * x[r]
    S = [[s00 + lam, s01, swy0], [s01, s11 + lam, swy1], [swy0, swy1, sw]]
    A = [[0.0, 0.0], [0.0, 0.0]]
    t = [0.0, 0.0]
    for r in range(2):
        rhs = [sx[r][0] + (lam if r == 0 else 0.0), sx[r][1] + (lam if r == 1 else 0.0), sx[r][2]]
        a0, a1, tr = _solve(S, rhs)
        A[r] = [a0, a1]
        t[r] = tr
    return A, t


def energy(X, Y, M, sc, sr, A, t, alpha: float, lam: float, beta: float) -> float:
    D = sq_dists(X, Y, A, t)
    e = lam * sum((A[i][k] - (1.0 if i == k else 0.0)) ** 2 for i in range(2) for k in range(2))
    for j, row in enumerate(M):
        for k, v in enumerate(row):
            e += v * (D[j][k] - alpha) + (v * math.log(v) - v) / beta if v > 0.0 else 0.0
    for v in list(sc) + list(sr):
        if v > 0.0:
            e += (v * math.log(v) - v) / beta
    return e


def rpm(X: Sequence[Point], Y: Sequence[Point], alpha: float, lam0: float = 10.0,
        lam_final: float = 0.01, beta0: float = 0.5, beta_final: float = 500.0,
        rate: float = 1.2, inner: int = 3, sinkhorn_iters: int = 30) -> Dict[str, object]:
    """Returns the map (A, t), the match matrix with its slacks, and the hard
    matches: pairs (j, k) where M_jk is the largest entry of its row and of
    its column, slacks included. The penalty weight is lam0 * beta0 / beta,
    but not below lam_final: strong at the start, weak at the end."""
    A = [[1.0, 0.0], [0.0, 1.0]]  # @line L1
    t = [0.0, 0.0]
    beta = beta0
    M, sc, sr = None, None, None
    while beta <= beta_final:  # @line L2
        lam = max(lam_final, lam0 * beta0 / beta)
        for _ in range(inner):  # @line L3
            M, sc, sr = softassign(X, Y, A, t, beta, alpha, sinkhorn_iters)  # @line L4
            A, t = pose_step(X, Y, M, lam)  # @line L8
        beta *= rate  # @line L9
    n, m = len(X), len(Y)
    matches = []
    for j in range(n):
        k = max(range(m), key=lambda c: M[j][c])
        if M[j][k] > sc[j] and all(M[j][k] >= M[i][k] for i in range(n)) and M[j][k] > sr[k]:
            matches.append((j, k))
    return {"A": A, "t": t, "M": M, "slack_col": sc, "slack_row": sr, "matches": matches}  # @line L10
