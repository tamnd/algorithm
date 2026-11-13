# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-chemistry-simulation/. The authors are listed in prov/184NCZ.jsonl.
"""The H2 molecule in the minimal STO-3G basis at R = 1.401 bohr, solved exactly in its 16-dimensional Fock space.

The molecular orbitals are g (bonding) and u (antibonding). The integrals in hartree
are those of Whitfield, Biamonte and Aspuru-Guzik (2011), Table 2. The spin orbital
(p, s) is the mode 2 p + s, with p = 0 for g, p = 1 for u, s = 0 for up and s = 1 for down.
"""

from qsim import eigvalsh, fermion_matrix

R = 1.401
H_CORE = {(0, 0): -1.252477, (1, 1): -0.475934}
# chemists' notation (pq|rs) for real orbitals; the integrals with an odd number of u are zero
ERI = {
    (0, 0, 0, 0): 0.674493,
    (1, 1, 1, 1): 0.697397,
    (0, 0, 1, 1): 0.663472,
    (1, 1, 0, 0): 0.663472,
    (0, 1, 0, 1): 0.181287,
    (0, 1, 1, 0): 0.181287,
    (1, 0, 0, 1): 0.181287,
    (1, 0, 1, 0): 0.181287,
}


def nuclear_repulsion(r: float = R) -> float:
    return 1.0 / r


def h2_terms() -> list:
    """H = sum h_pq a_p^dag a_q + 1/2 sum (pq|rs) a_p^dag a_r^dag a_s a_q over spin orbitals with matching spins."""
    terms = []
    for (p, q), h in H_CORE.items():
        for s in (0, 1):
            terms.append((h, ((2 * p + s, True), (2 * q + s, False))))
    for (p, q, r, t), v in ERI.items():
        for s1 in (0, 1):
            for s2 in (0, 1):
                i, j, k, l = 2 * p + s1, 2 * q + s1, 2 * r + s2, 2 * t + s2
                if i == k or j == l:
                    continue  # a_i^dag a_i^dag = 0
                terms.append((0.5 * v, ((i, True), (k, True), (l, False), (j, False))))
    return terms


def h2_matrix():
    return fermion_matrix(4, h2_terms())


def sector_energies(m, electrons: int, sz2: int) -> list[float]:
    """Eigenvalues on the states with the given electron count and 2 S_z = (up count) - (down count)."""
    idx = []
    for x in range(16):
        up = (x & 1) + (x >> 2 & 1)
        dn = (x >> 1 & 1) + (x >> 3 & 1)
        if up + dn == electrons and up - dn == sz2:
            idx.append(x)
    return eigvalsh([[m[a][b] for b in idx] for a in idx])


def hartree_fock_energy() -> float:
    """<g up, g down| H |g up, g down> = 2 h_gg + (gg|gg), the electronic energy of the closed-shell determinant."""
    return 2 * H_CORE[(0, 0)] + ERI[(0, 0, 0, 0)]


def two_by_two_ci() -> float:
    """The lowest root of [[2 h_gg + J_gg, K], [K, 2 h_uu + J_uu]] in the closed-shell singlet space."""
    a = hartree_fock_energy()
    b = 2 * H_CORE[(1, 1)] + ERI[(1, 1, 1, 1)]
    k = ERI[(0, 1, 0, 1)]
    return (a + b) / 2 - (((a - b) / 2) ** 2 + k * k) ** 0.5
