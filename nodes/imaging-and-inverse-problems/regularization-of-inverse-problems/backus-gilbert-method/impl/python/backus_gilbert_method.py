# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backus-gilbert-method/. The authors are listed in prov/GT011W.jsonl.
"""The Backus-Gilbert method of optimally localized averages.

The data are d_i = int G_i(t) x(t) dt + n_i for i = 1, ..., m, with noise
covariance C. For a point p the method looks for weights a with

    estimate x_hat(p) = sum_i a_i d_i,   averaging kernel K_p(t) = sum_i a_i G_i(t),

so that K_p has unit area (c^T a = 1 with c_i = int G_i) and is concentrated
near p. The spread is s(a) = 12 int (t - p)^2 K_p(t)^2 dt = a^T S(p) a, the
noise variance is a^T C a, and the method minimizes a^T (S(p) + mu C) a
subject to c^T a = 1. A Lagrange multiplier gives

    a = W^(-1) c / (c^T W^(-1) c),   W = S(p) + mu C.

The factor 12 makes a box of width w around p have spread w. The integrals
are computed by a quadrature rule on a fine grid: nodes ts and weights ws.
"""

from imgla import solve


def spread_matrix(kernels, ts, ws, p):
    """S(p)_ij = 12 int (t - p)^2 G_i(t) G_j(t) dt by the quadrature (ts, ws)."""
    m = len(kernels)
    wt = [12.0 * w * (t - p) ** 2 for t, w in zip(ts, ws)]
    return [[sum(f * gi * gj for f, gi, gj in zip(wt, kernels[i], kernels[j]))
             for j in range(m)] for i in range(m)]


def areas(kernels, ws):
    """c_i = int G_i by the quadrature weights."""
    return [sum(w * g for w, g in zip(ws, gk)) for gk in kernels]


def weights(kernels, ts, ws, p, mu, cov):
    """The Backus-Gilbert coefficients a for the point p and trade-off parameter mu."""
    m = len(kernels)
    s = spread_matrix(kernels, ts, ws, p)  # @line L2
    w = [[s[i][j] + mu * cov[i][j] for j in range(m)] for i in range(m)]  # @line L3
    c = areas(kernels, ws)
    z = solve(w, c)  # @line L4
    cz = sum(ci * zi for ci, zi in zip(c, z))
    return [zi / cz for zi in z]  # @line L5


def backus_gilbert(kernels, ts, ws, data, points, mu, cov):
    """Estimates x_hat(p) = a(p)^T d for every point p."""
    out = []
    for p in points:  # @line L1
        a = weights(kernels, ts, ws, p, mu, cov)
        out.append(sum(ai * di for ai, di in zip(a, data)))  # @line L6
    return out  # @line L7


def averaging_kernel(kernels, a):
    """K_p(t) = sum_i a_i G_i(t) on the grid."""
    return [sum(ai * gk[t] for ai, gk in zip(a, kernels)) for t in range(len(kernels[0]))]


def spread(kernel_values, ts, ws, p):
    """12 int (t - p)^2 K(t)^2 dt for a function given on the grid."""
    return 12.0 * sum(w * (t - p) ** 2 * k * k for t, w, k in zip(ts, ws, kernel_values))


def noise_variance(a, cov):
    """a^T C a."""
    return sum(a[i] * cov[i][j] * a[j] for i in range(len(a)) for j in range(len(a)))
