# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/limited-memory-bfgs/. The authors are listed in prov/AJV6AP.jsonl.

"""Limited-memory BFGS (L-BFGS) with the two-loop recursion and a strong Wolfe line search
(bracketing and zoom, as in Nocedal and Wright, Algorithms 3.5 and 3.6).

Vectors are lists of floats. All arithmetic is in floating point.
"""

import math
from collections import deque
from typing import Callable, Deque, List, Optional, Sequence, Tuple

Vector = List[float]
Function = Callable[[Vector], float]
Gradient = Callable[[Vector], Vector]
Pair = Tuple[Vector, Vector]


class LineSearchError(RuntimeError):
    pass


def dot(u: Vector, v: Vector) -> float:
    return sum(a * b for a, b in zip(u, v))


def norm(v: Vector) -> float:
    return math.sqrt(dot(v, v))


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


def two_loop(q: Vector, pairs: Sequence[Pair]) -> Vector:
    """Return H q, where H is the BFGS matrix built from gamma I with the pairs (s, y), oldest first,
    and gamma = s^T y / y^T y for the newest pair (gamma = 1 if there are no pairs)."""
    q = list(q)
    rhos, alphas = [], []
    for s, y in reversed(pairs):  # @line L9
        rho = 1.0 / dot(y, s)
        a = rho * dot(s, q)
        q = [qi - a * yi for qi, yi in zip(q, y)]
        rhos.append(rho)
        alphas.append(a)
    if pairs:  # @line L10
        s, y = pairs[-1]
        gamma = dot(s, y) / dot(y, y)
    else:
        gamma = 1.0
    r = [gamma * qi for qi in q]
    for (s, y), rho, a in zip(pairs, reversed(rhos), reversed(alphas)):  # @line L11
        b = rho * dot(y, r)
        r = [ri + (a - b) * si for ri, si in zip(r, s)]
    return r  # @line L12


def limited_memory_bfgs(
    f: Function,
    grad: Gradient,
    x0: Vector,
    memory: int = 5,
    iterations: int = 1000,
    tol: float = 1e-8,
    c1: float = 1e-4,
    c2: float = 0.9,
    step: Optional[Callable[[Vector, Vector, Vector], float]] = None,
) -> Tuple[List[Vector], List[Tuple[float, Vector, Vector, List[Pair]]]]:
    """Minimize f from x0, keeping at most `memory` pairs. Return the iterates and, for each step,
    (alpha, d, g, pairs) where g and pairs are the gradient and the stored pairs at the start of the step.

    If `step` is given, it is called as step(x, g, d) and must return the step (for example the exact
    step on a quadratic); otherwise a strong Wolfe line search with c1 and c2 is used.
    Stop after `iterations` steps, when ||g|| <= tol, or when the line search fails.
    """
    if memory < 1:
        raise ValueError("memory must be at least 1")
    x = list(x0)
    fx, g = f(x), grad(x)  # @line L1
    pairs: Deque[Pair] = deque()
    path, record = [list(x)], []
    for _ in range(iterations):  # @line L2
        if norm(g) <= tol:
            break
        d = [-t for t in two_loop(g, list(pairs))]  # @line L3
        if step is None:  # @line L4
            try:
                alpha, f_new, g_new = strong_wolfe(f, grad, x, fx, g, d, c1, c2)
            except LineSearchError:
                break
        else:
            alpha = step(x, g, d)
        record.append((alpha, list(d), list(g), list(pairs)))
        s = [alpha * di for di in d]  # @line L5
        x = [xi + si for xi, si in zip(x, s)]
        if step is not None:
            f_new, g_new = f(x), grad(x)
        y = [a - b for a, b in zip(g_new, g)]
        if dot(y, s) > 0.0:  # @line L6
            pairs.append((s, y))
            if len(pairs) > memory:
                pairs.popleft()
        fx, g = f_new, g_new  # @line L7
        path.append(list(x))
    return path, record  # @line L8
