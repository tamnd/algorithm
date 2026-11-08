# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gauss-hermite-quadrature/. The authors are listed in prov/VYBGF4.jsonl.

"""Gauss-Hermite quadrature for the weight e^(-x^2) on the real line.

The n-point rule is exact for polynomials of degree at most 2n - 1. The nodes are
the eigenvalues of the Jacobi matrix of the Hermite recurrence (alpha_k = 0,
beta_0 = sqrt(pi), beta_k = k/2), found by Sturm-count bisection; the weights are
sqrt(pi) / |v|^2 for the eigenvector v with v_0 = 1. The weights fall off like
e^(-x^2), so they are also returned as logarithms.
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


def hermite_recurrence(n: int) -> Tuple[List[float], List[float]]:
    """alpha_k = 0, beta_0 = sqrt(pi), beta_k = k / 2, for k < n."""
    return [0.0] * n, [math.sqrt(math.pi)] + [k / 2.0 for k in range(1, n)]


def gauss_hermite_log(n: int) -> Tuple[List[float], List[float]]:
    """Nodes (increasing) and log weights of the n-point Gauss-Hermite rule.

    Precondition: n >= 1. Cost: O(n^2) operations, no integrand evaluations.
    """
    # @line L1
    if n < 1:
        raise ValueError("need n >= 1")
    # @line L2
    alpha, beta = hermite_recurrence(n)
    # @line L3
    d, e2 = alpha, beta[1:]
    # @line L4
    # @line L5
    nodes, logw = _eigen_tridiagonal(d, e2, 0.5 * math.log(math.pi))
    # @line L6
    for j in range(n // 2):  # impose the exact symmetry x_j = -x_(n+1-j)
        m = 0.5 * (nodes[n - 1 - j] - nodes[j])
        lw = 0.5 * (logw[j] + logw[n - 1 - j])
        nodes[j], nodes[n - 1 - j] = -m, m
        logw[j] = logw[n - 1 - j] = lw
    if n % 2 == 1:
        nodes[n // 2] = 0.0
    # @line L7
    return nodes, logw


def gauss_hermite(n: int) -> Tuple[List[float], List[float]]:
    """Nodes and weights; weights below about 1e-308 underflow to 0."""
    x, lw = gauss_hermite_log(n)
    return x, [math.exp(t) for t in lw]


def integrate(f, n: int) -> float:
    """Integral of e^(-x^2) f(x) over the real line by the n-point rule (n evaluations)."""
    x, w = gauss_hermite(n)
    return math.fsum(wi * f(xi) for xi, wi in zip(x, w) if wi > 0.0)


def expectation(f, n: int, mu: float = 0.0, sigma: float = 1.0) -> float:
    """E[f(X)] for X normal with mean mu and standard deviation sigma > 0.

    Substitutes X = mu + sqrt(2) sigma x, so E[f(X)] = pi^(-1/2) * integral e^(-x^2) f(mu + sqrt(2) sigma x).
    """
    if not sigma > 0.0:
        raise ValueError("need sigma > 0")
    s = math.sqrt(2.0) * sigma
    return integrate(lambda t: f(mu + s * t), n) / math.sqrt(math.pi)


def integrate_plain(g, n: int, center: float = 0.0, width: float = 1.0) -> float:
    """Integral of g over the real line with modified weights w_i e^(x_i^2).

    Substitutes x = center + width t; suits integrands that decay like a Gaussian of
    that center and width. The modified weights are formed from log weights.
    """
    if not width > 0.0:
        raise ValueError("need width > 0")
    t, lw = gauss_hermite_log(n)
    return width * math.fsum(math.exp(lwi + ti * ti) * g(center + width * ti) for ti, lwi in zip(t, lw))
