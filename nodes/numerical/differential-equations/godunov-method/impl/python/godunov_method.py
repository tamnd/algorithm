# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/godunov-method/. The authors are listed in prov/H99E04.jsonl.

"""Godunov's method for a 1D scalar conservation law u_t + f(u)_x = 0 with convex flux f.

At every cell face the Riemann problem between the two neighbouring cell averages is solved
exactly and its value on the face (x/t = 0) gives the numerical flux.
"""

import math
from dataclasses import dataclass
from typing import Callable, List, Optional, Sequence

GRID_SLACK = 1e-9


@dataclass
class GodunovResult:
    u: List
    steps: int
    riemann_solves: int
    max_cfl: float     # largest Courant number max|f'(u)| dt/dx seen at the start of a step


def riemann_face_state(ul, ur, f: Callable, df: Callable, u_sonic=None):
    """Value at x/t = 0 of the entropy solution of the Riemann problem (ul, ur).

    f is convex with nondecreasing derivative df; u_sonic is the point with df = 0
    (None if df never vanishes).
    """
    if ul > ur:  # shock with Rankine-Hugoniot speed
        sigma = (f(ul) - f(ur)) / (ul - ur)
        return ul if sigma >= 0 else ur
    if df(ul) >= 0:  # rarefaction moving right
        return ul
    if df(ur) <= 0:  # rarefaction moving left
        return ur
    return u_sonic  # transonic rarefaction: the face sits in the fan at the sonic point


def godunov(u: Sequence, dx, dt, t_end, f: Callable, df: Callable, u_sonic=None,
            bc: str = "transmissive") -> GodunovResult:
    """Advance cell averages from t = 0 to t_end with Godunov's method (last step shortened)."""
    if not dx > 0 or not dt > 0:
        raise ValueError("dx and dt must be positive")
    if t_end < 0:
        raise ValueError("t_end must be nonnegative")
    if bc not in ("periodic", "transmissive"):
        raise ValueError("bc must be 'periodic' or 'transmissive'")
    m = len(u)
    u = list(u)
    if m == 0:
        return GodunovResult(u, 0, 0, 0.0)
    n_steps = 0 if t_end == 0 else max(1, math.ceil(t_end / dt - GRID_SLACK))
    t = 0
    solves = 0
    max_cfl = 0.0
    for n in range(n_steps):  # @line L1
        k = t_end - t if n == n_steps - 1 else dt
        max_cfl = max(max_cfl, float(max(abs(df(v)) for v in u) * k / dx))
        ext = ([u[-1]] + u + [u[0]]) if bc == "periodic" else ([u[0]] + u + [u[-1]])  # @line L2
        F = []
        for i in range(m + 1):
            w = riemann_face_state(ext[i], ext[i + 1], f, df, u_sonic)  # @line L3
            F.append(f(w))  # @line L4
        solves += m + 1
        lam = k / dx
        u = [u[i] - lam * (F[i + 1] - F[i]) for i in range(m)]  # @line L5
        t = t + k if n < n_steps - 1 else t_end
    return GodunovResult(u, n_steps, solves, max_cfl)  # @line L6
