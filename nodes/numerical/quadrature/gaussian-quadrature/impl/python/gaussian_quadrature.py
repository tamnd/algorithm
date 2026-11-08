# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gaussian-quadrature/. The authors are listed in prov/CMS5QF.jsonl.

"""Gaussian quadrature for a general weight, from the three-term recurrence.

The weight w enters only through its recurrence coefficients. The monic
orthogonal polynomials satisfy

    pi_{k+1}(x) = (x - alpha_k) pi_k(x) - beta_k pi_{k-1}(x),  pi_0 = 1, pi_{-1} = 0,

with beta_0 = integral of w. The n nodes are the zeros of pi_n, which are the
eigenvalues of the symmetric tridiagonal Jacobi matrix J_n with diagonal
alpha_0..alpha_{n-1} and off-diagonal sqrt(beta_1)..sqrt(beta_{n-1}). They are
found by Sturm-count bisection. The weights are the Christoffel numbers
lambda_j = 1 / sum_{k<n} p_k(x_j)^2, with p_k the orthonormal polynomials.
"""

import math
from typing import Callable, List, Sequence, Tuple

U = 2.0 ** -53  # unit roundoff of IEEE double precision


def sturm_count(alpha: Sequence[float], beta: Sequence[float], n: int, x: float) -> int:
    """Number of eigenvalues of J_n that are smaller than x.

    It counts the negative pivots of the LDL^T factorization of J_n - x I
    (Sylvester's law of inertia). Cost: O(n) operations.
    """
    count = 0
    d = 1.0
    for k in range(n):
        d = (alpha[k] - x) - (beta[k] / d if k > 0 else 0.0)
        if d == 0.0:
            d = -1e-300  # a zero pivot is moved to the negative side
        if d < 0.0:
            count += 1
    return count


def orthonormal_values(alpha: Sequence[float], beta: Sequence[float], n: int, x: float) -> List[float]:
    """Values p_0(x), ..., p_{n-1}(x) of the orthonormal polynomials. Cost: O(n)."""
    p = [0.0] * n
    p_prev, p_cur = 0.0, 1.0 / math.sqrt(beta[0])
    p[0] = p_cur
    for k in range(n - 1):
        p_next = ((x - alpha[k]) * p_cur - (math.sqrt(beta[k]) * p_prev if k > 0 else 0.0)) / math.sqrt(beta[k + 1])
        p_prev, p_cur = p_cur, p_next
        p[k + 1] = p_cur
    return p


def gauss_rule(alpha: Sequence[float], beta: Sequence[float], n: int) -> Tuple[List[float], List[float]]:
    """Nodes and weights of the n-point Gauss rule for the weight with these coefficients.

    Precondition: n >= 1, len(alpha) >= n, len(beta) >= n, beta[k] > 0 for k < n,
    and beta[0] equal to the integral of the weight.
    Cost: O(n^2) operations (about 110 Sturm counts of O(n) for each node);
    no evaluations of the integrand.
    Returns nodes in increasing order and the matching positive weights.
    """
    # @line L1
    if n < 1 or len(alpha) < n or len(beta) < n:
        raise ValueError("need n >= 1 and n recurrence coefficients")
    if any(not (beta[k] > 0.0) for k in range(n)):
        raise ValueError("beta_k must be positive")
    # @line L2
    lo, hi = math.inf, -math.inf
    for k in range(n):
        r = (math.sqrt(beta[k]) if k > 0 else 0.0) + (math.sqrt(beta[k + 1]) if k + 1 < n else 0.0)
        lo = min(lo, alpha[k] - r)
        hi = max(hi, alpha[k] + r)
    span = hi - lo
    lo -= U * span + 1e-300
    hi += U * span + 1e-300
    nodes: List[float] = []
    weights: List[float] = []
    # @line L3
    for j in range(n):
        # @line L4
        left = max(lo, nodes[-1]) if nodes else lo
        right = hi
        # @line L5
        while right - left > 4.0 * U * max(abs(left), abs(right)) and right - left > U * U * span:
            # @line L6
            mid = 0.5 * (left + right)
            if mid <= left or mid >= right:
                break
            # @line L7
            if sturm_count(alpha, beta, n, mid) >= j + 1:
                right = mid
            else:
                left = mid
        # @line L8
        x = 0.5 * (left + right)
        # @line L9
        p = orthonormal_values(alpha, beta, n, x)
        # @line L10
        nodes.append(x)
        weights.append(1.0 / math.fsum(v * v for v in p))
    # @line L11
    return nodes, weights


def apply_rule(f: Callable[[float], float], nodes: Sequence[float], weights: Sequence[float]) -> float:
    """Q_n(f) = sum of w_i f(x_i), summed with math.fsum. Cost: n evaluations of f."""
    return math.fsum(w * f(x) for x, w in zip(nodes, weights))


# Recurrence coefficients of the classical weights (alpha_k, beta_k for k < n).

def legendre_recurrence(n: int) -> Tuple[List[float], List[float]]:
    """w = 1 on [-1, 1]."""
    return [0.0] * n, [2.0] + [k * k / (4.0 * k * k - 1.0) for k in range(1, n)]


def chebyshev_recurrence(n: int) -> Tuple[List[float], List[float]]:
    """w = (1 - x^2)^(-1/2) on [-1, 1]."""
    return [0.0] * n, [math.pi] + [0.5 if k == 1 else 0.25 for k in range(1, n)]


def laguerre_recurrence(n: int, a: float = 0.0) -> Tuple[List[float], List[float]]:
    """w = x^a e^(-x) on (0, infinity), a > -1."""
    return [2.0 * k + a + 1.0 for k in range(n)], [math.gamma(a + 1.0)] + [k * (k + a) for k in range(1, n)]


def hermite_recurrence(n: int) -> Tuple[List[float], List[float]]:
    """w = e^(-x^2) on the real line."""
    return [0.0] * n, [math.sqrt(math.pi)] + [k / 2.0 for k in range(1, n)]


def gauss_legendre_on(f: Callable[[float], float], a: float, b: float, n: int) -> float:
    """Integral of f over [a, b] (finite, any order) by the n-point Gauss-Legendre rule."""
    if a == b:
        return 0.0
    x, w = gauss_rule(*legendre_recurrence(n), n)
    c, h = 0.5 * (a + b), 0.5 * (b - a)
    return h * math.fsum(wi * f(c + h * xi) for xi, wi in zip(x, w))
