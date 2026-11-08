# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/upwind-scheme/. The authors are listed in prov/K94YNY.jsonl.

"""The first-order upwind scheme.

Linear advection u_t + a u_x = 0 with Courant number nu = a dt/dx:
    U_j^(n+1) = U_j - nu (U_j - U_(j-1))      if a >= 0,
    U_j^(n+1) = U_j - nu (U_(j+1) - U_j)      if a < 0.
Stable in the max norm and the l2 norm exactly when |nu| <= 1.

Scalar conservation law u_t + f(u)_x = 0 in conservation form with the upwind
(Murman-Roe) flux: F_(j+1/2) = f(U_j) if the speed of the jump is >= 0, else f(U_(j+1)).
"""

import cmath
import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Callable, List

GRID_SLACK = 1e-9  # relative slack in the step count against rounding of T/dt


@dataclass
class UpwindResult:
    """Final cell values, final time, number of steps and number of flux evaluations."""
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


def _ghost(u: List[Any], bc: str):
    """Return (left, right) neighbour lists with periodic or transmissive (copy) ghost cells."""
    m = len(u)
    if bc == "periodic":
        return [u[j - 1] for j in range(m)], [u[(j + 1) % m] for j in range(m)]
    if bc == "transmissive":
        return [u[max(j - 1, 0)] for j in range(m)], [u[min(j + 1, m - 1)] for j in range(m)]
    raise ValueError("bc must be 'periodic' or 'transmissive'")


def upwind(u0: List[Any], a: Any, dx: Any, dt: Any, t_end: Any, bc: str = "periodic") -> UpwindResult:
    """Upwind scheme for u_t + a u_x = 0 from t = 0 to t_end; the last step is shortened.

    Works with float or Fraction data. Stable for |a| dt/dx <= 1; the caller chooses dt.
    """
    if not dx > 0:
        raise ValueError("dx must be positive")
    if len(u0) == 0:
        raise ValueError("need at least one cell")
    N = step_count(t_end, dt)  # @line L1
    u, t = list(u0), 0 * dt  # @line L2
    for n in range(N):  # @line L3
        t_next = t_end if n == N - 1 else (n + 1) * dt  # @line L4
        nu = a * (t_next - t) / dx  # @line L5
        left, right = _ghost(u, bc)  # @line L6
        if a >= 0:  # @line L7
            u = [u[j] - nu * (u[j] - left[j]) for j in range(len(u))]
        else:
            u = [u[j] - nu * (right[j] - u[j]) for j in range(len(u))]  # @line L8
        t = t_next  # @line L9
    return UpwindResult(u, t, N, 0)  # @line L10


def roe_flux(flux: Callable[[Any], Any], ul: Any, ur: Any, fl: Any, fr: Any) -> Any:
    """Upwind interface flux: the side the jump's speed (f(ur) - f(ul))/(ur - ul) comes from."""
    if ur == ul:
        return fl
    speed = (fr - fl) / (ur - ul)
    return fl if speed >= 0 else fr


def upwind_conservative(u0: List[Any], flux: Callable[[Any], Any], dx: Any, dt: Any, t_end: Any,
                        bc: str = "transmissive") -> UpwindResult:
    """Conservative upwind scheme U_j <- U_j - (dt/dx)(F_(j+1/2) - F_(j-1/2)) with the Roe flux."""
    if not dx > 0:
        raise ValueError("dx must be positive")
    m = len(u0)
    if m == 0:
        raise ValueError("need at least one cell")
    N = step_count(t_end, dt)
    u, t, evals = list(u0), 0 * dt, 0
    for n in range(N):
        t_next = t_end if n == N - 1 else (n + 1) * dt
        lam = (t_next - t) / dx
        fu = [flux(v) for v in u]
        evals += m
        _, ur = _ghost(u, bc)
        _, fr = _ghost(fu, bc)
        F = [roe_flux(flux, u[j], ur[j], fu[j], fr[j]) for j in range(m)]  # F[j] = F_(j+1/2)
        if bc == "periodic":
            Fl = [F[j - 1] for j in range(m)]
        else:  # transmissive: the flux through the left boundary is f(U_0)
            Fl = [fu[0]] + F[:-1]
            F = F[:-1] + [fu[-1]]
        u = [u[j] - lam * (F[j] - Fl[j]) for j in range(m)]
        t = t_next
    return UpwindResult(u, t, N, evals)


def upwind_nonconservative_burgers(u0: List[Any], dx: Any, dt: Any, t_end: Any) -> List[Any]:
    """The WRONG scheme U_j <- U_j - (dt/dx) U_j (U_j - U_(j-1)) for u_t + u u_x = 0 with u >= 0."""
    N = step_count(t_end, dt)
    u, t = list(u0), 0 * dt
    for n in range(N):
        t_next = t_end if n == N - 1 else (n + 1) * dt
        lam = (t_next - t) / dx
        left, _ = _ghost(u, "transmissive")
        u = [u[j] - lam * u[j] * (u[j] - left[j]) for j in range(len(u))]
        t = t_next
    return u


def amplification_factor(nu: float, theta: float) -> complex:
    """g(theta) for the linear scheme: 1 - nu (1 - e^(-i theta)) if nu >= 0, mirrored if nu < 0."""
    if nu >= 0:
        return 1 - nu * (1 - cmath.exp(-1j * theta))
    return 1 - nu * (cmath.exp(1j * theta) - 1)


def total_variation(u: List[Any], periodic: bool = True) -> Any:
    """TV(U) = sum |U_(j+1) - U_j|, with the wrap-around term when periodic."""
    m = len(u)
    tv = sum(abs(u[j + 1] - u[j]) for j in range(m - 1))
    return tv + (abs(u[0] - u[-1]) if periodic else 0)
