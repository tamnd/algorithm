# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chebyshev-interpolation/. The authors are listed in prov/YWEZA4.jsonl.

"""Chebyshev interpolation: sample at Chebyshev points of the second kind,
get the Chebyshev coefficients by a discrete cosine transform, evaluate by Clenshaw."""

import math
from typing import Callable, List, Sequence


def chebyshev_points(n: int) -> List[float]:
    """x_j = cos(j pi / n), j = 0 .. n, in decreasing order (sine form, exactly symmetric)."""
    if n == 0:
        return [0.0]
    return [math.sin(math.pi * (n - 2 * j) / (2 * n)) for j in range(n + 1)]


def chebyshev_coefficients(values: Sequence[float]) -> List[float]:
    """Coefficients c_0 .. c_n of the interpolant through values[j] at chebyshev_points(n).

    Direct DCT-I in O(n^2); a fast DCT does the same in O(n log n).
    """
    n = len(values) - 1
    if n == 0:
        return [float(values[0])]
    table = [math.cos(math.pi * m / n) for m in range(2 * n)]  # cos(m pi / n), reduced mod 2n
    c = []
    for k in range(n + 1):  # @line L2
        terms = [values[j] * table[(j * k) % (2 * n)] for j in range(n + 1)]
        terms[0] *= 0.5
        terms[n] *= 0.5
        c.append(2.0 / n * math.fsum(terms))
    c[0] *= 0.5  # @line L3
    c[n] *= 0.5
    return c


def clenshaw(c: Sequence[float], x: float) -> float:
    """Value at x in [-1, 1] of sum_k c_k T_k(x)."""
    b1 = b2 = 0.0  # @line L5
    for k in range(len(c) - 1, 0, -1):
        b1, b2 = c[k] + 2.0 * x * b1 - b2, b1
    return c[0] + x * b1 - b2  # @line L6


def chebyshev_interpolation(f: Callable[[float], float], n: int, a: float = -1.0,
                            b: float = 1.0) -> List[float]:
    """Chebyshev coefficients (in the variable mapped to [-1, 1]) of the degree-n interpolant of f on [a, b]."""
    if n < 0 or not a < b:
        raise ValueError("need n >= 0 and a < b")
    xs = chebyshev_points(n)
    vals = [f(0.5 * (a + b) + 0.5 * (b - a) * x) for x in xs]  # @line L1
    return chebyshev_coefficients(vals)


def chebyshev_eval(c: Sequence[float], t: float, a: float = -1.0, b: float = 1.0) -> float:
    """Value at t of the interpolant with coefficients c on [a, b]."""
    x = (2.0 * t - a - b) / (b - a)  # @line L4
    return clenshaw(c, x)


def adaptive_chebyshev(f: Callable[[float], float], a: float = -1.0, b: float = 1.0,
                       tol: float = 1e-14, max_n: int = 4096) -> List[float]:
    """Double n from 8 until the last three coefficients are below tol times the largest; then chop."""
    n = 8
    while True:
        c = chebyshev_interpolation(f, n, a, b)
        scale = max(abs(v) for v in c) or 1.0
        if max(abs(v) for v in c[-3:]) <= tol * scale or n >= max_n:
            k = len(c)
            while k > 1 and abs(c[k - 1]) <= tol * scale:
                k -= 1
            return c[:k]
        n *= 2
