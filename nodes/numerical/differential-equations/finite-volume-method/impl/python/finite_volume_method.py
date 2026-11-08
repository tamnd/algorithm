# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/finite-volume-method/. The authors are listed in prov/80XDHS.jsonl.

"""Explicit conservative finite volume method for a 1D scalar conservation law u_t + f(u)_x = 0.

Cell averages on a uniform grid are advanced by flux differences across cell faces,
u_i <- u_i - (dt/dx) (F(u_i, u_{i+1}) - F(u_{i-1}, u_i)), with a two-point numerical flux F.
Arithmetic is generic, so Fraction data with a rational flux give exact results.
"""

import math
from dataclasses import dataclass
from typing import Callable, List, Sequence

GRID_SLACK = 1e-9


@dataclass
class FVResult:
    u: List            # cell averages at the final time
    steps: int         # number of time steps taken
    flux_evals: int    # numerical flux evaluations
    mass_change: object  # total of dt * (inflow - outflow) through the two ends (0 if periodic)


def upwind_flux(a):
    """Exact Riemann flux of the linear advection equation u_t + a u_x = 0."""
    return lambda ul, ur: a * ul if a >= 0 else a * ur


def rusanov_flux(f: Callable, df: Callable):
    """Local Lax-Friedrichs (Rusanov) flux; monotone under the CFL condition."""
    def F(ul, ur):
        s = max(abs(df(ul)), abs(df(ur)))
        return (f(ul) + f(ur)) / 2 - s * (ur - ul) / 2
    return F


def cell_averages(u0: Callable, a: float, b: float, m: int) -> List[float]:
    """Averages of u0 over m equal cells of [a, b] by 3-point Gauss-Legendre quadrature."""
    dx = (b - a) / m
    r = math.sqrt(0.6) / 2
    out = []
    for i in range(m):
        c = a + (i + 0.5) * dx
        out.append((5 * u0(c - r * dx) + 8 * u0(c) + 5 * u0(c + r * dx)) / 18)
    return out


def finite_volume(u: Sequence, dx, dt, t_end, flux: Callable, bc: str = "periodic") -> FVResult:
    """Advance cell averages u from t = 0 to t_end with steps dt (the last one shortened).

    bc is "periodic" or "transmissive" (zero-gradient ghost cells).
    """
    if not dx > 0 or not dt > 0:
        raise ValueError("dx and dt must be positive")
    if t_end < 0:
        raise ValueError("t_end must be nonnegative")
    if bc not in ("periodic", "transmissive"):
        raise ValueError("bc must be 'periodic' or 'transmissive'")
    m = len(u)
    u = list(u)
    if m == 0:
        return FVResult(u, 0, 0, 0)
    n_steps = 0 if t_end == 0 else max(1, math.ceil(t_end / dt - GRID_SLACK))
    t = 0
    evals = 0
    mass_change = 0
    for n in range(n_steps):  # @line L1
        k = t_end - t if n == n_steps - 1 else dt
        if bc == "periodic":  # @line L2
            left, right = u[-1], u[0]
        else:
            left, right = u[0], u[-1]
        ext = [left] + u + [right]
        F = [flux(ext[i], ext[i + 1]) for i in range(m + 1)]  # @line L3
        evals += m + 1
        lam = k / dx
        u = [u[i] - lam * (F[i + 1] - F[i]) for i in range(m)]  # @line L4
        mass_change += k * (F[0] - F[m])
        t = t + k if n < n_steps - 1 else t_end
    return FVResult(u, n_steps, evals, mass_change if bc == "transmissive" else 0)  # @line L5


def total_variation(u: Sequence, periodic: bool = True):
    tv = sum(abs(u[i + 1] - u[i]) for i in range(len(u) - 1))
    return tv + (abs(u[0] - u[-1]) if periodic and u else 0)
