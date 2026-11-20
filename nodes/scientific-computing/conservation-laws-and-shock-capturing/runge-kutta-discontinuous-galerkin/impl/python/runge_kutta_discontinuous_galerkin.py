# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/runge-kutta-discontinuous-galerkin/. The authors are listed in prov/FE63NV.jsonl.

"""Runge-Kutta discontinuous Galerkin (RKDG) method of Cockburn and Shu, 1D scalar case.

Space: modal DG with Legendre polynomials P_0..P_k on each cell of a periodic grid of M
cells, xi = 2 (x - x_j) / dx, so U[j][0] is the cell average. Face fluxes come from a
monotone numerical flux. Time: three-stage SSP Runge-Kutta (Shu and Osher 1988). After
the initial projection and after every stage the TVB slope limiter of Cockburn and Shu
is applied: the face deviations u(x_{j+1/2}^-) - mean and mean - u(x_{j-1/2}^+) are passed
through the modified minmod function with the differences of the neighbouring means; if
either changes, the cell is replaced by a linear function with a limited slope. The
constant Mtvb (the TVB constant, a choice) switches limiting off where the deviation is at
most Mtvb dx^2; Mtvb = 0 gives the TVDM (minmod) limiter.

Precondition: M >= 3 cells, 0 <= k <= 2, dx > 0, dt > 0, a consistent monotone flux.
Cost: Theta(M (k + 1)^2) per stage, Theta(N M (k + 1)^2) for N steps; memory Theta(M (k + 1)).
"""

import math
from typing import Callable, List, Tuple

Coeffs = List[List[float]]


def legendre(l: int, x: float) -> float:
    """P_l(x) by the three-term recurrence."""
    p0, p1 = 1.0, x
    if l == 0:
        return p0
    for n in range(1, l):
        p0, p1 = p1, ((2 * n + 1) * x * p1 - n * p0) / (n + 1)
    return p1


def legendre_deriv(l: int, x: float) -> float:
    """P_l'(x) = sum over m < l with l - m odd of (2m + 1) P_m(x)."""
    return sum((2 * m + 1) * legendre(m, x) for m in range(l - 1, -1, -2))


def gauss_legendre(q: int) -> Tuple[List[float], List[float]]:
    """q-point Gauss-Legendre rule on [-1, 1] by Newton's method on P_q."""
    out = []
    for i in range(q):
        x = math.cos(math.pi * (i + 0.75) / (q + 0.5))
        for _ in range(100):
            dp = q * (legendre(q - 1, x) - x * legendre(q, x)) / (1 - x * x)
            step = legendre(q, x) / dp
            x -= step
            if abs(step) < 1e-16:
                break
        dp = q * (legendre(q - 1, x) - x * legendre(q, x)) / (1 - x * x)
        out.append((x, 2.0 / ((1 - x * x) * dp * dp)))
    out.sort()
    return [a for a, _ in out], [b for _, b in out]


def godunov_flux_burgers(ul: float, ur: float) -> float:
    """Exact Godunov flux for f(u) = u^2 / 2."""
    if ul > ur:
        return max(ul * ul, ur * ur) / 2
    if ul > 0:
        return ul * ul / 2
    if ur < 0:
        return ur * ur / 2
    return 0.0


def project(u0: Callable, M: int, k: int, xl: float, xr: float, q: int = 8) -> Coeffs:
    """L2 projection of u0 onto piecewise polynomials of degree k."""
    dx = (xr - xl) / M
    nodes, weights = gauss_legendre(q)
    return [[(2 * l + 1) / 2 * sum(w * u0(xl + (j + 0.5) * dx + s * dx / 2) * legendre(l, s)
                                   for s, w in zip(nodes, weights)) for l in range(k + 1)]
            for j in range(M)]


def dg_operator(U: Coeffs, dx: float, f: Callable, flux: Callable) -> Coeffs:
    """DG right side: dU[j][l]/dt = (2l+1)/dx (int f(u_h) P_l' - F_{j+1/2} + (-1)^l F_{j-1/2})."""
    M, k = len(U), len(U[0]) - 1
    nodes, weights = gauss_legendre(k + 2)
    P = [[legendre(l, s) for l in range(k + 1)] for s in nodes]
    WD = [[w * legendre_deriv(l, s) for s, w in zip(nodes, weights)] for l in range(k + 1)]
    F = [flux(sum(U[j]), sum(c if l % 2 == 0 else -c for l, c in enumerate(U[(j + 1) % M])))
         for j in range(M)]
    R = []
    for j in range(M):
        vals = [f(sum(c * p for c, p in zip(U[j], Pq))) for Pq in P]
        R.append([(2 * l + 1) / dx * (sum(a * b for a, b in zip(WD[l], vals)) - F[j]
                                      + (1 if l % 2 == 0 else -1) * F[j - 1])
                  for l in range(k + 1)])
    return R


def minmod(a: float, b: float, c: float) -> float:
    """s min(|a|, |b|, |c|) if a, b, c have the same sign s, else 0."""
    if a > 0 and b > 0 and c > 0:
        return min(a, b, c)
    if a < 0 and b < 0 and c < 0:
        return max(a, b, c)
    return 0.0


def tvb_minmod(a: float, b: float, c: float, Mdx2: float) -> float:
    """Modified minmod: a itself if |a| <= Mtvb dx^2, else minmod(a, b, c)."""
    return a if abs(a) <= Mdx2 else minmod(a, b, c)


def limit(U: Coeffs, dx: float, Mtvb: float) -> Coeffs:
    """TVB slope limiter of Cockburn and Shu applied to every cell (periodic grid)."""
    M, k = len(U), len(U[0]) - 1
    if k == 0:
        return [list(r) for r in U]
    Mdx2 = Mtvb * dx * dx
    out = []
    for j in range(M):
        mean = U[j][0]
        dp = U[(j + 1) % M][0] - mean                         # @line L5
        dm = mean - U[j - 1][0]
        right = sum(U[j]) - mean                              # u(x_{j+1/2}^-) - mean
        left = mean - sum(c if l % 2 == 0 else -c for l, c in enumerate(U[j]))
        r_mod = tvb_minmod(right, dp, dm, Mdx2)               # @line L6
        l_mod = tvb_minmod(left, dp, dm, Mdx2)
        if r_mod == right and l_mod == left:                  # @line L7
            out.append(list(U[j]))
        else:
            slope = tvb_minmod(U[j][1], dp, dm, Mdx2)         # @line L8
            out.append([mean, slope] + [0.0] * (k - 1))
    return out


def _lin(a, X, b, Y):
    return [[a * x + b * y for x, y in zip(rx, ry)] for rx, ry in zip(X, Y)]


def rkdg_step(U: Coeffs, dx: float, dt: float, f: Callable, flux: Callable, Mtvb: float) -> Coeffs:
    """One SSP-RK3 step with the limiter after each stage."""
    L = lambda V: dg_operator(V, dx, f, flux)
    U1 = limit(_lin(1, U, dt, L(U)), dx, Mtvb)                                 # @line L2
    U2 = limit(_lin(3 / 4, U, 1 / 4, _lin(1, U1, dt, L(U1))), dx, Mtvb)        # @line L3
    return limit(_lin(1 / 3, U, 2 / 3, _lin(1, U2, dt, L(U2))), dx, Mtvb)      # @line L4


def rkdg_solve(U: Coeffs, dx: float, dt: float, T: float, f: Callable, flux: Callable,
               Mtvb: float = 0.0, limiter: bool = True) -> Coeffs:
    """Advance from t = 0 to t = T; the last step is shortened. limiter=False gives plain DG."""
    if not dx > 0 or not dt > 0:
        raise ValueError("dx and dt must be positive")
    big = float("inf")
    U = limit(U, dx, Mtvb) if limiter else [list(r) for r in U]
    t = 0.0
    while t < T - 1e-14:                                                       # @line L1
        h = min(dt, T - t)
        U = rkdg_step(U, dx, h, f, flux, Mtvb if limiter else big)
        t += h
    return U


def means(U: Coeffs) -> List[float]:
    return [r[0] for r in U]


def total_variation(v: List[float]) -> float:
    """Periodic total variation sum |v_{j+1} - v_j|."""
    return sum(abs(v[(j + 1) % len(v)] - v[j]) for j in range(len(v)))
