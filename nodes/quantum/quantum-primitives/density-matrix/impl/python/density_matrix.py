# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/density-matrix/. The authors are listed in prov/1RRERC.jsonl.
"""Density matrices: build one from an ensemble, test the three conditions, and use it.

A matrix is a list of rows of complex numbers. Qubit 0 is the least significant
bit of a basis index (see qsim.py). Each function costs O(d^3) arithmetic
operations or less for a d x d matrix.
"""

from typing import List, Sequence, Tuple

from qsim import Matrix, X, Y, Z, add, dagger, eigvalsh, is_hermitian, matmul, outer, scale, trace, zeros


def from_ensemble(probs: Sequence[float], states: Sequence[Sequence[complex]]) -> Matrix:
    """rho = sum_i p_i |psi_i><psi_i|. Precondition: p_i >= 0, sum p_i = 1, unit vectors."""
    d = len(states[0])
    rho = zeros(d)
    for p, psi in zip(probs, states):
        rho = add(rho, scale(p, outer(psi, psi)))
    return rho


def is_density_matrix(rho: Matrix, tol: float = 1e-9) -> bool:
    """True when rho is Hermitian, has trace 1 and has no eigenvalue below -tol."""
    if not is_hermitian(rho, tol):
        return False
    if abs(trace(rho) - 1) > tol:
        return False
    return eigvalsh(rho)[0] >= -tol


def purity(rho: Matrix) -> float:
    """Tr(rho^2) = sum of |rho_ij|^2 for Hermitian rho. It lies in [1/d, 1]."""
    return sum(abs(x) ** 2 for row in rho for x in row)


def is_pure(rho: Matrix, tol: float = 1e-9) -> bool:
    """A density matrix is pure exactly when Tr(rho^2) = 1."""
    return abs(purity(rho) - 1) <= tol


def expectation(rho: Matrix, a: Matrix) -> float:
    """Tr(rho A) for a Hermitian observable A."""
    return trace(matmul(rho, a)).real


def outcome_probabilities(rho: Matrix, projectors: Sequence[Matrix]) -> List[float]:
    """Born rule p(m) = Tr(P_m rho) for projectors that sum to I."""
    return [trace(matmul(p, rho)).real for p in projectors]


def post_measurement(rho: Matrix, projector: Matrix) -> Tuple[float, Matrix]:
    """Probability p = Tr(P rho) and the state P rho P / p after outcome P (p > 0)."""
    p = trace(matmul(projector, rho)).real
    return p, scale(1 / p, matmul(matmul(projector, rho), projector))


def evolve(rho: Matrix, u: Matrix) -> Matrix:
    """U rho U^dagger."""
    return matmul(matmul(u, rho), dagger(u))


def bloch_vector(rho: Matrix) -> Tuple[float, float, float]:
    """(Tr rho X, Tr rho Y, Tr rho Z) for a 2 x 2 density matrix."""
    return expectation(rho, X), expectation(rho, Y), expectation(rho, Z)


def from_bloch(r: Sequence[float]) -> Matrix:
    """(I + r_x X + r_y Y + r_z Z) / 2. A density matrix exactly when |r| <= 1."""
    rx, ry, rz = r
    return [[(1 + rz) / 2, (rx - 1j * ry) / 2], [(rx + 1j * ry) / 2, (1 - rz) / 2]]
