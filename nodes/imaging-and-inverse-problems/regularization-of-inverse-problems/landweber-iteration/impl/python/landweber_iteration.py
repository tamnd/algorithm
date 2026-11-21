# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/landweber-iteration/. The authors are listed in prov/G6JZZF.jsonl.
"""Landweber iteration for a linear equation A x = y with noisy data.

The step is x_{k+1} = x_k + omega A^T (y - A x_k) with 0 < omega < 2 / ||A||^2.
The operator is given as two functions, apply_a(x) = A x and
apply_at(r) = A^T r, so the same code runs on a dense matrix, on a sparse
projector or on a diagonal model. The iteration count k is the
regularization parameter; with a noise level delta the discrepancy
principle stops at the first k with ||y - A x_k|| <= tau delta.
"""

import math
from typing import Callable, List, Optional, Sequence

from imgla import matvec, rmatvec, norm2

Vector = List[float]
Operator = Callable[[Sequence[float]], Vector]


class LandweberResult:
    """x: the last iterate; k: the number of steps done; residuals: ||y - A x_j||
    for j = 0, ..., k; stopped: "discrepancy" or "maxit"."""

    def __init__(self, x: Vector, k: int, residuals: List[float], stopped: str) -> None:
        self.x, self.k, self.residuals, self.stopped = x, k, residuals, stopped


def landweber(apply_a: Operator, apply_at: Operator, y: Sequence[float], omega: float, kmax: int,
              x0: Optional[Sequence[float]] = None, delta: Optional[float] = None,
              tau: float = 1.01, n: Optional[int] = None) -> LandweberResult:
    """Run at most kmax Landweber steps from x0 (default 0).

    Precondition: 0 < omega < 2 / ||A||^2 (not checked here). If delta is
    given, stop at the first k with ||y - A x_k|| <= tau delta. n is the
    number of unknowns; it is needed only when x0 is None.
    Cost: per step one product with A, one with A^T and O(m + n) more.
    """
    if x0 is None:
        x = [0.0] * (n if n is not None else len(apply_at([0.0] * len(y))))  # @line L1
    else:
        x = list(x0)
    residuals = []
    for k in range(kmax):  # @line L2
        ax = apply_a(x)
        r = [yi - v for yi, v in zip(y, ax)]  # @line L3
        rn = norm2(r)
        residuals.append(rn)
        if delta is not None and rn <= tau * delta:  # @line L4
            return LandweberResult(x, k, residuals, "discrepancy")
        g = apply_at(r)
        x = [xi + omega * gi for xi, gi in zip(x, g)]  # @line L5
    r = [yi - v for yi, v in zip(y, apply_a(x))]
    residuals.append(norm2(r))
    if delta is not None and residuals[-1] <= tau * delta:
        return LandweberResult(x, kmax, residuals, "discrepancy")
    return LandweberResult(x, kmax, residuals, "maxit")  # @line L6


def landweber_matrix(a: List[List[float]], y: Sequence[float], omega: Optional[float] = None,
                     kmax: int = 100, x0: Optional[Sequence[float]] = None,
                     delta: Optional[float] = None, tau: float = 1.01) -> LandweberResult:
    """Landweber for a dense matrix A (a list of rows).

    The default step is omega = 1 / ||A||_F^2. The Frobenius norm is at least
    the spectral norm, so this step is always in (0, 2 / ||A||^2).
    Cost: O(m n) per step.
    """
    if omega is None:
        omega = 1.0 / sum(v * v for row in a for v in row)
    return landweber(lambda x: matvec(a, x), lambda r: rmatvec(a, r), y, omega, kmax,
                     x0=x0, delta=delta, tau=tau, n=len(a[0]))


def filter_factor(omega: float, sigma: float, k: int) -> float:
    """The Landweber filter factor 1 - (1 - omega sigma^2)^k (start x0 = 0)."""
    return 1.0 - (1.0 - omega * sigma * sigma) ** k


def error_bound(nu: float, rho: float, omega: float, k: int, delta: float) -> float:
    """The bound (nu / (omega k))^nu rho + sqrt(omega k) delta on ||x_k - x^dagger||.

    It holds for x0 = 0, omega ||A||^2 <= 1, k >= 1, the source condition
    x^dagger = (A^T A)^nu w with ||w|| <= rho, and ||y - y^delta|| <= delta.
    """
    return (nu / (omega * k)) ** nu * rho + math.sqrt(omega * k) * delta
