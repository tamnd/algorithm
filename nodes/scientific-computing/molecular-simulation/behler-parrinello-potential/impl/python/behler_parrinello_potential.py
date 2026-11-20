# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/behler-parrinello-potential/. The authors are listed in prov/JVQRJ5.jsonl.

"""A small Behler-Parrinello potential for one element, with radial symmetry functions only.

This is a toy of the model: a real potential also uses angular symmetry
functions and is trained on quantum energies and forces. Here the weights are
given, and the code computes the energy and the exact forces.
"""

import math
import random

Point = list[float]


def cutoff(r: float, rc: float) -> float:
    return 0.5 * (math.cos(math.pi * r / rc) + 1) if r < rc else 0.0


def dcutoff(r: float, rc: float) -> float:
    return -0.5 * math.pi / rc * math.sin(math.pi * r / rc) if r < rc else 0.0


def g2(r: float, eta: float, rs: float, rc: float) -> float:
    """One term exp(-eta (r - rs)^2) f_c(r) of the radial symmetry function G2."""
    return math.exp(-eta * (r - rs) ** 2) * cutoff(r, rc)


def dg2(r: float, eta: float, rs: float, rc: float) -> float:
    e = math.exp(-eta * (r - rs) ** 2)
    return e * (dcutoff(r, rc) - 2 * eta * (r - rs) * cutoff(r, rc))


class AtomicNetwork:
    """E_i = b2 + sum_h w2[h] tanh(b1[h] + sum_m w1[h][m] G[m]), one hidden layer."""

    def __init__(self, w1: list[list[float]], b1: list[float], w2: list[float], b2: float):
        self.w1, self.b1, self.w2, self.b2 = w1, b1, w2, b2

    @classmethod
    def random(cls, inputs: int, hidden: int, seed: int) -> "AtomicNetwork":
        rng = random.Random(seed)
        w1 = [[rng.gauss(0, 1) for _ in range(inputs)] for _ in range(hidden)]
        b1 = [rng.gauss(0, 0.5) for _ in range(hidden)]
        w2 = [rng.gauss(0, 1) for _ in range(hidden)]
        return cls(w1, b1, w2, rng.gauss(0, 0.5))

    def energy_and_gradient(self, g: list[float]) -> tuple[float, list[float]]:
        """The output and its gradient with respect to the inputs, by backpropagation."""
        t = [math.tanh(b + sum(w * x for w, x in zip(row, g))) for row, b in zip(self.w1, self.b1)]
        e = self.b2 + sum(w * x for w, x in zip(self.w2, t))
        grad = [0.0] * len(g)
        for h, row in enumerate(self.w1):
            c = self.w2[h] * (1 - t[h] * t[h])
            for m, w in enumerate(row):
                grad[m] += c * w
        return e, grad


def bp_energy_forces(
    positions: list[Point], net: AtomicNetwork, params: list[tuple[float, float]], rc: float
) -> tuple[float, list[float], list[list[float]]]:
    """The energy U = sum_i E_i(G_i) and the forces, with G_i[m] = sum_j g2(r_ij, eta_m, rs_m, rc).

    params lists the pairs (eta, rs) of the radial symmetry functions. Returns
    (U, atomic energies, forces).
    """
    n, m = len(positions), len(params)
    gs = [[0.0] * m for _ in range(n)]  # @line L1
    close = []
    for i in range(n):  # @line L2
        for j in range(i + 1, n):  # @line L2
            d = [a - b for a, b in zip(positions[i], positions[j])]
            r = math.sqrt(sum(x * x for x in d))
            if r >= rc:  # @line L2
                continue
            close.append((i, j, r, d))
            for k, (eta, rs) in enumerate(params):  # @line L2
                v = g2(r, eta, rs, rc)
                gs[i][k] += v  # @line L2
                gs[j][k] += v  # @line L2
    atomic, grads = [], []
    for i in range(n):  # @line L3
        e, a = net.energy_and_gradient(gs[i])  # @line L3
        atomic.append(e)
        grads.append(a)
    u = sum(atomic)  # @line L4
    forces = [[0.0] * len(positions[0]) for _ in range(n)]
    for i, j, r, d in close:  # @line L5
        g = sum((grads[i][k] + grads[j][k]) * dg2(r, eta, rs, rc) for k, (eta, rs) in enumerate(params))  # @line L6
        for q in range(len(d)):
            c = g * d[q] / r
            forces[i][q] -= c  # @line L7
            forces[j][q] += c  # @line L7
    return u, atomic, forces  # @line L8


def symmetry_functions(positions: list[Point], i: int, params: list[tuple[float, float]], rc: float) -> list[float]:
    """The vector G_i of atom i, computed directly."""
    out = []
    for eta, rs in params:
        out.append(sum(g2(math.dist(positions[i], p), eta, rs, rc) for j, p in enumerate(positions) if j != i))
    return out
