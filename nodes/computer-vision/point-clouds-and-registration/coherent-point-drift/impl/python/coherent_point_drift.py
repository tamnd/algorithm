# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coherent-point-drift/. The authors are listed in prov/HWYJKB.jsonl.
"""Coherent point drift (CPD) of Myronenko and Song, 2010.

The moving set Y = [y_1, ..., y_K] gives the centroids of a Gaussian
mixture with one shared isotropic variance sigma2. The fixed set X = [x_1,
..., x_n] holds the data points. (The paper writes M for K and N for n; the
code keeps the paper's letters M and N as variable names.) A uniform
component of weight w models outliers. EM alternates two steps:

- E-step: the posterior P[k][i] that the point x_i comes from the centroid
  T(y_k).
- M-step: the transformation T and sigma2 that maximize the expected
  complete log-likelihood for this P.

Three kinds of T are given: rigid with scale (R, s, t), affine (B, t), and
non-rigid T(Y) = Y + G W with a Gaussian kernel matrix G and a penalty
(lam / 2) tr(W^T G W) on the motion field. All points are in R^D for any
D >= 1. Each iteration costs Theta(K n D) for the E-step; the non-rigid
M-step adds a dense K x K solve, Theta(K^3).

Every fit returns the negative log-likelihood of each iteration (plus the
penalty in the non-rigid case). EM makes this list nonincreasing.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

from cvla import det, mul, solve, svd, transpose

Matrix = List[List[float]]
Vector = List[float]


def _d2(a: Sequence[float], b: Sequence[float]) -> float:
    return sum((p - q) * (p - q) for p, q in zip(a, b))


def initial_sigma2(X: Sequence[Sequence[float]], TY: Sequence[Sequence[float]]) -> float:
    """sigma2 = (1 / (D N M)) sum_{m, n} |x_n - T(y_m)|^2, the start value."""
    N, M, D = len(X), len(TY), len(X[0])
    return sum(_d2(x, y) for x in X for y in TY) / (D * N * M)


def e_step(X: Sequence[Sequence[float]], TY: Sequence[Sequence[float]],
           sigma2: float, w: float) -> Tuple[Matrix, float]:
    """The posterior matrix P (M rows, N columns) and the negative
    log-likelihood of X under the mixture with centroids TY.

    P[m][n] = exp(-|x_n - T(y_m)|^2 / (2 sigma2)) / (sum_k exp(...) + c),
    with c = (2 pi sigma2)^(D/2) (w / (1 - w)) (M / N). The sums are done
    with a shift by the least distance, so no column underflows to 0 / 0."""
    N, M, D = len(X), len(TY), len(X[0])
    if not 0.0 <= w < 1.0:
        raise ValueError("w must be in [0, 1)")
    if w > 0.0:
        log_c = 0.5 * D * math.log(2.0 * math.pi * sigma2) + math.log(w / (1.0 - w)) + math.log(M / N)
    else:
        log_c = -math.inf
    base = math.log((1.0 - w) / M) - 0.5 * D * math.log(2.0 * math.pi * sigma2)
    P = [[0.0] * N for _ in range(M)]
    nll = 0.0
    for n, x in enumerate(X):
        d2 = [_d2(x, y) for y in TY]
        dmin = min(d2)
        e = [math.exp(-(d - dmin) / (2.0 * sigma2)) for d in d2]
        log_sum = math.log(sum(e))
        lc = log_c + dmin / (2.0 * sigma2)
        hi, lo = max(log_sum, lc), min(log_sum, lc)
        log_den = hi + math.log1p(math.exp(lo - hi)) if lo > -math.inf else hi
        for m in range(M):
            P[m][n] = math.exp(-(d2[m] - dmin) / (2.0 * sigma2) - log_den)
        nll -= base - dmin / (2.0 * sigma2) + log_den
    return P, nll


def _sums(P: Matrix) -> Tuple[Vector, Vector, float]:
    P1 = [sum(row) for row in P]
    Pt1 = [sum(col) for col in zip(*P)]
    return P1, Pt1, sum(P1)


def _centered(X, Y, P1, Pt1, Np):
    D = len(X[0])
    mux = [sum(Pt1[n] * X[n][d] for n in range(len(X))) / Np for d in range(D)]
    muy = [sum(P1[m] * Y[m][d] for m in range(len(Y))) / Np for d in range(D)]
    Xh = [[x[d] - mux[d] for d in range(D)] for x in X]
    Yh = [[y[d] - muy[d] for d in range(D)] for y in Y]
    return mux, muy, Xh, Yh


def _cross_cov(P: Matrix, Xh: Matrix, Yh: Matrix) -> Matrix:
    """A = Xh^T P^T Yh, a D x D matrix."""
    D = len(Xh[0])
    PXh = [[sum(row[n] * Xh[n][d] for n in range(len(Xh))) for d in range(D)] for row in P]
    return [[sum(PXh[m][i] * Yh[m][j] for m in range(len(Yh))) for j in range(D)] for i in range(D)]


def _apply_rigid(R, s, t, Y):
    return [[s * sum(R[i][k] * y[k] for k in range(len(y))) + t[i] for i in range(len(t))] for y in Y]


def _converged(hist: List[float], tol: float) -> bool:
    return len(hist) >= 2 and hist[-2] - hist[-1] <= tol * max(1.0, abs(hist[-1]))


def cpd_rigid(X: Sequence[Sequence[float]], Y: Sequence[Sequence[float]],
              w: float = 0.0, scale: bool = True, max_iter: int = 200,
              tol: float = 1e-10, sigma2_min: float = 1e-12) -> Dict[str, object]:
    """Rigid CPD: find R (det R = +1), s > 0 and t so that s R y_m + t fit X.

    With scale=False, s stays 1. Returns a dict with "R", "s", "t",
    "sigma2", "P" (the last posterior), "TY" (the moved Y) and "nll" (the
    negative log-likelihood at the start of each iteration)."""
    D = len(X[0])
    R = [[1.0 if i == j else 0.0 for j in range(D)] for i in range(D)]  # @line L1
    s, t = 1.0, [0.0] * D
    TY = [list(map(float, y)) for y in Y]
    sigma2 = initial_sigma2(X, TY)
    hist: List[float] = []
    P: Matrix = []
    for _ in range(max_iter):  # @line L2
        P, nll = e_step(X, TY, sigma2, w)  # @line L3
        hist.append(nll)
        if _converged(hist, tol) or sigma2 <= sigma2_min:  # @line L4
            break
        P1, Pt1, Np = _sums(P)  # @line L5
        mux, muy, Xh, Yh = _centered(X, Y, P1, Pt1, Np)
        A = _cross_cov(P, Xh, Yh)  # @line L6
        U, _, V = svd(A)
        C = [[1.0 if i == j else 0.0 for j in range(D)] for i in range(D)]
        C[D - 1][D - 1] = 1.0 if det(mul(U, transpose(V))) > 0.0 else -1.0
        R = mul(mul(U, C), transpose(V))  # @line L7
        trAR = sum(A[i][j] * R[i][j] for i in range(D) for j in range(D))
        yPy = sum(P1[m] * sum(v * v for v in Yh[m]) for m in range(len(Y)))
        xPx = sum(Pt1[n] * sum(v * v for v in Xh[n]) for n in range(len(X)))
        s = trAR / yPy if scale else 1.0
        t = [mux[i] - s * sum(R[i][k] * muy[k] for k in range(D)) for i in range(D)]
        sigma2 = (xPx - 2.0 * s * trAR + s * s * yPy) / (Np * D)  # @line L8
        sigma2 = max(sigma2, sigma2_min)
        TY = _apply_rigid(R, s, t, Y)
    return {"R": R, "s": s, "t": t, "sigma2": sigma2, "P": P, "TY": TY, "nll": hist}  # @line L9


def cpd_affine(X: Sequence[Sequence[float]], Y: Sequence[Sequence[float]],
               w: float = 0.0, max_iter: int = 200, tol: float = 1e-10,
               sigma2_min: float = 1e-12) -> Dict[str, object]:
    """Affine CPD: find B and t so that B y_m + t fit X. The M-step is
    B = (Xh^T P^T Yh)(Yh^T d(P1) Yh)^-1 and t = mu_x - B mu_y."""
    D = len(X[0])
    B = [[1.0 if i == j else 0.0 for j in range(D)] for i in range(D)]
    t = [0.0] * D
    TY = [list(map(float, y)) for y in Y]
    sigma2 = initial_sigma2(X, TY)
    hist: List[float] = []
    for _ in range(max_iter):
        P, nll = e_step(X, TY, sigma2, w)
        hist.append(nll)
        if _converged(hist, tol) or sigma2 <= sigma2_min:
            break
        P1, Pt1, Np = _sums(P)
        mux, muy, Xh, Yh = _centered(X, Y, P1, Pt1, Np)
        A = _cross_cov(P, Xh, Yh)
        YdY = [[sum(P1[m] * Yh[m][i] * Yh[m][j] for m in range(len(Y))) for j in range(D)] for i in range(D)]
        B = transpose(solve(YdY, transpose(A)))
        xPx = sum(Pt1[n] * sum(v * v for v in Xh[n]) for n in range(len(X)))
        trAB = sum(A[i][j] * B[i][j] for i in range(D) for j in range(D))
        t = [mux[i] - sum(B[i][k] * muy[k] for k in range(D)) for i in range(D)]
        sigma2 = max((xPx - trAB) / (Np * D), sigma2_min)
        TY = _apply_rigid(B, 1.0, t, Y)
    return {"B": B, "t": t, "sigma2": sigma2, "TY": TY, "nll": hist}


def gaussian_kernel(Y: Sequence[Sequence[float]], beta: float) -> Matrix:
    """G[i][j] = exp(-|y_i - y_j|^2 / (2 beta^2))."""
    return [[math.exp(-_d2(a, b) / (2.0 * beta * beta)) for b in Y] for a in Y]


def cpd_nonrigid(X: Sequence[Sequence[float]], Y: Sequence[Sequence[float]],
                 beta: float = 2.0, lam: float = 2.0, w: float = 0.0,
                 max_iter: int = 100, tol: float = 1e-8,
                 sigma2_min: float = 1e-12) -> Dict[str, object]:
    """Non-rigid CPD: T(Y) = Y + G W. The M-step solves
    (d(P1) G + lam sigma2 I) W = P X - d(P1) Y, the form of the paper's
    equation multiplied by d(P1), so no entry of P1 is divided by. The
    list "nll" holds the negative log-likelihood plus (lam / 2) tr(W^T G W)."""
    M, D = len(Y), len(X[0])
    G = gaussian_kernel(Y, beta)
    W = [[0.0] * D for _ in range(M)]
    TY = [list(map(float, y)) for y in Y]
    sigma2 = initial_sigma2(X, TY)
    hist: List[float] = []
    for _ in range(max_iter):
        P, nll = e_step(X, TY, sigma2, w)
        GW = mul(G, W)
        pen = 0.5 * lam * sum(W[m][d] * GW[m][d] for m in range(M) for d in range(D))
        hist.append(nll + pen)
        if _converged(hist, tol) or sigma2 <= sigma2_min:
            break
        P1, Pt1, Np = _sums(P)
        PX = [[sum(row[n] * X[n][d] for n in range(len(X))) for d in range(D)] for row in P]
        lhs = [[P1[i] * G[i][j] + (lam * sigma2 if i == j else 0.0) for j in range(M)] for i in range(M)]
        rhs = [[PX[m][d] - P1[m] * Y[m][d] for d in range(D)] for m in range(M)]
        W = solve(lhs, rhs)
        GW = mul(G, W)
        TY = [[Y[m][d] + GW[m][d] for d in range(D)] for m in range(M)]
        xPx = sum(Pt1[n] * sum(v * v for v in X[n]) for n in range(len(X)))
        cross = sum(PX[m][d] * TY[m][d] for m in range(M) for d in range(D))
        tPt = sum(P1[m] * sum(v * v for v in TY[m]) for m in range(M))
        sigma2 = max((xPx - 2.0 * cross + tPt) / (Np * D), sigma2_min)
    return {"W": W, "G": G, "TY": TY, "sigma2": sigma2, "nll": hist}
