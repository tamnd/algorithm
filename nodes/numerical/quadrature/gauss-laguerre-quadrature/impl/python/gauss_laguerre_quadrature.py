# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gauss-laguerre-quadrature/. The authors are listed in prov/B0FCH8.jsonl.

"""Gauss-Laguerre quadrature for the weight x^a e^(-x) on (0, infinity), a > -1.

The n-point rule is exact for polynomials of degree at most 2n - 1. The nodes are
the eigenvalues of the Jacobi matrix of the Laguerre recurrence (Sturm-count
bisection); the weights are Gamma(a + 1) / |v|^2 for the eigenvector v with v_0 = 1.
The weights fall off like e^(-x), so they are also returned as logarithms; for an
integrand without the factor e^(-x), the "modified" weights w_i e^(x_i) are used.
"""

import math
from typing import List, Sequence, Tuple

U = 2.0 ** -53


def _count(d: Sequence[float], e2: Sequence[float], x: float) -> int:
    """Number of eigenvalues below x of the tridiagonal matrix (diag d, squared off-diagonal e2)."""
    c, piv = 0, 1.0
    for k in range(len(d)):
        piv = (d[k] - x) - (e2[k - 1] / piv if k > 0 else 0.0)
        if piv == 0.0:
            piv = -1e-300
        if piv < 0.0:
            c += 1
    return c


def _eigen_tridiagonal(d: Sequence[float], e2: Sequence[float], log_mu0: float) -> Tuple[List[float], List[float]]:
    """Eigenvalues by Sturm bisection, and log weights log(mu0 / |v|^2) with v_0 = 1.

    The eigenvector recurrence is rescaled when it grows, so tiny weights are
    returned as finite logarithms instead of overflowing. O(n^2) operations.
    """
    n = len(d)
    e = [math.sqrt(t) for t in e2]
    lo = min(d[k] - (e[k - 1] if k > 0 else 0.0) - (e[k] if k < n - 1 else 0.0) for k in range(n))
    hi = max(d[k] + (e[k - 1] if k > 0 else 0.0) + (e[k] if k < n - 1 else 0.0) for k in range(n))
    span = hi - lo + 1e-300
    lo, hi = lo - U * span - 1e-300, hi + U * span + 1e-300
    nodes, logw = [], []
    for j in range(n):
        left, right = (max(lo, nodes[-1]) if nodes else lo), hi
        while right - left > 4.0 * U * max(abs(left), abs(right)) and right - left > U * U * span:
            mid = 0.5 * (left + right)
            if mid <= left or mid >= right:
                break
            if _count(d, e2, mid) >= j + 1:
                right = mid
            else:
                left = mid
        x = 0.5 * (left + right)
        v_prev, v, s, scale = 0.0, 1.0, [1.0], 0.0  # true v = v * exp(scale)
        for k in range(n - 1):
            v_prev, v = v, ((x - d[k]) * v - (e[k - 1] * v_prev if k > 0 else 0.0)) / e[k]
            if abs(v) > 1e100:
                v, v_prev = v * 1e-100, v_prev * 1e-100
                s = [t * 1e-200 for t in s]
                scale += 100.0 * math.log(10.0)
            s.append(v * v)
        nodes.append(x)
        logw.append(log_mu0 - math.log(math.fsum(s)) - 2.0 * scale)
    return nodes, logw


def laguerre_recurrence(n: int, a: float = 0.0) -> Tuple[List[float], List[float]]:
    """alpha_k = 2k + a + 1, beta_0 = Gamma(a + 1), beta_k = k (k + a), for k < n."""
    return [2.0 * k + a + 1.0 for k in range(n)], [math.gamma(a + 1.0)] + [k * (k + a) for k in range(1, n)]


def gauss_laguerre_log(n: int, a: float = 0.0) -> Tuple[List[float], List[float]]:
    """Nodes (increasing) and log weights of the n-point generalized Gauss-Laguerre rule.

    Precondition: n >= 1, a > -1. Cost: O(n^2) operations, no integrand evaluations.
    """
    # @line L1
    if n < 1 or not a > -1.0:
        raise ValueError("need n >= 1 and a > -1")
    # @line L2
    alpha = [2.0 * k + a + 1.0 for k in range(n)]
    beta = [k * (k + a) for k in range(1, n)]
    log_beta0 = math.lgamma(a + 1.0)
    # @line L3
    d, e2 = alpha, beta
    # @line L4
    # @line L5
    nodes, logw = _eigen_tridiagonal(d, e2, log_beta0)
    # @line L6
    return nodes, logw


def gauss_laguerre(n: int, a: float = 0.0) -> Tuple[List[float], List[float]]:
    """Nodes and weights; weights below about 1e-308 underflow to 0."""
    x, lw = gauss_laguerre_log(n, a)
    return x, [math.exp(t) for t in lw]


def integrate(f, n: int, a: float = 0.0) -> float:
    """Integral of x^a e^(-x) f(x) over (0, infinity) by the n-point rule (n evaluations of f)."""
    x, w = gauss_laguerre(n, a)
    return math.fsum(wi * f(xi) for xi, wi in zip(x, w) if wi > 0.0)


def integrate_plain(g, n: int, lo: float = 0.0, rate: float = 1.0) -> float:
    """Integral of g over (lo, infinity) with modified weights w_i e^(x_i).

    Substitutes x = lo + t / rate, so the rule is tuned to integrands that decay like
    e^(-rate (x - lo)). The modified weights are formed from log weights, so they do
    not overflow; they grow with n and only suit integrands that really decay.
    """
    if not rate > 0.0:
        raise ValueError("need rate > 0")
    t, lw = gauss_laguerre_log(n)
    return math.fsum(math.exp(lwi + ti) * g(lo + ti / rate) for ti, lwi in zip(t, lw)) / rate
