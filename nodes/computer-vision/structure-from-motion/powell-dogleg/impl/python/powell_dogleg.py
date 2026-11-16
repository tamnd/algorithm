# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/powell-dogleg/. The authors are listed in prov/GQ5JQ6.jsonl.

"""Powell's dog leg method for nonlinear least squares.

The problem is to minimize F(x) = 1/2 ||r(x)||^2 for r: R^n -> R^m. Each
step works in a trust region of radius Delta around x. It takes the
Gauss-Newton step b if ||b|| <= Delta; else the steepest descent step cut at
the boundary if the Cauchy step a = -alpha g is already outside; else the
point where the segment from a to b meets the boundary. The radius update is
the one of Madsen, Nielsen and Tingleff (2004, Algorithm 3.21).
"""

import math
from typing import Callable, List, Sequence, Tuple

Vector = List[float]
Matrix = List[List[float]]


def cost(r: Sequence[float]) -> float:
    """F = 1/2 ||r||^2."""
    return 0.5 * sum(v * v for v in r)


def _norm(v: Sequence[float]) -> float:
    return math.sqrt(sum(x * x for x in v))


def _matvec(a: Sequence[Sequence[float]], x: Sequence[float]) -> Vector:
    return [sum(ai * xi for ai, xi in zip(row, x)) for row in a]


def cholesky_solve(a: Sequence[Sequence[float]], b: Sequence[float]) -> Vector:
    """Solve a x = b for a symmetric positive definite a by a = L L^T."""
    n = len(a)
    low = [[0.0] * n for _ in range(n)]
    for j in range(n):
        d = a[j][j] - sum(low[j][k] ** 2 for k in range(j))
        if d <= 0.0:
            raise ValueError("J^T J is not positive definite: J is rank deficient")
        low[j][j] = math.sqrt(d)
        for i in range(j + 1, n):
            low[i][j] = (a[i][j] - sum(low[i][k] * low[j][k] for k in range(j))) / low[j][j]
    y = [0.0] * n
    for i in range(n):
        y[i] = (b[i] - sum(low[i][k] * y[k] for k in range(i))) / low[i][i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(low[k][i] * x[k] for k in range(i + 1, n))) / low[i][i]
    return x


def dogleg_step(jac: Sequence[Sequence[float]], r: Sequence[float], delta: float) -> Tuple[Vector, str]:
    """The dog leg step for the model L(h) = 1/2 ||r + J h||^2 and radius delta.

    Returns (h, kind), kind is "gauss-newton", "steepest" or "dogleg"."""
    m, n = len(jac), len(jac[0])
    g = [sum(jac[k][i] * r[k] for k in range(m)) for i in range(n)]
    jg = _matvec(jac, g)
    alpha = sum(v * v for v in g) / sum(v * v for v in jg)  # @line L5
    a = [-alpha * v for v in g]  # @line L6
    jtj = [[sum(jac[k][i] * jac[k][j] for k in range(m)) for j in range(n)] for i in range(n)]
    b = cholesky_solve(jtj, [-v for v in g])
    if _norm(b) <= delta:  # @line L7
        return b, "gauss-newton"
    if _norm(a) >= delta:  # @line L8
        return [-(delta / _norm(g)) * v for v in g], "steepest"
    d = [bi - ai for ai, bi in zip(a, b)]  # @line L9
    c = sum(ai * di for ai, di in zip(a, d))
    dd = sum(v * v for v in d)
    rad = delta * delta - sum(v * v for v in a)  # positive, since ||a|| < delta
    if c <= 0:
        beta = (-c + math.sqrt(c * c + dd * rad)) / dd
    else:
        beta = rad / (c + math.sqrt(c * c + dd * rad))
    return [ai + beta * di for ai, di in zip(a, d)], "dogleg"


def powell_dogleg(residual: Callable[[Vector], Vector],
                  jacobian: Callable[[Vector], Matrix],
                  x0: Sequence[float], delta0: float = 1.0,
                  eps1: float = 1e-12, eps2: float = 1e-14,
                  max_iter: int = 200):
    """Run the dog leg method from x0 with initial radius delta0.

    Returns (x, info). info["costs"] holds F at x0 and after each accepted
    step; info["steps"] holds (kind, ||h||, delta) for each step tried."""
    x, delta = [float(v) for v in x0], float(delta0)  # @line L1
    r, jac = residual(x), jacobian(x)
    f = cost(r)
    info = {"costs": [f], "steps": []}
    for _ in range(max_iter):  # @line L2
        g = [sum(jac[k][i] * r[k] for k in range(len(r))) for i in range(len(x))]  # @line L3
        if max(abs(v) for v in g) <= eps1:  # @line L4
            break
        h, kind = dogleg_step(jac, r, delta)
        info["steps"].append((kind, _norm(h), delta))
        if _norm(h) <= eps2 * (_norm(x) + eps2):  # @line L10
            break
        x_new = [xi + hi for xi, hi in zip(x, h)]
        r_new = residual(x_new)
        f_new = cost(r_new)
        jh = _matvec(jac, h)
        predicted = -sum(gi * hi for gi, hi in zip(g, h)) - 0.5 * sum(v * v for v in jh)  # L(0) - L(h)
        if predicted <= 0.0:  # only rounding can give this: no decrease is left
            break
        rho = (f - f_new) / predicted  # @line L11
        if rho > 0:  # @line L12
            x, r, f = x_new, r_new, f_new
            jac = jacobian(x)
            info["costs"].append(f)
        if rho > 0.75:  # @line L13
            delta = max(delta, 3.0 * _norm(h))
        elif rho < 0.25:  # @line L14
            delta /= 2.0
    return x, info  # @line L15
