# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/state-discrimination-problem/. The authors are listed in prov/YN47TX.jsonl.

"""Minimum-error (Helstrom) and unambiguous discrimination of two quantum states.

A state is a density matrix (a list of rows). The prior of rho is p and the
prior of sigma is 1 - p. A two-outcome measurement is given by the operator P
of the outcome "rho"; the other outcome is I - P.
"""

import math

from qsim import eigvalsh, inner, mat_add, matmul, outer, positive_part_projector, trace


def gamma(p, rho, sigma):
    """The Helstrom operator p rho - (1 - p) sigma."""
    return mat_add(rho, sigma, p, -(1 - p))


def trace_norm_hermitian(A):
    return sum(abs(v) for v in eigvalsh(A))


def helstrom_success(p, rho, sigma):
    """The best success probability (1 + ||p rho - (1 - p) sigma||_1) / 2."""
    return (1 + trace_norm_hermitian(gamma(p, rho, sigma))) / 2


def helstrom_measurement(p, rho, sigma):
    """The projector on the positive part of p rho - (1 - p) sigma: answer "rho" on it."""
    return positive_part_projector(gamma(p, rho, sigma))


def success_of(p, rho, sigma, P):
    """p Tr(P rho) + (1 - p) Tr((I - P) sigma)."""
    return (p * trace(matmul(P, rho)) + (1 - p) * (trace(sigma) - trace(matmul(P, sigma)))).real


def pure_helstrom_success(p, overlap):
    """The closed form for pure states with |<psi|phi>| = overlap."""
    return (1 + math.sqrt(1 - 4 * p * (1 - p) * overlap ** 2)) / 2


def unambiguous_povm(psi, phi):
    """The optimal unambiguous measurement of two pure qubit states with equal priors.

    Returns (E_psi, E_phi, E_fail). E_psi is proportional to the projector on the
    vector orthogonal to phi, so it never fires on phi, and the other way round.
    The success probability is 1 - |<psi|phi>| (Ivanovic, Dieks, Peres).
    """
    def perp(v):
        return [-complex(v[1]).conjugate(), complex(v[0]).conjugate()]

    c = 1 / (1 + abs(inner(psi, phi)))
    e_psi = [[c * x for x in row] for row in outer(perp(phi), perp(phi))]
    e_phi = [[c * x for x in row] for row in outer(perp(psi), perp(psi))]
    e_fail = [[(1 if i == j else 0) - e_psi[i][j] - e_phi[i][j] for j in range(2)] for i in range(2)]
    return e_psi, e_phi, e_fail
