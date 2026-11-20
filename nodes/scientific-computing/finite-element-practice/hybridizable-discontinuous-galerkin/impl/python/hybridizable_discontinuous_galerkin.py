# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybridizable-discontinuous-galerkin/. The authors are listed in prov/EC181T.jsonl.

"""HDG for -u'' = f on (0, 1) with u(0) = g0 and u(1) = g1.

The first-order form is q + u' = 0 and q' = f. The mesh is uniform with m
cells K_j = (x_j, x_j + h), h = 1/m. On each cell q and u are polynomials
of degree k in the local monomial basis xi^r, xi = (x - x_j) / h. The
global unknowns are the traces uhat_0, ..., uhat_m at the nodes. On the
boundary of a cell, with the outward normal n = -1 at the left end and
n = +1 at the right end, the numerical flux is

    qhat n = q n + tau (u - uhat).

Local equations on K, for all polynomials r, w of degree k:

    (q, r)_K - (u, r')_K + [uhat r n]_{boundary of K} = 0
    -(q, w')_K + [qhat n w]_{boundary of K} = (f, w)_K

Global equation at an interior node: the two values of qhat n add up to 0.
With Fraction data (f, tau, g0, g1) every step is exact.
"""

from fractions import Fraction

import scimat
import scisparse

BOOLE = [(Fraction(0), Fraction(7, 90)), (Fraction(1, 4), Fraction(32, 90)),
         (Fraction(1, 2), Fraction(12, 90)), (Fraction(3, 4), Fraction(32, 90)),
         (Fraction(1), Fraction(7, 90))]


def local_matrix(k, h, tau):
    """Matrix of the local problem; unknowns (q_0..q_k, u_0..u_k), rows (r_0..r_k, w_0..w_k)."""
    n = k + 1
    L = scimat.zeros(2 * n)
    for i in range(n):
        for s in range(n):
            L[i][s] = h / (i + s + 1)  # (q, r_i)_K, mass matrix
            if i >= 1:
                d = Fraction(i, i + s) if isinstance(h, Fraction) else i / (i + s)  # (xi^s, (xi^i)')_K
                L[i][n + s] -= d  # -(u, r_i')_K
                L[n + i][s] -= d  # -(q, w_i')_K
            # right end: q n w = q(1) w_i(1), and tau u(1) w_i(1)
            L[n + i][s] += 1
            L[n + i][n + s] += tau
    # left end: n = -1 and w_i(0) = 1 only for i = 0, so row w_0 gets -q(0) + tau u(0)
    L[n][0] -= 1
    L[n][n] += tau
    return L


def local_rhs(f, k, h, x0, tau):
    """Three right sides of the local problem: for uhat_L = 1, for uhat_R = 1, and for f."""
    n = k + 1
    rL = [0] * (2 * n)
    rR = [0] * (2 * n)
    rf = [0] * (2 * n)
    for i in range(n):
        # first equation: -[uhat r n] moves to the right side; r_i(1) = 1, r_i(0) = [i = 0]
        rR[i] = -1
        rL[i] = 1 if i == 0 else 0
        # second equation: -tau uhat w moves to the right side as +tau uhat w
        rR[n + i] = tau
        rL[n + i] = tau if i == 0 else 0
        for xi, wq in BOOLE:
            rf[n + i] += wq * h * f(x0 + xi * h) * xi ** i
    return rL, rR, rf


def end_fluxes(sol, k, tau):
    """Return qhat n at the left and right end for a local solution with uhat = 0 there."""
    n = k + 1
    q, u = sol[:n], sol[n:]
    left = -q[0] + tau * u[0]
    right = sum(q) + tau * sum(u)
    return left, right


def hdg(f, m, k, tau=1, g0=0, g1=0):
    """Solve the HDG problem. Return (uhat, cells) where cells[j] = (q coefficients, u coefficients).

    Precondition: m >= 2, k >= 0, tau > 0. Cost: Theta(m k^3) for the local
    solves and Theta(m) for the trace system.
    """
    exact_data = isinstance(tau, Fraction)
    h = Fraction(1, m) if exact_data else 1.0 / m
    n = k + 1
    L = local_matrix(k, h, tau)
    lo = [0] * (m + 1)
    di = [0] * (m + 1)
    up = [0] * (m + 1)
    rhs = [0] * (m + 1)
    local = []
    for j in range(m):  # @line L1
        rL, rR, rf = local_rhs(f, k, h, j * h, tau)
        cols = scimat.solve(L, [[rL[i], rR[i], rf[i]] for i in range(2 * n)])  # @line L2
        sL = [row[0] for row in cols]
        sR = [row[1] for row in cols]
        sf = [row[2] for row in cols]
        local.append((sL, sR, sf))
        # qhat n at each end is affine in (uhat_L, uhat_R): value(sL) uhat_L + value(sR) uhat_R
        # + value(sf), minus tau uhat at that end
        left_l, right_l = end_fluxes(sL, k, tau)
        left_r, right_r = end_fluxes(sR, k, tau)
        left_f, right_f = end_fluxes(sf, k, tau)
        fl = (left_l - tau, left_r, left_f)  # left end: coefficients of uhat_j, uhat_{j+1}, constant
        fr = (right_l, right_r - tau, right_f)  # right end  # @line L3
        # the global row of node e is -(sum of qhat n) = 0; cell j adds to rows j and j + 1
        di[j] -= fl[0]  # @line L4
        up[j] -= fl[1]
        rhs[j] += fl[2]
        lo[j + 1] -= fr[0]
        di[j + 1] -= fr[1]
        rhs[j + 1] += fr[2]
    rhs[1] -= lo[1] * g0  # @line L5
    rhs[m - 1] -= up[m - 1] * g1
    lo[1] = 0
    up[m - 1] = 0
    inner = scisparse.thomas(lo[1:m], di[1:m], up[1:m], rhs[1:m])  # @line L6
    uhat = [g0] + inner + [g1]
    cells = []
    for j in range(m):  # @line L7
        sL, sR, sf = local[j]
        sol = [sL[i] * uhat[j] + sR[i] * uhat[j + 1] + sf[i] for i in range(2 * n)]
        cells.append((sol[:n], sol[n:]))
    return uhat, cells  # @line L8


def trace_matrix(m, k, tau):
    """Dense matrix of the trace system on the interior nodes (for tests), f = 0."""
    exact_data = isinstance(tau, Fraction)
    zero = (lambda x: Fraction(0)) if exact_data else (lambda x: 0.0)
    size = m - 1
    S = scimat.zeros(size)
    for e in range(1, m):
        g = [0] * (m + 1)
        g[e] = 1
        # the residual of the global rows for uhat = unit vector e, f = 0
        res = residual(zero, m, k, tau, g)
        for i in range(1, m):
            S[i - 1][e - 1] = res[i]
    return S


def residual(f, m, k, tau, uhat):
    """Return the global rows -(sum of qhat n) at every node for given traces (local problems solved exactly)."""
    exact_data = isinstance(tau, Fraction)
    h = Fraction(1, m) if exact_data else 1.0 / m
    n = k + 1
    L = local_matrix(k, h, tau)
    res = [0] * (m + 1)
    for j in range(m):
        rL, rR, rf = local_rhs(f, k, h, j * h, tau)
        b = [rL[i] * uhat[j] + rR[i] * uhat[j + 1] + rf[i] for i in range(2 * n)]
        sol = scimat.solve(L, b)
        q, u = sol[:n], sol[n:]
        left = -q[0] + tau * (u[0] - uhat[j])
        right = sum(q) + tau * (sum(u) - uhat[j + 1])
        res[j] -= left
        res[j + 1] -= right
    return res
