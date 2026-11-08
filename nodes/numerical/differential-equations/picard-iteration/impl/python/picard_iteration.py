# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/picard-iteration/. The authors are listed in prov/56X5PF.jsonl.

"""Picard iteration for y' = f(t, y), y(t0) = y0.

The continuous iteration is

    y^(k+1)(t) = y0 + integral from t0 to t of f(s, y^(k)(s)) ds.

picard_iteration carries it out on a grid: [t0, T] is cut into windows, each
window into m equal sub-intervals, and the integral is the cumulative
trapezoidal rule.  On each window the iteration is repeated until two
iterates differ by at most tol times a scale, the larger of 1, the largest
|y| and the window length times the largest |f| (an absolute test cannot
be met in floating point when the terms h f are large).  Its fixed point is the solution of the
implicit trapezoidal rule on the grid.

picard_polynomial carries out the continuous iteration exactly for a
right-hand side that is a polynomial in t and y, with Fraction coefficients.
"""

import math
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Callable, List

GRID_SLACK = 1e-9


@dataclass
class PicardResult:
    """Final time and value, iterations used in each window, evaluations of f."""

    t: Any
    y: Any
    iterations: List[int]
    f_evals: int
    converged: bool
    grid: List[Any] = field(default_factory=list)
    values: List[Any] = field(default_factory=list)


def _is_vec(y: Any) -> bool:
    return isinstance(y, list)


def _add(u: Any, v: Any) -> Any:
    if _is_vec(u):
        return [a + b for a, b in zip(u, v)]
    return u + v


def _scale(k: Any, u: Any) -> Any:
    if _is_vec(u):
        return [k * a for a in u]
    return k * u


def _dist(u: Any, v: Any) -> float:
    if _is_vec(u):
        return max((abs(a - b) for a, b in zip(u, v)), default=0.0)
    return abs(u - v)


def _norm(u: Any) -> float:
    if _is_vec(u):
        return float(max((abs(a) for a in u), default=0.0))
    return float(abs(u))


def _finite(u: Any) -> bool:
    vals = u if _is_vec(u) else [u]
    return all(isinstance(a, Fraction) or math.isfinite(a) for a in vals)


def picard_iteration(f: Callable[[Any, Any], Any], t0: Any, y0: Any, t_end: Any,
                     m: int = 64, windows: int = 1, tol: float = 1e-12,
                     max_iter: int = 200, keep_grid: bool = False) -> PicardResult:
    """Windowed Picard iteration with the cumulative trapezoidal rule.

    f(t, y) returns a scalar or a list like y.  Each of the `windows` equal
    windows of [t0, t_end] has m sub-intervals.  If an iterate stops being
    finite or max_iter is reached in a window, the result has converged=False
    and holds the last iterate reached.
    """
    if m < 1 or windows < 1:
        raise ValueError("m and windows must be at least 1")
    if t_end < t0:
        raise ValueError("t_end must not be before t0")
    if t_end == t0:                                     # zero steps
        return PicardResult(t0, y0, [], 0, True, [t0], [y0])
    length = (t_end - t0) / windows                     # @line L1
    y_start = y0
    iters: List[int] = []
    f_evals = 0
    grid_all: List[Any] = [t0]
    vals_all: List[Any] = [y0]
    ok = True
    for w in range(windows):                            # @line L2
        a = t0 + w * length
        b = t_end if w == windows - 1 else t0 + (w + 1) * length
        tau = [a + (b - a) * i / m for i in range(m)] + [b]
        Y = [y_start] * (m + 1)                         # @line L3
        k = 0
        done = False
        while k < max_iter:                             # @line L4
            k += 1
            F = [f(tau[i], Y[i]) for i in range(m + 1)]  # @line L5
            f_evals += m + 1
            Z = [y_start]                               # @line L6
            for i in range(1, m + 1):
                half = (tau[i] - tau[i - 1]) / 2
                Z.append(_add(Z[i - 1], _scale(half, _add(F[i - 1], F[i]))))
            delta = max(_dist(Z[i], Y[i]) for i in range(m + 1))  # @line L7
            scale = max(1.0, max(_norm(z) for z in Z),
                        float(abs(b - a)) * max(_norm(v) for v in F))
            Y = Z                                       # @line L8
            if not all(_finite(z) for z in Y):
                break
            if delta <= tol * scale:                    # @line L9
                done = True
                break
        iters.append(k)
        if keep_grid:
            grid_all.extend(tau[1:])
            vals_all.extend(Y[1:])
        y_start = Y[m]                                  # @line L10
        if not done:
            ok = False
            break
    t_fin = t_end if ok else b
    return PicardResult(t_fin, y_start, iters, f_evals, ok,  # @line L11
                        grid_all if keep_grid else [], vals_all if keep_grid else [])


# Exact Picard iterates for polynomial right-hand sides.  A polynomial in
# s = t - t0 is a list of coefficients, lowest degree first.

def padd(p: List[Any], q: List[Any]) -> List[Any]:
    n = max(len(p), len(q))
    return [(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(n)]


def pscale(c: Any, p: List[Any]) -> List[Any]:
    return [c * a for a in p]


def pmul(p: List[Any], q: List[Any]) -> List[Any]:
    if not p or not q:
        return []
    r = [Fraction(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i + j] += a * b
    return r


def pint(p: List[Any]) -> List[Any]:
    """The antiderivative that vanishes at s = 0."""
    return [Fraction(0)] + [Fraction(a) / (i + 1) for i, a in enumerate(p)]


def picard_polynomial(f: Callable[[List[Any], List[Any]], List[Any]], y0: Any,
                      k: int) -> List[List[Fraction]]:
    """Return the iterates y^(0), ..., y^(k) as coefficient lists in s = t - t0.

    f(s, y) receives the polynomials s = [0, 1] and y and must return a
    polynomial built with padd, pscale and pmul.
    """
    if k < 0:
        raise ValueError("k must be nonnegative")
    s = [Fraction(0), Fraction(1)]
    ys = [[Fraction(y0)]]
    for _ in range(k):
        ys.append(padd([Fraction(y0)], pint(f(s, ys[-1]))))
    return ys
