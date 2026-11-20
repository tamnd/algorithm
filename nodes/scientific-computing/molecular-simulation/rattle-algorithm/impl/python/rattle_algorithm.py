# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rattle-algorithm/. The authors are listed in prov/VJX93A.jsonl.
"""RATTLE: velocity Verlet with bond-length constraints on positions and velocities.

This is the method of Andersen (1983). Each constraint (i, j, d) asks
|x_i - x_j| = d, and its time derivative asks (x_i - x_j) . (v_i - v_j) = 0.
One step has two constraint stages.

1. Position stage. Kick and drift as in velocity Verlet, then correct the
   half-step velocities along the old bond vectors (the SHAKE iteration)
   until the new positions satisfy every bond length.
2. Velocity stage. Kick with the new forces, then correct the velocities
   along the new bond vectors until every bond has zero relative velocity
   along its own direction.

w_i = 1 / m_i is the inverse mass (0 for a fixed atom). Both stages solve
their equations to a relative tolerance by Gauss-Seidel sweeps. If both are
solved exactly, the map is symplectic on the constraint manifold and
time-reversible.
"""

from typing import Callable

Vec = list[float]
Bond = tuple[int, int, float]
Force = Callable[[list[Vec]], list[Vec]]


def _dot(a: Vec, b: Vec) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def rattle_step(
    x: list[Vec], v: list[Vec], f: list[Vec], inv_mass: list[float], force: Force, h: float,
    bonds: list[Bond], tol: float = 1e-13, max_sweeps: int = 1000,
) -> tuple[list[Vec], list[Vec], list[Vec]]:
    """One RATTLE step from (x, v) with forces f = force(x); return the new x, v and forces."""
    n = len(x)
    vh = [[v[i][a] + 0.5 * h * inv_mass[i] * f[i][a] for a in range(3)] for i in range(n)]  # @line L1
    xn = [[x[i][a] + h * vh[i][a] for a in range(3)] for i in range(n)]  # @line L2
    for _ in range(max_sweeps):  # @line L3
        done = True
        for i, j, d in bonds:
            s = [xn[i][a] - xn[j][a] for a in range(3)]
            diff = d * d - _dot(s, s)
            if abs(diff) <= 2.0 * tol * d * d:
                continue
            done = False
            r = [x[i][a] - x[j][a] for a in range(3)]
            g = diff / (2.0 * (inv_mass[i] + inv_mass[j]) * _dot(s, r))  # @line L4
            for a in range(3):
                xn[i][a] += inv_mass[i] * g * r[a]
                xn[j][a] -= inv_mass[j] * g * r[a]
                vh[i][a] += inv_mass[i] * g * r[a] / h
                vh[j][a] -= inv_mass[j] * g * r[a] / h
        if done:
            break
    else:
        raise RuntimeError("RATTLE position stage did not converge")
    fn = force(xn)  # @line L5
    vn = [[vh[i][a] + 0.5 * h * inv_mass[i] * fn[i][a] for a in range(3)] for i in range(n)]  # @line L6
    for _ in range(max_sweeps):  # @line L7
        done = True
        for i, j, d in bonds:
            r = [xn[i][a] - xn[j][a] for a in range(3)]
            rv = _dot(r, [vn[i][a] - vn[j][a] for a in range(3)])
            if abs(rv) <= tol * d * d:
                continue
            done = False
            k = -rv / ((inv_mass[i] + inv_mass[j]) * d * d)  # @line L8
            for a in range(3):
                vn[i][a] += inv_mass[i] * k * r[a]
                vn[j][a] -= inv_mass[j] * k * r[a]
        if done:
            break
    else:
        raise RuntimeError("RATTLE velocity stage did not converge")
    return xn, vn, fn  # @line L9


def constraint_errors(x: list[Vec], v: list[Vec], bonds: list[Bond]) -> tuple[float, float]:
    """Largest relative bond-length error and largest |r_ij . v_ij| / d^2."""
    pos = max(abs(_dot(s, s) ** 0.5 - d) / d for s, d in (([x[i][a] - x[j][a] for a in range(3)], d) for i, j, d in bonds))
    vel = max(abs(_dot([x[i][a] - x[j][a] for a in range(3)], [v[i][a] - v[j][a] for a in range(3)])) / (d * d) for i, j, d in bonds)
    return pos, vel
