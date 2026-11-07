# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jacobi-method/. The authors are listed in prov/R75FV5.jsonl.

"""The Jacobi iteration for A x = b, with A in compressed sparse row (CSR) form.

Every sweep computes the off-diagonal sums s_i from the old vector; the residual
comes from the same sums, so the stopping test is free. The arithmetic uses only
+, -, * and /, so the code also runs on fractions.Fraction.
"""

from dataclasses import dataclass, field


@dataclass
class CSR:
    """Row i holds the values data[indptr[i]:indptr[i+1]] in the columns indices[...]."""

    n: int
    indptr: list
    indices: list
    data: list

    @staticmethod
    def from_dense(a):
        indptr, indices, data = [0], [], []
        for row in a:
            for j, v in enumerate(row):
                if v != 0:
                    indices.append(j)
                    data.append(v)
            indptr.append(len(indices))
        return CSR(len(a), indptr, indices, data)

    def matvec(self, v):
        out = []
        for i in range(self.n):
            s = 0 * v[0]
            for p in range(self.indptr[i], self.indptr[i + 1]):
                s += self.data[p] * v[self.indices[p]]
            out.append(s)
        return out


@dataclass
class JacobiResult:
    x: list
    iterations: int
    converged: bool
    residual_norms: list = field(default_factory=list)


def _split(a: CSR):
    """Return the diagonal and, per row, the off-diagonal (column, value) pairs."""
    diag, off = [], []
    for i in range(a.n):
        d, row = 0, []
        for p in range(a.indptr[i], a.indptr[i + 1]):
            j, v = a.indices[p], a.data[p]
            if j == i:
                d += v
            else:
                row.append((j, v))
        if d == 0:
            raise ValueError(f"zero diagonal entry in row {i}")
        diag.append(d)
        off.append(row)
    return diag, off


def jacobi(a, b, x0=None, tol=1e-10, maxit=1000):
    """Run Jacobi sweeps until ||b - A x||_inf <= tol * ||b||_inf or maxit sweeps are done.

    `a` is a CSR matrix or a dense list of rows. Raises ValueError on a zero diagonal entry.
    """
    if not isinstance(a, CSR):
        a = CSR.from_dense(a)
    n = a.n
    if len(b) != n:
        raise ValueError("dimension mismatch")
    diag, off = _split(a)
    x = list(x0) if x0 is not None else [0 * b[0] for _ in range(n)]
    bnorm = max(abs(v) for v in b) if n else 0
    history = []
    for k in range(maxit + 1):  # @line L1
        s = [None] * n
        r = [None] * n
        for i in range(n):  # @line L2
            acc = 0 * b[0]
            for j, v in off[i]:
                acc += v * x[j]
            s[i] = acc  # @line L3
            r[i] = b[i] - acc - diag[i] * x[i]  # @line L4
        rnorm = max(abs(v) for v in r) if n else 0
        history.append(rnorm)
        if rnorm <= tol * bnorm:  # @line L5
            return JacobiResult(x, k, True, history)
        if k == maxit:  # @line L6
            return JacobiResult(x, k, False, history)
        x = [(b[i] - s[i]) / diag[i]  # @line L8
             for i in range(n)]  # @line L7
    raise AssertionError("unreachable")
