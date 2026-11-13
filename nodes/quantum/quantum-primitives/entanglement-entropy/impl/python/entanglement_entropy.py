# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/entanglement-entropy/. The authors are listed in prov/VEC71F.jsonl.

"""Entanglement entropy of a pure state across a cut, from its Schmidt coefficients.

A pure state of n qubits is a list of 2^n amplitudes, with qubit 0 as the least
significant bit. The part A is a list of qubit numbers; B is the rest.
Entropies are in bits (logarithm to base 2).
"""

import math

from qsim import eigvalsh, entropy_of, reduced_density


def schmidt_coefficients(state, n, part_a):
    """The Schmidt coefficients lambda_1 >= lambda_2 >= ... > 0 across the cut A | B.

    They are the square roots of the nonzero eigenvalues of rho_A.
    """
    vals = eigvalsh(reduced_density(state, n, part_a))
    return sorted((math.sqrt(v) for v in vals if v > 1e-14), reverse=True)


def entanglement_entropy(state, n, part_a):
    """S(rho_A) = -sum lambda_i^2 log2 lambda_i^2."""
    return entropy_of([c * c for c in schmidt_coefficients(state, n, part_a)])


def renyi2_entropy(state, n, part_a):
    """S_2(rho_A) = -log2 Tr(rho_A^2), a lower bound on S(rho_A)."""
    rho = reduced_density(state, n, part_a)
    purity = sum(abs(rho[i][j]) ** 2 for i in range(len(rho)) for j in range(len(rho)))
    return -math.log2(purity)


def schmidt_rank(state, n, part_a):
    return len(schmidt_coefficients(state, n, part_a))
