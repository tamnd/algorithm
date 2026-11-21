# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lepskii-balancing-principle/. The authors are listed in prov/WKH6V6.jsonl.
"""The Lepskii balancing principle for Tikhonov regularization.

Model: y = A x + e with ||e|| <= delta. Tikhonov: x_alpha minimizes
||A x - y||^2 + alpha ||x||^2. The noise part of the error is bounded by
psi(alpha) = delta / (2 sqrt(alpha)), because s / (s^2 + alpha) <= 1 / (2 sqrt(alpha)).

On a grid alpha_1 < alpha_2 < ... < alpha_N the rule takes the largest j with
||x_{alpha_j} - x_{alpha_i}|| <= 4 kappa psi(alpha_i) for every i < j
(kappa >= 1 is a safety factor; kappa = 1 is the plain rule).
"""

import math

from imgla import norm2, svd


def coefficients(u, s, y):
    """b_i = <u_i, y> for the s_i > 0."""
    m = len(y)
    return [sum(u[i][k] * y[i] for i in range(m)) for k in range(len(s)) if s[k] > 0.0]


def noise_bound(delta, alpha):
    """psi(alpha) = delta / (2 sqrt(alpha)): the bound on ||(A^T A + alpha I)^(-1) A^T e||."""
    return delta / (2.0 * math.sqrt(alpha))


def geometric_grid(alpha_min, alpha_max, ratio):
    """alpha_min, alpha_min * ratio, ... up to the first value >= alpha_max."""
    out = [alpha_min]
    while out[-1] < alpha_max:
        out.append(out[-1] * ratio)
    return out


def tikhonov_coeffs(s, b, alpha):
    """The coefficients of x_alpha in the basis v_i: s_i b_i / (s_i^2 + alpha)."""
    return [si * bi / (si * si + alpha) for si, bi in zip(s, b)]


def tikhonov_svd(s, v, b, alpha):
    """x_alpha = sum_i s_i b_i / (s_i^2 + alpha) v_i."""
    n = len(v)
    c = tikhonov_coeffs(s, b, alpha)
    return [sum(c[k] * v[j][k] for k in range(len(c))) for j in range(n)]


def balancing(u, s, v, y, delta, alphas=None, kappa=1.0, ratio=1.5):
    """Return (alpha, x, j) for the balancing principle on the increasing grid alphas.

    By default the grid runs from (s_r^2) / 100 to s_1^2 with the given ratio.
    Index j is 0-based. The scan goes from the largest alpha down and stops at
    the first admissible index, which is the largest one.
    """
    s = [si for si in s if si > 0.0]
    b = coefficients(u, s, y)  # @line L1
    if alphas is None:
        alphas = geometric_grid(s[-1] ** 2 / 100.0, s[0] ** 2, ratio)
    coeffs = [tikhonov_coeffs(s, b, a) for a in alphas]  # @line L2
    psi = [noise_bound(delta, a) for a in alphas]  # @line L3
    for j in range(len(alphas) - 1, -1, -1):  # @line L4
        ok = True
        for i in range(j):  # @line L5
            dist = math.sqrt(sum((p - q) ** 2 for p, q in zip(coeffs[j], coeffs[i])))
            if dist > 4.0 * kappa * psi[i]:  # @line L6
                ok = False
                break
        if ok:  # @line L7
            return alphas[j], tikhonov_svd(s, v, b, alphas[j]), j  # @line L8
    raise AssertionError("index 0 is always admissible")


def balancing_matrix(a, y, delta, **kw):
    """The same for a dense matrix: compute the SVD, then call balancing."""
    u, s, v = svd(a)
    return balancing(u, s, v, y, delta, **kw)


def bias_norms(s, v, xt, alphas):
    """phi(alpha) = ||x_alpha^0 - x_true|| for exact data y = A x_true (an oracle, for tests).

    With c_i = <v_i, x_true>, x_alpha^0 - x_true has the coefficients
    -alpha / (s_i^2 + alpha) c_i on v_i, plus the part of x_true outside the
    span of the v_i, which no alpha changes.
    """
    n = len(xt)
    s = [si for si in s if si > 0.0]
    c = [sum(v[j][k] * xt[j] for j in range(n)) for k in range(len(s))]
    out2 = max(norm2(xt) ** 2 - sum(t * t for t in c), 0.0)
    res = []
    for a in alphas:
        tot = out2
        for si, ci in zip(s, c):
            tot += (a / (si * si + a) * ci) ** 2
        res.append(math.sqrt(tot))
    return res
