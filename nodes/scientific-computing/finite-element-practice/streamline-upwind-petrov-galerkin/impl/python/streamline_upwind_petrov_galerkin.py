# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/streamline-upwind-petrov-galerkin/. The authors are listed in prov/CZJ24B.jsonl.

"""SUPG with P1 elements for -eps u'' + a u' = f on (0, 1), u(0) = g0, u(1) = g1.

The mesh is uniform with m cells of width h = 1/m. eps > 0 and a != 0 are
constants. The test function of the SUPG method is v + tau a v' on each
cell. With P1 elements u'' = 0 inside a cell, so the SUPG term is
tau (a v', a u' - f) on each cell. The global matrix is tridiagonal and is
solved by the Thomas algorithm, so one solve costs Theta(m) operations.
With Fraction data and a Fraction tau the result is exact.
"""

import math
from fractions import Fraction

import scisparse

# Boole's rule on [0, 1]: exact for polynomials of degree <= 5, rational weights.
BOOLE = [(Fraction(0), Fraction(7, 90)), (Fraction(1, 4), Fraction(32, 90)),
         (Fraction(1, 2), Fraction(12, 90)), (Fraction(3, 4), Fraction(32, 90)),
         (Fraction(1), Fraction(7, 90))]


def cell_peclet(eps, a, h):
    """Return the cell Peclet number Pe_h = |a| h / (2 eps)."""
    return abs(a) * h / (2 * eps)


def optimal_tau(eps, a, h):
    """Return tau = h / (2 |a|) (coth(Pe_h) - 1 / Pe_h), the nodally exact choice in 1D."""
    pe = float(cell_peclet(eps, a, h))
    if pe < 1e-4:
        xi = pe / 3.0 - pe ** 3 / 45.0  # series of coth(pe) - 1/pe, avoids cancellation
    else:
        xi = 1.0 / math.tanh(pe) - 1.0 / pe
    return float(h) / (2.0 * abs(float(a))) * xi


def supg(eps, a, f, m, g0=0, g1=0, tau=None):
    """Solve the SUPG problem and return the nodal values U_0, ..., U_m.

    f is a function of x. tau=None takes optimal_tau; tau=0 gives the plain
    Galerkin method. Precondition: m >= 2, eps > 0, a != 0, and tau >= 0.
    Cost: Theta(m) operations and Theta(m) memory.
    """
    h = Fraction(1, m) if isinstance(eps, Fraction) else 1.0 / m  # @line L1
    if tau is None:
        tau = optimal_tau(eps, a, h)  # @line L2
    n = m + 1
    lo = [0] * n  # sub-diagonal: lo[i] multiplies U[i-1] in row i
    di = [0] * n  # diagonal
    up = [0] * n  # super-diagonal: up[i] multiplies U[i+1] in row i
    rhs = [0] * n
    dphi = (-1 / h, 1 / h)  # derivatives of the two local hat functions
    for j in range(m):  # @line L3
        x0 = j * h
        ak = [[0, 0], [0, 0]]
        bk = [0, 0]
        for r in range(2):
            for s in range(2):
                # eps (phi_s', phi_r') + a (phi_s', phi_r) + tau a^2 (phi_s', phi_r')
                ak[r][s] = (eps + tau * a * a) * dphi[s] * dphi[r] * h + a * dphi[s] * h / 2  # @line L4
            for xi, w in BOOLE:
                phi = (1 - xi, xi)[r]
                bk[r] += w * h * f(x0 + xi * h) * (phi + tau * a * dphi[r])  # @line L5
        # add the 2 by 2 block into the tridiagonal arrays
        di[j] += ak[0][0]  # @line L6
        up[j] += ak[0][1]
        lo[j + 1] += ak[1][0]
        di[j + 1] += ak[1][1]
        rhs[j] += bk[0]
        rhs[j + 1] += bk[1]
    # Dirichlet rows: U_0 = g0 and U_m = g1; move the known values to the right side
    rhs[1] -= lo[1] * g0  # @line L7
    rhs[m - 1] -= up[m - 1] * g1
    lo[1] = 0
    up[m - 1] = 0
    inner = scisparse.thomas(lo[1:m], di[1:m], up[1:m], rhs[1:m])  # @line L8
    return [g0] + inner + [g1]  # @line L9


def exact(eps, a, c, g0, g1, x):
    """Exact solution of -eps u'' + a u' = c (a constant c) with u(0) = g0, u(1) = g1."""
    r = a / eps
    if r > 0:
        # w(x) = (e^(r x) - 1) / (e^r - 1), written as e^(r (x - 1)) forms to avoid overflow
        w = (math.exp(r * (x - 1)) - math.exp(-r)) / (1 - math.exp(-r))
    else:
        w = (math.exp(r * x) - 1) / (math.exp(r) - 1)
    lin = c * x / a
    # u = lin + g0 + (g1 - g0 - c / a) w satisfies both boundary values
    return lin + g0 + (g1 - g0 - c / a) * w
