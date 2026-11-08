# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adi-method/. The authors are listed in prov/G6HHDK.jsonl.

"""Peaceman-Rachford ADI for the 2D heat equation u_t = kappa (u_xx + u_yy) on a rectangle.

Grid x_i = i dx (i = 0..mx), y_j = j dy (j = 0..my), U[i][j] ~ u(x_i, y_j, t_n),
rx = kappa dt / dx^2, ry = kappa dt / dy^2. One step is two half steps:

    (I - rx/2 Dx) U* = (I + ry/2 Dy) U^n          (implicit in x, one tridiagonal solve per row)
    (I - ry/2 Dy) U^{n+1} = (I + rx/2 Dx) U*      (implicit in y, one tridiagonal solve per column)

Boundaries: "dirichlet" (u = 0) or "neumann" (zero flux, ghost points). With zero flux the
trapezoidal total heat is conserved exactly.
"""

import math
from typing import Callable, List, Tuple, Union


def thomas(a: List[float], b: List[float], c: List[float], d: List[float]) -> List[float]:
    """Solve a_i x_{i-1} + b_i x_i + c_i x_{i+1} = d_i without pivoting."""
    n = len(b)
    cp, dp = [0.0] * n, [0.0] * n
    cp[0], dp[0] = c[0] / b[0], d[0] / b[0]
    for i in range(1, n):
        m = b[i] - a[i] * cp[i - 1]
        cp[i] = c[i] / m if i < n - 1 else 0.0
        dp[i] = (d[i] - a[i] * dp[i - 1]) / m
    x = [0.0] * n
    x[-1] = dp[-1]
    for i in range(n - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]
    return x


class _Line:
    """The 1D operators along one direction with m intervals and ratio r."""

    def __init__(self, m: int, r: float, bc: str):
        self.m, self.r, self.bc = m, r, bc
        self.lo, self.hi = (1, m - 1) if bc == "dirichlet" else (0, m)
        n = self.hi - self.lo + 1
        h = r / 2
        self.a, self.b, self.c = [-h] * n, [1 + 2 * h] * n, [-h] * n
        if bc == "neumann":
            self.c[0] = self.a[-1] = -2 * h

    def second_diff(self, v: List[float], i: int) -> float:
        """(delta^2 v)_i with zero Dirichlet values or zero-flux ghost points."""
        m = self.m
        left = v[i - 1] if i > 0 else v[1]
        right = v[i + 1] if i < m else v[m - 1]
        return left - 2 * v[i] + right

    def solve(self, d: List[float]) -> List[float]:
        """Solve (I - r/2 delta^2) w = d on the unknowns and return the full line."""
        w = thomas(self.a, self.b, self.c, d)
        return [0.0] + w + [0.0] if self.bc == "dirichlet" else w


def adi(u0: Union[Callable[[float, float], float], List[List[float]]], kappa: float, lx: float, ly: float,
        t_end: float, mx: int, my: int, dt: float, bc: str = "dirichlet") -> Tuple[List[List[float]], dict]:
    """Advance from t = 0 to t_end with N = ceil(t_end / dt) equal steps.

    u0 is a function of (x, y) or an (mx + 1) x (my + 1) table. Returns (U, info), info = {"steps", "dt", "rx", "ry"}.
    """
    if mx < 2 or my < 2 or kappa < 0 or lx <= 0 or ly <= 0 or t_end < 0 or dt <= 0 \
            or bc not in ("dirichlet", "neumann"):
        raise ValueError("invalid arguments")
    dx, dy = lx / mx, ly / my  # @line L1: grid, number of steps and ratios
    n_steps = 0 if t_end == 0 else max(1, math.ceil(t_end / dt - 1e-12))
    k = t_end / n_steps if n_steps else 0.0
    rx, ry = kappa * k / dx ** 2, kappa * k / dy ** 2
    if callable(u0):
        u = [[float(u0(i * dx, j * dy)) for j in range(my + 1)] for i in range(mx + 1)]
    else:
        u = [[float(v) for v in row] for row in u0]
    if bc == "dirichlet":
        for i in range(mx + 1):
            u[i][0] = u[i][my] = 0.0
        u[0] = [0.0] * (my + 1)
        u[mx] = [0.0] * (my + 1)
    lx_op, ly_op = _Line(mx, rx, bc), _Line(my, ry, bc)
    for _ in range(n_steps):  # @line L2
        star = [[0.0] * (my + 1) for _ in range(mx + 1)]
        for j in range(ly_op.lo, ly_op.hi + 1):  # first half step: rows j, implicit in x
            d = [u[i][j] + ry / 2 * ly_op.second_diff(u[i], j) for i in range(lx_op.lo, lx_op.hi + 1)]  # @line L3
            col = lx_op.solve(d)  # @line L4
            for i in range(mx + 1):
                star[i][j] = col[i]
        new = [[0.0] * (my + 1) for _ in range(mx + 1)]
        for i in range(lx_op.lo, lx_op.hi + 1):  # second half step: columns i, implicit in y
            west = star[i - 1] if i > 0 else star[1]  # zero-flux ghost row when i = 0
            east = star[i + 1] if i < mx else star[mx - 1]
            mid = star[i]
            d = [mid[j] + rx / 2 * (west[j] - 2 * mid[j] + east[j]) for j in range(ly_op.lo, ly_op.hi + 1)]  # @line L5
            new[i] = ly_op.solve(d)  # @line L6
        u = new
    return u, {"steps": n_steps, "dt": k, "rx": rx, "ry": ry}  # @line L7
