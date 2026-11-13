# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fidelity/. The authors are listed in prov/N6ND1W.jsonl.
"""Fidelity of quantum states, in the convention F = Tr sqrt(sqrt(rho) sigma sqrt(rho)).

This is the convention of Nielsen and Chuang. The squared fidelity F^2 (the
convention of Jozsa 1994) is given by squared_fidelity. Each function costs
O(d^3) per Jacobi sweep for d x d input.
"""

import math
from typing import Sequence

from qsim import Matrix, dagger, eigh, inner, matmul, sqrtm_psd, trace


def fidelity(rho: Matrix, sigma: Matrix) -> float:
    """F(rho, sigma) = Tr sqrt(sqrt(rho) sigma sqrt(rho)), a number in [0, 1]."""
    s = sqrtm_psd(rho)
    return trace(sqrtm_psd(matmul(matmul(s, sigma), s))).real


def squared_fidelity(rho: Matrix, sigma: Matrix) -> float:
    """F^2, the convention of Jozsa and of Uhlmann's transition probability."""
    return fidelity(rho, sigma) ** 2


def trace_norm(m: Matrix) -> float:
    """||M||_1 = Tr sqrt(M^dagger M), the sum of the singular values of M."""
    return trace(sqrtm_psd(matmul(dagger(m), m))).real


def fidelity_by_trace_norm(rho: Matrix, sigma: Matrix) -> float:
    """F = || sqrt(rho) sqrt(sigma) ||_1."""
    return trace_norm(matmul(sqrtm_psd(rho), sqrtm_psd(sigma)))


def fidelity_pure(psi: Sequence[complex], phi: Sequence[complex]) -> float:
    """F(|psi><psi|, |phi><phi|) = |<psi|phi>|."""
    return abs(inner(psi, phi))


def fidelity_pure_mixed(psi: Sequence[complex], sigma: Matrix) -> float:
    """F(|psi><psi|, sigma) = sqrt(<psi|sigma|psi>)."""
    d = len(psi)
    v = [sum(sigma[i][j] * psi[j] for j in range(d)) for i in range(d)]
    return math.sqrt(max(0.0, inner(psi, v).real))


def qubit_squared_fidelity(rho: Matrix, sigma: Matrix) -> float:
    """For 2 x 2 states, F^2 = Tr(rho sigma) + 2 sqrt(det rho det sigma)."""

    def det(a: Matrix) -> float:
        return (a[0][0] * a[1][1] - a[0][1] * a[1][0]).real

    return trace(matmul(rho, sigma)).real + 2 * math.sqrt(max(0.0, det(rho)) * max(0.0, det(sigma)))


def classical_fidelity(p: Sequence[float], q: Sequence[float]) -> float:
    """The Bhattacharyya coefficient sum_i sqrt(p_i q_i), the fidelity of commuting states."""
    return sum(math.sqrt(a * b) for a, b in zip(p, q))


def canonical_purification(rho: Matrix) -> list:
    """(sqrt(rho) tensor I)|Omega> with |Omega> = sum_i |i>|i>; index system * d + reference."""
    d = len(rho)
    s = sqrtm_psd(rho)
    return [s[i][k] for i in range(d) for k in range(d)]


def spectral_purification(rho: Matrix) -> list:
    """sum_k sqrt(lambda_k) |e_k>|k>; index system * d + reference."""
    vals, vecs = eigh(rho)
    d = len(rho)
    return [math.sqrt(max(vals[k], 0.0)) * vecs[i][k] for i in range(d) for k in range(d)]
