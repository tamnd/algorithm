# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ftcs-method/. The authors are listed in prov/RYE9V7.jsonl.

"""The FTCS scheme for the heat equation u_t = kappa u_xx on [a, b] with Dirichlet
boundary values: u_j^(n+1) = u_j^n + r (u_(j+1)^n - 2 u_j^n + u_(j-1)^n), r = kappa dt/dx^2."""

import math
from typing import Any, Callable, List, Optional, Sequence


def mesh_ratio(kappa: Any, dx: Any, dt: Any) -> Any:
    """r = kappa dt / dx^2. The scheme is stable in the maximum norm and in l2 iff r <= 1/2."""
    return kappa * dt / (dx * dx)


def amplification_factor(r: Any, theta: float) -> float:
    """g(theta) = 1 - 4 r sin^2(theta/2): the factor of one step on the mode exp(i j theta)."""
    return 1 - 4 * r * math.sin(theta / 2) ** 2


def ftcs_method(u0: Sequence[Any], kappa: Any, dx: Any, dt: Any, steps: int,
                left: Optional[Callable[[Any], Any]] = None,
                right: Optional[Callable[[Any], Any]] = None,
                t0: Any = 0) -> List[Any]:
    """Advance the grid values u0[0..J] by `steps` FTCS steps of length dt.

    u0[0] and u0[J] are boundary values; left(t) and right(t) give the boundary values
    at later times (default: keep u0[0] and u0[J]). Precondition: J >= 1, steps >= 0.
    The scheme is stable only for r = kappa dt/dx^2 <= 1/2; this function does not check it.
    Cost: (J - 1) steps updates of 4 additions and 2 multiplications; O(J) extra space.
    Works with float or Fraction data.
    """
    if len(u0) < 2:
        raise ValueError("the grid needs at least the two boundary points")
    if steps < 0:
        raise ValueError("the number of steps must be non-negative")
    r = mesh_ratio(kappa, dx, dt)  # @line L1
    u = list(u0)  # @line L2
    big_j = len(u) - 1
    for n in range(steps):  # @line L3
        v = [u[j] + r * (u[j + 1] - 2 * u[j] + u[j - 1]) if 0 < j < big_j else u[j]
             for j in range(big_j + 1)]  # @line L4
        t_next = t0 + (n + 1) * dt
        v[0] = left(t_next) if left else u[0]  # @line L5
        v[big_j] = right(t_next) if right else u[big_j]
        u = v  # @line L6
    return u  # @line L7
