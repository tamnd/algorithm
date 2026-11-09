# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bfgs/. The authors are listed in prov/54MPPW.jsonl.

"""The BFGS quasi-Newton method in inverse form with a strong Wolfe line search
(bracketing and zoom, as in Nocedal and Wright, Algorithms 3.5 and 3.6).

Vectors are lists of floats and matrices are lists of rows. All arithmetic is in floating point.
"""

import math
from typing import Callable, List, Optional, Tuple

Vector = List[float]
Matrix = List[List[float]]
Function = Callable[[Vector], float]
Gradient = Callable[[Vector], Vector]


class LineSearchError(RuntimeError):
    pass


def dot(u: Vector, v: Vector) -> float:
    return sum(a * b for a, b in zip(u, v))


def norm(v: Vector) -> float:
    return math.sqrt(dot(v, v))


def matvec(a: Matrix, v: Vector) -> Vector:
    return [dot(row, v) for row in a]


def strong_wolfe(
    f: Function,
    grad: Gradient,
    x: Vector,
    fx: float,
    gx: Vector,
    d: Vector,
    c1: float = 1e-4,
    c2: float = 0.9,
    alpha0: float = 1.0,
    max_evals: int = 100,
) -> Tuple[float, float, Vector]:
    """Return (alpha, f(x + alpha d), grad f(x + alpha d)) with
    f(x + alpha d) <= fx + c1 alpha g^T d and |grad f(x + alpha d)^T d| <= c2 |g^T d|."""
    slope0 = dot(gx, d)
    if slope0 >= 0.0:
        raise ValueError("d is not a descent direction")
    if not (0.0 < c1 < c2 < 1.0):
        raise ValueError("need 0 < c1 < c2 < 1")
    evals = 0

    def phi(a: float) -> Tuple[float, Vector, float]:
        nonlocal evals
        evals += 1
        if evals > max_evals:
            raise LineSearchError("no strong Wolfe step found")
        y = [xi + a * di for xi, di in zip(x, d)]
        g = grad(y)
        return f(y), g, dot(g, d)

    def zoom(lo, f_lo, s_lo, hi, f_hi):
        while True:
            width = hi - lo
            denom = 2.0 * (f_hi - f_lo - s_lo * width)
            a = lo - s_lo * width * width / denom if denom > 0.0 else lo + 0.5 * width
            if not (min(lo, hi) + 0.1 * abs(width) <= a <= max(lo, hi) - 0.1 * abs(width)):
                a = lo + 0.5 * width
            f_a, g_a, s_a = phi(a)
            if f_a > fx + c1 * a * slope0 or f_a >= f_lo:
                hi, f_hi = a, f_a
            else:
                if abs(s_a) <= -c2 * slope0:
                    return a, f_a, g_a
                if s_a * (hi - lo) >= 0.0:
                    hi, f_hi = lo, f_lo
                lo, f_lo, s_lo = a, f_a, s_a

    a_prev, f_prev, s_prev = 0.0, fx, slope0
    a = alpha0
    first = True
    while True:
        f_a, g_a, s_a = phi(a)
        if f_a > fx + c1 * a * slope0 or (not first and f_a >= f_prev):
            return zoom(a_prev, f_prev, s_prev, a, f_a)
        if abs(s_a) <= -c2 * slope0:
            return a, f_a, g_a
        if s_a >= 0.0:
            return zoom(a, f_a, s_a, a_prev, f_prev)
        a_prev, f_prev, s_prev = a, f_a, s_a
        a *= 2.0
        first = False


def bfgs_update(h: Matrix, s: Vector, y: Vector) -> Matrix:
    """H+ = (I - rho s y^T) H (I - rho y s^T) + rho s s^T with rho = 1 / (y^T s), in O(n^2)."""
    ys = dot(y, s)
    if not ys > 0.0:
        raise ValueError("need y^T s > 0")
    rho = 1.0 / ys
    v = matvec(h, y)
    c = rho * rho * dot(y, v) + rho
    n = len(s)
    return [[h[i][j] - rho * (s[i] * v[j] + v[i] * s[j]) + c * s[i] * s[j] for j in range(n)] for i in range(n)]


def bfgs(
    f: Function,
    grad: Gradient,
    x0: Vector,
    h0: Optional[Matrix] = None,
    iterations: int = 1000,
    tol: float = 1e-8,
    c1: float = 1e-4,
    c2: float = 0.9,
    step: Optional[Callable[[Vector, Vector, Vector], float]] = None,
) -> Tuple[List[Vector], List[Tuple[float, Vector, Vector, Matrix]]]:
    """Minimize f from x0. Return the iterates and, for each step, (alpha, d, g, H) where g and H
    are the gradient and the inverse Hessian approximation at the start of the step.

    If h0 is None, H starts as the identity and is rescaled to (y^T s / y^T y) I before the first
    update. If `step` is given, it is called as step(x, g, d) and must return the step (for example
    the exact step on a quadratic); otherwise a strong Wolfe line search with c1 and c2 is used.
    Stop after `iterations` steps, when ||g|| <= tol, or when the line search fails.
    """
    n = len(x0)
    x = list(x0)
    fx, g = f(x), grad(x)  # @line L1
    h = [row[:] for row in h0] if h0 is not None else [[float(i == j) for j in range(n)] for i in range(n)]
    path, record = [list(x)], []
    for k in range(iterations):  # @line L2
        if norm(g) <= tol:
            break
        d = [-t for t in matvec(h, g)]  # @line L3
        if step is None:  # @line L4
            try:
                alpha, f_new, g_new = strong_wolfe(f, grad, x, fx, g, d, c1, c2)
            except LineSearchError:
                break
        else:
            alpha = step(x, g, d)
        record.append((alpha, list(d), list(g), [row[:] for row in h]))
        s = [alpha * di for di in d]  # @line L5
        x = [xi + si for xi, si in zip(x, s)]
        if step is not None:
            f_new, g_new = f(x), grad(x)
        y = [a - b for a, b in zip(g_new, g)]
        if k == 0 and h0 is None:  # @line L6
            gamma = dot(y, s) / dot(y, y)
            h = [[gamma * float(i == j) for j in range(n)] for i in range(n)]
        if dot(y, s) > 0.0:  # @line L7
            h = bfgs_update(h, s, y)
        fx, g = f_new, g_new  # @line L8
        path.append(list(x))
    return path, record  # @line L9
