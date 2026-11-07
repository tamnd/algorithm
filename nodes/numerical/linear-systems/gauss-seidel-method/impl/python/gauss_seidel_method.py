# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gauss-seidel-method/. The authors are listed in prov/2WJJ4E.jsonl.

"""The Gauss-Seidel iteration for A x = b, with A in compressed sparse row (CSR) form.

Each sweep overwrites x in place, so x_j for j < i is already new when row i is
processed. symmetric=True adds a backward sweep (symmetric Gauss-Seidel).
Only +, -, * and / are used, so the code also runs on fractions.Fraction.
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
class GSResult:
    x: list
    iterations: int
    converged: bool
    residual_norms: list = field(default_factory=list)


def _split(a: CSR):
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


def _relax(i, x, b, diag, off):
    s = 0 * b[0]
    for j, v in off[i]:
        s += v * x[j]  # @line L6
    x[i] = (b[i] - s) / diag[i]  # @line L7


def gauss_seidel(a, b, x0=None, tol=1e-10, maxit=1000, symmetric=False):
    """Run Gauss-Seidel sweeps until ||b - A x||_inf <= tol * ||b||_inf or maxit sweeps are done.

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
        ax = a.matvec(x) if n else []
        rnorm = max((abs(bi - vi) for bi, vi in zip(b, ax)), default=0)  # @line L2
        history.append(rnorm)
        if rnorm <= tol * bnorm:  # @line L3
            return GSResult(x, k, True, history)
        if k == maxit:  # @line L4
            return GSResult(x, k, False, history)
        for i in range(n):  # @line L5
            _relax(i, x, b, diag, off)
        if symmetric:
            for i in range(n - 1, -1, -1):
                _relax(i, x, b, diag, off)
    raise AssertionError("unreachable")
