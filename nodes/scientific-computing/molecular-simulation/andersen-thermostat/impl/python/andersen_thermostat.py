# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/andersen-thermostat/. The authors are listed in prov/8Z4JVW.jsonl.
"""Molecular dynamics at constant temperature with the Andersen thermostat.

The state is the positions x and the velocities v of N particles in d
dimensions, with masses m. A force field returns the potential energy U(x)
and the forces f = -grad U(x). Each step of length h is one velocity Verlet
step, followed by the collisions: each particle, with probability
p = 1 - exp(-nu h), forgets its velocity and gets a new one from the
Maxwell-Boltzmann distribution at the temperature kT (each component normal
with mean 0 and variance kT / m_i). This is Andersen (1980): the collisions of
each particle form a Poisson process of rate nu.

All random numbers come from the random.Random object rng, so a run is
reproducible from its seed.

Cost: one force evaluation and Theta(N d) extra work per step.
"""

import math
import random
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


def andersen_thermostat(
    x: list[Vec], v: list[Vec], m: list[float], forces: ForceField, h: float,
    steps: int, kT: float, nu: float, rng: random.Random,
) -> tuple[list[Vec], list[Vec], list[float]]:
    """Run steps of velocity Verlet with Andersen collisions at rate nu.

    Returns the final positions, the final velocities and the kinetic energy
    after each step. The inputs are not changed.
    """
    if h <= 0 or nu < 0 or kT <= 0:
        raise ValueError("need h > 0, nu >= 0 and kT > 0")
    x = [list(p) for p in x]
    v = [list(p) for p in v]
    n = len(x)
    p_coll = 1.0 - math.exp(-nu * h)
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
        for i in range(n):  # @line L7
            if rng.random() < p_coll:  # @line L8
                s = math.sqrt(kT / m[i])
                v[i] = [s * rng.gauss(0.0, 1.0) for _ in v[i]]  # @line L9
        ks.append(kinetic(v, m))  # @line L10
    return x, v, ks  # @line L11
