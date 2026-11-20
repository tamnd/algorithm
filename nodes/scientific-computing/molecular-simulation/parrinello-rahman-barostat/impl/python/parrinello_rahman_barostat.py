# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parrinello-rahman-barostat/. The authors are listed in prov/A5VK4X.jsonl.
"""The Parrinello-Rahman barostat in two dimensions, with a symmetric splitting.

The periodic cell is the 2 by 2 matrix H whose columns are the cell vectors.
Particle i has scaled coordinates s_i in [0, 1)^2 and the position r_i = H s_i.
With G = H^T H, the momenta pi_i = m_i G ds_i/dt, the cell momentum P_H, the
cell mass W and the external pressure P, the Hamiltonian is

    E = sum_i pi_i^T G^-1 pi_i / (2 m_i) + U(H s) + tr(P_H^T P_H) / (2 W) + P det(H).

E is the enthalpy of the particles plus the kinetic energy of the cell. The
flow of E samples the isoenthalpic-isobaric (NPH) ensemble. A thermostat on
the particles and on the cell is needed for the NPT ensemble.

E is split into three parts. Each part has an exact flow:

    V: U + P det(H)      pi_i += t H^T f_i,
                          P_H += t (sum_pairs f_ij s_ij^T - P det(H) H^-T)
    T: particle kinetic  s_i += t H^-1 v_i,  P_H += t sum_i m_i v_i (H^-1 v_i)^T,
                          with v_i = H^-T pi_i / m_i (fixed during the flow)
    C: cell kinetic      H += t P_H / W

One step of length h is V(h/2) T(h/2) C(h) T(h/2) V(h/2). It is symplectic,
time reversible and second order, and it uses one force evaluation per step.

The pair potential is the Lennard-Jones potential with a force shift at the
cutoff rc, so that the energy and the force are continuous at rc.

Cost per step: one force evaluation, here Theta(N^2) pairs, and Theta(N)
other work.
"""

import math
from typing import Callable

Vec = list[float]
Mat = list[list[float]]
PairPotential = Callable[[float], tuple[float, float]]


def lj_force_shifted(rc: float, eps: float = 1.0, sigma: float = 1.0) -> PairPotential:
    """Lennard-Jones phi(r) - phi(rc) - (r - rc) phi'(rc); returns (energy, -dphi/dr)."""
    def raw(r: float) -> tuple[float, float]:
        sr6 = (sigma / r) ** 6
        return 4.0 * eps * (sr6 * sr6 - sr6), 24.0 * eps * (2.0 * sr6 * sr6 - sr6) / r
    ec, fc = raw(rc)

    def phi(r: float) -> tuple[float, float]:
        e, f = raw(r)
        return e - ec + (r - rc) * fc, f - fc
    phi.rc = rc
    return phi


def det2(a: Mat) -> float:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inv2(a: Mat) -> Mat:
    d = det2(a)
    return [[a[1][1] / d, -a[0][1] / d], [-a[1][0] / d, a[0][0] / d]]


def mv(a: Mat, x: Vec) -> Vec:
    return [a[0][0] * x[0] + a[0][1] * x[1], a[1][0] * x[0] + a[1][1] * x[1]]


def mtv(a: Mat, x: Vec) -> Vec:
    """a^T x."""
    return [a[0][0] * x[0] + a[1][0] * x[1], a[0][1] * x[0] + a[1][1] * x[1]]


def min_width(cell: Mat) -> float:
    """The smaller of the two distances between opposite sides of the cell."""
    area = abs(det2(cell))
    la = math.hypot(cell[0][0], cell[1][0])
    lb = math.hypot(cell[0][1], cell[1][1])
    return min(area / la, area / lb)


def pair_forces(s: list[Vec], cell: Mat, phi: PairPotential) -> tuple[float, list[Vec], Mat, Mat]:
    """Return U, the Cartesian forces f_i, sum f_ij s_ij^T and the virial sum f_ij r_ij^T.

    Each pair uses the image with scaled separation in [-1/2, 1/2]^2. If
    2 rc is less than the smallest width w_k of the cell, this image is the
    only one closer than rc: a scaled component of a vector r has size at
    most |r| / w_k < 1/2. So the function raises ValueError if 2 rc >= the
    smallest width.
    """
    rc = phi.rc
    if 2.0 * rc >= min_width(cell):
        raise ValueError("cutoff too large for the cell")
    n = len(s)
    u = 0.0
    f = [[0.0, 0.0] for _ in range(n)]
    fs = [[0.0, 0.0], [0.0, 0.0]]
    vir = [[0.0, 0.0], [0.0, 0.0]]
    rc2 = rc * rc
    for i in range(n):
        si = s[i]
        for j in range(i + 1, n):
            d0 = si[0] - s[j][0]
            d1 = si[1] - s[j][1]
            a0 = d0 - round(d0)
            a1 = d1 - round(d1)
            r0 = cell[0][0] * a0 + cell[0][1] * a1
            r1 = cell[1][0] * a0 + cell[1][1] * a1
            r2 = r0 * r0 + r1 * r1
            if r2 >= rc2:
                continue
            r = math.sqrt(r2)
            e, mag = phi(r)
            u += e
            g0 = mag * r0 / r
            g1 = mag * r1 / r
            f[i][0] += g0
            f[i][1] += g1
            f[j][0] -= g0
            f[j][1] -= g1
            fs[0][0] += g0 * a0
            fs[0][1] += g0 * a1
            fs[1][0] += g1 * a0
            fs[1][1] += g1 * a1
            vir[0][0] += g0 * r0
            vir[0][1] += g0 * r1
            vir[1][0] += g1 * r0
            vir[1][1] += g1 * r1
    return u, f, fs, vir


def _velocities(pi: list[Vec], m: list[float], cell: Mat) -> list[Vec]:
    hinv = inv2(cell)
    return [[c / mi for c in mtv(hinv, p)] for p, mi in zip(pi, m)]


def _kick(pi, ph, f, fs, cell, pressure, t):
    """The exact flow of U + P det(H) for a time t."""
    for i, fi in enumerate(f):
        g = mtv(cell, fi)
        pi[i][0] += t * g[0]
        pi[i][1] += t * g[1]
    vol = det2(cell)
    hit = inv2(cell)
    for a in range(2):
        for b in range(2):
            ph[a][b] += t * (fs[a][b] - pressure * vol * hit[b][a])


def _drift_particles(s, pi, ph, m, cell, t):
    """The exact flow of the particle kinetic energy for a time t."""
    hinv = inv2(cell)
    for i, vi in enumerate(_velocities(pi, m, cell)):
        sd = mv(hinv, vi)
        s[i][0] += t * sd[0]
        s[i][1] += t * sd[1]
        for a in range(2):
            for b in range(2):
                ph[a][b] += t * m[i] * vi[a] * sd[b]


def energy(s, pi, ph, m, cell, pressure, w, u) -> float:
    """The conserved quantity E = K + U + tr(P_H^T P_H) / (2 W) + P det(H)."""
    k = sum(0.5 * mi * (vi[0] ** 2 + vi[1] ** 2) for vi, mi in zip(_velocities(pi, m, cell), m))
    kc = sum(ph[a][b] ** 2 for a in range(2) for b in range(2)) / (2.0 * w)
    return k + u + kc + pressure * det2(cell)


def pressure_tensor(v: list[Vec], m: list[float], vir: Mat, cell: Mat) -> Mat:
    """The internal pressure tensor (sum m v v^T + sum f_ij r_ij^T) / det(H)."""
    vol = det2(cell)
    return [[(sum(mi * vi[a] * vi[b] for vi, mi in zip(v, m)) + vir[a][b]) / vol
             for b in range(2)] for a in range(2)]


def parrinello_rahman(
    r: list[Vec], v: list[Vec], m: list[float], cell: Mat, cell_velocity: Mat,
    phi: PairPotential, h: float, steps: int, pressure: float, w: float,
) -> tuple[list[Vec], list[Vec], Mat, Mat, list[tuple[float, float, Mat]]]:
    """Run steps of the Parrinello-Rahman equations (NPH) in two dimensions.

    r and v are Cartesian positions and velocities. cell_velocity is dH/dt.
    Returns the final positions (unwrapped), velocities, cell and cell
    velocity, and (E, det(H), internal pressure tensor) after each step.
    The inputs are not changed.
    """
    if h <= 0 or w <= 0:
        raise ValueError("need h > 0 and w > 0")
    cell = [list(row) for row in cell]
    hinv = inv2(cell)
    s = [mv(hinv, ri) for ri in r]
    pi = [[mi * c for c in mtv(cell, vi)] for vi, mi in zip(v, m)]
    ph = [[w * c for c in row] for row in cell_velocity]
    u, f, fs, vir = pair_forces(s, cell, phi)  # @line L1
    out = []
    for _ in range(steps):  # @line L2
        _kick(pi, ph, f, fs, cell, pressure, 0.5 * h)  # @line L3
        _drift_particles(s, pi, ph, m, cell, 0.5 * h)  # @line L4
        for a in range(2):
            for b in range(2):
                cell[a][b] += h * ph[a][b] / w  # @line L5
        _drift_particles(s, pi, ph, m, cell, 0.5 * h)  # @line L6
        u, f, fs, vir = pair_forces(s, cell, phi)  # @line L7
        _kick(pi, ph, f, fs, cell, pressure, 0.5 * h)  # @line L8
        vel = _velocities(pi, m, cell)
        out.append((energy(s, pi, ph, m, cell, pressure, w, u), det2(cell),
                    pressure_tensor(vel, m, vir, cell)))  # @line L9
    pos = [mv(cell, si) for si in s]
    vel = _velocities(pi, m, cell)
    return pos, vel, cell, [[c / w for c in row] for row in ph], out  # @line L10


def triangular_lattice(cols: int, rows: int, a: float) -> tuple[list[Vec], Mat]:
    """A triangular lattice of cols by rows sites (rows even) with spacing a, and its cell."""
    if rows % 2:
        raise ValueError("rows must be even")
    dy = a * math.sqrt(3.0) / 2.0
    pos = [[(c + 0.5 * (k % 2)) * a, k * dy] for k in range(rows) for c in range(cols)]
    return pos, [[cols * a, 0.0], [0.0, rows * dy]]
