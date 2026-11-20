# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/embedded-atom-method/. The authors are listed in prov/4CFCM8.jsonl.

import math
from typing import Callable, Optional

Point = list[float]
Fn = Callable[[float], float]


def _separation(ri: Point, rj: Point, box: Optional[float]) -> list[float]:
    d = [a - b for a, b in zip(ri, rj)]
    if box is not None:
        d = [x - box * round(x / box) for x in d]
    return d


def eam_energy_forces(
    positions: list[Point],
    embed: Fn,
    dembed: Fn,
    density: Fn,
    ddensity: Fn,
    pair: Fn,
    dpair: Fn,
    rc: float,
    box: Optional[float] = None,
) -> tuple[float, list[float], list[list[float]]]:
    """The EAM energy U = sum_i F(rho_i) + sum_{i<j} phi(r_ij), with rho_i = sum_{j != i} f(r_ij).

    One species. embed, density and pair are F, f and phi; the d-functions
    are their derivatives. f and phi are taken as zero from rc on. With box
    set, the box is cubic and periodic and pairs use the nearest image, which
    needs rc <= box / 2. Returns (U, rho, forces).
    """
    if box is not None and rc > box / 2:
        raise ValueError("the cutoff must be at most half the box")
    n = len(positions)
    rho = [0.0] * n  # @line L1
    u = 0.0  # @line L1
    close = []
    for i in range(n):  # @line L2
        for j in range(i + 1, n):  # @line L2
            d = _separation(positions[i], positions[j], box)
            r = math.sqrt(sum(x * x for x in d))
            if r >= rc:  # @line L2
                continue
            close.append((i, j, r, d))
            fr = density(r)  # @line L3
            rho[i] += fr  # @line L3
            rho[j] += fr  # @line L3
            u += pair(r)  # @line L3
    for i in range(n):  # @line L4
        u += embed(rho[i])  # @line L4
    dF = [dembed(x) for x in rho]
    forces = [[0.0] * len(positions[0]) for _ in range(n)]
    for i, j, r, d in close:  # @line L5
        g = (dF[i] + dF[j]) * ddensity(r) + dpair(r)  # @line L6
        for q in range(len(d)):
            c = g * d[q] / r
            forces[i][q] -= c  # @line L7
            forces[j][q] += c  # @line L7
    return u, rho, forces  # @line L8


def fcc_lattice(cells: int, a: float) -> list[Point]:
    """An fcc crystal of 4 cells^3 atoms with cubic lattice constant a, in a box of side cells a."""
    basis = [(0, 0, 0), (0.5, 0.5, 0), (0.5, 0, 0.5), (0, 0.5, 0.5)]
    return [
        [a * (x + b[0]), a * (y + b[1]), a * (z + b[2])]
        for x in range(cells)
        for y in range(cells)
        for z in range(cells)
        for b in basis
    ]
