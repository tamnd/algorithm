# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heuns-method/. The authors are listed in prov/G2M62V.jsonl.

"""Heun's method (explicit trapezoidal rule) for y' = f(t, y), y(t0) = y0.

    k1 = f(t_n, y_n)
    k2 = f(t_n + h, y_n + h k1)
    y_(n+1) = y_n + (h/2) (k1 + k2)
"""

import math
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Callable, List, Tuple

# A step count within this relative amount of an integer is rounded to it,
# so that (T - t0)/h = 3.0000000000000004 gives 3 steps and not 4.
GRID_SLACK = 1e-9

# The Butcher tableau (A, b, c) with s = 2 stages, in exact arithmetic.
TABLEAU_A = [[Fraction(0), Fraction(0)], [Fraction(1), Fraction(0)]]
TABLEAU_B = [Fraction(1, 2), Fraction(1, 2)]
TABLEAU_C = [Fraction(0), Fraction(1)]


@dataclass
class HeunResult:
    """The final time and value, the number of steps and of evaluations of f."""

    t: Any
    y: Any
    steps: int
    f_evals: int
    path: List[Tuple[Any, Any]] = field(default_factory=list)


def _axpy(y: Any, k: Any, v: Any) -> Any:
    """Return y + k v for a scalar y or a list y."""
    if isinstance(y, list):
        return [a + k * b for a, b in zip(y, v)]
    return y + k * v


def _avg(u: Any, v: Any) -> Any:
    """Return (u + v)/2 for scalars or lists, exact for Fraction data."""
    if isinstance(u, list):
        return [(a + b) / 2 for a, b in zip(u, v)]
    return (u + v) / 2


def step_count(t0: Any, t_end: Any, h: Any) -> int:
    """The number N of steps of length at most h (up to GRID_SLACK) from t0 to t_end."""
    if not h > 0:
        raise ValueError("the step size h must be positive")
    if t_end < t0:
        raise ValueError("t_end must not be before t0")
    r = (t_end - t0) / h
    if isinstance(r, (int, Fraction)):
        return math.ceil(r)
    return max(0, math.ceil(r - GRID_SLACK * max(1.0, r)))


def stability_function(z: Any) -> Any:
    """R(z) = 1 + z + z^2/2: one step of Heun's method on y' = lambda y multiplies y by R(h lambda)."""
    return 1 + z + z * z / 2


def heuns_method(f: Callable[[Any, Any], Any], t0: Any, y0: Any, t_end: Any, h: Any,
                 keep_path: bool = False) -> HeunResult:
    """Integrate y' = f(t, y) from t0 to t_end with Heun's method.

    y0 is a number or a list of numbers; f(t, y) returns the same shape. The grid is
    t_n = t0 + n h, and the last step is shortened (or stretched by at most a relative
    GRID_SLACK) so that it ends exactly at t_end. Works with float or Fraction data.
    Cost: 2N evaluations of f with N = ceil((t_end - t0)/h), O(N d) arithmetic,
    O(d) extra space (O(N d) with keep_path).
    """
    n_steps = step_count(t0, t_end, h)  # @line L1
    t, y = t0, (list(y0) if isinstance(y0, list) else y0)  # @line L2
    path = [(t, y)] if keep_path else []
    for n in range(n_steps):  # @line L3
        t_next = t_end if n == n_steps - 1 else t0 + (n + 1) * h  # @line L4
        hn = t_next - t  # @line L5
        k1 = f(t, y)  # @line L6
        k2 = f(t_next, _axpy(y, hn, k1))  # @line L7
        y = _axpy(y, hn, _avg(k1, k2))  # @line L8
        t = t_next  # @line L9
        if keep_path:
            path.append((t, y))
    return HeunResult(t, y, n_steps, 2 * n_steps, path)  # @line L10
