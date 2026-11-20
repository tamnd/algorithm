# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/langevin-dynamics/. The authors are listed in prov/YHB5S5.jsonl.
"""Langevin dynamics with the Bussi-Parrinello (OBABO) integrator.

The Langevin equations for N particles in d dimensions are

    dx_i = v_i dt,
    m_i dv_i = f_i dt - m_i gamma v_i dt + sqrt(2 m_i gamma kT) dW_i,

with the friction coefficient gamma, the temperature kT and independent
Wiener processes W_i. The canonical density exp(-(K + U) / kT) is invariant.

One step of length h is the splitting of Bussi and Parrinello (2007): an
exact Ornstein-Uhlenbeck half step of the velocities (friction and noise
only), a velocity Verlet step, and a second exact Ornstein-Uhlenbeck half
step. The exact half step is

    v <- c v + sqrt((1 - c^2) kT / m) R,   c = exp(-gamma h / 2),

with R standard normal. With gamma = 0 the step is velocity Verlet. With no
forces the velocities are an exact sample path of the Ornstein-Uhlenbeck
process at the step times.

Cost: one force evaluation, N d normal draws and Theta(N d) extra work per
step.
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


def _ou_half(v, m, c, kT, rng):
    """Exact Ornstein-Uhlenbeck flow of the velocities over a time h / 2."""
    for i, vi in enumerate(v):
        s = math.sqrt((1.0 - c * c) * kT / m[i])
        for a in range(len(vi)):
            vi[a] = c * vi[a] + s * rng.gauss(0.0, 1.0)


def langevin_dynamics(
    x: list[Vec], v: list[Vec], m: list[float], forces: ForceField, h: float,
    steps: int, kT: float, gamma: float, rng: random.Random, every: int = 1,
) -> tuple[list[Vec], list[Vec], list[tuple[list[Vec], list[Vec]]]]:
    """Run steps of Langevin dynamics with the OBABO splitting.

    Returns the final positions and velocities, and copies of (x, v) after
    every `every` steps. The inputs are not changed.
    """
    if h <= 0 or gamma < 0 or kT <= 0 or every < 1:
        raise ValueError("need h > 0, gamma >= 0, kT > 0 and every >= 1")
    x = [list(p) for p in x]
    v = [list(p) for p in v]
    n = len(x)
    c = math.exp(-0.5 * gamma * h)
    _, f = forces(x)  # @line L1
    samples = []
    for step in range(1, steps + 1):  # @line L2
        _ou_half(v, m, c, kT, rng)  # @line L3
        for i in range(n):
            for a in range(len(x[i])):
                v[i][a] += 0.5 * h * f[i][a] / m[i]  # @line L4
                x[i][a] += h * v[i][a]  # @line L5
        _, f = forces(x)  # @line L6
        for i in range(n):
            for a in range(len(x[i])):
                v[i][a] += 0.5 * h * f[i][a] / m[i]  # @line L7
        _ou_half(v, m, c, kT, rng)  # @line L8
        if step % every == 0:  # @line L9
            samples.append(([list(p) for p in x], [list(p) for p in v]))
    return x, v, samples  # @line L10
