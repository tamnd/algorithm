# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/least-squares-channel-estimation/. The authors are listed in prov/JGTN3A.jsonl.

"""Least squares (LS) estimation of the taps of an FIR channel from known pilots.

The model is y[k] = sum_{l=0}^{L-1} h[l] x[k-l] + w[k] at one sample per
symbol, with complex taps h and noise w ~ CN(0, N0). The transmitter sends
Np known pilots x[0], ..., x[Np-1]. The receiver uses only the m = Np - L + 1
samples y[L-1], ..., y[Np-1], which depend on pilots alone. In matrix form
v = X h + w with X[i][l] = x[i + L - 1 - l], and the LS estimate is
h_hat = (X^H X)^(-1) X^H v. Its error covariance is N0 (X^H X)^(-1), so its
mean squared error is N0 tr((X^H X)^(-1)).
"""

import cbb


def training_matrix(x: list[complex], taps: int) -> list[list[complex]]:
    """The m by L pilot matrix X with X[i][l] = x[i + L - 1 - l], m = len(x) - L + 1."""
    m = len(x) - taps + 1  # @line L1
    if taps < 1 or m < taps:
        raise ValueError("need at least 2L - 1 pilots for L taps")
    return [[complex(x[i + taps - 1 - l]) for l in range(taps)] for i in range(m)]  # @line L2


def _chol_solve(g: list[list[complex]], b: list[complex]) -> list[complex]:
    """Solve g z = b for a Hermitian positive definite g, by Cholesky g = C C^H."""
    try:
        c = cbb.cholesky(g)
    except ValueError:
        raise ValueError("X^H X is singular: the pilots do not excite every tap") from None
    n = len(g)
    u = [0j] * n
    for i in range(n):  # forward substitution, C u = b
        u[i] = (b[i] - sum(c[i][k] * u[k] for k in range(i))) / c[i][i]
    z = [0j] * n
    for i in range(n - 1, -1, -1):  # back substitution, C^H z = u
        z[i] = (u[i] - sum(c[k][i].conjugate() * z[k] for k in range(i + 1, n))) / c[i][i].conjugate()
    return z


def ls_estimate(x: list[complex], y: list[complex], taps: int) -> list[complex]:
    """The LS estimate of L = taps channel taps from Np pilots x and the Np samples y[0..Np-1]."""
    if len(y) != len(x):
        raise ValueError("need one received sample per pilot")
    xm = training_matrix(x, taps)  # @line L1
    v = [complex(s) for s in y[taps - 1 :]]  # @line L3
    xh = cbb.herm(xm)
    g = cbb.matmul(xh, xm)  # @line L4
    b = cbb.matvec(xh, v)  # @line L5
    return _chol_solve(g, b)  # @line L6


def ls_matrix(x: list[complex], taps: int) -> list[list[complex]]:
    """The L by m matrix P = (X^H X)^(-1) X^H. For fixed pilots, h_hat = P v costs O(m L)."""
    xm = training_matrix(x, taps)
    xh = cbb.herm(xm)
    g = cbb.matmul(xh, xm)
    cols = [_chol_solve(g, col) for col in (list(c) for c in zip(*xh))]
    return [list(r) for r in zip(*cols)]


def ls_mse(x: list[complex], taps: int, n0: float) -> float:
    """The mean squared error E||h_hat - h||^2 = N0 tr((X^H X)^(-1)) of the LS estimate."""
    xm = training_matrix(x, taps)
    g = cbb.matmul(cbb.herm(xm), xm)
    inv_g = [_chol_solve(g, col) for col in cbb.eye(taps)]
    return n0 * sum(inv_g[i][i].real for i in range(taps))


def received(x: list[complex], h: list[complex], noise: list[complex] | None = None) -> list[complex]:
    """y[k] = sum_l h[l] x[k-l] + w[k] for k = 0..len(x)-1, with x[k] = 0 for k < 0."""
    y = cbb.conv(x, h)[: len(x)]
    if noise is not None:
        y = [a + b for a, b in zip(y, noise)]
    return y
