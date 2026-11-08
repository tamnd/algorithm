# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lax-friedrichs-scheme/. The authors are listed in prov/5WKGZC.jsonl.

"""The Lax-Friedrichs scheme for a scalar conservation law u_t + f(u)_x = 0.

    U_j^(n+1) = (U_(j-1)^n + U_(j+1)^n)/2 - (dt/(2 dx)) (f(U_(j+1)^n) - f(U_(j-1)^n))

in conservation form with the numerical flux
    F_(j+1/2) = (f(U_j) + f(U_(j+1)))/2 - (dx/(2 dt)) (U_(j+1) - U_j).
For f(u) = a u it is linear with Courant number nu = a dt/dx, stable for |nu| <= 1.
"""

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Callable, List

GRID_SLACK = 1e-9  # relative slack in the step count against rounding of T/dt


@dataclass
class LFResult:
    """Final values, final time, the number of steps and of flux evaluations."""

    u: List[Any]
    t: Any
    steps: int
    flux_evals: int


def step_count(t_end: Any, dt: Any) -> int:
    """The number N of time steps of length at most dt (up to GRID_SLACK) from 0 to t_end."""
    if not dt > 0:
        raise ValueError("the time step dt must be positive")
    if t_end < 0:
        raise ValueError("t_end must not be negative")
    r = t_end / dt
    if isinstance(r, (int, Fraction)):
        return math.ceil(r)
    return max(0, math.ceil(r - GRID_SLACK * max(1.0, r)))


def _neighbours(u: List[Any], bc: str):
    """Values U_(j-1) and U_(j+1) for each j, with periodic or transmissive (copy) ghosts."""
    m = len(u)
    if bc == "periodic":
        left = [u[j - 1] for j in range(m)]
        right = [u[(j + 1) % m] for j in range(m)]
    elif bc == "transmissive":
        left = [u[max(j - 1, 0)] for j in range(m)]
        right = [u[min(j + 1, m - 1)] for j in range(m)]
    else:
        raise ValueError("bc must be 'periodic' or 'transmissive'")
    return left, right


def lf_step(u: List[Any], flux: Callable[[Any], Any], lam: Any, bc: str = "periodic") -> List[Any]:
    """One Lax-Friedrichs step with lam = dt/dx."""
    fu = [flux(v) for v in u]
    fl, fr = _neighbours(fu, bc)
    ul, ur = _neighbours(u, bc)
    return [(ul[j] + ur[j]) / 2 - lam * (fr[j] - fl[j]) / 2 for j in range(len(u))]


def amplification_factor(nu: float, theta: float) -> complex:
    """g(theta) = cos(theta) - i nu sin(theta) for u_t + a u_x = 0, nu = a dt/dx."""
    return complex(math.cos(theta), -nu * math.sin(theta))


def lax_friedrichs(u0: List[Any], flux: Callable[[Any], Any], dx: Any, dt: Any, t_end: Any,
                   bc: str = "periodic") -> LFResult:
    """March U from t = 0 to t_end with time step dt; the last step is shortened to end at t_end.

    u0 holds the cell values U_j^0 (j = 0..m-1, m >= 1). Each step evaluates the flux m times
    and does O(m) arithmetic. Works with float or Fraction data. Stability needs
    max |f'(u)| dt/dx <= 1; the caller chooses dt.
    """
    if not dx > 0:
        raise ValueError("dx must be positive")
    if len(u0) == 0:
        raise ValueError("need at least one cell")
    n_steps = step_count(t_end, dt)  # @line L1
    u, t = list(u0), 0 * dt  # @line L2
    for n in range(n_steps):  # @line L3
        t_next = t_end if n == n_steps - 1 else (n + 1) * dt  # @line L4
        lam = (t_next - t) / dx  # @line L5
        fu = [flux(v) for v in u]  # @line L6
        fl, fr = _neighbours(fu, bc)  # @line L7
        ul, ur = _neighbours(u, bc)
        u = [(ul[j] + ur[j]) / 2 - lam * (fr[j] - fl[j]) / 2 for j in range(len(u))]  # @line L8
        t = t_next  # @line L9
    return LFResult(u, t, n_steps, n_steps * len(u0))  # @line L10
