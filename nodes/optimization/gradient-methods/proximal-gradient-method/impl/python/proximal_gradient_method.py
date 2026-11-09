# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/proximal-gradient-method/. The authors are listed in prov/QWQCF9.jsonl.

"""The proximal gradient method (ISTA, forward-backward splitting).

It minimizes F(x) = f(x) + h(x), where f is convex and L_f-smooth and h is closed,
convex and has a cheap proximal operator. Vectors are lists of floats.
"""

from collections.abc import Callable

Vector = list[float]


def soft_threshold(v: Vector, tau: float) -> Vector:
    """The prox of tau * ||.||_1: shrink each entry toward 0 by tau."""
    out = []
    for a in v:
        if a > tau:
            out.append(a - tau)
        elif a < -tau:
            out.append(a + tau)
        else:
            out.append(0.0)
    return out


def proximal_gradient(
    grad_f: Callable[[Vector], Vector],
    prox_h: Callable[[Vector, float], Vector],
    x0: Vector,
    step: float,
    iters: int,
) -> list[Vector]:
    """Run iters steps with a constant step and return [x_0, x_1, ..., x_iters].

    prox_h(v, t) must return prox_{t h}(v). The rate of the page holds for step <= 1/L_f.
    """
    xs = [list(x0)]
    x = list(x0)
    for _ in range(iters):  # @line L1
        g = grad_f(x)
        y = [xi - step * gi for xi, gi in zip(x, g)]  # @line L2
        x = prox_h(y, step)  # @line L3
        xs.append(x)
    return xs  # @line L4


def lasso_parts(
    a: list[Vector], b: Vector, lam: float
) -> tuple[Callable[[Vector], float], Callable[[Vector], Vector], Callable[[Vector, float], Vector]]:
    """Return (F, grad_f, prox_h) for F(x) = 0.5 ||A x - b||^2 + lam ||x||_1."""

    def residual(x: Vector) -> Vector:
        return [sum(r[j] * x[j] for j in range(len(x))) - bi for r, bi in zip(a, b)]

    def objective(x: Vector) -> float:
        r = residual(x)
        return 0.5 * sum(ri * ri for ri in r) + lam * sum(abs(xi) for xi in x)

    def grad_f(x: Vector) -> Vector:
        r = residual(x)
        return [sum(a[i][j] * r[i] for i in range(len(a))) for j in range(len(x))]

    def prox_h(v: Vector, t: float) -> Vector:
        return soft_threshold(v, t * lam)

    return objective, grad_f, prox_h
