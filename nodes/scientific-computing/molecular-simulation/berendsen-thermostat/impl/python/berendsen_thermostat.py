# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/berendsen-thermostat/. The authors are listed in prov/VZN3KE.jsonl.
"""Molecular dynamics with the Berendsen (weak coupling) thermostat.

The state is the positions x and the velocities v of N particles in d
dimensions, with masses m. Each step of length h is one velocity Verlet step,
followed by a scaling of all velocities by

    lambda = sqrt(1 + (h / tau) (T0 / T - 1)),

where T = 2 K / (N_f k_B) is the kinetic temperature after the Verlet step,
T0 the target, tau the coupling time and N_f the number of degrees of
freedom (Berendsen et al. 1984). The scaling sets the new kinetic energy to
K + (h / tau) (K0 - K), with K0 = N_f k_B T0 / 2, so that without forces the
kinetic energy relaxes to K0 as (1 - h / tau)^n.

The method is deterministic. It does not sample the canonical ensemble: the
fluctuations of K are too small.

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


def free() -> ForceField:
    """No forces: U = 0 and f = 0."""
    def field(pos: list[Vec]) -> tuple[float, list[Vec]]:
        return 0.0, [[0.0] * len(p) for p in pos]
    return field


def kinetic(v: list[Vec], m: list[float]) -> float:
    """The kinetic energy K = sum_i m_i |v_i|^2 / 2."""
    return sum(0.5 * mi * sum(c * c for c in vi) for vi, mi in zip(v, m))


def berendsen_thermostat(
    x: list[Vec], v: list[Vec], m: list[float], forces: ForceField, h: float,
    steps: int, kT: float, tau: float, nf: int,
) -> tuple[list[Vec], list[Vec], list[float]]:
    """Run steps of velocity Verlet with Berendsen scaling toward kT.

    nf is the number of degrees of freedom used for the kinetic temperature.
    Returns the final positions, the final velocities and the kinetic energy
    after each step. The inputs are not changed. Needs tau >= h.
    """
    if h <= 0 or tau < h or kT <= 0 or nf <= 0:
        raise ValueError("need h > 0, tau >= h, kT > 0 and nf > 0")
    x = [list(p) for p in x]
    v = [list(p) for p in v]
    n = len(x)
    k0 = 0.5 * nf * kT
    _, f = forces(x)  # @line L1
    ks = []
    for _ in range(steps):  # @line L2
        for i in range(n):
            for a in range(len(x[i])):
                v[i][a] += 0.5 * h * f[i][a] / m[i]  # @line L3
                x[i][a] += h * v[i][a]  # @line L4
        _, f = forces(x)  # @line L5
        for i in range(n):
            for a in range(len(x[i])):
                v[i][a] += 0.5 * h * f[i][a] / m[i]  # @line L6
        k = kinetic(v, m)  # @line L7
        if k > 0:
            lam = math.sqrt(1.0 + (h / tau) * (k0 / k - 1.0))  # @line L8
            for vi in v:
                for a in range(len(vi)):
                    vi[a] *= lam  # @line L9
            k *= lam * lam
        ks.append(k)  # @line L10
    return x, v, ks  # @line L11
