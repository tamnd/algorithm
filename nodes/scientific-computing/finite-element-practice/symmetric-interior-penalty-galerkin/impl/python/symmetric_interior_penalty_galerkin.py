# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/symmetric-interior-penalty-galerkin/. The authors are listed in prov/Z6FE5T.jsonl.

"""SIPG for -u'' = f on (0, 1) with u(0) = g0 and u(1) = g1, imposed weakly.

The mesh is uniform with m cells x_j = j h, h = 1/m. On each cell the
discrete solution is a polynomial of degree k, written in the local
monomial basis phi_r(x) = xi^r with xi = (x - x_j) / h, r = 0, ..., k.
The unknown of (cell j, power r) has the global index j (k + 1) + r.

Jumps and averages at a node x_e: [v] = v(x_e-) - v(x_e+) and
{v'} = (v'(x_e-) + v'(x_e+)) / 2 inside; [v] = v(1-), {v'} = v'(1-) at
x = 1 and [v] = -v(0+), {v'} = v'(0+) at x = 0. The bilinear form is

    a(u, v) = sum_K (u', v')_K - sum_e ({u'}[v] + {v'}[u]) + sum_e (sigma / h) [u][v].

With Fraction data the matrix and the solution are exact.
"""

from fractions import Fraction

import scimat

BOOLE = [(Fraction(0), Fraction(7, 90)), (Fraction(1, 4), Fraction(32, 90)),
         (Fraction(1, 2), Fraction(12, 90)), (Fraction(3, 4), Fraction(32, 90)),
         (Fraction(1), Fraction(7, 90))]


def local_traces(k, h, side):
    """Return (values, derivatives) of phi_0..phi_k at the left (side=0) or right (side=1) end."""
    if side == 0:
        val = [1 if r == 0 else 0 for r in range(k + 1)]
        der = [1 / h if r == 1 else 0 for r in range(k + 1)]
    else:
        val = [1] * (k + 1)
        der = [r / h for r in range(k + 1)]
    return val, der


def sipg_system(f, m, k, sigma, g0=0, g1=0):
    """Return the SIPG matrix A and load vector b, of size m (k + 1).

    Precondition: m >= 1, k >= 1. sigma is the penalty parameter; the
    penalty on a node is sigma / h. Cost: Theta(m k^2) entries.
    """
    exact_data = isinstance(sigma, Fraction)
    h = Fraction(1, m) if exact_data else 1.0 / m
    n = k + 1
    size = m * n
    A = scimat.zeros(size)
    b = [0] * size
    for j in range(m):  # @line L1
        off = j * n
        for r in range(n):
            for s in range(n):
                if r >= 1 and s >= 1:
                    # (phi_s', phi_r')_K = r s / (h (r + s - 1))
                    A[off + r][off + s] += Fraction(r * s, r + s - 1) / h if exact_data else r * s / (h * (r + s - 1))  # @line L2
            for xi, w in BOOLE:
                b[off + r] += w * h * f(j * h + xi * h) * xi ** r  # @line L3
    # node e = 0..m; each side is (cell, end, weight of the average, sign of the jump)
    for e in range(m + 1):  # @line L4
        sides = []
        if e > 0:
            sides.append((e - 1, 1, Fraction(1, 2) if e < m else 1, 1))  # left cell, its right end
        if e < m:
            sides.append((e, 0, Fraction(1, 2) if e > 0 else 1, -1))  # right cell, its left end
        for (cu, eu, wu, su) in sides:
            vu, du = local_traces(k, h, eu)
            for (cv, ev, wv, sv) in sides:
                vv, dv = local_traces(k, h, ev)
                for r in range(n):  # test function row
                    for s in range(n):  # trial function column
                        term = -wu * du[s] * sv * vv[r]  # -{u'}[v]
                        term -= wv * dv[r] * su * vu[s]  # -{v'}[u]
                        term += sigma / h * su * vu[s] * sv * vv[r]  # (sigma/h)[u][v]
                        A[cv * n + r][cu * n + s] += term  # @line L5
        # weak Dirichlet data: the exact [u] is g1 at x = 1 and -g0 at x = 0
        if e == 0 or e == m:
            gj = -g0 if e == 0 else g1
            cv, ev, wv, sv = sides[0]
            vv, dv = local_traces(k, h, ev)
            for r in range(n):
                b[cv * n + r] += -wv * dv[r] * gj + sigma / h * sv * vv[r] * gj  # @line L6
    return A, b


def sipg(f, m, k, sigma=None, g0=0, g1=0):
    """Solve the SIPG problem; return the coefficients, one list of k + 1 per cell.

    sigma=None takes sigma = 2 k^2 + 1, above the coercivity bound 2 k^2.
    Cost: assembly Theta(m k^2); the dense solve here costs Theta((m k)^3),
    and a banded solver would cost Theta(m k^3).
    """
    if sigma is None:
        sigma = 2 * k * k + 1
    A, b = sipg_system(f, m, k, sigma, g0, g1)
    c = scimat.solve(A, b)  # @line L7
    n = k + 1
    return [c[j * n:(j + 1) * n] for j in range(m)]  # @line L8


def evaluate(coef, m, x):
    """Value and derivative of the discrete solution at x (from the right at a node, left at 1)."""
    h = 1.0 / m
    j = min(int(x * m), m - 1)
    xi = (x - j * h) / h
    c = coef[j]
    val = sum(float(cr) * xi ** r for r, cr in enumerate(c))
    der = sum(float(cr) * r * xi ** (r - 1) for r, cr in enumerate(c) if r >= 1) / h
    return val, der
