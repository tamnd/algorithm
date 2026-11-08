# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gauss-lobatto-quadrature/. The authors are listed in prov/4NBTQ5.jsonl.

"""Gauss-Lobatto quadrature: an n-point rule whose first and last nodes are the endpoints.

The weight w is given by the recurrence coefficients of its monic orthogonal
polynomials, pi_{k+1} = (x - alpha_k) pi_k - beta_k pi_{k-1}, beta_0 = integral of w.
Golub's construction replaces alpha_{n-1} by alpha' and beta_{n-1} by beta', chosen
so that both endpoints l < r become eigenvalues of the modified Jacobi matrix:

    beta'  = (l - r) / (1/r_l - 1/r_r),   alpha' = l - beta' / r_l,

where r_c = pi_{n-1}(c) / pi_{n-2}(c). The eigenvalues are the Lobatto nodes, found
here by Sturm-count bisection, and the weights are beta_0 / |v|^2 for the eigenvector
v with v_0 = 1. The rule is exact for polynomials of degree at most 2n - 3.
"""

import math
from typing import List, Sequence, Tuple

U = 2.0 ** -53


def legendre_recurrence(n: int) -> Tuple[List[float], List[float]]:
    """w = 1 on [-1, 1]."""
    return [0.0] * n, [2.0] + [k * k / (4.0 * k * k - 1.0) for k in range(1, n)]


def chebyshev_recurrence(n: int) -> Tuple[List[float], List[float]]:
    """w = (1 - x^2)^(-1/2) on (-1, 1)."""
    return [0.0] * n, ([math.pi, 0.5] + [0.25] * (n - 2))[:n]


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
    """Eigenvalues by bisection; weights mu0 / |v|^2 from the eigenvector recurrence with v_0 = 1. O(n^2)."""
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


def _ratio(c: float, alpha: Sequence[float], beta: Sequence[float], m: int) -> float:
    """pi_m(c) / pi_{m-1}(c) by r_1 = c - alpha_0, r_{k+1} = c - alpha_k - beta_k / r_k."""
    r = c - alpha[0]
    for k in range(1, m):
        r = (c - alpha[k]) - beta[k] / r
    return r


def gauss_lobatto(n: int, left: float = -1.0, right: float = 1.0, alpha: Sequence[float] = None,
                  beta: Sequence[float] = None) -> Tuple[List[float], List[float]]:
    """Nodes (increasing) and weights of the n-point Gauss-Lobatto rule with nodes `left` and `right`.

    Default weight: w = 1 on [-1, 1]. Otherwise pass n recurrence coefficients
    (only the first n - 1 are used). Precondition: n >= 2 and left < right are the
    endpoints of the support of w (or lie outside it). Cost: O(n^2) operations.
    """
    if n < 2:
        raise ValueError("a Lobatto rule needs n >= 2 nodes")
    if not left < right:
        raise ValueError("need left < right")
    if alpha is None or beta is None:
        alpha, beta = legendre_recurrence(n)
    if len(alpha) < n - 1 or len(beta) < n - 1 or any(not (beta[k] > 0.0) for k in range(n - 1)):
        raise ValueError("need n - 1 recurrence coefficients with beta_k > 0")
    # @line L1
    r_l = _ratio(left, alpha, beta, n - 1)
    r_r = _ratio(right, alpha, beta, n - 1)
    if r_l == 0.0 or r_r == 0.0:
        raise ValueError("an endpoint is a zero of pi_(n-1); the fixed nodes must be endpoints")
    # @line L2
    beta_mod = (left - right) / (1.0 / r_l - 1.0 / r_r)
    if not beta_mod > 0.0:
        raise ValueError("the fixed nodes must enclose the support of w")
    # @line L3
    alpha_mod = left - beta_mod / r_l
    # @line L4
    d = [float(alpha[k]) for k in range(n - 1)] + [alpha_mod]
    e2 = [float(beta[k]) for k in range(1, n - 1)] + [beta_mod]
    # @line L5
    nodes, weights = _eigen_tridiagonal(d, e2, beta[0])
    # @line L6
    nodes[0], nodes[-1] = float(left), float(right)
    # @line L7
    return nodes, weights


def integrate(f, a: float, b: float, n: int) -> float:
    """Integral of f over [a, b] by the mapped n-point Legendre-Lobatto rule (n evaluations)."""
    if a == b:
        return 0.0
    x, w = gauss_lobatto(n)
    c, h = 0.5 * (a + b), 0.5 * (b - a)
    return h * math.fsum(wi * f(c + h * xi) for xi, wi in zip(x, w))


def composite(f, a: float, b: float, n: int, m: int) -> Tuple[float, int]:
    """Composite n-point Lobatto rule on m panels of width h = (b - a)/m.

    Neighbouring panels share an endpoint, which is evaluated once.
    Returns (value, evaluations) with evaluations = m (n - 1) + 1.
    """
    if m < 1:
        raise ValueError("need m >= 1 panels")
    x, w = gauss_lobatto(n)
    h = (b - a) / m
    ends = [a + p * h for p in range(m)] + [b]
    fe = [f(t) for t in ends]
    terms = [0.5 * h * w[0] * fe[0], 0.5 * h * w[-1] * fe[m]]
    terms += [h * w[0] * fe[p] for p in range(1, m)]  # w[0] = w[-1]: two panels meet here
    for p in range(m):
        c = ends[p] + 0.5 * h
        terms += [0.5 * h * w[i] * f(c + 0.5 * h * x[i]) for i in range(1, n - 1)]
    return math.fsum(terms), (m + 1) + m * (n - 2)
