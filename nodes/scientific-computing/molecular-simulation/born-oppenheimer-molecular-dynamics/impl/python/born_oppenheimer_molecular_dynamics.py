# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/born-oppenheimer-molecular-dynamics/. The authors are listed in prov/KR4Y5Q.jsonl.
"""Born-Oppenheimer molecular dynamics on a toy electronic model.

This is a toy, not a quantum chemistry code. It keeps the structure of BOMD:
at every time step the electrons are solved self-consistently for the
current nuclear positions, the forces come from the Hellmann-Feynman
theorem, and the nuclei move by velocity Verlet.

The model: N atoms on a line, one orbital per atom, two electrons (one spin
pair) in the lowest orbital c, with |c| = 1.

    H0_ij = t(r_ij) = -t0 exp(-a (r_ij - d0))   for i != j, H0_ii = 0,
    E_el(c) = 2 c^T H0 c + U sum_i c_i^4,       (a mean-field on-site repulsion)
    Phi = sum_{i<j} A exp(-b (r_ij - d0)),       (repulsion of the cores)
    E = E_el(c) + Phi.

E_el is stationary on |c| = 1 when c is the lowest eigenvector of the
self-consistent matrix H(c) = H0 + U diag(c_i^2). At that point
dE/dx_k = 2 c^T (dH0/dx_k) c + dPhi/dx_k, with no term from dc/dx_k.
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
        off = sum(m[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < tol * tol:
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
                    mkp, mkq = m[k][p], m[k][q]
                    m[k][p], m[k][q] = c * mkp - s * mkq, s * mkp + c * mkq
                for k in range(n):
                    mpk, mqk = m[p][k], m[q][k]
                    m[p][k], m[q][k] = c * mpk - s * mqk, s * mpk + c * mqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p], v[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    order = sorted(range(n), key=lambda i: m[i][i])
    vals = [m[i][i] for i in order]
    vecs = [[v[k][i] for i in order] for k in range(n)]
    return vals, vecs


class ToyModel:
    def __init__(self, t0=1.0, a=1.0, d0=1.0, big_a=1.0, b=2.0, u=1.0):
        self.t0, self.a, self.d0, self.big_a, self.b, self.u = t0, a, d0, big_a, b, u

    def hopping(self, x: Sequence[float]) -> list[list[float]]:
        n = len(x)
        h = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                h[i][j] = h[j][i] = -self.t0 * math.exp(-self.a * (abs(x[i] - x[j]) - self.d0))
        return h

    def repulsion(self, x: Sequence[float]) -> float:
        n = len(x)
        return sum(self.big_a * math.exp(-self.b * (abs(x[i] - x[j]) - self.d0))
                   for i in range(n) for j in range(i + 1, n))

    def electronic_energy(self, h0, c) -> float:
        n = len(c)
        e = 2.0 * sum(c[i] * h0[i][j] * c[j] for i in range(n) for j in range(n))
        return e + self.u * sum(ci ** 4 for ci in c)

    def scf(self, x, dens=None, tol=1e-10, max_iter=200, mix=0.5):
        """Self-consistent lowest orbital. Returns (c, E, residual, iterations)."""
        h0 = self.hopping(x)
        n = len(x)
        if dens is None:
            dens = [1.0 / n] * n
        for it in range(1, max_iter + 1):
            h = [[h0[i][j] + (self.u * dens[i] if i == j else 0.0) for j in range(n)] for i in range(n)]
            _, vecs = jacobi_eigen(h)
            c = [vecs[k][0] for k in range(n)]
            new = [ci * ci for ci in c]
            res = max(abs(p - q) for p, q in zip(new, dens))
            dens = [(1 - mix) * p + mix * q for p, q in zip(dens, new)]
            if res < tol:
                break
        return c, self.electronic_energy(h0, c) + self.repulsion(x), res, it

    def forces(self, x, c) -> list[float]:
        """Hellmann-Feynman forces -dE/dx_k for the orbital c."""
        n = len(x)
        f = [0.0] * n
        for i in range(n):
            for j in range(i + 1, n):
                r = abs(x[i] - x[j])
                sgn = 1.0 if x[i] > x[j] else -1.0
                dt = self.a * self.t0 * math.exp(-self.a * (r - self.d0))        # dt/dr
                dphi = -self.b * self.big_a * math.exp(-self.b * (r - self.d0))  # dPhi/dr
                de_dr = 2.0 * 2.0 * c[i] * c[j] * dt + dphi                     # both (i,j) and (j,i)
                f[i] -= de_dr * sgn
                f[j] += de_dr * sgn
        return f


def bomd(model: ToyModel, x: list[float], v: list[float], m: Sequence[float], h: float,
         steps: int, tol: float = 1e-10, max_iter: int = 200) -> list[float]:
    """Velocity Verlet with an SCF solve at every step. Returns the total energy at each step."""
    c, e, _, _ = model.scf(x, tol=tol, max_iter=200)                      # @line L1
    dens = [ci * ci for ci in c]
    f = model.forces(x, c)                                                # @line L2
    energies = [e + 0.5 * sum(mi * vi * vi for mi, vi in zip(m, v))]
    for _ in range(steps):                                                # @line L3
        v = [vi + 0.5 * h * fi / mi for vi, fi, mi in zip(v, f, m)]       # @line L4
        x = [xi + h * vi for xi, vi in zip(x, v)]                         # @line L5
        c, e, _, _ = model.scf(x, dens, tol, max_iter)                    # @line L6
        dens = [ci * ci for ci in c]
        f = model.forces(x, c)                                            # @line L7
        v = [vi + 0.5 * h * fi / mi for vi, fi, mi in zip(v, f, m)]       # @line L8
        energies.append(e + 0.5 * sum(mi * vi * vi for mi, vi in zip(m, v)))
    return energies                                                       # @line L9
