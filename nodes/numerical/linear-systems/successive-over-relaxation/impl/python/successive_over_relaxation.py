# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/successive-over-relaxation/. The authors are listed in prov/MJSE1P.jsonl.

"""Successive over-relaxation (SOR) for A x = b, with A stored by sparse rows.

A matrix is a list of rows; row i is a list of (j, a_ij) pairs with a_ij != 0.
from_dense converts a list of lists. Entries may be floats or Fractions.
"""

import math
from fractions import Fraction
from typing import TypeVar

T = TypeVar("T", float, Fraction)

SparseRows = list[list[tuple[int, T]]]


class ZeroDiagonal(ValueError):
    """Raised when some a_ii is zero, so the SOR sweep is undefined."""


def from_dense(a: list[list[T]]) -> SparseRows:
    """Keep the nonzero entries of each row."""
    return [[(j, v) for j, v in enumerate(row) if v != 0] for row in a]


def residual(rows: SparseRows, b: list[T], x: list[T]) -> list[T]:
    """r = b - A x, in 2 nnz(A) flops."""
    return [b[i] - sum(v * x[j] for j, v in row) for i, row in enumerate(rows)]


def _diag(rows: SparseRows) -> list:
    d = []
    for i, row in enumerate(rows):
        aii = next((v for j, v in row if j == i), 0)
        if aii == 0:
            raise ZeroDiagonal("a[%d][%d] is zero" % (i, i))
        d.append(aii)
    return d


def sor_sweep(rows: SparseRows, b: list[T], x: list[T], omega: T, diag: list[T]) -> None:
    """One forward SOR sweep, in place: x_i <- (1 - omega) x_i + omega (b_i - sum_{j != i} a_ij x_j) / a_ii.

    Cost: 2 nnz(A) + 2n flops.
    """
    for i, row in enumerate(rows):  # @line L3
        s = b[i]
        for j, v in row:  # @line L4
            if j != i:
                s -= v * x[j]
        x[i] = (1 - omega) * x[i] + omega * s / diag[i]  # @line L5


def sor(rows: SparseRows, b: list[float], omega: float, x0: list[float] | None = None,
        tol: float = 1e-10, maxiter: int = 10000) -> tuple[list[float], int, bool]:
    """Run SOR sweeps until ||b - A x||_2 <= tol ||b||_2 or maxiter sweeps.

    Returns (x, sweeps, converged). Precondition: a_ii != 0 for all i (raises
    ZeroDiagonal). Converges for every x0 iff rho(G_omega) < 1; for symmetric
    positive definite A this holds exactly when 0 < omega < 2.
    Cost per sweep: 2 nnz(A) + 2n flops for the sweep and 2 nnz(A) + 2n for the residual test.
    """
    n = len(rows)
    diag = _diag(rows)
    x = list(x0) if x0 is not None else [0.0] * n  # @line L1
    nb = math.sqrt(sum(v * v for v in b))
    target = tol * (nb if nb > 0 else 1.0)
    for k in range(1, maxiter + 1):  # @line L2
        sor_sweep(rows, b, x, omega, diag)
        r = residual(rows, b, x)
        if math.sqrt(sum(v * v for v in r)) <= target:  # @line L6
            return x, k, True
    return x, maxiter, False  # @line L7


def optimal_omega(mu: float) -> float:
    """Young's optimal parameter 2 / (1 + sqrt(1 - mu^2)) for a consistently ordered matrix with rho(Jacobi) = mu < 1."""
    return 2.0 / (1.0 + math.sqrt(1.0 - mu * mu))


def sor_radius(mu: float, omega: float) -> float:
    """rho(G_omega) for a consistently ordered matrix with real Jacobi spectrum and rho(Jacobi) = mu < 1, 0 < omega < 2."""
    wopt = optimal_omega(mu)
    if omega >= wopt:
        return omega - 1.0
    t = omega * mu + math.sqrt(omega * omega * mu * mu - 4.0 * (omega - 1.0))
    return (t / 2.0) ** 2
