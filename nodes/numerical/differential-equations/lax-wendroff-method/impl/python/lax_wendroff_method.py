# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lax-wendroff-method/. The authors are listed in prov/N95ZRW.jsonl.

"""The Lax-Wendroff method for u_t + f(u)_x = 0, in Richtmyer's two-step form.

    U_(j+1/2)^(n+1/2) = (U_j + U_(j+1))/2 - (dt/(2 dx)) (f(U_(j+1)) - f(U_j))
    U_j^(n+1) = U_j - (dt/dx) (f(U_(j+1/2)^(n+1/2)) - f(U_(j-1/2)^(n+1/2)))

For f(u) = a u this is the one-step Lax-Wendroff scheme
    U_j^(n+1) = U_j - (nu/2)(U_(j+1) - U_(j-1)) + (nu^2/2)(U_(j+1) - 2 U_j + U_(j-1)),
second order, stable for |nu| <= 1 with nu = a dt/dx.
"""

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Callable, List

GRID_SLACK = 1e-9  # relative slack in the step count against rounding of T/dt


@dataclass
class LWResult:
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


def _right(u: List[Any], bc: str) -> List[Any]:
    """U_(j+1) for j = 0..m-1 with periodic or transmissive ghosts."""
    m = len(u)
    if bc == "periodic":
        return [u[(j + 1) % m] for j in range(m)]
    if bc == "transmissive":
        return [u[min(j + 1, m - 1)] for j in range(m)]
    raise ValueError("bc must be 'periodic' or 'transmissive'")


def _left(u: List[Any], bc: str) -> List[Any]:
    """U_(j-1) for j = 0..m-1 with periodic or transmissive ghosts."""
    m = len(u)
    if bc == "periodic":
        return [u[j - 1] for j in range(m)]
    return [u[max(j - 1, 0)] for j in range(m)]


def lw_step(u: List[Any], flux: Callable[[Any], Any], lam: Any, bc: str = "periodic") -> List[Any]:
    """One two-step Lax-Wendroff step with lam = dt/dx."""
    m = len(u)
    fu = [flux(v) for v in u]
    ur, fr = _right(u, bc), _right(fu, bc)
    half = [(u[j] + ur[j]) / 2 - lam * (fr[j] - fu[j]) / 2 for j in range(m)]  # at j + 1/2
    fh = [flux(v) for v in half]
    fhl = _left(fh, bc) if bc == "periodic" else [fh[j - 1] if j > 0 else fu[0] for j in range(m)]
    return [u[j] - lam * (fh[j] - fhl[j]) for j in range(m)]


def lw_linear_step(u: List[Any], nu: Any) -> List[Any]:
    """The one-step form for f(u) = a u on a periodic grid."""
    m = len(u)
    return [u[j] - nu * (u[(j + 1) % m] - u[j - 1]) / 2
            + nu * nu * (u[(j + 1) % m] - 2 * u[j] + u[j - 1]) / 2 for j in range(m)]


def amplification_factor(nu: float, theta: float) -> complex:
    """g(theta) = 1 - i nu sin(theta) - nu^2 (1 - cos(theta)) for u_t + a u_x = 0."""
    return complex(1 - nu * nu * (1 - math.cos(theta)), -nu * math.sin(theta))


def lax_wendroff(u0: List[Any], flux: Callable[[Any], Any], dx: Any, dt: Any, t_end: Any,
                 bc: str = "periodic") -> LWResult:
    """March U from t = 0 to t_end with time step dt; the last step is shortened to end at t_end.

    u0 holds the cell values U_j^0 (j = 0..m-1, m >= 1). Each step evaluates the flux 2m times
    (m at the cells, m at the half points) and does O(m) arithmetic. Works with float or
    Fraction data. Stability for linear advection needs |nu| <= 1.
    """
    if not dx > 0:
        raise ValueError("dx must be positive")
    if len(u0) == 0:
        raise ValueError("need at least one cell")
    m = len(u0)
    n_steps = step_count(t_end, dt)  # @line L1
    u, t = list(u0), 0 * dt  # @line L2
    for n in range(n_steps):  # @line L3
        t_next = t_end if n == n_steps - 1 else (n + 1) * dt  # @line L4
        lam = (t_next - t) / dx  # @line L5
        fu = [flux(v) for v in u]  # @line L6
        ur, fr = _right(u, bc), _right(fu, bc)  # @line L7
        half = [(u[j] + ur[j]) / 2 - lam * (fr[j] - fu[j]) / 2 for j in range(m)]  # @line L8
        fh = [flux(v) for v in half]  # @line L9
        if bc == "periodic":
            fhl = _left(fh, bc)
        else:  # transmissive: the face left of cell 0 carries the flux of U_0
            fhl = [fh[j - 1] if j > 0 else fu[0] for j in range(m)]
        u = [u[j] - lam * (fh[j] - fhl[j]) for j in range(m)]  # @line L10
        t = t_next  # @line L11
    return LWResult(u, t, n_steps, 2 * m * n_steps)  # @line L12
