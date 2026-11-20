# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/baoab-langevin-integrator/. The authors are listed in prov/V8MPCG.jsonl.
"""The BAOAB splitting for Langevin dynamics (Leimkuhler and Matthews 2013).

The Langevin equations for N particles in d dimensions are

    dx_i = v_i dt,
    m_i dv_i = f_i dt - m_i gamma v_i dt + sqrt(2 m_i gamma kT) dW_i.

The vector field is split into three parts, each solved exactly:

    B: dv = (f / m) dt                  (kick, positions fixed)
    A: dx = v dt                        (drift, velocities fixed)
    O: dv = -gamma v dt + noise         (Ornstein-Uhlenbeck, positions fixed)

One step of length h is B for h / 2, A for h / 2, O for h, A for h / 2 and
B for h / 2. The O step is v <- c v + sqrt((1 - c^2) kT / m) R with
c = exp(-gamma h) and R standard normal. The force after the second A part
is kept for the first B part of the next step, so there is one force
evaluation per step.

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


def quartic() -> ForceField:
    """Independent quartic wells U = |x_i|^4 / 4 for each particle (1D use)."""
    def field(pos: list[Vec]) -> tuple[float, list[Vec]]:
        u = sum(0.25 * c ** 4 for p in pos for c in p)
        return u, [[-c ** 3 for c in p] for p in pos]
    return field


def baoab(
    x: list[Vec], v: list[Vec], m: list[float], forces: ForceField, h: float,
    steps: int, kT: float, gamma: float, rng: random.Random, every: int = 1,
) -> tuple[list[Vec], list[Vec], list[tuple[list[Vec], list[Vec]]]]:
    """Run steps of BAOAB.

    Returns the final positions and velocities, and copies of (x, v) after
    every `every` steps. The inputs are not changed.
    """
    if h <= 0 or gamma < 0 or kT <= 0 or every < 1:
        raise ValueError("need h > 0, gamma >= 0, kT > 0 and every >= 1")
    x = [list(p) for p in x]
    v = [list(p) for p in v]
    n = len(x)
    c = math.exp(-gamma * h)
    sd = [math.sqrt((1.0 - c * c) * kT / mi) for mi in m]
    _, f = forces(x)  # @line L1
    samples = []
    for step in range(1, steps + 1):  # @line L2
        for i in range(n):
            for a in range(len(x[i])):
                v[i][a] += 0.5 * h * f[i][a] / m[i]  # @line L3
                x[i][a] += 0.5 * h * v[i][a]  # @line L4
                v[i][a] = c * v[i][a] + sd[i] * rng.gauss(0.0, 1.0)  # @line L5
                x[i][a] += 0.5 * h * v[i][a]  # @line L6
        _, f = forces(x)  # @line L7
        for i in range(n):
            for a in range(len(x[i])):
                v[i][a] += 0.5 * h * f[i][a] / m[i]  # @line L8
        if step % every == 0:  # @line L9
            samples.append(([list(p) for p in x], [list(p) for p in v]))
    return x, v, samples  # @line L10
