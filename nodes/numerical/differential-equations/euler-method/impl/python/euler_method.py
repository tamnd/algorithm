# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/euler-method/. The authors are listed in prov/P0J8GY.jsonl.

"""Euler's method for y' = f(t, y), y(t0) = y0: the step y_(n+1) = y_n + h f(t_n, y_n)."""

import math
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Callable, List, Tuple

# A step count that is within this relative amount of an integer is rounded to it,
# so that (T - t0)/h = 3.0000000000000004 gives 3 steps and not 4.
GRID_SLACK = 1e-9


@dataclass
class EulerResult:
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


def euler_method(f: Callable[[Any, Any], Any], t0: Any, y0: Any, t_end: Any, h: Any,
                 keep_path: bool = False) -> EulerResult:
    """Integrate y' = f(t, y) from t0 to t_end with Euler's method.

    y0 is a number or a list of numbers; f(t, y) returns the same shape. The grid is
    t_n = t0 + n h, and the last step is shortened (or stretched by at most a relative
    GRID_SLACK) so that it ends exactly at t_end. Works with float or Fraction data.
    Cost: N = ceil((t_end - t0)/h) evaluations of f and O(N d) arithmetic operations;
    O(d) extra space, or O(N d) with keep_path.
    """
    n_steps = step_count(t0, t_end, h)  # @line L1
    t, y = t0, (list(y0) if isinstance(y0, list) else y0)  # @line L2
    path = [(t, y)] if keep_path else []
    for n in range(n_steps):  # @line L3
        t_next = t_end if n == n_steps - 1 else t0 + (n + 1) * h  # @line L4
        y = _axpy(y, t_next - t, f(t, y))  # @line L5
        t = t_next  # @line L6
        if keep_path:
            path.append((t, y))
    return EulerResult(t, y, n_steps, n_steps, path)  # @line L7
