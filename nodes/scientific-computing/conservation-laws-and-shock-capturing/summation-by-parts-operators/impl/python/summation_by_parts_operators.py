# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/summation-by-parts-operators/. The authors are listed in prov/SK4AFB.jsonl.

"""Diagonal-norm summation-by-parts (SBP) first-derivative operators and SAT boundary terms.

An SBP operator on the n + 1 nodes x_i = i h of [0, L] is D = H^{-1} Q with H diagonal and
positive and Q + Q^T = B = diag(-1, 0, ..., 0, 1). Two operators are built here, with exact
rational entries when h is a Fraction:
  sbp21: second order inside, first order at the boundary (H = h diag(1/2, 1, ..., 1, 1/2));
  sbp42: fourth order inside, second order at the boundary (H = h diag(17/48, 59/48, 43/48,
         49/48, 1, ...)), the classical diagonal-norm operator with these weights.
SAT: for u_t + a u_x = 0 with a > 0 and inflow data g at x = 0, the semi-discrete scheme
du/dt = -a D u - tau a H^{-1} e_0 (u_0 - g) is energy stable for tau >= 1/2.

Precondition: n >= 2 (sbp21) or n >= 8 (sbp42), h > 0. Cost: building D is Theta(n^2)
in this dense form (it has Theta(n) nonzeros); one product D u costs Theta(n) with the
sparse rows used by apply().
"""

from fractions import Fraction as Fr
from typing import List, Tuple

Matrix = List[List]

_D42 = [
    [Fr(-24, 17), Fr(59, 34), Fr(-4, 17), Fr(-3, 34), 0, 0],
    [Fr(-1, 2), 0, Fr(1, 2), 0, 0, 0],
    [Fr(4, 43), Fr(-59, 86), 0, Fr(59, 86), Fr(-4, 43), 0],
    [Fr(3, 98), 0, Fr(-59, 98), 0, Fr(32, 49), Fr(-4, 49)],
]
_H42 = [Fr(17, 48), Fr(59, 48), Fr(43, 48), Fr(49, 48)]


def sbp21(n: int, h) -> Tuple[List, Matrix]:
    """Norm weights H (a list) and dense D for the (2,1) operator on n + 1 nodes."""
    if n < 2:
        raise ValueError("need n >= 2")
    H = [h / 2] + [h] * (n - 1) + [h / 2]                    # @line L1
    D = [[0 * h] * (n + 1) for _ in range(n + 1)]
    D[0][0], D[0][1] = -1 / h, 1 / h
    D[n][n - 1], D[n][n] = -1 / h, 1 / h
    for i in range(1, n):
        D[i][i - 1], D[i][i + 1] = -1 / (2 * h), 1 / (2 * h)  # @line L2
    return H, D


def sbp42(n: int, h) -> Tuple[List, Matrix]:
    """Norm weights H and dense D for the diagonal-norm (4,2) operator on n + 1 nodes."""
    if n < 8:
        raise ValueError("need n >= 8")
    H = [w * h for w in _H42] + [h] * (n - 7) + [w * h for w in reversed(_H42)]
    D = [[0 * h] * (n + 1) for _ in range(n + 1)]
    for i in range(4):
        for j in range(6):
            D[i][j] = _D42[i][j] / h
            D[n - i][n - j] = -_D42[i][j] / h                # mirror: D[n-i][n-j] = -D[i][j]
    for i in range(4, n - 3):
        for off, c in ((-2, Fr(1, 12)), (-1, Fr(-2, 3)), (1, Fr(2, 3)), (2, Fr(-1, 12))):
            D[i][i + off] = c / h
    return H, D


def q_matrix(H: List, D: Matrix) -> Matrix:
    """Q = H D."""
    return [[H[i] * d for d in D[i]] for i in range(len(H))]


def apply(D: Matrix, u: List) -> List:
    """D u using only the nonzero entries of each row."""
    return [sum(d * x for d, x in zip(row, u) if d != 0) for row in D]


def sat_advection_rhs(H: List, D: Matrix, u: List, a, g, tau=1) -> List:
    """du/dt = -a D u - tau a H^{-1} e_0 (u_0 - g) for u_t + a u_x = 0, a > 0."""
    r = [-a * x for x in apply(D, u)]                         # @line L3
    r[0] -= tau * a * (u[0] - g) / H[0]                       # @line L4
    return r


def energy_rate(H: List, D: Matrix, u: List, a, g, tau=1):
    """d/dt (u^T H u) for the SAT scheme, computed from the right side."""
    r = sat_advection_rhs(H, D, u, a, g, tau)
    return 2 * sum(w * x * y for w, x, y in zip(H, u, r))    # @line L5


def solve_advection(op, n: int, a: float, T: float, cfl: float, u0, g) -> List[float]:
    """Classical RK4 for u_t + a u_x = 0 on [0, 1] with SAT inflow g(t) at x = 0."""
    h = 1.0 / n
    H, D = op(n, h)
    H, D = [float(w) for w in H], [[float(d) for d in row] for row in D]
    u = [u0(i * h) for i in range(n + 1)]
    steps = max(1, int(round(T / (cfl * h / a))))
    dt, t = T / steps, 0.0
    f = lambda t, v: sat_advection_rhs(H, D, v, a, g(t))
    for _ in range(steps):
        k1 = f(t, u)
        k2 = f(t + dt / 2, [x + dt / 2 * y for x, y in zip(u, k1)])
        k3 = f(t + dt / 2, [x + dt / 2 * y for x, y in zip(u, k2)])
        k4 = f(t + dt, [x + dt * y for x, y in zip(u, k3)])
        u = [x + dt / 6 * (p + 2 * q + 2 * r + s) for x, p, q, r, s in zip(u, k1, k2, k3, k4)]
        t += dt
    return u
