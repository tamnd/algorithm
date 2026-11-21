# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unbiased-predictive-risk-estimator/. The authors are listed in prov/FEKTYX.jsonl.
"""The unbiased predictive risk estimator (UPRE) for Tikhonov regularization and TSVD.

Model: y = A x + e with e ~ N(0, sigma^2 I_m) and a known sigma. Tikhonov:
x_alpha minimizes ||A x - y||^2 + alpha ||x||^2, and A x_alpha = H_alpha y with
the influence matrix H_alpha = A (A^T A + alpha I)^(-1) A^T. UPRE minimizes

    U(alpha) = (1/m) ||(I - H_alpha) y||^2 + (2 sigma^2 / m) trace(H_alpha) - sigma^2,

an unbiased estimate of the predictive risk (1/m) E ||A x_alpha - A x||^2.
With the thin SVD, trace(H_alpha) = sum_i s_i^2 / (s_i^2 + alpha).
"""

import math

from imgla import norm2, svd

INV_PHI = (math.sqrt(5.0) - 1.0) / 2.0


def coefficients(u, s, y):
    """b_i = <u_i, y> for the s_i > 0, and p2 = ||y||^2 - sum b_i^2 (clamped at 0)."""
    m = len(y)
    b = [sum(u[i][k] * y[i] for i in range(m)) for k in range(len(s)) if s[k] > 0.0]
    p2 = max(norm2(y) ** 2 - sum(t * t for t in b), 0.0)
    return b, p2


def upre_function(s, b, p2, m, sigma, alpha):
    """U(alpha) from the SVD data."""
    res2 = p2
    tr = 0.0
    for si, bi in zip(s, b):
        f = si * si / (si * si + alpha)
        res2 += (1.0 - f) ** 2 * bi * bi
        tr += f
    return res2 / m + 2.0 * sigma * sigma * tr / m - sigma * sigma


def predictive_risk(s, c, m, sigma, alpha):
    """The exact predictive risk (1/m) E ||A x_alpha - A x||^2 when c_i = <u_i, A x> are known.

    It equals (1/m) [sum_i (1 - f_i)^2 c_i^2 + sigma^2 sum_i f_i^2].
    """
    tot = 0.0
    for si, ci in zip(s, c):
        f = si * si / (si * si + alpha)
        tot += (1.0 - f) ** 2 * ci * ci + sigma * sigma * f * f
    return tot / m


def tikhonov_svd(s, v, b, alpha):
    """x_alpha = sum_i s_i b_i / (s_i^2 + alpha) v_i."""
    n = len(v)
    x = [0.0] * n
    for k, (si, bi) in enumerate(zip(s, b)):
        c = si * bi / (si * si + alpha)
        for j in range(n):
            x[j] += c * v[j][k]
    return x


def upre_tikhonov(u, s, v, y, sigma, alpha_min=None, alpha_max=None, points=60, eps=1e-6):
    """Return (alpha, x, U(alpha)) for the UPRE choice of the Tikhonov parameter.

    A geometric grid of `points` values on [alpha_min, alpha_max] (by default
    [s_r^2, s_1^2]), then golden-section search in log alpha between the
    neighbours of the best grid point.
    """
    m = len(y)
    s = [si for si in s if si > 0.0]
    b, p2 = coefficients(u, s, y)  # @line L1

    def g(t):  # @line L2
        return upre_function(s, b, p2, m, sigma, math.exp(t))

    lo_t = math.log(alpha_min if alpha_min is not None else s[-1] ** 2)
    hi_t = math.log(alpha_max if alpha_max is not None else s[0] ** 2)
    ts = [lo_t + (hi_t - lo_t) * j / (points - 1) for j in range(points)]  # @line L3
    gs = [g(t) for t in ts]
    j = min(range(points), key=lambda i: gs[i])  # @line L4
    a, c = ts[max(j - 1, 0)], ts[min(j + 1, points - 1)]  # @line L5
    best_t, best_g = ts[j], gs[j]
    t1, t2 = c - INV_PHI * (c - a), a + INV_PHI * (c - a)
    g1, g2 = g(t1), g(t2)
    while c - a > eps:  # @line L6
        if g1 <= g2:  # @line L7
            c, t2, g2 = t2, t1, g1
            t1 = c - INV_PHI * (c - a)
            g1 = g(t1)
        else:
            a, t1, g1 = t1, t2, g2
            t2 = a + INV_PHI * (c - a)
            g2 = g(t2)
        for t, gv in ((t1, g1), (t2, g2)):  # @line L8
            if gv < best_g:
                best_t, best_g = t, gv
    alpha = math.exp(best_t)  # @line L9
    return alpha, tikhonov_svd(s, v, b, alpha), best_g  # @line L10


def upre_tikhonov_matrix(a, y, sigma, **kw):
    """The same for a dense matrix: compute the SVD, then call upre_tikhonov."""
    u, s, v = svd(a)
    return upre_tikhonov(u, s, v, y, sigma, **kw)


def upre_tsvd(u, s, y, sigma):
    """The discrete rule for TSVD (Mallows' C_L): minimize (1/m) ||r_k||^2 + 2 sigma^2 k / m - sigma^2.

    Returns (k, list of U(k)) for k = 0..r.
    """
    m = len(y)
    s = [si for si in s if si > 0.0]
    b, p2 = coefficients(u, s, y)
    res2 = p2 + sum(t * t for t in b)
    vals = []
    for k in range(0, len(s) + 1):
        if k > 0:
            res2 -= b[k - 1] ** 2
        vals.append(max(res2, 0.0) / m + 2.0 * sigma * sigma * k / m - sigma * sigma)
    k = min(range(len(vals)), key=lambda i: vals[i])
    return k, vals
