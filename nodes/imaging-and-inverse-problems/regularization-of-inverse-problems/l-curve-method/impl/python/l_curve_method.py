# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/l-curve-method/. The authors are listed in prov/W03DNM.jsonl.
"""The L-curve corner rule for Tikhonov regularization.

The L-curve is the curve (log ||A x_alpha - y||, log ||x_alpha||) for
alpha > 0, where x_alpha minimizes ||A x - y||^2 + alpha ||x||^2. The rule
picks the alpha of largest curvature. With eta = ||x_alpha||^2,
rho = ||A x_alpha - y||^2 and eta' = d eta / d alpha, the curvature is

    kappa = -2 eta rho (alpha eta' rho + alpha^2 eta' eta + eta rho)
            / (eta' (alpha^2 eta^2 + rho^2)^(3/2)),

so it needs no second derivative. Everything comes from the thin SVD.
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


def norms(s, b, p2, alpha):
    """(eta, rho, eta') at alpha: ||x_alpha||^2, ||A x_alpha - y||^2 and d eta / d alpha."""
    eta = rho = deta = 0.0
    for si, bi in zip(s, b):
        q = si * si + alpha
        eta += si * si * bi * bi / (q * q)
        rho += (alpha / q) ** 2 * bi * bi
        deta -= 2.0 * si * si * bi * bi / (q * q * q)
    return eta, rho + p2, deta


def curvature(s, b, p2, alpha):
    """The signed curvature of the L-curve at alpha (positive at the corner)."""
    eta, rho, deta = norms(s, b, p2, alpha)
    num = alpha * deta * rho + alpha * alpha * deta * eta + eta * rho
    return -2.0 * eta * rho * num / (deta * (alpha * alpha * eta * eta + rho * rho) ** 1.5)


def tikhonov_svd(s, v, b, alpha):
    """x_alpha = sum_i s_i b_i / (s_i^2 + alpha) v_i."""
    n = len(v)
    x = [0.0] * n
    for k, (si, bi) in enumerate(zip(s, b)):
        c = si * bi / (si * si + alpha)
        for j in range(n):
            x[j] += c * v[j][k]
    return x


def l_curve_corner(u, s, v, y, alpha_min=None, alpha_max=None, points=60, eps=1e-6):
    """Return (alpha, x, kappa) at the point of largest curvature of the L-curve.

    The search is over [alpha_min, alpha_max], by default [s_r^2, s_1^2]: a
    geometric grid of the given number of points, then golden-section search
    in log alpha between the neighbours of the best grid point.
    """
    s = [si for si in s if si > 0.0]
    b, p2 = coefficients(u, s, y)  # @line L1
    lo_t = math.log(alpha_min if alpha_min is not None else s[-1] ** 2)
    hi_t = math.log(alpha_max if alpha_max is not None else s[0] ** 2)
    ts = [lo_t + (hi_t - lo_t) * j / (points - 1) for j in range(points)]  # @line L2

    def kappa(t):
        return curvature(s, b, p2, math.exp(t))

    ks = [kappa(t) for t in ts]  # @line L3
    j = max(range(points), key=lambda i: ks[i])  # @line L4
    a, c = ts[max(j - 1, 0)], ts[min(j + 1, points - 1)]  # @line L5
    best_t, best_k = ts[j], ks[j]
    t1, t2 = c - INV_PHI * (c - a), a + INV_PHI * (c - a)
    k1, k2 = kappa(t1), kappa(t2)
    while c - a > eps:  # @line L6
        if k1 >= k2:  # @line L7
            c, t2, k2 = t2, t1, k1
            t1 = c - INV_PHI * (c - a)
            k1 = kappa(t1)
        else:
            a, t1, k1 = t1, t2, k2
            t2 = a + INV_PHI * (c - a)
            k2 = kappa(t2)
        for t, k in ((t1, k1), (t2, k2)):  # @line L8
            if k > best_k:
                best_t, best_k = t, k
    alpha = math.exp(best_t)  # @line L9
    return alpha, tikhonov_svd(s, v, b, alpha), best_k  # @line L10


def l_curve_corner_matrix(a, y, **kw):
    """The same for a dense matrix: compute the SVD, then call l_curve_corner."""
    u, s, v = svd(a)
    return l_curve_corner(u, s, v, y, **kw)


def l_curve_points(s, b, p2, alphas):
    """The points (log ||A x_alpha - y||, log ||x_alpha||) for a list of alphas."""
    out = []
    for al in alphas:
        eta, rho, _ = norms(s, b, p2, al)
        out.append((0.5 * math.log(rho), 0.5 * math.log(eta)))
    return out
