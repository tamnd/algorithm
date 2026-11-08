# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sinc-quadrature/. The authors are listed in prov/T9V8KG.jsonl.

import math
from typing import Callable, List, Tuple


def sinc_parameters(n: int, alpha: float, beta: float, d: float) -> Tuple[int, int, float]:
    """Stenger's choice of (M, N, h) for decay rates alpha at a, beta at b.

    M = n, N = ceil(alpha n / beta), h = sqrt(2 pi d / (alpha n)), so that
    both truncation errors and the discretization error are of order
    exp(-sqrt(2 pi d alpha n)).
    """
    if n < 1 or alpha <= 0 or beta <= 0 or not 0 < d < math.pi:
        raise ValueError("need n >= 1, alpha > 0, beta > 0 and 0 < d < pi")
    # @line L1
    M = n
    N = math.ceil(alpha * n / beta - 1e-12)
    h = math.sqrt(2 * math.pi * d / (alpha * n))
    return M, N, h


def sinc_nodes(a: float, b: float, M: int, N: int, h: float) -> List[Tuple[float, float, float, float]]:
    """Nodes and weights of the sinc rule on [a, b] with a < b finite.

    Returns tuples (x_k, x_k - a, b - x_k, w_k) for k = -M..N, where
    x_k = (a + b e^(kh)) / (1 + e^(kh)) and w_k = h (x_k - a)(b - x_k)/(b - a).
    Distances are computed without cancellation; tiny ones may underflow to 0.
    """
    L = b - a
    out = []
    for k in range(-M, N + 1):
        # @line L3
        t = k * h
        if t <= 0:
            e = math.exp(t)  # in (0, 1]
            da = L * e / (1 + e)
            db = L / (1 + e)
            w = h * L * e / ((1 + e) * (1 + e))
        else:
            e = math.exp(-t)
            da = L / (1 + e)
            db = L * e / (1 + e)
            w = h * L * e / ((1 + e) * (1 + e))
        x = a + da if t <= 0 else b - db
        out.append((x, da, db, w))
    return out


def sinc_quadrature(
    f: Callable[..., float],
    a: float,
    b: float,
    n: int,
    alpha: float = 1.0,
    beta: float = 1.0,
    d: float = math.pi / 2,
    with_distances: bool = False,
) -> float:
    """Stenger's sinc quadrature of f on the finite interval [a, b].

    Substitutes x = (a + b e^t)/(1 + e^t), the inverse of
    phi(x) = log((x - a)/(b - x)), and applies the trapezoidal rule with step
    h to t in [-M h, N h], with (M, N, h) from sinc_parameters.

    Precondition: a and b finite; f analytic in the eye-shaped region
    |arg((z - a)/(b - z))| < d and |f(x)| (x - a)(b - x)/(b - a) bounded by
    C (x - a)^alpha near a and C (b - x)^beta near b. Then the error is
    O(exp(-sqrt(2 pi d alpha n))). If with_distances is true, f is called as
    f(x, x - a, b - x) with accurate distances. For b < a the result is
    minus the integral over [b, a]; alpha and beta then refer to b and a,
    the lower and upper ends, and the distances to them likewise.

    Cost: M + N + 1 evaluations of f, about (1 + alpha/beta) n.
    """
    if a == b:
        return 0.0
    if b < a:
        # alpha and beta refer to the lower and upper ends, so they stay
        return -sinc_quadrature(f, b, a, n, alpha, beta, d, with_distances)
    if math.isinf(a) or math.isinf(b):
        raise ValueError("finite interval required; use a map such as log(sinh x) for infinite ones")
    M, N, h = sinc_parameters(n, alpha, beta, d)
    terms = []
    # @line L2
    for x, da, db, w in sinc_nodes(a, b, M, N, h):
        if w == 0.0:
            continue
        # @line L4
        if with_distances:
            terms.append(w * f(x, da, db))
        elif a < x < b:
            terms.append(w * f(x))
        else:
            # the node rounded onto an end point: use f there if finite
            try:
                fx = f(a if x <= a else b)
            except (ArithmeticError, ValueError):
                continue
            if math.isfinite(fx):
                terms.append(w * fx)
    # @line L5
    return math.fsum(terms)
