# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morozov-discrepancy-principle/. The authors are listed in prov/6BGG92.jsonl.
"""The discrepancy principle of Morozov for Tikhonov regularization.

Tikhonov: x_alpha minimizes ||A x - y||^2 + alpha ||x||^2. With the thin SVD
A = U diag(s) V^T, x_alpha = sum_i s_i b_i / (s_i^2 + alpha) v_i with
b_i = <u_i, y>. The discrepancy principle picks the alpha with
||A x_alpha - y|| = tau delta, where delta bounds the noise norm.

The root is found by a safeguarded Newton method in t = log(alpha): every
second step is a bisection step, so the bracket width halves at least once in
every two steps.
"""

import math

from imgla import norm2, svd


class DiscrepancyFailure(ValueError):
    """No alpha in (0, infinity) reaches the target residual tau * delta."""


def coefficients(u, s, y):
    """b_i = <u_i, y> for the s_i > 0, and p2 = ||y||^2 - sum b_i^2 (clamped at 0)."""
    m = len(y)
    b = [sum(u[i][k] * y[i] for i in range(m)) for k in range(len(s)) if s[k] > 0.0]
    p2 = max(norm2(y) ** 2 - sum(t * t for t in b), 0.0)
    return b, p2


def residual_norm(s, b, p2, alpha):
    """||A x_alpha - y|| from the SVD data, for alpha > 0."""
    tot = p2
    for si, bi in zip(s, b):
        f = alpha / (si * si + alpha)
        tot += f * f * bi * bi
    return math.sqrt(tot)


def tikhonov_svd(s, v, b, alpha):
    """x_alpha = sum_i s_i b_i / (s_i^2 + alpha) v_i (only the s_i > 0 are used)."""
    n = len(v)
    x = [0.0] * n
    for k, (si, bi) in enumerate(zip(s, b)):
        c = si * bi / (si * si + alpha)
        for j in range(n):
            x[j] += c * v[j][k]
    return x


def _f_and_slope(s, b, p2, target2, t):
    """F(t) = ||A x_alpha - y||^2 - target^2 and dF/dt, with alpha = e^t."""
    alpha = math.exp(t)
    f = p2 - target2
    d = 0.0
    for si, bi in zip(s, b):
        q = si * si + alpha
        f += (alpha / q) ** 2 * bi * bi
        d += 2.0 * alpha * alpha * si * si * bi * bi / (q * q * q)
    return f, d


def discrepancy_tikhonov(u, s, v, y, delta, tau=1.1, eps=1e-10, max_steps=1000):
    """Return (alpha, x, steps) with ||A x - y|| = tau * delta, x = x_alpha.

    u, s, v is the thin SVD of A (s descending). Raises DiscrepancyFailure if
    the part of y outside the range of A already has norm >= tau * delta. If
    ||y|| <= tau * delta, returns (math.inf, 0, 0): x = 0 fits the data.
    """
    s = [si for si in s if si > 0.0]
    b, p2 = coefficients(u, s, y)  # @line L1
    target = tau * delta
    if p2 >= target * target:  # @line L2
        raise DiscrepancyFailure("the residual cannot go below tau * delta")
    ynorm = norm2(y)
    if ynorm <= target:  # @line L3
        return math.inf, [0.0] * len(v), 0
    target2 = target * target

    def big_f(t):  # @line L4
        return _f_and_slope(s, b, p2, target2, t)

    q = (1.0 + target / ynorm) / 2.0
    hi = math.log(s[0] * s[0] * q / (1.0 - q))  # @line L5
    lo = math.log(s[-1] * s[-1] * math.sqrt((target2 - p2) / 2.0) / ynorm)  # @line L6
    f_lo, d_lo = big_f(lo)
    f_hi, d_hi = big_f(hi)
    steps = 0
    while steps < max_steps:  # @line L7
        if abs(f_lo) <= abs(f_hi):  # @line L8
            c, fc, dc = lo, f_lo, d_lo
        else:
            c, fc, dc = hi, f_hi, d_hi
        if hi - lo <= eps or abs(fc) <= eps * dc:  # @line L9
            break
        steps += 1
        t = c - fc / dc if dc > 0.0 else lo  # @line L10
        if steps % 2 == 0 or not lo < t < hi:
            t = (lo + hi) / 2.0
        ft, dt = big_f(t)
        if ft > 0.0:  # @line L11
            hi, f_hi, d_hi = t, ft, dt
        else:
            lo, f_lo, d_lo = t, ft, dt
    alpha = math.exp(c)  # @line L12
    return alpha, tikhonov_svd(s, v, b, alpha), steps  # @line L13


def discrepancy_tikhonov_matrix(a, y, delta, tau=1.1, eps=1e-10):
    """The same for a dense matrix A: compute its SVD, then call discrepancy_tikhonov."""
    u, s, v = svd(a)
    return discrepancy_tikhonov(u, s, v, y, delta, tau, eps)


def discrepancy_index(residuals, delta, tau=1.1):
    """The discrete rule: the first k with residuals[k] <= tau * delta, or None."""
    for k, r in enumerate(residuals):
        if r <= tau * delta:
            return k
    return None
