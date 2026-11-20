# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/material-point-method/. The authors are listed in prov/AX0ZM2.jsonl.
"""The material point method (MPM) of Sulsky, Chen and Schreyer in 1D.

A linear elastic bar is a set of material points (particles) with mass m_p,
volume V_p, velocity v_p, deformation gradient F_p and stress sigma_p. The
background grid has nodes x_i = i dx, i = 0, ..., n - 1, with the linear hat
shape functions N_i(x) = max(0, 1 - |x - x_i| / dx). Each step maps the
particles to the grid, solves the momentum equation on the grid with an
explicit step, and maps the result back (update stress last, USL, with the
FLIP velocity update). The grid carries no state from step to step.

Cost per step: Theta(N + n) time and Theta(n) extra space for N particles
and n nodes.
"""

import math
from dataclasses import dataclass, field


@dataclass
class Particles:
    x: list[float]
    v: list[float]
    m: list[float]
    vol0: list[float]
    F: list[float] = field(default_factory=list)
    stress: list[float] = field(default_factory=list)

    def __post_init__(self):
        if not self.F:
            self.F = [1.0] * len(self.x)
        if not self.stress:
            self.stress = [0.0] * len(self.x)

    def volume(self, p: int) -> float:
        return self.F[p] * self.vol0[p]


def hat_weights(x: float, dx: float) -> list[tuple[int, float, float]]:
    """The two nodes i with N_i(x) > 0 or at the left of x, with N_i(x) and dN_i/dx (one-sided at a node)."""
    j = math.floor(x / dx)
    w = x / dx - j
    return [(j, 1 - w, -1 / dx), (j + 1, w, 1 / dx)]


def grid_force(ps: Particles, dx: float, n: int) -> list[float]:
    """Internal nodal force f_i = -sum_p V_p sigma_p dN_i(x_p)."""
    f = [0.0] * n
    for p in range(len(ps.x)):
        for i, _, dn in hat_weights(ps.x[p], dx):
            f[i] -= ps.volume(p) * ps.stress[p] * dn
    return f


def mpm_step(ps: Particles, dx: float, n: int, young: float, h: float, fixed: frozenset = frozenset()) -> Particles:
    """One USL step for a linear elastic material, sigma = E (F - 1) by the increment rule."""
    mass = [0.0] * n
    mom = [0.0] * n
    for p in range(len(ps.x)):  # @line L1
        for i, w, _ in hat_weights(ps.x[p], dx):
            mass[i] += w * ps.m[p]  # @line L2
            mom[i] += w * ps.m[p] * ps.v[p]  # @line L2
    f = grid_force(ps, dx, n)  # @line L3
    v_old = [mom[i] / mass[i] if mass[i] > 0 else 0.0 for i in range(n)]  # @line L4
    v_new = [v_old[i] + h * f[i] / mass[i] if mass[i] > 0 else 0.0 for i in range(n)]  # @line L4
    for i in fixed:  # @line L5
        v_new[i] = 0.0  # @line L5
    acc = [(v_new[i] - v_old[i]) / h for i in range(n)]  # @line L5
    out = Particles(list(ps.x), list(ps.v), list(ps.m), list(ps.vol0), list(ps.F), list(ps.stress))
    for p in range(len(ps.x)):  # @line L6
        ws = hat_weights(ps.x[p], dx)
        out.v[p] = ps.v[p] + h * sum(w * acc[i] for i, w, _ in ws)  # @line L7
        out.x[p] = ps.x[p] + h * sum(w * v_new[i] for i, w, _ in ws)  # @line L8
        rate = sum(dn * v_new[i] for i, _, dn in ws)  # @line L9
        out.F[p] = ps.F[p] * (1 + h * rate)  # @line L10
        out.stress[p] = ps.stress[p] + young * h * rate  # @line L11
    return out  # @line L12


def vibrating_bar(cells: int, ppc: int, length: float, young: float, rho: float, v0: float, h: float):
    """Particles of a bar on [0, length] in its first mode, v = v0 sin(pi x / (2 length)), and the grid size."""
    dx = length / cells
    xs, vs, ms, vols = [], [], [], []
    for c in range(cells):
        for k in range(ppc):
            x = (c + (k + 0.5) / ppc) * dx
            xs.append(x)
            vs.append(v0 * math.sin(math.pi * x / (2 * length)))
            vols.append(dx / ppc)
            ms.append(rho * dx / ppc)
    return Particles(xs, vs, ms, vols), dx, cells + 2
