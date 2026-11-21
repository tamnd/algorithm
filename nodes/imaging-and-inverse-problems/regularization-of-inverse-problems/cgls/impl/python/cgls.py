# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cgls/. The authors are listed in prov/83ANX4.jsonl.
"""CGLS: the conjugate gradient method on the normal equations A^T A x = A^T y.

The iterate x_k minimizes ||y - A x|| over x0 + K_k(A^T A, A^T r_0), but the
method never forms A^T A. It needs one product with A and one with A^T per
step. The step count k is the regularization parameter; with a noise level
delta the discrepancy principle stops at the first k with
||y - A x_k|| <= tau delta.

The loop takes no square roots: the stop test compares squared norms. So the
code runs in exact Fraction arithmetic if the operator and the data are
Fractions, and then it gives the exact Krylov solutions.
"""

from typing import Any, Callable, List, Optional, Sequence

from imgla import matvec, rmatvec

Vector = List[Any]
Operator = Callable[[Sequence[Any]], Vector]


def _sq(v: Sequence[Any]) -> Any:
    return sum(t * t for t in v)


class CGLSResult:
    """x: the last iterate; k: the number of steps done; iterates: x_0, ..., x_k;
    res2: ||y - A x_j||^2 for j = 0, ..., k; stopped: "discrepancy", "breakdown"
    (A^T r = 0, so x_k is a least squares solution) or "maxit"."""

    def __init__(self, x: Vector, k: int, iterates: List[Vector], res2: List[Any], stopped: str) -> None:
        self.x, self.k, self.iterates, self.res2, self.stopped = x, k, iterates, res2, stopped


def cgls(apply_a: Operator, apply_at: Operator, y: Sequence[Any], kmax: int,
         x0: Optional[Sequence[Any]] = None, delta: Optional[Any] = None, tau: Any = 1.01,
         n: Optional[int] = None) -> CGLSResult:
    """Run at most kmax CGLS steps from x0 (default 0).

    Precondition: apply_at is the adjoint of apply_a. If delta is given, stop
    at the first k with ||y - A x_k|| <= tau delta. n is the number of
    unknowns; it is needed only when x0 is None and apply_at cannot tell it.
    Cost: per step one product with A, one with A^T and O(m + n) more; the
    iterates list takes O(k n) space.
    """
    if x0 is None:
        size = n if n is not None else len(apply_at([0 * t for t in y]))
        x = [0 * y[0]] * size
    else:
        x = list(x0)
    r = [yi - v for yi, v in zip(y, apply_a(x))]
    s = apply_at(r)
    p = list(s)
    gamma = _sq(s)  # @line L1
    rr = _sq(r)
    iterates, res2 = [list(x)], [rr]
    for k in range(kmax):  # @line L2
        if delta is not None and rr <= (tau * delta) ** 2:  # @line L3
            return CGLSResult(x, k, iterates, res2, "discrepancy")
        if gamma == 0:  # @line L4
            return CGLSResult(x, k, iterates, res2, "breakdown")
        q = apply_a(p)  # @line L5
        alpha = gamma / _sq(q)  # @line L6
        x = [xi + alpha * pi for xi, pi in zip(x, p)]  # @line L7
        r = [ri - alpha * qi for ri, qi in zip(r, q)]  # @line L8
        s = apply_at(r)  # @line L9
        gamma_new = _sq(s)
        beta = gamma_new / gamma  # @line L10
        gamma = gamma_new
        p = [si + beta * pi for si, pi in zip(s, p)]  # @line L11
        rr = _sq(r)
        iterates.append(list(x))
        res2.append(rr)
    if delta is not None and rr <= (tau * delta) ** 2:
        return CGLSResult(x, kmax, iterates, res2, "discrepancy")
    return CGLSResult(x, kmax, iterates, res2, "maxit")  # @line L12


def cgls_matrix(a: List[List[float]], y: Sequence[float], kmax: int,
                x0: Optional[Sequence[float]] = None, delta: Optional[float] = None,
                tau: float = 1.01) -> CGLSResult:
    """CGLS for a dense matrix A (a list of rows of floats). Cost: O(m n) per step."""
    return cgls(lambda x: matvec(a, x), lambda r: rmatvec(a, r), y, kmax,
                x0=x0, delta=delta, tau=tau, n=len(a[0]))


def ritz_filter_factor(sigma: float, ritz: Sequence[float]) -> float:
    """The CGLS filter factor 1 - prod_j (1 - sigma^2 / theta_j) for x0 = 0.

    ritz holds the k Ritz values theta_j of A^T A on K_k(A^T A, A^T y).
    """
    f = 1.0
    for theta in ritz:
        f *= 1.0 - sigma * sigma / theta
    return 1.0 - f
