# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chebyshev-iteration/. The authors are listed in prov/3W6N6C.jsonl.

"""Chebyshev iteration for A x = b when the spectrum of A lies in [lmin, lmax], 0 < lmin.

Three-term form of Saad, Algorithm 12.1. No inner products are needed for
the iteration itself; the residual norm is computed only for the stopping
test, every `check` steps. Works with floats or fractions.Fraction.
Standard library only.
"""


class CSR:
    """Compressed sparse row matrix: row i holds data[ptr[i]:ptr[i+1]]."""

    def __init__(self, n, ptr, ind, data):
        self.n, self.ptr, self.ind, self.data = n, ptr, ind, data

    @classmethod
    def from_dense(cls, a):
        ptr, ind, data = [0], [], []
        for row in a:
            for j, v in enumerate(row):
                if v != 0:
                    ind.append(j)
                    data.append(v)
            ptr.append(len(ind))
        return cls(len(a), ptr, ind, data)

    def matvec(self, x):
        out = []
        for i in range(self.n):
            acc = 0 * x[0]
            for p in range(self.ptr[i], self.ptr[i + 1]):
                acc += self.data[p] * x[self.ind[p]]
            out.append(acc)
        return out


def _mv(a, x):
    if isinstance(a, CSR):
        return a.matvec(x)
    return [sum((aij * xj for aij, xj in zip(row, x)), 0 * x[0]) for row in a]


class ChebyshevResult:
    def __init__(self, x, converged, iterations, status):
        self.x = x
        self.converged = converged
        self.iterations = iterations
        self.status = status  # "converged", "maxit" or "diverged"


def chebyshev(a, b, lmin, lmax, x0=None, tol=1e-10, maxit=1000, check=1, trace=None):
    """Iterate until ||r||_2 <= tol ||b||_2 (squared norms are compared).

    trace, if a list, receives x_k for k = 0, 1, ... (for exact tests).
    Raises ValueError unless 0 < lmin <= lmax.
    """
    if not (0 < lmin <= lmax):
        raise ValueError("need 0 < lmin <= lmax; Chebyshev iteration needs a definite spectrum")
    n = len(b)
    zero = 0 * b[0]
    x = [zero] * n if x0 is None else list(x0)
    theta = (lmax + lmin) / 2  # @line L1
    delta = (lmax - lmin) / 2
    r = [bi - t for bi, t in zip(b, _mv(a, x))]  # @line L2
    d = [ri / theta for ri in r]
    if delta != 0:
        sigma = theta / delta
        rho = 1 / sigma
    bb = sum((t * t for t in b), zero)
    target = tol * tol * bb
    rr0 = sum((t * t for t in r), zero)
    if trace is not None:
        trace.append(list(x))
    for k in range(maxit + 1):  # @line L3
        if k % check == 0 or k == maxit:
            rr = sum((t * t for t in r), zero)
            if rr <= target:  # @line L4
                return ChebyshevResult(x, True, k, "converged")
            if rr > 1e12 * (rr0 + bb) and rr0 + bb > 0:
                return ChebyshevResult(x, False, k, "diverged")
        if k == maxit:
            break
        ad = _mv(a, d)  # @line L5
        x = [xi + di for xi, di in zip(x, d)]  # @line L6
        r = [ri - t for ri, t in zip(r, ad)]  # @line L7
        if trace is not None:
            trace.append(list(x))
        if delta == 0:
            d = [ri / theta for ri in r]
            continue
        rho_new = 1 / (2 * sigma - rho)  # @line L8
        d = [rho_new * rho * di + (2 * rho_new / delta) * ri for di, ri in zip(d, r)]  # @line L9
        rho = rho_new
    return ChebyshevResult(x, False, maxit, "maxit")
