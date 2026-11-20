# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lmmse-channel-estimation/. The authors are listed in prov/5PBE09.jsonl.

"""Linear MMSE estimation of the taps of an FIR channel from known pilots.

The model is v = X h + w, where X is the m by L pilot matrix with
X[i][l] = x[i + L - 1 - l], v holds the samples y[L-1], ..., y[Np-1], the
taps h have mean zero and covariance R_h, and w ~ CN(0, N0 I) is independent
of h. The LMMSE estimate is

    h_hat = R_h X^H (X R_h X^H + N0 I)^(-1) v = (R_h X^H X + N0 I)^(-1) R_h X^H v.

The second form solves an L by L system and needs no inverse of R_h, so a
singular R_h (a tap that is known to be zero) is allowed. The error
covariance is C_e = N0 (R_h X^H X + N0 I)^(-1) R_h.
"""

import cbb


def training_matrix(x: list[complex], taps: int) -> list[list[complex]]:
    """The m by L pilot matrix X with X[i][l] = x[i + L - 1 - l], m = len(x) - L + 1."""
    m = len(x) - taps + 1
    if taps < 1 or m < 1:
        raise ValueError("need at least L pilots for L taps")
    return [[complex(x[i + taps - 1 - l]) for l in range(taps)] for i in range(m)]


def _system(x: list[complex], taps: int, r_h: list[list[complex]], n0: float):
    if len(r_h) != taps or any(len(r) != taps for r in r_h):
        raise ValueError("R_h must be L by L")
    if n0 <= 0:
        raise ValueError("N0 must be positive")
    xm = training_matrix(x, taps)
    xh = cbb.herm(xm)
    g = cbb.matmul(xh, xm)
    a = cbb.add(cbb.matmul(r_h, g), cbb.scale(n0, cbb.eye(taps)))
    return xm, xh, a


def lmmse_estimate(x: list[complex], y: list[complex], taps: int, r_h: list[list[complex]], n0: float) -> list[complex]:
    """The LMMSE estimate of L = taps zero-mean taps with covariance r_h, from pilots x and samples y[0..Np-1]."""
    if len(y) != len(x):
        raise ValueError("need one received sample per pilot")
    if len(r_h) != taps or any(len(r) != taps for r in r_h):
        raise ValueError("R_h must be L by L")
    if n0 <= 0:
        raise ValueError("N0 must be positive")
    xm = training_matrix(x, taps)  # @line L1
    v = [complex(s) for s in y[taps - 1 :]]  # @line L2
    xh = cbb.herm(xm)
    g, b = cbb.matmul(xh, xm), cbb.matvec(xh, v)  # @line L3
    a = cbb.add(cbb.matmul(r_h, g), cbb.scale(n0, cbb.eye(taps)))  # @line L4
    c = cbb.matvec(r_h, b)  # @line L5
    return cbb.solve(a, c)  # @line L6


def lmmse_matrix(x: list[complex], taps: int, r_h: list[list[complex]], n0: float) -> list[list[complex]]:
    """The L by m matrix W = (R_h X^H X + N0 I)^(-1) R_h X^H, so that h_hat = W v."""
    _, xh, a = _system(x, taps, r_h, n0)
    return cbb.solve(a, cbb.matmul(r_h, xh))


def error_covariance(x: list[complex], taps: int, r_h: list[list[complex]], n0: float) -> list[list[complex]]:
    """C_e = E[(h_hat - h)(h_hat - h)^H] = N0 (R_h X^H X + N0 I)^(-1) R_h."""
    _, _, a = _system(x, taps, r_h, n0)
    return cbb.scale(n0, cbb.solve(a, r_h))


def lmmse_mse(x: list[complex], taps: int, r_h: list[list[complex]], n0: float) -> float:
    """The mean squared error E||h_hat - h||^2 = tr(C_e)."""
    c = error_covariance(x, taps, r_h, n0)
    return sum(c[i][i].real for i in range(taps))
