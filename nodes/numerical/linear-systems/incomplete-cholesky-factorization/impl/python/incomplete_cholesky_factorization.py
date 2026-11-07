# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incomplete-cholesky-factorization/. The authors are listed in prov/19QPY7.jsonl.

"""Zero fill incomplete Cholesky factorization IC(0), with an optional shift.

A is a symmetric CSR matrix (both triangles stored). The factor L is lower
triangular with the pattern of the lower triangle of A and satisfies
(L L^T)_ij = a_ij on that pattern. Row (up-looking) form. A diagonal shift
alpha factors A + alpha diag(A) instead (Manteuffel 1980). Standard
library only; with sqrt_fn the code also runs on exact square numbers.
"""

import math


class CSR:
    """Compressed sparse row matrix with sorted column indices per row."""

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

    def to_dense(self):
        z = 0 * self.data[0] if self.data else 0
        out = [[z] * self.n for _ in range(self.n)]
        for i in range(self.n):
            for p in range(self.ptr[i], self.ptr[i + 1]):
                out[i][self.ind[p]] = self.data[p]
        return out


class Breakdown(ArithmeticError):
    """A nonpositive pivot appeared: A is not SPD, or IC(0) fails for it."""

    def __init__(self, row, value):
        super().__init__("nonpositive pivot %r in row %d" % (value, row))
        self.row, self.value = row, value


class IC:
    def __init__(self, lower):
        self.L = lower  # CSR, lower triangular with diagonal last in each row

    def solve(self, r):
        """(L L^T)^{-1} r: forward sweep with L, backward sweep with L^T."""
        n = self.L.n
        lp, li, ld = self.L.ptr, self.L.ind, self.L.data
        y = list(r)
        for i in range(n):
            acc = y[i]
            for p in range(lp[i], lp[i + 1] - 1):
                acc -= ld[p] * y[li[p]]
            y[i] = acc / ld[lp[i + 1] - 1]
        for i in range(n - 1, -1, -1):
            y[i] = y[i] / ld[lp[i + 1] - 1]
            yi = y[i]
            for p in range(lp[i], lp[i + 1] - 1):
                y[li[p]] -= ld[p] * yi
        return y


def ic0(a, shift=0, sqrt_fn=math.sqrt):
    """IC(0) of a symmetric CSR matrix. Raises Breakdown on a pivot <= 0."""
    n = a.n
    rows = []  # rows[i] = dict column -> l_ij for j <= i
    for i in range(n):  # @line L1
        lower = [(a.ind[p], a.data[p]) for p in range(a.ptr[i], a.ptr[i + 1]) if a.ind[p] <= i]
        row = {}
        diag = 0 * a.data[0]
        for j, aij in lower:  # @line L2
            if j == i:
                diag = aij * (1 + shift)
                continue
            rj = rows[j]
            s = aij
            # sum over k < j in the patterns of both rows i and j
            small, big = (row, rj) if len(row) < len(rj) else (rj, row)
            for k, v in small.items():  # @line L3
                if k < j and k in big:
                    s -= v * big[k]
            row[j] = s / rj[j]  # @line L4
        d = diag - sum((v * v for v in row.values()), 0 * diag)  # @line L5
        if d <= 0:  # @line L6
            raise Breakdown(i, d)
        row[i] = sqrt_fn(d)  # @line L7
        rows.append(row)
    ptr, ind, data = [0], [], []
    for row in rows:
        for j in sorted(row):
            ind.append(j)
            data.append(row[j])
        ptr.append(len(ind))
    return IC(CSR(n, ptr, ind, data))
