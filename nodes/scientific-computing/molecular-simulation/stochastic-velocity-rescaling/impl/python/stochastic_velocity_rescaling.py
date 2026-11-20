# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stochastic-velocity-rescaling/. The authors are listed in prov/BYYCSC.jsonl.
"""Molecular dynamics with the stochastic velocity rescaling thermostat.

Bussi, Donadio and Parrinello (2007) let the kinetic energy K follow the
stochastic differential equation

    dK = (K0 - K) dt / tau + 2 sqrt(K K0 / N_f) dW / sqrt(tau),

with K0 = N_f kT / 2, the number of degrees of freedom N_f and the coupling
time tau. Its stationary law is the canonical law of K, with density
proportional to K^(N_f / 2 - 1) exp(-K / kT). The exact solution over a time
h is drawn as

    K' = (sqrt(c K) + sqrt((1 - c) K0 / N_f) R_1)^2 + (1 - c) (K0 / N_f) S,

with c = exp(-h / tau), R_1 standard normal and S a chi-squared variable with
N_f - 1 degrees of freedom (2 times a gamma variable of shape (N_f - 1) / 2).
All velocities are then scaled by alpha = sqrt(K' / K), with the sign of
sqrt(c K) + sqrt((1 - c) K0 / N_f) R_1.

One step of length h here is one velocity Verlet step followed by one
rescaling. The sum of the changes of K made by the thermostat is kept, so
that the effective energy H~ = K + U - (that sum) can be monitored: it is
conserved up to the error of the Verlet step.

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


def rescale_factor(k: float, k0: float, nf: int, c: float, rng: random.Random) -> float:
    """Draw alpha with alpha^2 K distributed as the exact SDE solution over a time h."""
    r1 = rng.gauss(0.0, 1.0)  # @line L8
    s = 2.0 * rng.gammavariate(0.5 * (nf - 1), 1.0) if nf > 1 else 0.0  # @line L9
    a = math.sqrt(c * k) + math.sqrt((1.0 - c) * k0 / nf) * r1
    k_new = a * a + (1.0 - c) * (k0 / nf) * s  # @line L10
    alpha = math.sqrt(k_new / k)  # @line L11
    return alpha if a >= 0 else -alpha


def stochastic_velocity_rescaling(
    x: list[Vec], v: list[Vec], m: list[float], forces: ForceField, h: float,
    steps: int, kT: float, tau: float, nf: int, rng: random.Random,
) -> tuple[list[Vec], list[Vec], list[float], list[float]]:
    """Run steps of velocity Verlet with stochastic velocity rescaling.

    Returns the final positions and velocities, the kinetic energy after each
    step and the effective energy H~ after each step. The inputs are not
    changed. Needs a nonzero kinetic energy at each rescaling.
    """
    if h <= 0 or tau <= 0 or kT <= 0 or nf <= 0:
        raise ValueError("need h > 0, tau > 0, kT > 0 and nf > 0")
    x = [list(p) for p in x]
    v = [list(p) for p in v]
    n = len(x)
    k0 = 0.5 * nf * kT
    c = math.exp(-h / tau)
    u, f = forces(x)  # @line L1
    heat = 0.0
    ks, effective = [], []
    for _ in range(steps):  # @line L2
        for i in range(n):
            for a in range(len(x[i])):
                v[i][a] += 0.5 * h * f[i][a] / m[i]  # @line L3
                x[i][a] += h * v[i][a]  # @line L4
        u, f = forces(x)  # @line L5
        for i in range(n):
            for a in range(len(x[i])):
                v[i][a] += 0.5 * h * f[i][a] / m[i]  # @line L6
        k = kinetic(v, m)  # @line L7
        alpha = rescale_factor(k, k0, nf, c, rng)
        for vi in v:
            for a in range(len(vi)):
                vi[a] *= alpha  # @line L12
        heat += (alpha * alpha - 1.0) * k  # @line L13
        ks.append(alpha * alpha * k)
        effective.append(alpha * alpha * k + u - heat)  # @line L14
    return x, v, ks, effective  # @line L15
