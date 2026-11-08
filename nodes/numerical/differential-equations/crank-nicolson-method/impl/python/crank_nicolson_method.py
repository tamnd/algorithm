# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/crank-nicolson-method/. The authors are listed in prov/NNF3BE.jsonl.

"""The Crank-Nicolson scheme (and the theta family) for the heat equation u_t = kappa u_xx.

Grid x_j = j dx on [0, length], j = 0..M, and t_n = n dt. With r = kappa dt / dx^2 and the
second difference (D U)_j = U_{j-1} - 2 U_j + U_{j+1}, one step solves

    (I - theta r D) U^{n+1} = (I + (1 - theta) r D) U^n,

theta = 1/2 is Crank-Nicolson, theta = 1 is backward Euler, theta = 0 is the explicit FTCS scheme.
Boundaries: "dirichlet" with values left(t), right(t), or "neumann" with zero flux (ghost points),
for which the trapezoidal total heat dx (U_0/2 + U_1 + ... + U_{M-1} + U_M/2) is conserved.
"""

import math
from typing import Callable, List, Sequence, Tuple, Union

Value = Union[float, Callable[[float], float]]


def thomas(a: Sequence[float], b: Sequence[float], c: Sequence[float], d: Sequence[float]) -> List[float]:
    """Solve a_i x_{i-1} + b_i x_i + c_i x_{i+1} = d_i (a_0 and c_{n-1} unused) without pivoting."""
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


def _val(g: Value, t: float) -> float:
    return float(g(t)) if callable(g) else float(g)


def crank_nicolson(u0: Union[Callable[[float], float], Sequence[float]], kappa: float, length: float,
                   t_end: float, m: int, dt: float, left: Value = 0.0, right: Value = 0.0,
                   bc: str = "dirichlet", theta: float = 0.5) -> Tuple[List[float], List[float], dict]:
    """Advance from t = 0 to t_end with N = ceil(t_end / dt) equal steps of size t_end / N.

    u0 is a function of x or a list of m + 1 grid values. Returns (xs, U at t_end, info) with
    info = {"steps", "dt", "r"}.
    """
    if m < 2 or kappa < 0 or length <= 0 or t_end < 0 or dt <= 0 or bc not in ("dirichlet", "neumann"):
        raise ValueError("invalid arguments")
    dx = length / m  # @line L1: grid, number of steps and r
    xs = [j * dx for j in range(m + 1)]
    u = [float(u0(x)) for x in xs] if callable(u0) else [float(v) for v in u0]
    if len(u) != m + 1:
        raise ValueError("u0 must have m + 1 values")
    n_steps = 0 if t_end == 0 else max(1, math.ceil(t_end / dt - 1e-12))
    k = t_end / n_steps if n_steps else 0.0
    r = kappa * k / (dx * dx)
    if bc == "dirichlet":
        u[0], u[-1] = _val(left, 0.0), _val(right, 0.0)
        lo, hi = 1, m - 1  # unknowns U_1..U_{M-1}
    else:
        lo, hi = 0, m  # unknowns U_0..U_M, ghost values U_{-1} = U_1, U_{M+1} = U_{M-1}
    size = hi - lo + 1
    a = [-theta * r] * size
    b = [1 + 2 * theta * r] * size
    c = [-theta * r] * size
    if bc == "neumann":
        c[0] = -2 * theta * r
        a[-1] = -2 * theta * r
    for n in range(n_steps):  # @line L2
        t1 = (n + 1) * k
        if bc == "dirichlet":
            d = [u[j] + (1 - theta) * r * (u[j - 1] - 2 * u[j] + u[j + 1]) for j in range(1, m)]  # @line L3
            g0, g1 = _val(left, t1), _val(right, t1)
            d[0] += theta * r * g0  # @line L4: boundary values at the new time
            d[-1] += theta * r * g1
        else:
            ext = [u[1]] + u + [u[m - 1]]
            d = [ext[j + 1] + (1 - theta) * r * (ext[j] - 2 * ext[j + 1] + ext[j + 2]) for j in range(m + 1)]
        v = thomas(a, b, c, d)  # @line L5
        u = [g0] + v + [g1] if bc == "dirichlet" else v  # @line L6
    return xs, u, {"steps": n_steps, "dt": k, "r": r}  # @line L7
