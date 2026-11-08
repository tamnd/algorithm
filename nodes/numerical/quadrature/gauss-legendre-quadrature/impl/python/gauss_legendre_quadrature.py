# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gauss-legendre-quadrature/. The authors are listed in prov/ACS9SM.jsonl.

"""Gauss-Legendre quadrature by safeguarded Newton iteration on P_n.

The n nodes are the zeros of the Legendre polynomial P_n on (-1, 1) and the
weights are w_i = 2 / ((1 - x_i^2) P_n'(x_i)^2). Writing x_i = cos(theta_i) with
the nodes in decreasing order, each theta_i lies in the interval
((i - 1/2) pi / (n + 1/2), i pi / (n + 1/2)) (Bruns' inequality), which brackets
exactly one zero. Newton's method starts at the middle of that interval and
falls back to bisection whenever a step leaves the bracket.
"""

import math
from typing import Callable, List, Tuple


def legendre_pair(n: int, x: float) -> Tuple[float, float]:
    """(P_n(x), P_{n-1}(x)) by the three-term recurrence. Cost: O(n)."""
    p_prev, p = 1.0, x  # P_0, P_1
    if n == 0:
        return 1.0, 0.0
    for k in range(1, n):
        p_prev, p = p, ((2 * k + 1) * x * p - k * p_prev) / (k + 1)
    return p, p_prev


def gauss_legendre(n: int, max_iter: int = 100) -> Tuple[List[float], List[float]]:
    """Nodes (increasing) and weights of the n-point Gauss-Legendre rule on [-1, 1].

    Precondition: n >= 1.
    Cost: O(n) per Newton step for each node, a few steps per node, so O(n^2)
    operations; the symmetric half is mirrored.
    """
    if n < 1:
        raise ValueError("n must be at least 1")
    x_out = [0.0] * n
    w_out = [0.0] * n
    # @line L1
    for i in range(1, n // 2 + 1):
        # @line L2
        lo = math.cos(i * math.pi / (n + 0.5))
        hi = math.cos((i - 0.5) * math.pi / (n + 0.5))
        x = math.cos((i - 0.25) * math.pi / (n + 0.5))
        p_lo = legendre_pair(n, lo)[0]
        dp = 0.0
        # @line L3
        for _ in range(max_iter):
            # @line L4
            p, q = legendre_pair(n, x)
            # @line L5
            dp = n * (x * p - q) / ((x - 1.0) * (x + 1.0))
            # @line L6
            if p == 0.0:
                break
            if (p < 0.0) == (p_lo < 0.0):
                lo, p_lo = x, p
            else:
                hi = x
            step = p / dp
            # @line L7
            if abs(step) <= 2.0 * 2.0 ** -53 * abs(x):
                x -= step
                break
            x_new = x - step
            if not (lo < x_new < hi):
                x_new = 0.5 * (lo + hi)
            x = x_new
        p, q = legendre_pair(n, x)
        dp = n * (x * p - q) / ((x - 1.0) * (x + 1.0))
        # @line L8
        w = 2.0 / ((1.0 - x) * (1.0 + x) * dp * dp)
        # @line L9
        x_out[n - i], w_out[n - i] = x, w
        x_out[i - 1], w_out[i - 1] = -x, w
    # @line L10
    if n % 2 == 1:
        p, q = legendre_pair(n, 0.0)
        dp = n * (0.0 * p - q) / -1.0
        x_out[n // 2], w_out[n // 2] = 0.0, 2.0 / (dp * dp)
    # @line L11
    return x_out, w_out


def integrate(f: Callable[[float], float], a: float, b: float, n: int) -> float:
    """Integral of f over [a, b] by the n-point Gauss-Legendre rule (n evaluations).

    Works for a = b (returns 0) and for b < a (the sign changes).
    """
    if a == b:
        return 0.0
    x, w = gauss_legendre(n)
    c, h = 0.5 * (a + b), 0.5 * (b - a)
    return h * math.fsum(wi * f(c + h * xi) for xi, wi in zip(x, w))


def composite(f: Callable[[float], float], a: float, b: float, n: int, m: int) -> float:
    """Composite rule: the n-point rule on each of m panels of width h = (b - a)/m (n m evaluations)."""
    if m < 1:
        raise ValueError("m must be at least 1")
    x, w = gauss_legendre(n)
    h = (b - a) / m
    terms = []
    for j in range(m):
        c = a + (j + 0.5) * h
        terms.extend(0.5 * h * wi * f(c + 0.5 * h * xi) for xi, wi in zip(x, w))
    return math.fsum(terms)
