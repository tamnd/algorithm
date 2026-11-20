# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shake-constraint-algorithm/. The authors are listed in prov/3AE47X.jsonl.
"""SHAKE: Verlet integration with holonomic bond-length constraints.

This is the method of Ryckaert, Ciccotti and Berendsen (1977). Each
constraint (i, j, d) asks |x_i - x_j| = d. The unconstrained Verlet step
gives trial positions. The constraint forces act along the bond vectors of
the old positions, so the correct new positions are

    x_i = x_unc_i + w_i sum over constraints c of +-g_c r_old_c,

with w_i = 1 / m_i the inverse mass (0 for a fixed atom). SHAKE finds the
multipliers g_c one constraint at a time, in a Gauss-Seidel sweep, with one
linearised Newton step per constraint, and repeats the sweep until every
constraint holds to a relative tolerance.

Cost: Theta(C) per sweep for C constraints. The number of sweeps grows
when the constraints are strongly coupled (rings, long rigid chains).
"""

import math
from typing import Callable

Vec = list[float]
Bond = tuple[int, int, float]


def shake(
    x_old: list[Vec], x_unc: list[Vec], inv_mass: list[float], bonds: list[Bond],
    tol: float = 1e-12, max_sweeps: int = 1000,
) -> tuple[list[Vec], int]:
    """Correct x_unc so that every bond holds; return the positions and the number of sweeps."""
    x = [list(p) for p in x_unc]
    for sweep in range(1, max_sweeps + 1):  # @line L2
        done = True
        for i, j, d in bonds:  # @line L3
            s = [x[i][a] - x[j][a] for a in range(3)]
            diff = d * d - (s[0] * s[0] + s[1] * s[1] + s[2] * s[2])
            if abs(diff) <= 2.0 * tol * d * d:  # @line L4
                continue
            done = False
            r = [x_old[i][a] - x_old[j][a] for a in range(3)]
            dot = s[0] * r[0] + s[1] * r[1] + s[2] * r[2]
            wsum = inv_mass[i] + inv_mass[j]
            if wsum == 0.0 or dot <= 0.0:
                raise ValueError("constraint cannot be corrected along the old bond")
            g = diff / (2.0 * wsum * dot)  # @line L5
            for a in range(3):  # @line L6
                x[i][a] += inv_mass[i] * g * r[a]
                x[j][a] -= inv_mass[j] * g * r[a]
        if done:  # @line L7
            return x, sweep
    raise RuntimeError("SHAKE did not converge")


def shake_verlet_step(
    x_prev: list[Vec], x: list[Vec], inv_mass: list[float], force: Callable[[list[Vec]], list[Vec]],
    h: float, bonds: list[Bond], tol: float = 1e-12,
) -> list[Vec]:
    """One step of position Verlet with SHAKE: from x_(n-1) and x_n return x_(n+1)."""
    f = force(x)
    x_unc = [[2.0 * x[i][a] - x_prev[i][a] + h * h * inv_mass[i] * f[i][a] for a in range(3)] for i in range(len(x))]  # @line L1
    x_new, _ = shake(x, x_unc, inv_mass, bonds, tol)
    return x_new  # @line L8


def bond_error(x: list[Vec], bonds: list[Bond]) -> float:
    """Largest relative error |(|x_i - x_j| - d) / d| over the bonds."""
    return max(abs(math.dist(x[i], x[j]) - d) / d for i, j, d in bonds)
