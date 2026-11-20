# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brownian-dynamics/. The authors are listed in prov/1T83PZ.jsonl.
"""Brownian dynamics with the Ermak-McCammon step.

In the overdamped limit the velocities are not kept. With the diffusion
tensor D (an (N d) by (N d) symmetric positive definite matrix), the
positions follow

    dx = (D f / kT) dt + div(D) dt + sqrt(2) L dW,   L L^T = D.

The Ermak-McCammon step of length h is

    x <- x + (h / kT) D f + h div(D) + sqrt(2 h) L R,

with R a vector of independent standard normals. Here the divergence term
is left out, which is exact for a constant D and for the Rotne-Prager-
Yamakawa tensor (its divergence is zero). With one diffusion coefficient
D_i per particle and no hydrodynamic coupling, the step is

    x_i <- x_i + (h D_i / kT) f_i + sqrt(2 D_i h) R_i,

the Euler-Maruyama step for the overdamped Langevin equation.

Cost per step: one force evaluation and N d normal draws. With a full
tensor, also Theta((N d)^2) to build D and Theta((N d)^3) for its Cholesky
factor.
"""

import math
import random
from typing import Callable, Union

from scimat import cholesky

Vec = list[float]
Matrix = list[list[float]]
ForceField = Callable[[list[Vec]], tuple[float, list[Vec]]]
Diffusion = Union[float, list[float], Callable[[list[Vec]], Matrix]]


def harmonic(k: float) -> ForceField:
    """Independent springs U = k |x_i|^2 / 2 for each particle."""
    def field(pos: list[Vec]) -> tuple[float, list[Vec]]:
        u = sum(0.5 * k * c * c for p in pos for c in p)
        return u, [[-k * c for c in p] for p in pos]
    return field


def constant_force(g: Vec) -> ForceField:
    """The same force g on every particle, U = -sum_i g . x_i."""
    def field(pos: list[Vec]) -> tuple[float, list[Vec]]:
        u = -sum(ga * c for p in pos for ga, c in zip(g, p))
        return u, [list(g) for _ in pos]
    return field


def free() -> ForceField:
    """No forces: U = 0 and f = 0."""
    def field(pos: list[Vec]) -> tuple[float, list[Vec]]:
        return 0.0, [[0.0] * len(p) for p in pos]
    return field


def rpy_tensor(a: float, kT: float, eta: float) -> Callable[[list[Vec]], Matrix]:
    """The Rotne-Prager-Yamakawa diffusion tensor for spheres of radius a in 3D.

    The diagonal blocks are D0 I with D0 = kT / (6 pi eta a). For two spheres
    at distance r >= 2a the block is
        kT / (8 pi eta r) ((1 + 2 a^2 / (3 r^2)) I + (1 - 2 a^2 / r^2) e e^T),
    and for r < 2a it is
        D0 ((1 - 9 r / (32 a)) I + (3 r / (32 a)) e e^T),
    with e the unit vector from one center to the other. The matrix is
    positive definite for every configuration.
    """
    d0 = kT / (6.0 * math.pi * eta * a)

    def tensor(pos: list[Vec]) -> Matrix:
        n = len(pos)
        out = [[0.0] * (3 * n) for _ in range(3 * n)]
        for i in range(n):
            for s in range(3):
                out[3 * i + s][3 * i + s] = d0
            for j in range(i + 1, n):
                dx = [pos[i][s] - pos[j][s] for s in range(3)]
                r = math.sqrt(sum(c * c for c in dx))
                e = [c / r for c in dx]
                if r >= 2.0 * a:
                    pre = kT / (8.0 * math.pi * eta * r)
                    ci = pre * (1.0 + 2.0 * a * a / (3.0 * r * r))
                    ce = pre * (1.0 - 2.0 * a * a / (r * r))
                else:
                    ci = d0 * (1.0 - 9.0 * r / (32.0 * a))
                    ce = d0 * 3.0 * r / (32.0 * a)
                for s in range(3):
                    for t in range(3):
                        val = ce * e[s] * e[t] + (ci if s == t else 0.0)
                        out[3 * i + s][3 * j + t] = val
                        out[3 * j + t][3 * i + s] = val
        return out
    return tensor


def brownian_dynamics(
    x: list[Vec], forces: ForceField, h: float, steps: int, kT: float,
    diffusion: Diffusion, rng: random.Random, every: int = 1,
) -> tuple[list[Vec], list[list[Vec]]]:
    """Run steps of Brownian dynamics with the Ermak-McCammon step.

    diffusion is one coefficient for all particles, a list with one
    coefficient per particle, or a function that maps the positions to the
    (N d) by (N d) diffusion tensor (row i d + s is coordinate s of particle i).
    Returns the final positions and copies of the positions after every
    `every` steps. The input is not changed.
    """
    if h <= 0 or kT <= 0 or every < 1:
        raise ValueError("need h > 0, kT > 0 and every >= 1")
    x = [list(p) for p in x]
    n = len(x)
    tensor = diffusion if callable(diffusion) else None
    if tensor is None:
        dlist = list(diffusion) if isinstance(diffusion, list) else [float(diffusion)] * n
        if len(dlist) != n or min(dlist) <= 0:
            raise ValueError("need one positive diffusion coefficient per particle")
        sd = [math.sqrt(2.0 * di * h) for di in dlist]
    _, f = forces(x)  # @line L1
    samples = []
    for step in range(1, steps + 1):  # @line L2
        if tensor is None:
            for i in range(n):
                for s in range(len(x[i])):
                    r = rng.gauss(0.0, 1.0)  # @line L5
                    x[i][s] += h * dlist[i] * f[i][s] / kT + sd[i] * r  # @line L6
        else:
            d = len(x[0])
            dm = tensor(x)  # @line L3
            low = cholesky(dm)  # @line L4
            r = [rng.gauss(0.0, 1.0) for _ in range(n * d)]  # @line L5
            fl = [c for p in f for c in p]
            dx = [0.0] * (n * d)
            for row in range(n * d):
                drift = sum(dm[row][col] * fl[col] for col in range(n * d))
                noise = sum(low[row][col] * r[col] for col in range(row + 1))
                dx[row] = h * drift / kT + math.sqrt(2.0 * h) * noise
            for i in range(n):
                for s in range(d):
                    x[i][s] += dx[i * d + s]  # @line L6
        _, f = forces(x)  # @line L7
        if step % every == 0:  # @line L8
            samples.append([list(p) for p in x])
    return x, samples  # @line L9
