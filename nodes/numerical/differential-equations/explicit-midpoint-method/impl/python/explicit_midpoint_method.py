# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/explicit-midpoint-method/. The authors are listed in prov/WJ3SQA.jsonl.

"""The explicit midpoint method for y' = f(t, y): one Euler half step, then a full step
with the slope at the midpoint. Order 2, two evaluations of f per step."""

import math
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Callable, List, Tuple

GRID_SLACK = 1e-9  # relative slack when counting steps in floating point

# The Butcher tableau (A, b, c) of the method.
TABLEAU_A = [[Fraction(0), Fraction(0)], [Fraction(1, 2), Fraction(0)]]
TABLEAU_B = [Fraction(0), Fraction(1)]
TABLEAU_C = [Fraction(0), Fraction(1, 2)]


@dataclass
class MidpointResult:
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
    """The number of steps of length at most h (up to GRID_SLACK) from t0 to t_end."""
    if not h > 0:
        raise ValueError("the step size h must be positive")
    if t_end < t0:
        raise ValueError("t_end must not be before t0")
    r = (t_end - t0) / h
    if isinstance(r, (int, Fraction)):
        return math.ceil(r)
    return max(0, math.ceil(r - GRID_SLACK * max(1.0, r)))


def stability_function(z: Any) -> Any:
    """R(z) = 1 + z + z^2/2: the factor of one step on y' = lambda y with z = h lambda."""
    return 1 + z + z * z / 2


def explicit_midpoint_method(f: Callable[[Any, Any], Any], t0: Any, y0: Any, t_end: Any,
                             h: Any, keep_path: bool = False) -> MidpointResult:
    """Integrate y' = f(t, y) from t0 to t_end with the explicit midpoint method.

    y0 is a number or a list; f(t, y) returns the same shape. The grid is t_n = t0 + n h
    and the last step ends exactly at t_end. Works with float or Fraction data.
    Cost: 2N evaluations of f with N = ceil((t_end - t0)/h), O(N d) arithmetic,
    O(d) extra space (O(N d) with keep_path).
    """
    n_steps = step_count(t0, t_end, h)  # @line L1
    t, y = t0, (list(y0) if isinstance(y0, list) else y0)  # @line L2
    path = [(t, y)] if keep_path else []
    for n in range(n_steps):  # @line L3
        t_next = t_end if n == n_steps - 1 else t0 + (n + 1) * h  # @line L4
        s = t_next - t
        k1 = f(t, y)  # @line L5
        k2 = f(t + s / 2, _axpy(y, s / 2, k1))  # @line L6
        y = _axpy(y, s, k2)  # @line L7
        t = t_next  # @line L8
        if keep_path:
            path.append((t, y))
    return MidpointResult(t, y, n_steps, 2 * n_steps, path)  # @line L9
