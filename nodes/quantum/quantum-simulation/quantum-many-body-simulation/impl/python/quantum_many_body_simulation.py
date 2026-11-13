# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-many-body-simulation/. The authors are listed in prov/TMRF7Z.jsonl.
"""Small instances of the three standard lattice models, solved by exact diagonalization.

These are reference answers for tiny sizes: the matrices have 2^n rows, so the method
fails beyond a few tens of sites. That growth is the reason for the quantum algorithms.
"""

from qsim import eigvalsh, fermion_matrix, pauli_on, qop_add, qop_matrix


def heisenberg(n: int, j: float, periodic: bool = True) -> dict:
    """H = J sum S_x . S_{x+1} with S = sigma / 2, on a chain or a ring of n spins."""
    h: dict = {}
    bonds = [(x, (x + 1) % n) for x in range(n if periodic else n - 1)]
    for x, y in bonds:
        h = qop_add(h, {pauli_on(n, {x: p, y: p}): j / 4 for p in "XYZ"})
    return h


def transverse_field_ising(n: int, j: float, g: float, periodic: bool = True) -> dict:
    """H = -J sum Z_x Z_{x+1} - g sum X_x."""
    h: dict = {}
    bonds = [(x, (x + 1) % n) for x in range(n if periodic else n - 1)]
    for x, y in bonds:
        h = qop_add(h, {pauli_on(n, {x: "Z", y: "Z"}): -j})
    for x in range(n):
        h = qop_add(h, {pauli_on(n, {x: "X"}): -g})
    return h


def hubbard_chain_terms(sites: int, t: float, u: float) -> list:
    """H = -t sum_<ij>,s (a_is^dag a_js + h.c.) + U sum_i n_i,up n_i,down on an open chain.

    The spin orbital (i, s) is the mode 2 i + s, with s = 0 for up and s = 1 for down.
    """
    terms = []
    for i in range(sites - 1):
        for s in (0, 1):
            p, q = 2 * i + s, 2 * (i + 1) + s
            terms += [(-t, ((p, True), (q, False))), (-t, ((q, True), (p, False)))]
    for i in range(sites):
        up, dn = 2 * i, 2 * i + 1
        terms.append((u, ((up, True), (up, False), (dn, True), (dn, False))))
    return terms


def sector(m, n_modes, keep):
    """The block of m on the basis states x with keep(x) true."""
    idx = [x for x in range(1 << n_modes) if keep(x)]
    return [[m[a][b] for b in idx] for a in idx]


def hubbard_dimer_spectrum(t: float, u: float) -> list[float]:
    """The energies of the 2-site Hubbard model with one up and one down electron."""
    h = fermion_matrix(4, hubbard_chain_terms(2, t, u))
    up = lambda x: (x & 1) + (x >> 2 & 1)  # modes 0 and 2
    dn = lambda x: (x >> 1 & 1) + (x >> 3 & 1)  # modes 1 and 3
    return eigvalsh(sector(h, 4, lambda x: up(x) == 1 and dn(x) == 1))


def ground_energy(h: dict, n: int) -> float:
    return eigvalsh(qop_matrix(h, n))[0]
