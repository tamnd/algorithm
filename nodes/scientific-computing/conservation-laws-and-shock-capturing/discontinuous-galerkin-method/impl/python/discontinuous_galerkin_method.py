# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discontinuous-galerkin-method/. The authors are listed in prov/TAT3SX.jsonl.

"""Modal discontinuous Galerkin method for a 1D scalar conservation law u_t + f(u)_x = 0.

The grid is periodic with M cells of width dx. On cell C_j the solution is
u_h(x) = sum_{l=0}^{k} U[j][l] P_l(xi), with xi = 2 (x - x_j) / dx in [-1, 1] and P_l the
Legendre polynomials, so U[j][0] is the cell average. The space operator is the DG
operator with a numerical flux on each face; time stepping is the three-stage SSP
Runge-Kutta method of Shu and Osher (method of lines). No limiter is applied.

Precondition: M >= 1 cells, degree k >= 0, dx > 0, dt > 0, and a numerical flux that is
consistent (flux(u, u) = f(u)). With q = k + 1 Gauss points the volume integral is exact
when f is linear; for f(u) = u^2 / 2 it is exact for k <= 2.

Cost: one evaluation of the operator takes Theta(M (k + 1)^2) operations after the
basis tables are built, three evaluations make one step, and the memory is Theta(M (k + 1)).
"""

import math
from typing import Callable, List, Sequence, Tuple

Coeffs = List[List[float]]


def legendre(l: int, x: float) -> float:
    """P_l(x) by the three-term recurrence."""
    if l == 0:
        return 1.0 + 0 * x
    p0, p1 = 1.0 + 0 * x, x
    for n in range(1, l):
        p0, p1 = p1, ((2 * n + 1) * x * p1 - n * p0) / (n + 1)
    return p1


def legendre_deriv(l: int, x: float) -> float:
    """P_l'(x) from the identity P_l' = sum over m < l with l - m odd of (2m + 1) P_m."""
    return sum((2 * m + 1) * legendre(m, x) for m in range(l - 1, -1, -2))


def gauss_legendre(q: int) -> Tuple[List[float], List[float]]:
    """Nodes and weights of the q-point Gauss-Legendre rule on [-1, 1] (Newton on P_q)."""
    nodes, weights = [], []
    for i in range(q):
        x = math.cos(math.pi * (i + 0.75) / (q + 0.5))
        for _ in range(100):
            p, dp = legendre(q, x), q * (legendre(q - 1, x) - x * legendre(q, x)) / (1 - x * x)
            dx = p / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        dp = q * (legendre(q - 1, x) - x * legendre(q, x)) / (1 - x * x)
        nodes.append(x)
        weights.append(2.0 / ((1 - x * x) * dp * dp))
    order = sorted(range(q), key=lambda i: nodes[i])
    return [nodes[i] for i in order], [weights[i] for i in order]


def upwind_flux(a: float) -> Callable:
    """Upwind flux for f(u) = a u."""
    return lambda ul, ur: a * ul if a >= 0 else a * ur


def godunov_flux_burgers(ul: float, ur: float) -> float:
    """Exact Godunov flux for f(u) = u^2 / 2."""
    if ul > ur:
        return max(ul * ul, ur * ur) / 2
    if ul > 0:
        return ul * ul / 2
    if ur < 0:
        return ur * ur / 2
    return 0.0


def project(u0: Callable, M: int, k: int, xl: float, xr: float, q: int = 0) -> Coeffs:
    """L2 projection of u0 onto piecewise polynomials of degree k (Gauss quadrature)."""
    dx = (xr - xl) / M
    nodes, weights = gauss_legendre(q or k + 3)
    U = []
    for j in range(M):
        xc = xl + (j + 0.5) * dx
        U.append([(2 * l + 1) / 2 * sum(w * u0(xc + s * dx / 2) * legendre(l, s)
                                         for s, w in zip(nodes, weights)) for l in range(k + 1)])
    return U


def dg_operator(U: Coeffs, dx: float, f: Callable, flux: Callable, quad=None) -> Coeffs:
    """Right side R = L(U) of the semi-discrete DG system dU/dt = L(U), periodic grid."""
    M, k = len(U), len(U[0]) - 1
    nodes, weights = quad or gauss_legendre(k + 1)
    P = [[legendre(l, s) for l in range(k + 1)] for s in nodes]
    WD = [[w * legendre_deriv(l, s) for s, w in zip(nodes, weights)] for l in range(k + 1)]
    F = []
    for j in range(M):                                        # face j + 1/2
        um = sum(U[j])                                        # @line L2
        up = sum(c if l % 2 == 0 else -c for l, c in enumerate(U[(j + 1) % M]))
        F.append(flux(um, up))                                # @line L3
    R = []
    for j in range(M):                                        # @line L4
        vals = [f(sum(c * p for c, p in zip(U[j], Pq))) for Pq in P]
        row = []
        for l in range(k + 1):
            V = sum(wd * v for wd, v in zip(WD[l], vals))     # @line L5
            sign = 1 if l % 2 == 0 else -1
            row.append((2 * l + 1) / dx * (V - F[j] + sign * F[j - 1]))  # @line L6
        R.append(row)
    return R                                                  # @line L7


def _axpy(a, X, b, Y):
    return [[a * x + b * y for x, y in zip(rx, ry)] for rx, ry in zip(X, Y)]


def ssp_rk3_step(U: Coeffs, dt: float, L: Callable) -> Coeffs:
    """One step of the three-stage SSP Runge-Kutta method of Shu and Osher (1988)."""
    U1 = _axpy(1, U, dt, L(U))
    U2 = _axpy(3 / 4, U, 1 / 4, _axpy(1, U1, dt, L(U1)))
    return _axpy(1 / 3, U, 2 / 3, _axpy(1, U2, dt, L(U2)))


def dg_solve(U: Coeffs, dx: float, dt: float, T: float, f: Callable, flux: Callable) -> Coeffs:
    """Advance the DG coefficients from t = 0 to t = T; the last step is shortened."""
    if not dx > 0 or not dt > 0:
        raise ValueError("dx and dt must be positive")
    quad = gauss_legendre(len(U[0]))
    t = 0.0
    U = [list(r) for r in U]
    while t < T - 1e-14:                                      # @line L1
        h = min(dt, T - t)
        U = ssp_rk3_step(U, h, lambda V: dg_operator(V, dx, f, flux, quad))
        t += h
    return U


def evaluate(U: Coeffs, j: int, xi: float) -> float:
    """u_h at the reference point xi of cell j."""
    return sum(c * legendre(l, xi) for l, c in enumerate(U[j]))


def l2_error(U: Coeffs, exact: Callable, xl: float, xr: float, q: int = 8) -> float:
    """||u_h - exact||_2 over the domain, by q-point Gauss quadrature in each cell."""
    M = len(U)
    dx = (xr - xl) / M
    nodes, weights = gauss_legendre(q)
    s = 0.0
    for j in range(M):
        xc = xl + (j + 0.5) * dx
        s += sum(w * (evaluate(U, j, xi) - exact(xc + xi * dx / 2)) ** 2
                 for xi, w in zip(nodes, weights)) * dx / 2
    return math.sqrt(s)


def total_mass(U: Coeffs, dx: float) -> float:
    """sum_j U[j][0] dx, the integral of u_h."""
    return sum(r[0] for r in U) * dx


def energy(U: Coeffs, dx: float) -> float:
    """||u_h||_2^2 = sum_j sum_l dx / (2l + 1) U[j][l]^2."""
    return sum(dx / (2 * l + 1) * c * c for r in U for l, c in enumerate(r))
