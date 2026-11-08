# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weno-scheme/. The authors are listed in prov/EF32M5.jsonl.

"""Fifth-order WENO finite volume scheme for a scalar conservation law u_t + f(u)_x = 0.

Space: WENO5 reconstruction (Jiang-Shu weights, or WENO-Z weights of Borges et al.)
applied to the Lax-Friedrichs flux splitting f = f+ + f-, f+- = (f(u) +- alpha u)/2,
with alpha >= max |f'(u)|. Time: the third-order SSP Runge-Kutta method of Shu and Osher.
Boundary conditions: periodic or transmissive (ghost cells copy the edge value).
The grid values are cell averages; the error is measured in the max or L1 norm.
"""

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Callable, List, Sequence, Tuple

GRID_SLACK = 1e-9  # relative slack in the step count against rounding of T/dt
LINEAR_WEIGHTS = (Fraction(1, 10), Fraction(3, 5), Fraction(3, 10))
GHOSTS = 3


@dataclass
class WenoResult:
    """Final cell averages, final time, number of time steps and number of flux evaluations."""
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


def candidates(v: Sequence[Any]) -> Tuple[Any, Any, Any]:
    """The three third-order values at x_(j+1/2) from the averages v = (v_(j-2), ..., v_(j+2))."""
    a, b, c, d, e = v
    return ((2 * a - 7 * b + 11 * c) / 6,
            (-b + 5 * c + 2 * d) / 6,
            (2 * c + 5 * d - e) / 6)


def smoothness(v: Sequence[Any]) -> Tuple[Any, Any, Any]:
    """The Jiang-Shu smoothness indicators beta_0, beta_1, beta_2 of the three stencils."""
    a, b, c, d, e = v
    k = Fraction(13, 12) if isinstance(a, Fraction) else 13.0 / 12.0
    q = Fraction(1, 4) if isinstance(a, Fraction) else 0.25
    return (k * (a - 2 * b + c) ** 2 + q * (a - 4 * b + 3 * c) ** 2,
            k * (b - 2 * c + d) ** 2 + q * (b - d) ** 2,
            k * (c - 2 * d + e) ** 2 + q * (3 * c - 4 * d + e) ** 2)


def nonlinear_weights(beta: Sequence[Any], eps: float = 1e-6, variant: str = "js") -> List[float]:
    """The weights omega_k: d_k/(eps + beta_k)^2 (Jiang-Shu) or d_k (1 + (tau/(eps + beta_k))^2) (WENO-Z)."""
    d = [float(x) for x in LINEAR_WEIGHTS]
    b = [float(x) for x in beta]
    if variant == "js":
        alpha = [d[k] / (eps + b[k]) ** 2 for k in range(3)]
    elif variant == "z":
        tau = abs(b[0] - b[2])
        alpha = [d[k] * (1.0 + (tau / (eps + b[k])) ** 2) for k in range(3)]
    elif variant == "linear":
        alpha = d
    else:
        raise ValueError("variant must be 'js', 'z' or 'linear'")
    s = sum(alpha)
    return [x / s for x in alpha]


def reconstruct(v: Sequence[Any], eps: float = 1e-6, variant: str = "js") -> float:
    """The WENO5 value at the right edge x_(j+1/2) of cell j from v = (v_(j-2), ..., v_(j+2))."""
    q = candidates(v)
    if variant == "linear":
        return sum(LINEAR_WEIGHTS[k] * q[k] for k in range(3))
    w = nonlinear_weights(smoothness(v), eps, variant)
    return sum(w[k] * float(q[k]) for k in range(3))


def _extend(u: List[Any], bc: str) -> List[Any]:
    """Pad with GHOSTS ghost cells on each side, periodic or transmissive."""
    m = len(u)
    if bc == "periodic":
        return [u[(j - GHOSTS) % m] for j in range(m + 2 * GHOSTS)]
    if bc == "transmissive":
        return [u[min(max(j - GHOSTS, 0), m - 1)] for j in range(m + 2 * GHOSTS)]
    raise ValueError("bc must be 'periodic' or 'transmissive'")


def weno_rhs(u: List[Any], flux: Callable[[Any], Any], alpha: float, dx: float,
             bc: str = "periodic", eps: float = 1e-6, variant: str = "js") -> List[float]:
    """The semi-discrete right-hand side L(U)_j = -(F_(j+1/2) - F_(j-1/2))/dx."""
    m = len(u)
    ue = _extend(u, bc)
    fe = [flux(x) for x in ue]  # @line L7
    fp = [(fe[i] + alpha * ue[i]) / 2 for i in range(len(ue))]
    fm = [(fe[i] - alpha * ue[i]) / 2 for i in range(len(ue))]
    F = []
    for i in range(GHOSTS - 1, GHOSTS + m):  # interface i+1/2 for extended index i
        plus = fp[i - 2:i + 3]  # @line L8
        minus = [fm[i + 3 - k] for k in range(5)]  # mirrored stencil for the left-moving part
        F.append(reconstruct(plus, eps, variant) + reconstruct(minus, eps, variant))  # @line L9
    return [-(F[j + 1] - F[j]) / dx for j in range(m)]  # @line L10


def ssp_rk3_step(u: List[Any], L: Callable[[List[Any]], List[Any]], h: Any) -> List[Any]:
    """One step of the Shu-Osher SSP-RK3 method: three forward Euler steps and convex averages."""
    k = len(u)
    L0 = L(u)
    u1 = [u[j] + h * L0[j] for j in range(k)]  # @line L3
    L1 = L(u1)
    u2 = [(3 * u[j] + u1[j] + h * L1[j]) / 4 for j in range(k)]  # @line L4
    L2 = L(u2)
    return [(u[j] + 2 * (u2[j] + h * L2[j])) / 3 for j in range(k)]  # @line L5


def ssp_rk3_tableau():
    """The Butcher tableau (A, b, c) of SSP-RK3, in Fractions."""
    F = Fraction
    A = [[F(0), F(0), F(0)], [F(1), F(0), F(0)], [F(1, 4), F(1, 4), F(0)]]
    return A, [F(1, 6), F(1, 6), F(2, 3)], [F(0), F(1), F(1, 2)]


def weno(u0: List[Any], flux: Callable[[Any], Any], alpha: float, dx: float, dt: float, t_end: float,
         bc: str = "periodic", eps: float = 1e-6, variant: str = "js") -> WenoResult:
    """WENO5 in space with SSP-RK3 in time from t = 0 to t_end; the last step is shortened.

    alpha must bound |f'(u)| over the data (the Lax-Friedrichs splitting needs it).
    The caller chooses dt; the SSP-RK3 step is stable for about alpha dt/dx <= 1.
    """
    if not dx > 0:
        raise ValueError("dx must be positive")
    if len(u0) == 0:
        raise ValueError("need at least one cell")
    if alpha < 0:
        raise ValueError("alpha must not be negative")
    N = step_count(t_end, dt)  # @line L1
    u, t, evals = [float(x) for x in u0], 0.0, 0
    per_rhs = len(u0) + 2 * GHOSTS

    def L(v: List[float]) -> List[float]:
        return weno_rhs(v, flux, alpha, dx, bc, eps, variant)

    for n in range(N):
        h = (t_end if n == N - 1 else (n + 1) * dt) - t  # @line L2
        u = ssp_rk3_step(u, L, h)
        t += h
        evals += 3 * per_rhs
    return WenoResult(u, t, N, evals)  # @line L6


def cell_averages(F: Callable[[float], float], m: int, a: float = 0.0, b: float = 1.0) -> List[float]:
    """Exact cell averages (F(x_(j+1/2)) - F(x_(j-1/2)))/dx from an antiderivative F."""
    dx = (b - a) / m
    return [(F(a + (j + 1) * dx) - F(a + j * dx)) / dx for j in range(m)]


def total_variation(u: List[Any], periodic: bool = True) -> Any:
    """TV(U) = sum |U_(j+1) - U_j|, with the wrap-around term when periodic."""
    m = len(u)
    tv = sum(abs(u[j + 1] - u[j]) for j in range(m - 1))
    return tv + (abs(u[0] - u[-1]) if periodic else 0)
