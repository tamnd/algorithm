# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gauss-jacobi-quadrature/. The authors are listed in prov/47J4QB.jsonl.

"""Gauss-Jacobi quadrature for the weight (1 - x)^a (1 + x)^b on (-1, 1), a, b > -1.

The n-point rule is exact for polynomials of degree at most 2n - 1. The nodes are
the eigenvalues of the Jacobi matrix built from the three-term recurrence of the
Jacobi polynomials (found by Sturm-count bisection); the weights are beta_0 / |v|^2
for the eigenvector v with v_0 = 1. The weight absorbs algebraic endpoint
singularities, so f only needs to be smooth.
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


def jacobi_recurrence(n: int, a: float, b: float) -> Tuple[List[float], List[float]]:
    """alpha_k, beta_k (k < n) of the monic Jacobi polynomials; beta_0 = integral of the weight."""
    alpha, beta = [], []
    for k in range(n):
        s = 2 * k + a + b
        if k == 0:
            alpha.append((b - a) / (a + b + 2.0))
            beta.append(math.exp((a + b + 1.0) * math.log(2.0) + math.lgamma(a + 1.0)
                                 + math.lgamma(b + 1.0) - math.lgamma(a + b + 2.0)))
        else:
            alpha.append((b * b - a * a) / (s * (s + 2.0)))
            if k == 1:
                beta.append(4.0 * (1.0 + a) * (1.0 + b) / ((2.0 + a + b) ** 2 * (3.0 + a + b)))
            else:
                beta.append(4.0 * k * (k + a) * (k + b) * (k + a + b) / (s * s * (s + 1.0) * (s - 1.0)))
    return alpha, beta


def gauss_jacobi(n: int, a: float = 0.0, b: float = 0.0) -> Tuple[List[float], List[float]]:
    """Nodes (increasing) and weights of the n-point Gauss-Jacobi rule on (-1, 1).

    Precondition: n >= 1, a > -1, b > -1. Cost: O(n^2) operations, no integrand evaluations.
    """
    # @line L1
    if n < 1 or not (a > -1.0 and b > -1.0):
        raise ValueError("need n >= 1 and a, b > -1")
    # @line L2
    alpha, beta = jacobi_recurrence(n, a, b)
    # @line L3
    d, e2 = alpha, beta[1:]
    # @line L4
    # @line L5
    nodes, logw = _eigen_tridiagonal(d, e2, math.log(beta[0]))
    # @line L6
    return nodes, [math.exp(t) for t in logw]


def integrate(f, lo: float, hi: float, n: int, a: float = 0.0, b: float = 0.0) -> float:
    """Integral of (hi - x)^a (x - lo)^b f(x) over [lo, hi] with the mapped n-point rule.

    n evaluations of f, none at the endpoints. Requires lo <= hi.
    """
    if lo == hi:
        return 0.0
    if hi < lo:
        raise ValueError("need lo <= hi: the weight is not defined on a reversed interval")
    x, w = gauss_jacobi(n, a, b)
    half = 0.5 * (hi - lo)
    scale = half ** (a + b + 1.0)
    return scale * math.fsum(wi * f(lo + half * (xi + 1.0)) for xi, wi in zip(x, w))
