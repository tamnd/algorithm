# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/golub-welsch-algorithm/. The authors are listed in prov/H4E8X2.jsonl.

"""Golub-Welsch algorithm: Gauss nodes and weights from the Jacobi matrix.

The monic orthogonal polynomials of the weight w satisfy

    pi_{k+1}(x) = (x - alpha_k) pi_k(x) - beta_k pi_{k-1}(x),  beta_0 = integral of w.

The Jacobi matrix J_n is symmetric tridiagonal with diagonal alpha_0..alpha_{n-1}
and off-diagonal sqrt(beta_1)..sqrt(beta_{n-1}). Its eigenvalues are the Gauss
nodes, and if v_j is the unit eigenvector for the node x_j, the Gauss weight is
beta_0 * v_j[0]^2. The eigenvalues come from the implicit QL algorithm with a
shift from the 2 x 2 block at the top of the active part; only the first row of
the accumulated rotations is kept, so the whole computation costs O(n^2).
"""

import math
from typing import List, Sequence, Tuple

U = 2.0 ** -53


def golub_welsch(alpha: Sequence[float], beta: Sequence[float], n: int,
                 max_sweeps_per_eigenvalue: int = 60) -> Tuple[List[float], List[float]]:
    """Nodes (increasing) and weights of the n-point Gauss rule.

    Precondition: n >= 1, len(alpha) >= n, len(beta) >= n, beta[k] > 0 for k < n,
    beta[0] = integral of the weight.
    Cost: O(n^2) floating-point operations in practice (a bounded number of
    QL sweeps of O(n) per eigenvalue); no evaluations of the integrand.
    """
    # @line L1
    if n < 1 or len(alpha) < n or len(beta) < n:
        raise ValueError("need n >= 1 and n recurrence coefficients")
    if any(not (beta[k] > 0.0) for k in range(n)):
        raise ValueError("beta_k must be positive")
    # @line L2
    d = [float(alpha[k]) for k in range(n)]
    e = [math.sqrt(beta[k + 1]) for k in range(n - 1)] + [0.0]
    z = [1.0] + [0.0] * (n - 1)  # first row of the accumulated rotations
    # @line L3
    for l in range(n):
        sweeps = 0
        # @line L4
        while True:
            # @line L5
            m = l
            while m < n - 1:
                if abs(e[m]) <= U * (abs(d[m]) + abs(d[m + 1])):
                    break
                m += 1
            # @line L6
            if m == l:
                break
            sweeps += 1
            if sweeps > max_sweeps_per_eigenvalue:
                raise ArithmeticError("QL iteration did not converge")
            # @line L7
            g = (d[l + 1] - d[l]) / (2.0 * e[l])
            r = math.hypot(g, 1.0)
            g = d[m] - d[l] + e[l] / (g + math.copysign(r, g))
            s, c, p = 1.0, 1.0, 0.0
            deflated = False
            # @line L8
            for i in range(m - 1, l - 1, -1):
                f = s * e[i]
                b = c * e[i]
                r = math.hypot(f, g)
                e[i + 1] = r
                if r == 0.0:
                    d[i + 1] -= p
                    e[m] = 0.0
                    deflated = True
                    break
                s = f / r
                c = g / r
                g = d[i + 1] - p
                r = (d[i] - g) * s + 2.0 * c * b
                p = s * r
                d[i + 1] = g + p
                g = c * r - b
                # @line L9
                f = z[i + 1]
                z[i + 1] = s * z[i] + c * f
                z[i] = c * z[i] - s * f
            if deflated:
                continue
            d[l] -= p
            e[l] = g
            e[m] = 0.0
    # @line L10
    pairs = sorted((d[j], beta[0] * z[j] * z[j]) for j in range(n))
    # @line L11
    return [x for x, _ in pairs], [w for _, w in pairs]


def legendre_recurrence(n: int) -> Tuple[List[float], List[float]]:
    """w = 1 on [-1, 1]."""
    return [0.0] * n, [2.0] + [k * k / (4.0 * k * k - 1.0) for k in range(1, n)]


def laguerre_recurrence(n: int, a: float = 0.0) -> Tuple[List[float], List[float]]:
    """w = x^a e^(-x) on (0, infinity), a > -1."""
    return [2.0 * k + a + 1.0 for k in range(n)], [math.gamma(a + 1.0)] + [k * (k + a) for k in range(1, n)]


def hermite_recurrence(n: int) -> Tuple[List[float], List[float]]:
    """w = e^(-x^2) on the real line."""
    return [0.0] * n, [math.sqrt(math.pi)] + [k / 2.0 for k in range(1, n)]
