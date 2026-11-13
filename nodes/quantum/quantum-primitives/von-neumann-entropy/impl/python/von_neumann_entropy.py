# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/von-neumann-entropy/. The authors are listed in prov/AFM9DC.jsonl.
"""Von Neumann entropy S(rho) = -Tr(rho log rho), in bits unless a base is given.

S is the Shannon entropy of the eigenvalues of rho, with 0 log 0 = 0. The
eigenvalues come from the Jacobi method of qsim.py, O(d^3) per sweep.
"""

import math
from typing import Sequence

from qsim import Matrix, eigvalsh, matmul, matrix_function, trace, trace_out_first, trace_out_second

CUTOFF = 1e-15  # eigenvalues below this count as 0, so that 0 log 0 = 0


def shannon_entropy(p: Sequence[float], base: float = 2.0) -> float:
    return -sum(x * math.log(x, base) for x in p if x > CUTOFF)


def von_neumann_entropy(rho: Matrix, base: float = 2.0) -> float:
    """-sum lambda log lambda over the eigenvalues of rho."""
    return shannon_entropy(eigvalsh(rho), base)


def binary_entropy(x: float) -> float:
    return shannon_entropy([x, 1 - x])


def qubit_entropy(rho: Matrix) -> float:
    """h((1 + |r|) / 2) for a qubit state with Bloch vector r. The eigenvalues are (1 +- |r|) / 2."""
    det = (rho[0][0] * rho[1][1] - rho[0][1] * rho[1][0]).real
    r = math.sqrt(max(0.0, 1 - 4 * det))  # |r|^2 = 1 - 4 det rho
    return binary_entropy((1 + r) / 2)


def relative_entropy(rho: Matrix, sigma: Matrix, base: float = 2.0) -> float:
    """S(rho || sigma) = Tr rho (log rho - log sigma), for sigma of full rank."""
    log_rho = matrix_function(rho, lambda x: math.log(x, base) if x > CUTOFF else 0.0)
    log_sigma = matrix_function(sigma, lambda x: math.log(x, base))
    return (trace(matmul(rho, log_rho)) - trace(matmul(rho, log_sigma))).real


def conditional_entropy(rho_ab: Matrix, da: int, db: int) -> float:
    """S(A | B) = S(AB) - S(B). It is negative for some entangled states."""
    return von_neumann_entropy(rho_ab) - von_neumann_entropy(trace_out_first(rho_ab, da, db))


def mutual_information(rho_ab: Matrix, da: int, db: int) -> float:
    """I(A : B) = S(A) + S(B) - S(AB) >= 0."""
    s_a = von_neumann_entropy(trace_out_second(rho_ab, da, db))
    s_b = von_neumann_entropy(trace_out_first(rho_ab, da, db))
    return s_a + s_b - von_neumann_entropy(rho_ab)
