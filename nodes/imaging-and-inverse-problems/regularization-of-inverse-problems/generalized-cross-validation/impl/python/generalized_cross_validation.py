# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-cross-validation/. The authors are listed in prov/7S65BE.jsonl.
"""Generalized cross-validation (GCV) for Tikhonov regularization and TSVD.

Tikhonov: x_alpha minimizes ||A x - y||^2 + alpha ||x||^2. The influence
matrix is H_alpha = A (A^T A + alpha I)^(-1) A^T, so A x_alpha = H_alpha y.
GCV picks the alpha that minimizes

    V(alpha) = (1/m) ||(I - H_alpha) y||^2 / [(1/m) trace(I - H_alpha)]^2.

With the thin SVD A = U diag(s) V^T, b_i = <u_i, y> and the filter factors
f_i = s_i^2 / (s_i^2 + alpha), the numerator is the squared residual norm
sum_i (1 - f_i)^2 b_i^2 + p2 and trace(I - H_alpha) = m - sum_i f_i.
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


def gcv_function(s, b, p2, m, alpha):
    """V(alpha) = m ||(I - H) y||^2 / trace(I - H)^2 for Tikhonov, from the SVD data."""
    res2 = p2
    tr = float(m)
    for si, bi in zip(s, b):
        f = si * si / (si * si + alpha)
        res2 += (1.0 - f) ** 2 * bi * bi
        tr -= f
    return m * res2 / (tr * tr)


def tikhonov_svd(s, v, b, alpha):
    """x_alpha = sum_i s_i b_i / (s_i^2 + alpha) v_i."""
    n = len(v)
    x = [0.0] * n
    for k, (si, bi) in enumerate(zip(s, b)):
        c = si * bi / (si * si + alpha)
        for j in range(n):
            x[j] += c * v[j][k]
    return x


def gcv_tikhonov(u, s, v, y, alpha_min=None, alpha_max=None, points=60, eps=1e-6):
    """Return (alpha, x, V(alpha)) for the GCV choice of the Tikhonov parameter.

    The search is a geometric grid of `points` values on [alpha_min, alpha_max]
    (by default [s_r^2, s_1^2]), then golden-section search in log alpha
    between the neighbours of the best grid point.
    """
    m = len(y)
    s = [si for si in s if si > 0.0]
    b, p2 = coefficients(u, s, y)  # @line L1

    def g(t):  # @line L2
        return gcv_function(s, b, p2, m, math.exp(t))

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


def gcv_tikhonov_matrix(a, y, **kw):
    """The same for a dense matrix: compute the SVD, then call gcv_tikhonov."""
    u, s, v = svd(a)
    return gcv_tikhonov(u, s, v, y, **kw)


def gcv_tsvd(u, s, y):
    """The discrete rule for TSVD: the k in 0..min(r, m - 1) that minimizes m ||r_k||^2 / (m - k)^2.

    Returns (k, list of G(k)). The filter factors of TSVD are 1 for i <= k and 0
    after, so trace(I - H_k) = m - k.
    """
    m = len(y)
    s = [si for si in s if si > 0.0]
    b, p2 = coefficients(u, s, y)
    res2 = p2 + sum(t * t for t in b)
    vals = []
    for k in range(0, min(len(s), m - 1) + 1):
        if k > 0:
            res2 -= b[k - 1] ** 2
        vals.append(m * max(res2, 0.0) / ((m - k) ** 2))
    k = min(range(len(vals)), key=lambda i: vals[i])
    return k, vals
