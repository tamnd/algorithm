# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/logistic-map/. The authors are listed in prov/DM7V7K.jsonl.
"""The logistic map x_(t+1) = r x_t (1 - x_t) as a population model.

orbit gives the trajectory. The other functions give the fixed points,
the 2-cycle in closed form, the multiplier of a cycle, the period of the
attractor found by iteration, and an estimate of the Lyapunov exponent.
Cost: Theta(T) arithmetic operations for T steps.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple


def step(r: float, x: float) -> float:
    """One generation of the map."""
    return r * x * (1 - x)


def orbit(r: float, x0: float, steps: int) -> List[float]:
    """The values x_1, ..., x_steps from the start x0."""
    if steps < 0:
        raise ValueError("steps must be >= 0")
    x = x0  # @line L1
    out: List[float] = []
    for _ in range(steps):  # @line L2
        x = r * x * (1 - x)  # @line L3
        out.append(x)  # @line L4
    return out  # @line L5


def fixed_points(r: float) -> Tuple[float, float]:
    """The two fixed points 0 and 1 - 1/r (r > 0)."""
    if r <= 0:
        raise ValueError("r must be > 0")
    return 0.0, 1 - 1 / r


def two_cycle(r: float) -> Optional[Tuple[float, float]]:
    """The 2-cycle (r + 1 -/+ sqrt((r - 3)(r + 1))) / (2 r), or None for r <= 3."""
    if r <= 3:
        return None
    d = math.sqrt((r - 3) * (r + 1))
    return (r + 1 - d) / (2 * r), (r + 1 + d) / (2 * r)


def multiplier(r: float, cycle: Sequence[float]) -> float:
    """The product of f'(x) = r (1 - 2 x) over the points of a cycle."""
    m = 1.0
    for x in cycle:
        m *= r * (1 - 2 * x)
    return m


def attractor(r: float, x0: float = 0.3, burn: int = 100000,
              max_period: int = 64, tol: float = 1e-9) -> Optional[List[float]]:
    """The cycle that the orbit settles on, sorted, or None if no period <= max_period."""
    x = x0
    for _ in range(burn):
        x = step(r, x)
    path = [x]
    for _ in range(max_period):
        x = step(r, x)
        path.append(x)
    for p in range(1, max_period + 1):
        if abs(path[p] - path[0]) < tol:
            return sorted(path[:p])
    return None


def lyapunov(r: float, x0: float = 0.3, steps: int = 100000, burn: int = 1000) -> float:
    """The mean of log |r (1 - 2 x_t)| along the orbit."""
    x = x0
    for _ in range(burn):
        x = step(r, x)
    total = 0.0
    for _ in range(steps):
        total += math.log(abs(r * (1 - 2 * x)))
        x = step(r, x)
    return total / steps
