# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/entropy-stable-scheme/. The authors are listed in prov/0A1T0M.jsonl.

"""Entropy conservative and entropy stable finite volume fluxes for Burgers' equation.

Equation u_t + (u^2 / 2)_x = 0 on a periodic grid of M cells. Entropy pair U(u) = u^2 / 2,
q(u) = u^3 / 3, entropy variable v = U'(u) = u, potential psi = v f(u) - q(u) = u^3 / 6.
Tadmor's entropy conservative flux satisfies (v_R - v_L) F* = psi_R - psi_L; adding the
dissipation -(1/2) D (v_R - v_L) with D >= 0 gives an entropy stable flux. Values may be
floats or fractions.Fraction (exact arithmetic for the entropy identities).

Precondition: M >= 2 cells, dx > 0. Cost: Theta(M) per evaluation of the right side.
"""

from typing import Callable, List


def entropy(u):
    """U(u) = u^2 / 2, v(u) = u and psi(u) = u^3 / 6 for Burgers."""
    return u * u / 2, u, u ** 3 / 6                          # @line L1


def ec_flux(ul, ur):
    """Tadmor's entropy conservative flux (ul^2 + ul ur + ur^2) / 6."""
    return (ul * ul + ul * ur + ur * ur) / 6                 # @line L2


def es_flux(ul, ur):
    """Entropy conservative flux plus Rusanov-type dissipation in the entropy variable."""
    d = max(abs(ul), abs(ur))
    return ec_flux(ul, ur) - d * (ur - ul) / 2               # @line L3


def central_flux(ul, ur):
    """Arithmetic mean of f, for comparison (neither entropy conservative nor stable)."""
    return (ul * ul + ur * ur) / 4


def residual(u: List, dx, flux: Callable) -> List:
    """R_j = -(F_{j+1/2} - F_{j-1/2}) / dx on a periodic grid."""
    M = len(u)
    F = [flux(u[j], u[(j + 1) % M]) for j in range(M)]
    return [-(F[j] - F[j - 1]) / dx for j in range(M)]       # @line L4


def entropy_rate(u: List, dx, flux: Callable):
    """d/dt of the total entropy sum_j U(u_j) dx for the semi-discrete scheme."""
    return sum(v * r for v, r in zip(u, residual(u, dx, flux))) * dx


def total_entropy(u: List, dx):
    return sum(x * x / 2 for x in u) * dx


def solve(u: List[float], dx: float, dt: float, T: float, flux: Callable) -> List[float]:
    """SSP-RK3 in time from 0 to T; the last step is shortened."""
    if not dx > 0 or not dt > 0:
        raise ValueError("dx and dt must be positive")
    t = 0.0
    while t < T - 1e-14:
        h = min(dt, T - t)
        a = [x + h * r for x, r in zip(u, residual(u, dx, flux))]
        b = [0.75 * x + 0.25 * (y + h * r) for x, y, r in zip(u, a, residual(a, dx, flux))]
        u = [x / 3 + 2 / 3 * (y + h * r) for x, y, r in zip(u, b, residual(b, dx, flux))]
        t += h
    return u
