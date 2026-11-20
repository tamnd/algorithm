# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dissipative-particle-dynamics/. The authors are listed in prov/9VVD0G.jsonl.
"""Dissipative particle dynamics (Hoogerbrugge and Koelman 1992; Espanol and Warren 1995).

N beads of mass 1 in a periodic square box of side box. Each pair i, j
closer than the cutoff rc feels three forces along e_ij = r_ij / |r_ij|,
with the weight w(r) = 1 - r / rc:

    conservative  F^C = a w(r) e_ij
    dissipative   F^D = -gamma w(r)^2 (e_ij . v_ij) e_ij
    random        F^R = sigma w(r) theta_ij e_ij / sqrt(h)

with v_ij = v_i - v_j, an independent standard normal theta_ij = theta_ji
per pair and per step, and the time step h. The fluctuation-dissipation
relation of Espanol and Warren, w^D = (w^R)^2 and sigma^2 = 2 gamma kT,
makes the Gibbs distribution with the soft potential stationary for the
stochastic dynamics (h -> 0). Each pair force acts with opposite signs on
i and j, so the total momentum is conserved.

The integrator is the modified velocity Verlet scheme of Groot and Warren
(1997) with the parameter lam; lam = 1/2 is plain velocity Verlet with the
velocity-dependent forces evaluated at a predicted velocity.
"""

import math
import random
from typing import Sequence

Vec = list[float]


def _wrap(d: float, box: float) -> float:
    return d - box * round(d / box)


def dpd_forces(x: Sequence[Vec], v: Sequence[Vec], box: float, a: float, gamma: float,
               sigma: float, h: float, rng: random.Random, rc: float = 1.0) -> list[Vec]:
    """The total DPD force on each bead for positions x and velocities v."""
    n = len(x)
    f = [[0.0, 0.0] for _ in range(n)]
    noise = sigma / math.sqrt(h)
    for i in range(n):                                                    # @line L6
        for j in range(i + 1, n):
            dx = _wrap(x[i][0] - x[j][0], box)
            dy = _wrap(x[i][1] - x[j][1], box)
            r2 = dx * dx + dy * dy
            if r2 >= rc * rc:
                continue
            r = math.sqrt(r2)
            ex, ey = dx / r, dy / r
            w = 1.0 - r / rc                                              # @line L7
            theta = rng.gauss(0.0, 1.0)
            ev = ex * (v[i][0] - v[j][0]) + ey * (v[i][1] - v[j][1])
            fij = a * w - gamma * w * w * ev + noise * w * theta          # @line L8
            f[i][0] += fij * ex                                           # @line L9
            f[i][1] += fij * ey
            f[j][0] -= fij * ex
            f[j][1] -= fij * ey
    return f


def dpd_step(x: list[Vec], v: list[Vec], f: list[Vec], box: float, a: float, gamma: float,
             sigma: float, h: float, rng: random.Random, lam: float = 0.5,
             rc: float = 1.0) -> list[Vec]:
    """One modified velocity Verlet step; x and v change in place, the new forces are returned."""
    n = len(x)
    for i in range(n):
        for k in range(2):
            x[i][k] = (x[i][k] + h * v[i][k] + 0.5 * h * h * f[i][k]) % box     # @line L1
    v_pred = [[v[i][k] + lam * h * f[i][k] for k in range(2)] for i in range(n)]  # @line L2
    f_new = dpd_forces(x, v_pred, box, a, gamma, sigma, h, rng, rc)              # @line L3
    for i in range(n):
        for k in range(2):
            v[i][k] += 0.5 * h * (f[i][k] + f_new[i][k])                         # @line L4
    return f_new                                                                 # @line L5


def conservative_energy(x: Sequence[Vec], box: float, a: float, rc: float = 1.0) -> float:
    """U = sum over pairs with r < rc of (a rc / 2) (1 - r / rc)^2, whose force is F^C."""
    u = 0.0
    n = len(x)
    for i in range(n):
        for j in range(i + 1, n):
            r = math.hypot(_wrap(x[i][0] - x[j][0], box), _wrap(x[i][1] - x[j][1], box))
            if r < rc:
                u += 0.5 * a * rc * (1.0 - r / rc) ** 2
    return u


def kinetic_temperature(v: Sequence[Vec]) -> float:
    """kT = 2 K / N_f with K = sum |v|^2 / 2 and N_f = 2N - 2 (2D, total momentum fixed)."""
    return sum(p[0] * p[0] + p[1] * p[1] for p in v) / (2 * len(v) - 2)


def initial_state(n: int, box: float, kt: float, rng: random.Random) -> tuple[list[Vec], list[Vec]]:
    """Uniform random positions and Gaussian velocities with zero total momentum."""
    x = [[rng.uniform(0.0, box), rng.uniform(0.0, box)] for _ in range(n)]
    v = [[rng.gauss(0.0, math.sqrt(kt)), rng.gauss(0.0, math.sqrt(kt))] for _ in range(n)]
    for k in range(2):
        mean = sum(p[k] for p in v) / n
        for p in v:
            p[k] -= mean
    return x, v


def run(n: int, box: float, a: float, gamma: float, sigma: float, h: float, steps: int,
        seed: int, lam: float = 0.5, kt0: float = 1.0) -> tuple[list[Vec], list[Vec], list[float]]:
    """Run a DPD simulation and return the final x, v and the kinetic temperature per step."""
    rng = random.Random(seed)
    x, v = initial_state(n, box, kt0, rng)
    f = dpd_forces(x, v, box, a, gamma, sigma, h, rng)
    temps = []
    for _ in range(steps):
        f = dpd_step(x, v, f, box, a, gamma, sigma, h, rng, lam)
        temps.append(kinetic_temperature(v))
    return x, v, temps
