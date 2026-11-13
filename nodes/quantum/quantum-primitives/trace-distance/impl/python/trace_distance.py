# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trace-distance/. The authors are listed in prov/GZQ3SX.jsonl.
"""Trace distance D(rho, sigma) = (1/2) ||rho - sigma||_1 and the measurement that attains it.

For a Hermitian matrix the trace norm is the sum of the absolute values of
its eigenvalues. Each function costs O(d^3) per Jacobi sweep for d x d input.
"""

from typing import Sequence

from qsim import Matrix, eigh, eigvalsh, matmul, outer, scale, sub, trace, zeros


def trace_norm_hermitian(a: Matrix) -> float:
    """||A||_1 = sum |lambda_i| for a Hermitian matrix A."""
    return sum(abs(x) for x in eigvalsh(a))


def trace_distance(rho: Matrix, sigma: Matrix) -> float:
    return 0.5 * trace_norm_hermitian(sub(rho, sigma))


def optimal_projector(rho: Matrix, sigma: Matrix) -> Matrix:
    """The projector P onto the positive eigenspace of rho - sigma. Tr(P (rho - sigma)) = D(rho, sigma)."""
    vals, vecs = eigh(sub(rho, sigma))
    d = len(rho)
    p = zeros(d)
    for k, lam in enumerate(vals):
        if lam > 0:
            col = [vecs[i][k] for i in range(d)]
            p = [[p[i][j] + x for j, x in enumerate(row)] for i, row in enumerate(outer(col, col))]
    return p


def helstrom_success(rho: Matrix, sigma: Matrix, prior: float = 0.5) -> float:
    """Best probability to name the state right, when rho has probability prior and sigma the rest.

    (1 + || prior rho - (1 - prior) sigma ||_1) / 2.
    """
    return 0.5 * (1 + trace_norm_hermitian(sub(scale(prior, rho), scale(1 - prior, sigma))))


def measured_success(rho: Matrix, sigma: Matrix, p: Matrix, prior: float = 0.5) -> float:
    """Success probability of the test: answer rho on outcome P, sigma on outcome I - P."""
    return prior * trace(matmul(p, rho)).real + (1 - prior) * (1 - trace(matmul(p, sigma)).real)


def total_variation(p: Sequence[float], q: Sequence[float]) -> float:
    """Classical total variation distance (1/2) sum |p_i - q_i|."""
    return 0.5 * sum(abs(a - b) for a, b in zip(p, q))
