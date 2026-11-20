# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ewald-summation/. The authors are listed in prov/674E3C.jsonl.
"""Ewald summation of the Coulomb energy and forces of point charges in a cubic periodic box.

Units are Gaussian: the energy of two charges at distance r is q_i q_j / r.
The splitting parameter alpha has the unit 1 / length. The energy is

    E = E_real + E_rec + E_self + E_surf,
    E_real = sum over pairs and images |r_ij + n L| < r_c of q_i q_j erfc(alpha d) / d,
    E_rec  = (2 pi / V) sum over k != 0 of exp(-k^2 / (4 alpha^2)) / k^2 |S(k)|^2,
    S(k)   = sum_j q_j exp(i k . r_j),  k = 2 pi m / L for integer vectors m,
    E_self = -(alpha / sqrt(pi)) sum_i q_i^2,
    E_surf = 0 for tin foil (conducting) boundary conditions, or
             (2 pi / (3 V)) |sum_i q_i r_i|^2 for a vacuum outside a large sphere.

The system must be neutral. Cost: the real-space loop visits the pairs and
images inside r_c, and the reciprocal loop costs Theta(N) for each of the
O(m_max^3) wave vectors.
"""

import math

Vec = list[float]


def ewald(
    q: list[float], pos: list[Vec], box: float, alpha: float, rc: float,
    mmax: int, surface: str = "tinfoil",
) -> tuple[float, list[Vec], dict]:
    """Ewald energy, forces and the parts of the energy for a neutral system in a cubic box."""
    n = len(q)
    if abs(sum(q)) > 1e-12 * max(1.0, sum(abs(x) for x in q)):
        raise ValueError("the system must be neutral")
    vol = box ** 3  # @line L1
    f = [[0.0, 0.0, 0.0] for _ in range(n)]
    # real-space sum over pairs i < j and over the images of each pair; i = j only for n != 0
    e_real = 0.0
    nimg = int(math.ceil(rc / box)) + 1
    rc2 = rc * rc
    two_a_sqrtpi = 2.0 * alpha / math.sqrt(math.pi)
    for i in range(n):  # @line L2
        for j in range(i, n):
            d0 = [pos[i][a] - pos[j][a] for a in range(3)]
            d0 = [x - box * round(x / box) for x in d0]
            for nx in range(-nimg, nimg + 1):
                for ny in range(-nimg, nimg + 1):
                    for nz in range(-nimg, nimg + 1):
                        if i == j and nx == 0 and ny == 0 and nz == 0:
                            continue
                        d = [d0[0] + nx * box, d0[1] + ny * box, d0[2] + nz * box]
                        r2 = d[0] * d[0] + d[1] * d[1] + d[2] * d[2]
                        if r2 >= rc2:
                            continue
                        r = math.sqrt(r2)
                        w = 0.5 if i == j else 1.0
                        e_real += w * q[i] * q[j] * math.erfc(alpha * r) / r  # @line L3
                        if i != j:
                            # -dU/dr / r for U = q_i q_j erfc(alpha r) / r
                            g = q[i] * q[j] * (math.erfc(alpha * r) / r + two_a_sqrtpi * math.exp(-alpha * alpha * r2)) / r2
                            for a in range(3):  # @line L4
                                f[i][a] += g * d[a]
                                f[j][a] -= g * d[a]
    # reciprocal sum over a half space of m (k and -k give the same term)
    e_rec = 0.0
    tpl = 2.0 * math.pi / box
    for mx in range(0, mmax + 1):  # @line L5
        for my in range(-mmax, mmax + 1):
            for mz in range(-mmax, mmax + 1):
                if (mx, my, mz) <= (0, 0, 0):  # keep one of each pair m, -m
                    continue
                if mx * mx + my * my + mz * mz > mmax * mmax:
                    continue
                k = (tpl * mx, tpl * my, tpl * mz)
                k2 = k[0] * k[0] + k[1] * k[1] + k[2] * k[2]
                gk = math.exp(-k2 / (4.0 * alpha * alpha)) / k2
                cs = [math.cos(k[0] * p[0] + k[1] * p[1] + k[2] * p[2]) for p in pos]
                sn = [math.sin(k[0] * p[0] + k[1] * p[1] + k[2] * p[2]) for p in pos]
                sre = sum(qj * c for qj, c in zip(q, cs))  # @line L6
                sim = sum(qj * s for qj, s in zip(q, sn))
                e_rec += 2.0 * (2.0 * math.pi / vol) * gk * (sre * sre + sim * sim)  # @line L7
                for i in range(n):
                    # Im(exp(i k.r_i) S*) = sin_i Re S - cos_i Im S
                    c = 2.0 * (4.0 * math.pi / vol) * q[i] * gk * (sn[i] * sre - cs[i] * sim)
                    for a in range(3):  # @line L8
                        f[i][a] += c * k[a]
    e_self = -alpha / math.sqrt(math.pi) * sum(x * x for x in q)  # @line L9
    e_surf = 0.0
    if surface == "vacuum":  # @line L10
        dip = [sum(q[i] * pos[i][a] for i in range(n)) for a in range(3)]
        e_surf = 2.0 * math.pi / (3.0 * vol) * sum(x * x for x in dip)
        for i in range(n):
            for a in range(3):
                f[i][a] -= 4.0 * math.pi / (3.0 * vol) * q[i] * dip[a]
    elif surface != "tinfoil":
        raise ValueError("surface must be 'tinfoil' or 'vacuum'")
    parts = {"real": e_real, "rec": e_rec, "self": e_self, "surf": e_surf}
    return e_real + e_rec + e_self + e_surf, f, parts  # @line L11


def nacl_cell(a: float = 1.0) -> tuple[list[float], list[Vec], float]:
    """The conventional cubic cell of rock salt: 8 ions, nearest-neighbour distance a, box 2a."""
    q, pos = [], []
    for ix in range(2):
        for iy in range(2):
            for iz in range(2):
                pos.append([ix * a, iy * a, iz * a])
                q.append(1.0 if (ix + iy + iz) % 2 == 0 else -1.0)
    return q, pos, 2.0 * a


def madelung_nacl(alpha: float = 2.5, rc: float = 2.5, mmax: int = 9) -> float:
    """The Madelung constant of NaCl from the Ewald energy: E = -(N / 2) M q^2 / a."""
    q, pos, box = nacl_cell(1.0)
    e, _, _ = ewald(q, pos, box, alpha, rc, mmax)
    return -e / (len(q) / 2)
