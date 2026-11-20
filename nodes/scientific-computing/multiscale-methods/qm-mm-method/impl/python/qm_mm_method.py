# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/qm-mm-method/. The authors are listed in prov/CDM80T.jsonl.
"""A toy QM/MM calculation on a chain of atoms in one dimension.

This is a toy. The "QM" part is a Hueckel tight-binding model, not a real
electronic structure method, and the "MM" part is a chain of harmonic
bonds. The code shows the parts that every QM/MM program has: the split
into a QM region and an MM region, the link atoms that cap the cut bonds,
the transfer of the link atom forces onto the real atoms, and the two ways
to add the energies (additive and subtractive, also called ONIOM).

Atoms 0 .. n-1 sit at positions y[0] < y[1] < ... on a line, with a bond
between each pair of neighbors. The QM region is the block of atoms
q0 .. q1-1. Each bond (a, b) with a in the QM region and b outside it is
cut and gets a link atom at y_a + g (y_b - y_a).

QM model (for a chain of sites s_0 < s_1 < ... with bond lengths r_i):
    H_{i,i+1} = -t(r_i), t(r) = t0 exp(-beta (r - r0)), one orbital per site,
    one electron per site, each occupied orbital holds two electrons,
    E_QM = 2 (sum of the occupied eigenvalues) + sum_i A exp(-2 beta (r_i - r0)).
MM model: E_MM = sum over bonds of (k / 2) (r - d0)^2.
"""

import math
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class Params:
    t0: float = 1.0                 # hopping at r = r0
    beta: float = math.log(2.0)     # decay rate of the hopping
    rep: float = 1.0                # repulsion A; with A = t0 the QM dimer has its minimum at r0
    r0: float = 1.0
    k: float = 10.0                 # MM bond stiffness
    d0: float = 2.0                 # MM bond rest length
    g: float = 0.5                  # link atom placed at the fraction g of the cut bond


def jacobi_eigen(a: Sequence[Sequence[float]], tol: float = 1e-14,
                 max_sweeps: int = 60) -> tuple[list[float], list[list[float]]]:
    """Cyclic Jacobi method for a symmetric matrix.

    Returns the eigenvalues in increasing order and the eigenvectors as rows
    (vecs[k] belongs to vals[k]).
    """
    n = len(a)
    m = [list(map(float, row)) for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    scale = sum(m[i][j] ** 2 for i in range(n) for j in range(n)) or 1.0
    for _ in range(max_sweeps):
        off = sum(m[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off <= tol * tol * scale:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if m[p][q] == 0.0:
                    continue
                theta = (m[q][q] - m[p][p]) / (2.0 * m[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for r in range(n):          # columns p and q
                    mrp, mrq = m[r][p], m[r][q]
                    m[r][p] = c * mrp - s * mrq
                    m[r][q] = s * mrp + c * mrq
                for r in range(n):          # rows p and q
                    mpr, mqr = m[p][r], m[q][r]
                    m[p][r] = c * mpr - s * mqr
                    m[q][r] = s * mpr + c * mqr
                for r in range(n):
                    vrp, vrq = v[r][p], v[r][q]
                    v[r][p] = c * vrp - s * vrq
                    v[r][q] = s * vrp + c * vrq
    else:
        raise ArithmeticError("Jacobi method did not converge")
    order = sorted(range(n), key=lambda i: m[i][i])
    return [m[i][i] for i in order], [[v[r][i] for r in range(n)] for i in order]


def qm_chain(s: Sequence[float], p: Params) -> tuple[float, list[float]]:
    """Energy and forces of the tight-binding chain with sites at s (sorted)."""
    n = len(s)
    if n % 2 != 0:
        raise ValueError("the model system needs an even number of sites (closed shell)")
    r = [s[i + 1] - s[i] for i in range(n - 1)]
    t = [p.t0 * math.exp(-p.beta * (ri - p.r0)) for ri in r]
    h = [[0.0] * n for _ in range(n)]
    for i in range(n - 1):
        h[i][i + 1] = h[i + 1][i] = -t[i]
    vals, vecs = jacobi_eigen(h)
    occ = vecs[:n // 2]
    energy = 2.0 * sum(vals[:n // 2])
    f = [0.0] * n
    for i in range(n - 1):
        bond_order = 2.0 * sum(c[i] * c[i + 1] for c in occ)
        phi = p.rep * math.exp(-2.0 * p.beta * (r[i] - p.r0))
        energy += phi
        # Hellmann-Feynman: dE_el/dr = 2 P dH/dr = 2 P beta t; dphi/dr = -2 beta phi
        de_dr = 2.0 * bond_order * p.beta * t[i] - 2.0 * p.beta * phi
        f[i] += de_dr
        f[i + 1] -= de_dr
    return energy, f


def mm_bonds(y: Sequence[float], bonds: Sequence[tuple[int, int, float, float]],
             n: int) -> tuple[float, list[float]]:
    """Harmonic bonds (i, j, k, d0) with energy (k / 2) (y_j - y_i - d0)^2."""
    energy = 0.0
    f = [0.0] * n
    for i, j, k, d0 in bonds:
        stretch = (y[j] - y[i]) - d0
        energy += 0.5 * k * stretch * stretch
        f[i] += k * stretch
        f[j] -= k * stretch
    return energy, f


def model_sites(n: int, q0: int, q1: int, g: float) -> list[list[tuple[int, float]]]:
    """Each site of the model system as a list of (atom, weight); a link atom has two."""
    if not 0 <= q0 < q1 <= n:
        raise ValueError("the QM region must be a nonempty block of atoms")
    sites = []
    if q0 > 0:
        sites.append([(q0, 1.0 - g), (q0 - 1, g)])      # cut bond (q0 - 1, q0)
    sites.extend([[(i, 1.0)] for i in range(q0, q1)])
    if q1 < n:
        sites.append([(q1 - 1, 1.0 - g), (q1, g)])      # cut bond (q1 - 1, q1)
    return sites


def _spread(site_forces: Sequence[float], sites: Sequence[Sequence[tuple[int, float]]],
            n: int) -> list[float]:
    """Chain rule: a site at sum_w w y_atom passes the force w F_site to each atom."""
    f = [0.0] * n
    for fs, site in zip(site_forces, sites):
        for atom, w in site:
            f[atom] += w * fs
    return f


def additive(y: Sequence[float], q0: int, q1: int, p: Params = Params()) -> tuple[float, list[float]]:
    """Additive QM/MM with link atoms and mechanical embedding."""
    n = len(y)
    sites = model_sites(n, q0, q1, p.g)                                         # @line L1
    s = [sum(w * y[a] for a, w in site) for site in sites]
    e_qm, f_sites = qm_chain(s, p)                                              # @line L2
    f = _spread(f_sites, sites, n)                                              # @line L3
    mm = [(i, i + 1, p.k, p.d0) for i in range(n - 1) if not (q0 <= i and i + 1 < q1)]
    e_mm, f_mm = mm_bonds(y, mm, n)                                             # @line L4
    return e_qm + e_mm, [a + b for a, b in zip(f, f_mm)]                        # @line L5


def oniom(y: Sequence[float], q0: int, q1: int, p: Params = Params()) -> tuple[float, list[float]]:
    """Subtractive QM/MM (ONIOM): E_MM(real) + E_QM(model) - E_MM(model).

    In the model system, a bond to a link atom gets the MM parameters
    (k / g^2, g d0), so that its MM energy equals that of the cut bond.
    """
    n = len(y)
    sites = model_sites(n, q0, q1, p.g)
    s = [sum(w * y[a] for a, w in site) for site in sites]
    e_real, f_real = mm_bonds(y, [(i, i + 1, p.k, p.d0) for i in range(n - 1)], n)
    e_qm, f_qm = qm_chain(s, p)
    model_bonds = []
    for i in range(len(sites) - 1):
        link = len(sites[i]) == 2 or len(sites[i + 1]) == 2
        k, d0 = (p.k / p.g ** 2, p.g * p.d0) if link else (p.k, p.d0)
        model_bonds.append((i, i + 1, k, d0))
    e_low, f_low = mm_bonds(s, model_bonds, len(sites))
    f_model = _spread([a - b for a, b in zip(f_qm, f_low)], sites, n)
    return e_real + e_qm - e_low, [a + b for a, b in zip(f_real, f_model)]


def velocity_verlet(y: list[float], v: list[float], h: float, steps: int, q0: int, q1: int,
                    scheme=additive, p: Params = Params()) -> list[float]:
    """NVE run with unit masses; returns the total energy after each step."""
    e, f = scheme(y, q0, q1, p)
    energies = []
    for _ in range(steps):
        for i in range(len(y)):
            v[i] += 0.5 * h * f[i]
            y[i] += h * v[i]
        e, f = scheme(y, q0, q1, p)
        for i in range(len(y)):
            v[i] += 0.5 * h * f[i]
        energies.append(e + 0.5 * sum(vi * vi for vi in v))
    return energies
