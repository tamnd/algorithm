# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tanh-sinh-quadrature/. The authors are listed in prov/FDAEA3.jsonl.

import math
from typing import Callable, List, Tuple

HALF_PI = math.pi / 2


def tanh_sinh_node(t: float) -> Tuple[float, float]:
    """Return (delta, weight) of the map x(t) = tanh((pi/2) sinh t) at |t|.

    delta = 1 - x(|t|) is the distance to the nearer end of [-1, 1] and
    weight = x'(t) = (pi/2) cosh t / cosh^2((pi/2) sinh t). Both are computed
    from e = exp(-2u), so there is no cancellation and no overflow; for large
    |t| they underflow to 0.0, which is their correctly rounded value.
    """
    # @line L11
    u = HALF_PI * math.sinh(abs(t))
    e = math.exp(-2.0 * u)
    delta = 2.0 * e / (1.0 + e)
    weight = HALF_PI * math.cosh(t) * 4.0 * e / ((1.0 + e) * (1.0 + e))
    return delta, weight


def _finite(
    f: Callable[..., float],
    a: float,
    b: float,
    tol: float,
    max_level: int,
    min_level: int,
    t_max: float,
    with_distances: bool,
    counter: List[int],
) -> Tuple[float, float]:
    """Tanh-sinh on a finite interval with a < b; returns (value, estimate)."""
    # @line L2
    r = (b - a) / 2.0

    def term(t: float) -> float:
        delta, w = tanh_sinh_node(t)
        d = r * delta  # distance from the node to the nearer end
        if d == 0.0 or w == 0.0:
            return 0.0
        # @line L12
        if t >= 0:
            x, da, db = b - d, (b - a) - d, d
        else:
            x, da, db = a + d, d, (b - a) - d
        counter[0] += 1
        # @line L13
        if with_distances:
            return r * w * f(x, da, db)
        if a < x < b:
            return r * w * f(x)
        # The node rounded onto an end point. Use the end value if f has
        # one there; drop the term if f is singular there.
        x = a if x <= a else b
        try:
            fx = f(x)
        except (ArithmeticError, ValueError):
            return 0.0
        return r * w * fx if math.isfinite(fx) else 0.0

    # @line L3
    h = 1.0
    total = math.fsum(term(float(j)) for j in range(-int(t_max), int(t_max) + 1))
    # @line L4
    prev = h * total
    est = math.inf
    # @line L5
    for level in range(1, max_level + 1):
        # @line L6
        h /= 2.0
        # @line L7
        jmax = int(t_max / h)
        new = [term(j * h) for j in range(-jmax, jmax + 1) if j % 2 != 0]
        total = math.fsum([total] + new)
        # @line L8
        cur = h * total
        est = abs(cur - prev)
        # @line L9
        if level >= min_level and est <= tol:
            return cur, est
        prev = cur
    # @line L10
    return prev, est


def tanh_sinh(
    f: Callable[..., float],
    a: float,
    b: float,
    tol: float = 1e-12,
    max_level: int = 8,
    min_level: int = 2,
    t_max: float = 6.0,
    with_distances: bool = False,
) -> Tuple[float, float, int]:
    """Tanh-sinh (double exponential) quadrature of f on [a, b].

    Substitutes x = c + r tanh((pi/2) sinh t), c = (a + b)/2, r = (b - a)/2,
    and applies the trapezoidal rule in t on [-t_max, t_max] with steps
    h = 1, 1/2, 1/4, ..., reusing all earlier values, until two successive
    levels differ by at most tol (and at least min_level halvings are done).

    Precondition: f is finite on the open interval (a, b) and absolutely
    integrable there; singularities are allowed at a and b. a or b may be
    infinite; then x = a + u/(1 - u) (or x = b - u/(1 - u)) maps [0, 1) onto
    the interval first, and the part beyond |x - a| = 1e150 is dropped.
    A node that rounds onto a finite end point is evaluated there; if f
    raises an arithmetic or domain error or returns a non-finite value at
    the end point, that term is dropped.
    If with_distances is true, f is called as f(x, x - a, b - x) with both
    distances accurate (math.inf for an infinite end), which keeps full
    accuracy for a singularity at an end point that is not 0.

    Returns (value, estimate, evaluations), where estimate is the difference
    of the last two levels. Cost: at most 2 t_max 2^K + 1 evaluations of f
    when the loop stops at level K.
    """
    counter = [0]
    # @line L1
    if a == b:
        return 0.0, 0.0, 0
    if b < a:
        v, e, n = tanh_sinh(f, b, a, tol, max_level, min_level, t_max, with_distances)
        return -v, e, n
    inf_a, inf_b = math.isinf(a), math.isinf(b)
    if inf_a and inf_b:
        v1, e1, n1 = tanh_sinh(f, -math.inf, 0.0, tol / 2, max_level, min_level, t_max, with_distances)
        v2, e2, n2 = tanh_sinh(f, 0.0, math.inf, tol / 2, max_level, min_level, t_max, with_distances)
        return v1 + v2, e1 + e2, n1 + n2
    if inf_a or inf_b:
        base, s = (a, 1.0) if inf_b else (b, -1.0)

        def g(u: float, du: float, dv: float) -> float:
            # du = u and dv = 1 - u, both accurate; x = base + s du/dv
            if dv < 1e-150:
                return 0.0
            dist = du / dv
            x = base + s * dist
            jac = (1.0 / dv) / dv
            if with_distances:
                fx = f(x, dist, math.inf) if s > 0 else f(x, math.inf, dist)
            else:
                fx = f(x)
            return fx * jac

        v, e = _finite(g, 0.0, 1.0, tol, max_level, min_level, t_max, True, counter)
        return v, e, counter[0]
    v, e = _finite(f, a, b, tol, max_level, min_level, t_max, with_distances, counter)
    return v, e, counter[0]
