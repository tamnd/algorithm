# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/representer-theorem/. The authors are listed in prov/BWRZ8V.jsonl.

"""Numerical checks of the representer theorem in an explicit feature space.

The kernel (x . z + 1)^2 on R^2 has the explicit 6 dimensional feature map
phi below. With n < 6 training points, the span V of phi(x_1), ..., phi(x_n)
is a proper subspace of R^6. We minimize regularized objectives directly over
w in R^6, from a start outside V, and check that the minimizer lies in V.
"""

import math
from typing import Sequence

Vec = list[float]


def phi(x: Sequence[float]) -> Vec:
    """phi(x) . phi(z) = (x . z + 1)^2 for x, z in R^2."""
    r2 = math.sqrt(2)
    x1, x2 = x
    return [1.0, r2 * x1, r2 * x2, x1 * x1, r2 * x1 * x2, x2 * x2]


def kernel(x: Sequence[float], z: Sequence[float]) -> float:
    return (x[0] * z[0] + x[1] * z[1] + 1) ** 2


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    return sum(u * v for u, v in zip(a, b))


def solve(a: Sequence[Sequence[float]], b: Sequence[float]) -> Vec:
    """Gaussian elimination with partial pivoting."""
    n = len(a)
    m = [list(map(float, a[i])) + [float(b[i])] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            for k in range(c, n + 1):
                m[r][k] -= f * m[c][k]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (m[r][n] - sum(m[r][k] * x[k] for k in range(r + 1, n))) / m[r][r]
    return x


def distance_to_span(w: Sequence[float], basis: Sequence[Sequence[float]]) -> float:
    """Norm of the part of w that is orthogonal to span(basis), by Gram-Schmidt."""
    q: list[Vec] = []
    for v in basis:
        u = list(v)
        for e in q:
            c = dot(u, e)
            u = [a - c * b for a, b in zip(u, e)]
        nu = math.sqrt(dot(u, u))
        if nu > 1e-12:
            q.append([a / nu for a in u])
    r = list(w)
    for e in q:
        c = dot(r, e)
        r = [a - c * b for a, b in zip(r, e)]
    return math.sqrt(dot(r, r))


def ridge_in_feature_space(xs, ys, lam: float) -> Vec:
    """argmin_w sum_i (w . phi(x_i) - y_i)^2 + lam |w|^2, by the normal equations."""
    f = [phi(x) for x in xs]
    d = len(f[0])
    a = [[sum(r[i] * r[j] for r in f) + (lam if i == j else 0.0) for j in range(d)] for i in range(d)]
    b = [sum(r[i] * y for r, y in zip(f, ys)) for i in range(d)]
    return solve(a, b)


def ridge_dual(xs, ys, lam: float) -> Vec:
    """alpha = (K + lam I)^{-1} y; the minimizer is sum_i alpha_i phi(x_i)."""
    n = len(xs)
    k = [[kernel(xs[i], xs[j]) + (lam if i == j else 0.0) for j in range(n)] for i in range(n)]
    return solve(k, ys)


def logistic_objective(w, xs, ys, lam: float) -> float:
    return sum(math.log1p(math.exp(-y * dot(w, phi(x)))) for x, y in zip(xs, ys)) + lam * dot(w, w)


def logistic_gradient_descent(xs, ys, lam: float, w0: Sequence[float], steps: int, eta: float) -> Vec:
    """Minimize sum_i log(1 + exp(-y_i w . phi(x_i))) + lam |w|^2 over all of R^6.

    The gradient is a combination of the phi(x_i) plus 2 lam w, so the part of
    w orthogonal to the span shrinks by the factor (1 - 2 eta lam) per step.
    """
    f = [phi(x) for x in xs]
    w = list(w0)
    for _ in range(steps):
        g = [2 * lam * wi for wi in w]
        for r, y in zip(f, ys):
            s = -y / (1 + math.exp(y * dot(w, r)))
            g = [gi + s * ri for gi, ri in zip(g, r)]
        w = [wi - eta * gi for wi, gi in zip(w, g)]
    return w
