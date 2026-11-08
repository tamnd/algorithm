# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/euler-maruyama-method/. The authors are listed in prov/YNYFA8.jsonl.

"""Euler-Maruyama method for dX = a(t, X) dt + b(t, X) dW, X(t0) = X0.

The step is X_(n+1) = X_n + a(t_n, X_n) dt_n + b(t_n, X_n) dW_n with independent
Brownian increments dW_n ~ N(0, dt_n I_m).
"""

import math
import random
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Callable, List, Optional, Sequence, Tuple

# A step count within this relative amount of an integer is rounded to it.
GRID_SLACK = 1e-9


@dataclass
class EMResult:
    """Final time and state, number of steps, evaluations of a and b, increments used."""

    t: Any
    x: Any
    steps: int
    evals: int
    increments: List[Any] = field(default_factory=list)
    path: List[Tuple[Any, Any]] = field(default_factory=list)


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


def _step(x: Any, drift: Any, diff: Any, dt: Any, dw: Any) -> Any:
    """x + drift dt + diff dw for scalars, or for a list x, a d x m matrix diff, a list dw."""
    if isinstance(x, list):
        return [xi + ai * dt + sum(bij * wj for bij, wj in zip(bi, dw))
                for xi, ai, bi in zip(x, drift, diff)]
    return x + drift * dt + diff * dw


def _sample(rng: random.Random, dt: float, diff: Any, x: Any) -> Any:
    """One Brownian increment N(0, dt I_m), m read off the shape of the diffusion."""
    s = math.sqrt(dt)
    if isinstance(x, list):
        m = len(diff[0]) if diff else 0
        return [rng.gauss(0.0, s) for _ in range(m)]
    return rng.gauss(0.0, s)


def euler_maruyama(a: Callable[[Any, Any], Any], b: Callable[[Any, Any], Any],
                   t0: Any, x0: Any, t_end: Any, h: Any,
                   rng: Optional[random.Random] = None,
                   increments: Optional[Sequence[Any]] = None,
                   keep_path: bool = False) -> EMResult:
    """Integrate dX = a dt + b dW from t0 to t_end with the Euler-Maruyama method.

    x0 is a number (then b returns a number and the noise is scalar) or a list of d
    numbers (then a returns d numbers and b a d x m matrix as a list of rows).
    Increments are drawn from rng with variance equal to the actual step length, or
    taken from `increments` (one per step) to follow a given Brownian path; given
    increments may be Fractions, and then the arithmetic is exact.
    Cost: N evaluations each of a and b, N m normal samples, O(N d m) arithmetic.
    """
    n_steps = step_count(t0, t_end, h)  # @line L1
    if increments is not None and len(increments) != n_steps:
        raise ValueError("need exactly one increment per step")
    if increments is None and rng is None:
        rng = random.Random(0)
    t, x = t0, (list(x0) if isinstance(x0, list) else x0)  # @line L2
    used: List[Any] = []
    path = [(t, x)] if keep_path else []
    for n in range(n_steps):  # @line L3
        t_next = t_end if n == n_steps - 1 else t0 + (n + 1) * h  # @line L4
        dt = t_next - t  # @line L5
        drift, diff = a(t, x), b(t, x)
        dw = increments[n] if increments is not None else _sample(rng, float(dt), diff, x)  # @line L6
        x = _step(x, drift, diff, dt, dw)  # @line L7
        t = t_next  # @line L8
        used.append(dw)
        if keep_path:
            path.append((t, x))
    return EMResult(t, x, n_steps, n_steps, used, path)  # @line L9


def coarsen(increments: Sequence[float], r: int) -> List[float]:
    """Sum consecutive groups of r scalar increments: the same path on a grid r times coarser."""
    if r < 1 or len(increments) % r:
        raise ValueError("r must divide the number of increments")
    return [sum(increments[i:i + r]) for i in range(0, len(increments), r)]
