# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backtracking-line-search/. The authors are listed in prov/G81MN3.jsonl.

"""Backtracking line search for the Armijo condition, and gradient descent that uses it.

Vectors are lists of floats. All arithmetic is in floating point.
"""

from typing import Callable, List, Tuple

Vector = List[float]


def dot(u: Vector, v: Vector) -> float:
    return sum(a * b for a, b in zip(u, v))


def norm(v: Vector) -> float:
    return dot(v, v) ** 0.5


def backtracking_line_search(
    f: Callable[[Vector], float],
    x: Vector,
    fx: float,
    g: Vector,
    d: Vector,
    alpha0: float = 1.0,
    rho: float = 0.5,
    c: float = 1e-4,
) -> Tuple[float, int]:
    """Return (alpha, trials): the first alpha in alpha0, rho*alpha0, rho^2*alpha0, ...
    with f(x + alpha d) <= fx + c * alpha * g^T d, and the number of values of f computed.

    fx must be f(x) and g must be the gradient of f at x. d must be a descent direction.
    """
    if not (0.0 < rho < 1.0 and 0.0 < c < 1.0 and alpha0 > 0.0):
        raise ValueError("need 0 < rho < 1, 0 < c < 1 and alpha0 > 0")
    slope = dot(g, d)  # @line L1
    if slope >= 0.0:  # @line L2
        raise ValueError("d is not a descent direction")
    alpha = alpha0  # @line L3
    trials = 1
    while f([xi + alpha * di for xi, di in zip(x, d)]) > fx + c * alpha * slope:  # @line L4
        alpha *= rho  # @line L5
        trials += 1
    return alpha, trials  # @line L6


def gradient_descent_backtracking(
    f: Callable[[Vector], float],
    grad: Callable[[Vector], Vector],
    x0: Vector,
    iterations: int,
    alpha0: float = 1.0,
    rho: float = 0.5,
    c: float = 1e-4,
    tol: float = 0.0,
) -> Tuple[List[Vector], List[float]]:
    """Gradient descent with d = -grad f(x) and a backtracking step at each iteration.

    Return the list of iterates x_0, x_1, ... and the list of accepted steps.
    Stop after `iterations` steps or when the gradient norm is at most tol.
    """
    x = list(x0)
    path, steps = [list(x)], []
    for _ in range(iterations):
        g = grad(x)
        if norm(g) <= tol:
            break
        d = [-gi for gi in g]
        alpha, _ = backtracking_line_search(f, x, f(x), g, d, alpha0, rho, c)
        x = [xi + alpha * di for xi, di in zip(x, d)]
        path.append(list(x))
        steps.append(alpha)
    return path, steps
