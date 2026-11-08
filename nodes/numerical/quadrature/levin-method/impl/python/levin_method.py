# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/levin-method/. The authors are listed in prov/BPA5JP.jsonl.

import cmath
import math
from typing import Callable, List, Tuple


def chebyshev_values(t: float, n: int) -> Tuple[List[float], List[float]]:
    """T_0(t)..T_n(t) and their derivatives T_0'(t)..T_n'(t) by the three-term recurrence.

    Cost: O(n) arithmetic.
    """
    T = [1.0, t]
    D = [0.0, 1.0]
    for k in range(1, n):
        T.append(2 * t * T[k] - T[k - 1])
        D.append(2 * T[k] + 2 * t * D[k] - D[k - 1])
    return T[: n + 1], D[: n + 1]


def solve_complex(A: List[List[complex]], F: List[complex]) -> List[complex]:
    """Solve A c = F by Gaussian elimination with partial pivoting.

    Precondition: A square and nonsingular. Raises ZeroDivisionError if a
    pivot is exactly 0. Cost: O(m^3) arithmetic for m unknowns. A and F are
    not modified.
    """
    m = len(A)
    M = [row[:] + [F[i]] for i, row in enumerate(A)]
    for col in range(m):
        piv = max(range(col, m), key=lambda i: abs(M[i][col]))
        if M[piv][col] == 0:
            raise ZeroDivisionError("singular collocation matrix")
        M[col], M[piv] = M[piv], M[col]
        for i in range(col + 1, m):
            factor = M[i][col] / M[col][col]
            if factor != 0:
                Mi, Mc = M[i], M[col]
                for j in range(col, m + 1):
                    Mi[j] -= factor * Mc[j]
    c = [0j] * m
    for i in range(m - 1, -1, -1):
        s = M[i][m] - sum(M[i][j] * c[j] for j in range(i + 1, m))
        c[i] = s / M[i][i]
    return c


def levin(
    f: Callable[[float], complex],
    g: Callable[[float], float],
    dg: Callable[[float], float],
    a: float,
    b: float,
    omega: float,
    n: int,
) -> complex:
    """Levin's collocation method for I = integral over [a, b] of f(x) exp(i omega g(x)) dx.

    Finds p(x) = sum_{k=0}^n c_k T_k(t), x = (a + b)/2 + (b - a) t / 2, with
    p'(x_j) + i omega g'(x_j) p(x_j) = f(x_j) at the n + 1 Chebyshev-Lobatto
    points x_j, and returns p(b) e^(i omega g(b)) - p(a) e^(i omega g(a)).

    Precondition: a, b finite; omega != 0; n >= 1; f smooth and g' != 0 on
    [a, b] (no stationary points). dg is the derivative of g. Exact when
    f = q' + i omega g' q for a polynomial q of degree <= n and the system is
    nonsingular; for g(x) = x and f a polynomial of degree <= n always exact.

    Cost: n + 1 evaluations of f and of dg, 2 of g, and O(n^3) arithmetic.
    """
    if n < 1:
        raise ValueError("need n >= 1")
    if omega == 0:
        raise ValueError("omega must be nonzero; the collocation system is singular for omega = 0")
    if math.isinf(a) or math.isinf(b):
        raise ValueError("finite interval required")
    if a == b:
        return 0j
    # @line L1
    c, r = (a + b) / 2, (b - a) / 2
    A: List[List[complex]] = []
    F: List[complex] = []
    # @line L2
    for j in range(n + 1):
        # @line L3
        t = math.cos(math.pi * j / n)
        x = b if j == 0 else a if j == n else c + r * t
        T, D = chebyshev_values(t, n)
        # @line L4
        s = 1j * omega * dg(x)
        A.append([D[k] / r + s * T[k] for k in range(n + 1)])
        # @line L5
        F.append(complex(f(x)))
    # @line L6
    coef = solve_complex(A, F)
    # @line L7
    pb = math.fsum(z.real for z in coef) + 1j * math.fsum(z.imag for z in coef)
    alt = [z if k % 2 == 0 else -z for k, z in enumerate(coef)]
    pa = math.fsum(z.real for z in alt) + 1j * math.fsum(z.imag for z in alt)
    # @line L8
    return pb * cmath.exp(1j * omega * g(b)) - pa * cmath.exp(1j * omega * g(a))
