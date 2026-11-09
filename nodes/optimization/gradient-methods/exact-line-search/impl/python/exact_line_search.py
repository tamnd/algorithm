# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exact-line-search/. The authors are listed in prov/V5H45Q.jsonl.

"""Exact line search: bracket the minimizer of phi(alpha) = f(x + alpha d) on [0, inf),
then shrink the bracket by golden-section search. Also the closed form for quadratics,
and steepest descent with exact steps.

Vectors are lists of floats. All arithmetic is in floating point.
"""

import math
from typing import Callable, List, Tuple

Vector = List[float]
Matrix = List[List[float]]

GOLDEN = (math.sqrt(5.0) - 1.0) / 2.0  # 0.618...


def dot(u: Vector, v: Vector) -> float:
    return sum(a * b for a, b in zip(u, v))


def matvec(a: Matrix, v: Vector) -> Vector:
    return [dot(row, v) for row in a]


def exact_line_search(
    phi: Callable[[float], float], h: float = 1.0, tau: float = 1e-8, max_doublings: int = 200
) -> Tuple[float, float, float]:
    """Return (alpha, lo, hi): the minimizer of phi on [0, inf) lies in [lo, hi],
    hi - lo <= tau, and alpha = (lo + hi) / 2.

    phi must be strictly decreasing on [0, a*] and strictly increasing on [a*, inf)
    for some a* >= 0. h > 0 is the first trial step and tau > 0 the absolute tolerance.
    """
    if not (h > 0.0 and tau > 0.0):
        raise ValueError("need h > 0 and tau > 0")
    if phi(h) >= phi(0.0):  # @line L1
        lo, hi = 0.0, h
    else:  # @line L2
        lo, mid, hi = 0.0, h, 2.0 * h  # @line L3
        doublings = 0
        while phi(hi) < phi(mid):  # @line L4
            lo, mid, hi = mid, hi, 2.0 * hi  # @line L5
            doublings += 1
            if doublings > max_doublings:
                raise ValueError("no bracket found; phi may be unbounded below")
    r = GOLDEN  # @line L6
    while hi - lo > tau:  # @line L7
        u, v = hi - r * (hi - lo), lo + r * (hi - lo)  # @line L8
        if phi(u) < phi(v):  # @line L9
            hi = v
        else:
            lo = u
    return (lo + hi) / 2.0, lo, hi  # @line L10


def exact_step_quadratic(a: Matrix, g: Vector, d: Vector) -> float:
    """For f(x) = 1/2 x^T A x - b^T x with A positive definite, g = grad f(x) and d with
    d^T A d > 0, the exact step is -g^T d / (d^T A d)."""
    curvature = dot(d, matvec(a, d))
    if curvature <= 0.0:
        raise ValueError("need d^T A d > 0")
    return -dot(g, d) / curvature


def steepest_descent_quadratic(a: Matrix, b: Vector, x0: Vector, iterations: int, tol: float = 0.0) -> List[Vector]:
    """Steepest descent with exact steps on f(x) = 1/2 x^T A x - b^T x. Return the iterates.
    Stop after `iterations` steps or when the gradient norm is at most tol."""
    x = list(x0)
    path = [list(x)]
    for _ in range(iterations):
        g = [gi - bi for gi, bi in zip(matvec(a, x), b)]
        if math.sqrt(dot(g, g)) <= tol:
            break
        alpha = exact_step_quadratic(a, g, [-gi for gi in g])
        x = [xi - alpha * gi for xi, gi in zip(x, g)]
        path.append(list(x))
    return path


def steepest_descent_exact(
    f: Callable[[Vector], float],
    grad: Callable[[Vector], Vector],
    x0: Vector,
    iterations: int,
    tau: float = 1e-8,
    tol: float = 0.0,
) -> Tuple[List[Vector], List[float]]:
    """Steepest descent where each step is found by exact_line_search along -grad f.
    Return the iterates and the steps."""
    x = list(x0)
    path, steps = [list(x)], []
    for _ in range(iterations):
        g = grad(x)
        if math.sqrt(dot(g, g)) <= tol:
            break
        phi = lambda t, x=x, g=g: f([xi - t * gi for xi, gi in zip(x, g)])
        alpha, _, _ = exact_line_search(phi, 1.0, tau)
        x = [xi - alpha * gi for xi, gi in zip(x, g)]
        path.append(list(x))
        steps.append(alpha)
    return path, steps
