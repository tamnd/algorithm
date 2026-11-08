# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gauss-radau-quadrature/. The authors are listed in prov/T8RETN.jsonl.

"""Gauss-Radau quadrature: an n-point rule with one prescribed endpoint node.

The weight w is given by the recurrence coefficients of its monic orthogonal
polynomials, pi_{k+1} = (x - alpha_k) pi_k - beta_k pi_{k-1}, beta_0 = integral of w.
Golub's construction replaces alpha_{n-1} by

    alpha' = a - beta_{n-1} pi_{n-2}(a) / pi_{n-1}(a),

so that the fixed point a becomes an eigenvalue of the modified Jacobi matrix.
The eigenvalues are the Radau nodes, found here by Sturm-count bisection, and
the weights are beta_0 v_0^2 / |v|^2 for the eigenvector v, computed by the
recurrence. The rule is exact for polynomials of degree at most 2n - 2.
"""

import math
from typing import List, Sequence, Tuple

U = 2.0 ** -53


def legendre_recurrence(n: int) -> Tuple[List[float], List[float]]:
    """w = 1 on [-1, 1]."""
    return [0.0] * n, [2.0] + [k * k / (4.0 * k * k - 1.0) for k in range(1, n)]


def laguerre_recurrence(n: int, a: float = 0.0) -> Tuple[List[float], List[float]]:
    """w = x^a e^(-x) on (0, infinity)."""
    return [2.0 * k + a + 1.0 for k in range(n)], [math.gamma(a + 1.0)] + [k * (k + a) for k in range(1, n)]


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


def _eigen_tridiagonal(d: Sequence[float], e2: Sequence[float], mu0: float) -> Tuple[List[float], List[float]]:
    """Eigenvalues by bisection; weights mu0 v_0^2/|v|^2 from the eigenvector recurrence. O(n^2)."""
    n = len(d)
    e = [math.sqrt(t) for t in e2]
    lo = min(d[k] - (e[k - 1] if k > 0 else 0.0) - (e[k] if k < n - 1 else 0.0) for k in range(n))
    hi = max(d[k] + (e[k - 1] if k > 0 else 0.0) + (e[k] if k < n - 1 else 0.0) for k in range(n))
    span = hi - lo + 1e-300
    lo, hi = lo - U * span - 1e-300, hi + U * span + 1e-300
    nodes, weights = [], []
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
        v_prev, v = 0.0, 1.0
        s = [1.0]
        for k in range(n - 1):
            v_prev, v = v, ((x - d[k]) * v - (e[k - 1] * v_prev if k > 0 else 0.0)) / e[k]
            s.append(v * v)
        nodes.append(x)
        weights.append(mu0 / math.fsum(s))
    return nodes, weights


def gauss_radau(n: int, fixed: float = -1.0, alpha: Sequence[float] = None,
                beta: Sequence[float] = None) -> Tuple[List[float], List[float]]:
    """Nodes (increasing) and weights of the n-point Gauss-Radau rule with the node `fixed`.

    Default weight: w = 1 on [-1, 1]. Otherwise pass n recurrence coefficients.
    Precondition: n >= 1; `fixed` is an endpoint of the support of w (or outside it).
    Cost: O(n^2) operations; no evaluations of the integrand.
    """
    if n < 1:
        raise ValueError("n must be at least 1")
    if alpha is None or beta is None:
        alpha, beta = legendre_recurrence(n)
    if len(alpha) < n or len(beta) < n or any(not (beta[k] > 0.0) for k in range(n)):
        raise ValueError("need n recurrence coefficients with beta_k > 0")
    # @line L1
    if n == 1:
        return [float(fixed)], [float(beta[0])]
    # @line L2
    r = fixed - alpha[0]  # r_k = pi_k(a) / pi_{k-1}(a)
    for k in range(1, n - 1):
        r = (fixed - alpha[k]) - beta[k] / r
    if r == 0.0:
        raise ValueError("the fixed node is a zero of pi_(n-1); it must be an endpoint")
    # @line L3
    alpha_mod = fixed - beta[n - 1] / r
    # @line L4
    d = [float(alpha[k]) for k in range(n - 1)] + [alpha_mod]
    e2 = [float(beta[k]) for k in range(1, n)]
    # @line L5
    nodes, weights = _eigen_tridiagonal(d, e2, beta[0])
    # @line L6
    j = min(range(n), key=lambda i: abs(nodes[i] - fixed))
    nodes[j] = float(fixed)
    # @line L7
    return nodes, weights


def integrate(f, a: float, b: float, n: int, fixed_left: bool = True) -> float:
    """Integral of f over [a, b] by the mapped n-point Legendre-Radau rule (n evaluations)."""
    if a == b:
        return 0.0
    x, w = gauss_radau(n, -1.0 if fixed_left else 1.0)
    c, h = 0.5 * (a + b), 0.5 * (b - a)
    return h * math.fsum(wi * f(c + h * xi) for xi, wi in zip(x, w))
