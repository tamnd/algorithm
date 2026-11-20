# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/force-matching-coarse-graining/. The authors are listed in prov/3CW63P.jsonl.
"""Multiscale coarse-graining by force matching (MS-CG).

The coarse-grained (CG) model has one pair force f(r) between sites. The
force is a linear combination f(r) = sum_k c_k phi_k(r) of hat functions
on a uniform grid r_0 < ... < r_(K-1) = r_c. For a configuration of N
sites in a periodic box, the CG force on site i is

    F_i(c) = sum_(j != i) f(r_ij) e_ij,   e_ij = (x_i - x_j) / r_ij,

so a positive f is a repulsion. F_i is linear in c: each Cartesian
component of F_i is a row a of a design matrix A, with a . c = F_i.
Force matching chooses c to minimize

    chi^2(c) = sum over configurations, sites and components of (a . c - F_ref)^2,

where F_ref is the reference force mapped from an atomistic run. This is
a linear least squares problem. The code accumulates the normal equations
G c = b with G = A^T A and b = A^T F_ref, one row at a time, and solves
them with scimat.solve. A basis function that no pair distance touches
gives a zero row in G; its coefficient is set to 0.

Sites live in a 2D periodic square box with the minimum image convention.
"""

import math
from typing import Sequence

import scimat

Point = tuple[float, float]


class HatBasis:
    """Hat functions phi_k on the nodes r_k = r0 + k dr, k = 0..K-1, with r_(K-1) = rc."""

    def __init__(self, r0: float, rc: float, k: int):
        if k < 2 or not 0.0 <= r0 < rc:
            raise ValueError("need k >= 2 and 0 <= r0 < rc")
        self.r0, self.rc, self.k = r0, rc, k
        self.dr = (rc - r0) / (k - 1)
        self.nodes = [r0 + m * self.dr for m in range(k)]

    def values(self, r: float) -> list[tuple[int, float]]:
        """The nonzero values (k, phi_k(r)), at most two, for r0 <= r <= rc; empty outside."""
        if r < self.r0 or r > self.rc:
            return []
        s = (r - self.r0) / self.dr
        m = min(int(s), self.k - 2)
        t = s - m
        return [(m, 1.0 - t), (m + 1, t)]

    def force(self, c: Sequence[float], r: float) -> float:
        """f(r) = sum_k c_k phi_k(r)."""
        return sum(c[m] * v for m, v in self.values(r))

    def potential(self, c: Sequence[float], r: float) -> float:
        """V(r) = integral of f from r to rc, exact for the piecewise linear f; V(rc) = 0."""
        if r >= self.rc:
            return 0.0
        r = max(r, self.r0)
        m = min(int((r - self.r0) / self.dr), self.k - 2)
        fr = self.force(c, r)
        total = 0.5 * (fr + c[m + 1]) * (self.nodes[m + 1] - r)
        for q in range(m + 1, self.k - 1):
            total += 0.5 * (c[q] + c[q + 1]) * self.dr
        return total


def minimum_image(d: float, box: float) -> float:
    return d - box * round(d / box)


def design_rows(x: Sequence[Point], box: float, basis: HatBasis) -> list[list[float]]:
    """The 2N rows of the design matrix of one configuration: row 2i is F_i,x and row 2i+1 is F_i,y."""
    n = len(x)
    rows = [[0.0] * basis.k for _ in range(2 * n)]
    for i in range(n):
        for j in range(i + 1, n):
            dx = minimum_image(x[i][0] - x[j][0], box)
            dy = minimum_image(x[i][1] - x[j][1], box)
            r = math.hypot(dx, dy)
            for m, v in basis.values(r):
                ex, ey = v * dx / r, v * dy / r
                rows[2 * i][m] += ex
                rows[2 * i + 1][m] += ey
                rows[2 * j][m] -= ex
                rows[2 * j + 1][m] -= ey
    return rows


def cg_forces(x: Sequence[Point], box: float, basis: HatBasis, c: Sequence[float]) -> list[float]:
    """The CG forces (F_0x, F_0y, F_1x, ...) of one configuration for the coefficients c."""
    return [scimat.dot(a, c) for a in design_rows(x, box, basis)]


def force_matching(configs: Sequence[Sequence[Point]], forces: Sequence[Sequence[float]],
                   box: float, basis: HatBasis) -> list[float]:
    """Return the coefficients c that minimize chi^2 over all configurations.

    forces[t] is the flat list (F_0x, F_0y, F_1x, ...) of reference forces of configs[t].
    """
    k = basis.k
    g = [[0.0] * k for _ in range(k)]                                   # @line L1
    b = [0.0] * k
    for x, f_ref in zip(configs, forces):                               # @line L2
        rows = design_rows(x, box, basis)                               # @line L3
        for a, f in zip(rows, f_ref):                                   # @line L4
            for p in range(k):                                          # @line L5
                if a[p] != 0.0:
                    b[p] += a[p] * f
                    for q in range(k):
                        g[p][q] += a[p] * a[q]
    unused = [p for p in range(k) if g[p][p] == 0.0]                    # @line L6
    for p in unused:
        g[p][p] = 1.0
    return scimat.solve(g, b)                                           # @line L7


def chi2(configs: Sequence[Sequence[Point]], forces: Sequence[Sequence[float]],
         box: float, basis: HatBasis, c: Sequence[float]) -> float:
    """The force residual sum of squares chi^2(c)."""
    total = 0.0
    for x, f_ref in zip(configs, forces):
        for fc, f in zip(cg_forces(x, box, basis, c), f_ref):
            total += (fc - f) ** 2
    return total
