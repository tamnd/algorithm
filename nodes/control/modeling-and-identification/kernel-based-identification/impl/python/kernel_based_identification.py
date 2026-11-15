# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernel-based-identification/. The authors are listed in prov/BXFFBH.jsonl.

"""Kernel-based (regularized) FIR identification with the TC and DC kernels.

Input: an input sequence u_0, ..., u_(N-1) and an output sequence
y_0, ..., y_(N-1) (scalars) of a system y_k = sum_(t=1..d) g_t u_(k-t) + e_k
with u_t = 0 for t < 0, the FIR length d, a grid of kernel hyperparameters,
and the noise variance sigma2 (or None to estimate it from the residuals of
the least squares FIR fit).

Model: the impulse response g is a Gaussian vector with zero mean and
covariance K (the kernel matrix), and e is white Gaussian noise with variance
sigma2. Then y is Gaussian with covariance Z = Phi K Phi^T + sigma2 I, and

    g_hat = (Phi^T Phi + sigma2 K^-1)^-1 Phi^T y = K Phi^T Z^-1 y

is the posterior mean (the regularized least squares estimate). The
hyperparameters minimize the negative log marginal likelihood
y^T Z^-1 y + log det Z (empirical Bayes) over the grid.

With K = L L^T (Cholesky) and M = sigma2 I + L^T Phi^T Phi L, every step
uses d by d matrices only:

    g_hat = L M^-1 L^T Phi^T y,
    y^T Z^-1 y = (y^T y - y^T Phi L M^-1 L^T Phi^T y) / sigma2,
    log det Z = (N - d) log sigma2 + log det M.
"""

import math

from ctlmat import mul, solve, transpose

__all__ = ["regressor", "tc_kernel", "dc_kernel", "cholesky", "fit", "neg_log_marginal_likelihood", "kernel_fir"]


def regressor(u, d):
    """Return the N by d matrix Phi with Phi[k][t - 1] = u_(k-t) (zero for k - t < 0)."""
    return [[float(u[k - t]) if k - t >= 0 else 0.0 for t in range(1, d + 1)] for k in range(len(u))]


def tc_kernel(d, c, lam):
    """Tuned/correlated kernel: K[i][j] = c lam^max(i, j), for i, j = 1, ..., d."""
    return [[c * lam ** max(i, j) for j in range(1, d + 1)] for i in range(1, d + 1)]


def dc_kernel(d, c, lam, rho):
    """Diagonal/correlated kernel: K[i][j] = c lam^((i + j) / 2) rho^|i - j|."""
    return [[c * lam ** ((i + j) / 2.0) * rho ** abs(i - j) for j in range(1, d + 1)] for i in range(1, d + 1)]


def cholesky(a):
    """Return the lower triangular L with a = L L^T; raise ValueError if a is not positive definite."""
    n = len(a)
    L = [[0.0] * n for _ in range(n)]
    for j in range(n):
        s = a[j][j] - sum(L[j][k] ** 2 for k in range(j))
        if not s > 0.0:
            raise ValueError("cholesky: the matrix is not positive definite")
        L[j][j] = math.sqrt(s)
        for i in range(j + 1, n):
            L[i][j] = (a[i][j] - sum(L[i][k] * L[j][k] for k in range(j))) / L[j][j]
    return L


def _parts(R, r, K, sigma2):
    d = len(K)
    L = cholesky(K)
    M = mul(mul(transpose(L), R), L)
    for i in range(d):
        M[i][i] += sigma2
    Ltr = [sum(L[t][i] * r[t] for t in range(d)) for i in range(d)]
    w = solve(M, Ltr)
    return L, M, Ltr, w


def neg_log_marginal_likelihood(R, r, yy, N, K, sigma2):
    """Return y^T Z^-1 y + log det Z from R = Phi^T Phi, r = Phi^T y and yy = y^T y."""
    d = len(K)
    L, M, Ltr, w = _parts(R, r, K, sigma2)
    logdet_m = 2.0 * sum(math.log(v[i]) for i, v in enumerate(cholesky(M)))
    quad = (yy - sum(a * b for a, b in zip(Ltr, w))) / sigma2
    return quad + (N - d) * math.log(sigma2) + logdet_m


def fit(R, r, K, sigma2):
    """Return g_hat = L M^-1 L^T r, the regularized least squares estimate."""
    L, M, Ltr, w = _parts(R, r, K, sigma2)
    d = len(K)
    return [sum(L[i][t] * w[t] for t in range(d)) for i in range(d)]


def kernel_fir(u, y, d, grid, kernel=tc_kernel, sigma2=None):
    """Return (g_hat, best, sigma2): the estimate, the chosen hyperparameters and the noise variance.

    grid is a list of tuples; kernel(d, *eta) is called for each tuple eta.
    """
    N = len(y)
    Phi = regressor(u, d)  # @line L1
    R = mul(transpose(Phi), Phi)  # @line L2
    r = [sum(Phi[k][t] * y[k] for k in range(N)) for t in range(d)]
    yy = sum(v * v for v in y)
    if sigma2 is None:  # @line L3
        g_ls = solve(R, r)
        sigma2 = (yy - 2.0 * sum(a * b for a, b in zip(g_ls, r))
                  + sum(g_ls[i] * R[i][j] * g_ls[j] for i in range(d) for j in range(d))) / (N - d)
    best, best_cost = None, math.inf
    for eta in grid:  # @line L4
        K = kernel(d, *eta)  # @line L5
        cost = neg_log_marginal_likelihood(R, r, yy, N, K, sigma2)  # @line L6
        if cost < best_cost:  # @line L7
            best, best_cost = eta, cost
    g_hat = fit(R, r, kernel(d, *best), sigma2)  # @line L8
    return g_hat, best, sigma2  # @line L9
