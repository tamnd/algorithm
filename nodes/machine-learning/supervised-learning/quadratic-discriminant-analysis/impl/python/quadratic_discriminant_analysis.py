# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quadratic-discriminant-analysis/. The authors are listed in prov/GZK9TB.jsonl.

"""Quadratic discriminant analysis with Friedman's regularization (RDA).

Each class gets a Gaussian with its own mean and covariance. The covariance is
Sigma_c(lam, gam) = (1 - gam) S(lam) + gam * trace(S(lam)) / d * I with
S(lam) = ((1 - lam) W_c + lam W) / ((1 - lam) n_c + lam n), where W_c is the
scatter matrix of class c and W their sum. lam = gam = 0 is plain QDA with
maximum likelihood covariances; lam = 1, gam = 0 is LDA with the pooled
maximum likelihood covariance.
"""

import math
from typing import Hashable, Sequence

Matrix = list[list[float]]
Vector = Sequence[float]


def cholesky(a: Matrix) -> Matrix:
    """Return lower triangular L with L L^T = a. Raise ValueError if a is not positive definite."""
    d = len(a)
    low = [[0.0] * d for _ in range(d)]
    for j in range(d):
        s = a[j][j] - sum(low[j][p] ** 2 for p in range(j))
        if s <= 0:
            raise ValueError("matrix is not positive definite")
        low[j][j] = math.sqrt(s)
        for i in range(j + 1, d):
            low[i][j] = (a[i][j] - sum(low[i][p] * low[j][p] for p in range(j))) / low[j][j]
    return low


def forward_solve(low: Matrix, b: Vector) -> list[float]:
    """Solve L z = b for lower triangular L."""
    z: list[float] = []
    for i in range(len(low)):
        z.append((b[i] - sum(low[i][p] * z[p] for p in range(i))) / low[i][i])
    return z


def back_solve_transpose(low: Matrix, z: Vector) -> list[float]:
    """Solve L^T v = z."""
    d = len(low)
    v = [0.0] * d
    for i in range(d - 1, -1, -1):
        v[i] = (z[i] - sum(low[p][i] * v[p] for p in range(i + 1, d))) / low[i][i]
    return v


def log_det_from_cholesky(low: Matrix) -> float:
    return 2.0 * sum(math.log(low[i][i]) for i in range(len(low)))


def _scatter(rows: Sequence[Vector], mu: Vector) -> Matrix:
    d = len(mu)
    w = [[0.0] * d for _ in range(d)]
    for r in rows:
        dev = [r[j] - mu[j] for j in range(d)]
        for i in range(d):
            for j in range(d):
                w[i][j] += dev[i] * dev[j]
    return w


class QDA:
    def __init__(self, lam: float = 0.0, gam: float = 0.0) -> None:
        if not (0 <= lam <= 1 and 0 <= gam <= 1):
            raise ValueError("lam and gam must be in [0, 1]")
        self.lam, self.gam = lam, gam

    def fit(self, xs: Sequence[Vector], ys: Sequence[Hashable]) -> "QDA":
        n, d = len(xs), len(xs[0])
        self.classes = sorted(set(ys))
        rows = {c: [x for x, y in zip(xs, ys) if y == c] for c in self.classes}
        self.mean, self.log_prior, self.cov, self.chol, self.log_det = {}, {}, {}, {}, {}
        scatter = {}
        for c in self.classes:  # @line L1
            m = len(rows[c])
            self.log_prior[c] = math.log(m / n)  # @line L2
            self.mean[c] = [sum(r[j] for r in rows[c]) / m for j in range(d)]  # @line L3
            scatter[c] = _scatter(rows[c], self.mean[c])  # @line L4
        pooled = [[sum(scatter[c][i][j] for c in self.classes) for j in range(d)] for i in range(d)]
        lam, gam = self.lam, self.gam
        for c in self.classes:  # @line L5
            m = len(rows[c])
            wgt = (1 - lam) * m + lam * n
            s = [[((1 - lam) * scatter[c][i][j] + lam * pooled[i][j]) / wgt for j in range(d)] for i in range(d)]
            tr = sum(s[i][i] for i in range(d)) / d
            s = [[(1 - gam) * s[i][j] + (gam * tr if i == j else 0.0) for j in range(d)] for i in range(d)]
            self.cov[c] = s
            self.chol[c] = cholesky(s)  # @line L6
            self.log_det[c] = log_det_from_cholesky(self.chol[c])  # @line L7
        return self

    def discriminants(self, x: Vector) -> dict:
        out = {}
        for c in self.classes:  # @line L8
            dev = [x[j] - self.mean[c][j] for j in range(len(x))]
            z = forward_solve(self.chol[c], dev)  # @line L9
            out[c] = -0.5 * self.log_det[c] - 0.5 * sum(v * v for v in z) + self.log_prior[c]  # @line L10
        return out

    def predict(self, x: Vector) -> Hashable:
        s = self.discriminants(x)
        best = max(s.values())
        return min(c for c in self.classes if s[c] == best)  # @line L11

    def predict_proba(self, x: Vector) -> dict:
        s = self.discriminants(x)
        m = max(s.values())
        z = sum(math.exp(v - m) for v in s.values())
        return {c: math.exp(v - m) / z for c, v in s.items()}


def lda_linear(xs: Sequence[Vector], ys: Sequence[Hashable], pos: Hashable, neg: Hashable) -> tuple[list[float], float]:
    """Two-class LDA with the pooled maximum likelihood covariance: return (w, c) such that
    delta_pos(x) - delta_neg(x) = w . x + c."""
    n, d = len(xs), len(xs[0])
    groups = {k: [x for x, y in zip(xs, ys) if y == k] for k in (pos, neg)}
    mu = {k: [sum(r[j] for r in g) / len(g) for j in range(d)] for k, g in groups.items()}
    every = sorted(set(ys))
    pooled = [[0.0] * d for _ in range(d)]
    for k in every:
        g = [x for x, y in zip(xs, ys) if y == k]
        m = [sum(r[j] for r in g) / len(g) for j in range(d)]
        sc = _scatter(g, m)
        for i in range(d):
            for j in range(d):
                pooled[i][j] += sc[i][j] / n
    low = cholesky(pooled)
    diff = [mu[pos][j] - mu[neg][j] for j in range(d)]
    w = back_solve_transpose(low, forward_solve(low, diff))
    mid = [(mu[pos][j] + mu[neg][j]) / 2 for j in range(d)]
    c = -sum(w[j] * mid[j] for j in range(d)) + math.log(len(groups[pos]) / len(groups[neg]))
    return w, c
