# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nose-hoover-thermostat/. The authors are listed in prov/GC1X6T.jsonl.
"""Molecular dynamics with the Nose-Hoover thermostat.

The equations of motion of Hoover (1985) for N particles in d dimensions are

    dx_i/dt = v_i,
    dv_i/dt = f_i / m_i - xi v_i,
    dxi/dt  = (2 K - N_f kT) / Q,
    deta/dt = xi,

with the kinetic energy K, the number of degrees of freedom N_f, the target
temperature kT and the thermostat mass Q. The extended energy

    H' = K + U + Q xi^2 / 2 + N_f kT eta

is conserved by the exact flow.

One step of length h is the symmetric splitting of Martyna, Tuckerman,
Tobias and Klein (1996): a half step of the thermostat, a velocity Verlet step
of the particles, and a second half step of the thermostat. The thermostat
half step updates xi by a quarter step, scales the velocities by
exp(-xi h / 2), and updates xi by another quarter step. Each piece is the
exact flow of a part of the equations, so the step is time-reversible.

Cost: one force evaluation and Theta(N d) extra work per step.
"""

import math
from typing import Callable

Vec = list[float]
ForceField = Callable[[list[Vec]], tuple[float, list[Vec]]]


def harmonic(k: float) -> ForceField:
    """Independent springs U = k |x_i|^2 / 2 for each particle."""
    def field(pos: list[Vec]) -> tuple[float, list[Vec]]:
        u = sum(0.5 * k * c * c for p in pos for c in p)
        return u, [[-k * c for c in p] for p in pos]
    return field


def kinetic(v: list[Vec], m: list[float]) -> float:
    """The kinetic energy K = sum_i m_i |v_i|^2 / 2."""
    return sum(0.5 * mi * sum(c * c for c in vi) for vi, mi in zip(v, m))


def _thermostat_half(v, m, xi, eta, h, kT, q, nf):
    """Exact flows of the thermostat part for a time h / 2 (Trotter split)."""
    k = kinetic(v, m)
    xi += 0.25 * h * (2.0 * k - nf * kT) / q  # @line L11
    s = math.exp(-0.5 * h * xi)  # @line L12
    for vi in v:
        for a in range(len(vi)):
            vi[a] *= s
    k *= s * s
    eta += 0.5 * h * xi  # @line L13
    xi += 0.25 * h * (2.0 * k - nf * kT) / q  # @line L14
    return xi, eta


def nose_hoover_thermostat(
    x: list[Vec], v: list[Vec], m: list[float], forces: ForceField, h: float,
    steps: int, kT: float, q: float, nf: int, xi: float = 0.0, eta: float = 0.0,
) -> tuple[list[Vec], list[Vec], float, float, list[float]]:
    """Run steps of Nose-Hoover dynamics.

    Returns the final positions, velocities, xi and eta, and the extended
    energy H' after each step. The inputs are not changed.
    """
    if h <= 0 or q <= 0 or kT <= 0 or nf <= 0:
        raise ValueError("need h > 0, q > 0, kT > 0 and nf > 0")
    x = [list(p) for p in x]
    v = [list(p) for p in v]
    n = len(x)
    u, f = forces(x)  # @line L1
    energies = []
    for _ in range(steps):  # @line L2
        xi, eta = _thermostat_half(v, m, xi, eta, h, kT, q, nf)  # @line L3
        for i in range(n):
            for a in range(len(x[i])):
                v[i][a] += 0.5 * h * f[i][a] / m[i]  # @line L4
                x[i][a] += h * v[i][a]  # @line L5
        u, f = forces(x)  # @line L6
        for i in range(n):
            for a in range(len(x[i])):
                v[i][a] += 0.5 * h * f[i][a] / m[i]  # @line L7
        xi, eta = _thermostat_half(v, m, xi, eta, h, kT, q, nf)  # @line L8
        energies.append(kinetic(v, m) + u + 0.5 * q * xi * xi + nf * kT * eta)  # @line L9
    return x, v, xi, eta, energies  # @line L10
