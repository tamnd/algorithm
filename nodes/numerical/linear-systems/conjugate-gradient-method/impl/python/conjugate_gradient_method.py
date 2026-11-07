# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conjugate-gradient-method/. The authors are listed in prov/QAMAC5.jsonl.

"""The conjugate gradient method of Hestenes and Stiefel, with an optional preconditioner.

The matrix is given as a function v -> A v, so dense and sparse matrices both work.
Helpers build that function from a dense list of rows or from CSR arrays.
The code uses only +, -, * and /, so it also runs on fractions.Fraction (exact arithmetic).
"""

from dataclasses import dataclass, field
from typing import Callable, Sequence

Vector = list
MatVec = Callable[[Vector], Vector]


def dot(u: Sequence, v: Sequence):
    s = 0 * u[0] if u else 0
    for a, b in zip(u, v):
        s += a * b
    return s


def dense_matvec(a: list[list]) -> MatVec:
    """Return v -> A v for a dense matrix stored as a list of rows."""
    return lambda v: [dot(row, v) for row in a]


@dataclass
class CSR:
    """Compressed sparse row storage: row i holds data[indptr[i]:indptr[i+1]] in columns indices[...]."""

    n: int
    indptr: list[int]
    indices: list[int]
    data: list

    @staticmethod
    def from_dense(a: list[list]) -> "CSR":
        indptr, indices, data = [0], [], []
        for row in a:
            for j, v in enumerate(row):
                if v != 0:
                    indices.append(j)
                    data.append(v)
            indptr.append(len(indices))
        return CSR(len(a), indptr, indices, data)

    def matvec(self, v: Vector) -> Vector:
        out = []
        for i in range(self.n):
            s = 0 * v[0]
            for k in range(self.indptr[i], self.indptr[i + 1]):
                s += self.data[k] * v[self.indices[k]]
            out.append(s)
        return out


@dataclass
class CGResult:
    x: Vector
    iterations: int
    converged: bool
    rho_history: list = field(default_factory=list)  # r_k^T r_k for k = 0, 1, ...


class NotPositiveDefinite(ValueError):
    """Raised when p^T A p <= 0 at line L5."""


def conjugate_gradient(matvec: MatVec, b: Vector, x0: Vector | None = None, tol=1e-10,
                       maxit: int | None = None, precond: MatVec | None = None) -> CGResult:
    """Solve A x = b for symmetric positive definite A, given v -> A v.

    Stops when r^T r <= tol^2 b^T b (with a preconditioner M: when r^T M^-1 r <= tol^2 b^T M^-1 b).
    Precondition: A (and M if given) symmetric positive definite; len(b) = n >= 1.
    Cost per step: one matvec, two inner products, three vector updates; Theta(n) extra space.
    In exact arithmetic it converges in at most n steps; maxit defaults to 10 n.
    """
    n = len(b)
    if maxit is None:
        maxit = 10 * n
    x = list(x0) if x0 is not None else [0 * b[0] for _ in range(n)]
    ax = matvec(x)
    r = [bi - ai for bi, ai in zip(b, ax)]  # @line L1
    z = precond(r) if precond else r
    p = list(z)
    rho = dot(r, z)
    bb = dot(b, precond(b)) if precond else dot(b, b)
    hist = [rho]
    for k in range(maxit):  # @line L2
        if rho <= tol * tol * bb:  # @line L3
            return CGResult(x, k, True, hist)
        q = matvec(p)  # @line L4
        pq = dot(p, q)
        if pq <= 0:
            raise NotPositiveDefinite("p^T A p = %r at step %d" % (pq, k))
        alpha = rho / pq  # @line L5
        x = [xi + alpha * pi for xi, pi in zip(x, p)]  # @line L6
        r = [ri - alpha * qi for ri, qi in zip(r, q)]  # @line L7
        z = precond(r) if precond else r
        rho_new = dot(r, z)  # @line L8
        beta = rho_new / rho  # @line L9
        rho = rho_new
        hist.append(rho)
        p = [zi + beta * pi for zi, pi in zip(z, p)]  # @line L10
    return CGResult(x, maxit, rho <= tol * tol * bb, hist)  # @line L11
