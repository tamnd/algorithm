# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/respa-multiple-time-step/. The authors are listed in prov/2SQEWG.jsonl.
"""r-RESPA: the reversible multiple time step integrator of Tuckerman, Berne and Martyna (1992).

The force is split as F = F_fast + F_slow. One outer step of size h is the
Trotter splitting

    exp(h/2 L_slow) [exp(delta/2 L_fast) exp(delta L_x) exp(delta/2 L_fast)]^n exp(h/2 L_slow),

with delta = h / n: a half kick with the slow force, n velocity Verlet steps
with the fast force alone, and a second half kick with the slow force. The
slow force is computed once per outer step and the fast force n times.

Each factor is the exact flow of a Hamiltonian, so the map is symplectic, and
the splitting is symmetric, so it is time-reversible and of order 2. The
slow kicks are impulses spaced h apart. When h is near a multiple of half
the period of a fast motion the impulses resonate with it and the method is
unstable, even if each force is accurate.

Positions and velocities are flat lists of floats here; inv_mass has one
entry per coordinate.
"""

from typing import Callable

Field = Callable[[list[float]], list[float]]


def respa_step(
    x: list[float], v: list[float], inv_mass: list[float], f_fast: Field, f_slow: Field, h: float, n: int,
) -> tuple[list[float], list[float]]:
    """One outer r-RESPA step of size h with n inner steps on the fast force."""
    delta = h / n
    fs = f_slow(x)
    v = [vi + 0.5 * h * wi * fi for vi, wi, fi in zip(v, inv_mass, fs)]  # @line L1
    ff = f_fast(x)
    for _ in range(n):  # @line L2
        v = [vi + 0.5 * delta * wi * fi for vi, wi, fi in zip(v, inv_mass, ff)]  # @line L3
        x = [xi + delta * vi for xi, vi in zip(x, v)]  # @line L4
        ff = f_fast(x)
        v = [vi + 0.5 * delta * wi * fi for vi, wi, fi in zip(v, inv_mass, ff)]  # @line L5
    fs = f_slow(x)
    v = [vi + 0.5 * h * wi * fi for vi, wi, fi in zip(v, inv_mass, fs)]  # @line L6
    return x, v  # @line L7


def velocity_verlet_step(
    x: list[float], v: list[float], inv_mass: list[float], force: Field, h: float,
) -> tuple[list[float], list[float]]:
    """One velocity Verlet step with the full force, the reference for n = 1."""
    f = force(x)
    v = [vi + 0.5 * h * wi * fi for vi, wi, fi in zip(v, inv_mass, f)]
    x = [xi + h * vi for xi, vi in zip(x, v)]
    f = force(x)
    v = [vi + 0.5 * h * wi * fi for vi, wi, fi in zip(v, inv_mass, f)]
    return x, v
