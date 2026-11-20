# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/car-parrinello-molecular-dynamics/. The authors are listed in prov/PQJARX.jsonl.
"""Car-Parrinello molecular dynamics on a toy electronic model.

This is a toy, not a quantum chemistry code. It keeps the structure of CPMD:
the orbital coefficients c are dynamic variables with a fictitious mass mu,
and nuclei and orbital move together under the extended Lagrangian

    L = sum_k M_k v_k^2 / 2 + (mu / 2) |dc/dt|^2 - E(x, c) + Lambda (|c|^2 - 1).

There is no self-consistent solve during the run. The constraint |c| = 1 is
kept by a SHAKE step on the positions and a RATTLE step on the velocities,
and the conserved quantity is

    E_cons = sum_k M_k v_k^2 / 2 + (mu / 2) |dc/dt|^2 + E(x, c).

The model is the one of the BOMD page: N atoms on a line, one orbital per
atom, two electrons in the orbital c,

    E(x, c) = 2 c^T H0(x) c + U sum_i c_i^4 + Phi(x),
    H0_ij = -t0 exp(-a (r_ij - d0)) (i != j),  Phi = sum_{i<j} A exp(-b (r_ij - d0)).
"""

import math
from typing import Sequence


def jacobi_eigen(a: Sequence[Sequence[float]], tol: float = 1e-14,
                 max_sweeps: int = 100) -> tuple[list[float], list[list[float]]]:
    """Eigenvalues (ascending) and eigenvectors (as columns) of a symmetric matrix."""
    n = len(a)
    m = [list(row) for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(max_sweeps):
        if sum(m[i][j] ** 2 for i in range(n) for j in range(n) if i != j) < tol * tol:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(m[p][q]) < 1e-300:
                    continue
                theta = (m[q][q] - m[p][p]) / (2.0 * m[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    m[k][p], m[k][q] = c * m[k][p] - s * m[k][q], s * m[k][p] + c * m[k][q]
                for k in range(n):
                    m[p][k], m[q][k] = c * m[p][k] - s * m[q][k], s * m[p][k] + c * m[q][k]
                for k in range(n):
                    v[k][p], v[k][q] = c * v[k][p] - s * v[k][q], s * v[k][p] + c * v[k][q]
    order = sorted(range(n), key=lambda i: m[i][i])
    return [m[i][i] for i in order], [[v[k][i] for i in order] for k in range(n)]


class ToyModel:
    def __init__(self, t0=1.0, a=1.0, d0=1.0, big_a=1.0, b=2.0, u=1.0):
        self.t0, self.a, self.d0, self.big_a, self.b, self.u = t0, a, d0, big_a, b, u

    def hopping(self, x):
        n = len(x)
        h = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                h[i][j] = h[j][i] = -self.t0 * math.exp(-self.a * (abs(x[i] - x[j]) - self.d0))
        return h

    def energy(self, x, c) -> float:
        n = len(x)
        h0 = self.hopping(x)
        e = 2.0 * sum(c[i] * h0[i][j] * c[j] for i in range(n) for j in range(n))
        e += self.u * sum(ci ** 4 for ci in c)
        return e + sum(self.big_a * math.exp(-self.b * (abs(x[i] - x[j]) - self.d0))
                       for i in range(n) for j in range(i + 1, n))

    def orbital_force(self, x, c) -> list[float]:
        """-dE/dc = -4 (H0 + U diag(c^2)) c."""
        h0 = self.hopping(x)
        n = len(c)
        return [-4.0 * (sum(h0[i][j] * c[j] for j in range(n)) + self.u * c[i] ** 3) for i in range(n)]

    def nuclear_force(self, x, c) -> list[float]:
        """-dE/dx_k at fixed c."""
        n = len(x)
        f = [0.0] * n
        for i in range(n):
            for j in range(i + 1, n):
                r = abs(x[i] - x[j])
                sgn = 1.0 if x[i] > x[j] else -1.0
                dt = self.a * self.t0 * math.exp(-self.a * (r - self.d0))
                dphi = -self.b * self.big_a * math.exp(-self.b * (r - self.d0))
                de_dr = 4.0 * c[i] * c[j] * dt + dphi
                f[i] -= de_dr * sgn
                f[j] += de_dr * sgn
        return f

    def ground_state(self, x, dens=None, tol=1e-12, max_iter=500, mix=0.5):
        """Self-consistent lowest orbital, used only for the start and for comparison."""
        n = len(x)
        h0 = self.hopping(x)
        if dens is None:
            dens = [1.0 / n] * n
        for _ in range(max_iter):
            h = [[h0[i][j] + (self.u * dens[i] if i == j else 0.0) for j in range(n)] for i in range(n)]
            _, vecs = jacobi_eigen(h)
            c = [vecs[k][0] for k in range(n)]
            new = [ci * ci for ci in c]
            res = max(abs(p - q) for p, q in zip(new, dens))
            dens = [(1 - mix) * p + mix * q for p, q in zip(dens, new)]
            if res < tol:
                break
        return c


def cpmd(model: ToyModel, x: list[float], v: list[float], m: Sequence[float], c: list[float],
         cdot: list[float], mu: float, h: float, steps: int, fixed_nuclei: bool = False):
    """Velocity Verlet for nuclei and orbital, with SHAKE and RATTLE for |c| = 1.

    Returns a list of (x, c, nuclear KE, fictitious KE, E_cons) after each step,
    starting with the initial state.
    """
    def record():
        kn = 0.0 if fixed_nuclei else 0.5 * sum(mi * vi * vi for mi, vi in zip(m, v))
        ke = 0.5 * mu * sum(d * d for d in cdot)
        return list(x), list(c), kn, ke, kn + ke + model.energy(x, c)

    fx, fc = model.nuclear_force(x, c), model.orbital_force(x, c)           # @line L1
    out = [record()]
    for _ in range(steps):                                                  # @line L2
        if not fixed_nuclei:
            v = [vi + 0.5 * h * fi / mi for vi, fi, mi in zip(v, fx, m)]    # @line L3
            x = [xi + h * vi for xi, vi in zip(x, v)]                       # @line L3
        cdot = [d + 0.5 * h * f / mu for d, f in zip(cdot, fc)]             # @line L4
        d = [ci + h * di for ci, di in zip(c, cdot)]                        # @line L5
        dc = sum(p * q for p, q in zip(d, c))                               # SHAKE: |d + lam c| = 1
        lam = -dc + math.sqrt(dc * dc - sum(p * p for p in d) + 1.0)        # @line L5
        cdot = [di + lam * ci / h for di, ci in zip(cdot, c)]
        c = [p + lam * q for p, q in zip(d, c)]                             # @line L5
        fx, fc = model.nuclear_force(x, c), model.orbital_force(x, c)       # @line L6
        if not fixed_nuclei:
            v = [vi + 0.5 * h * fi / mi for vi, fi, mi in zip(v, fx, m)]    # @line L7
        cdot = [di + 0.5 * h * f / mu for di, f in zip(cdot, fc)]           # @line L7
        proj = sum(p * q for p, q in zip(c, cdot))                          # RATTLE: c . cdot = 0
        cdot = [di - proj * ci for di, ci in zip(cdot, c)]                  # @line L8
        out.append(record())
    return out                                                              # @line L9
