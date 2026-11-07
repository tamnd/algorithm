# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incomplete-lu-factorization/. The authors are listed in prov/YZPFA2.jsonl.

"""Incomplete LU factorization ILU(p) by levels of fill, in CSR form.

ILU(0) keeps exactly the sparsity pattern of A; ILU(p) keeps fill entries
of level at most p (Saad, Section 10.3). The row-wise IKJ variant is used.
Works with floats or fractions.Fraction. Standard library only.
"""

import heapq


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

    @classmethod
    def from_rows(cls, n, rows):
        """rows[i] is a dict column -> value."""
        ptr, ind, data = [0], [], []
        for i in range(n):
            for j in sorted(rows[i]):
                ind.append(j)
                data.append(rows[i][j])
            ptr.append(len(ind))
        return cls(n, ptr, ind, data)

    def row(self, i):
        return {self.ind[p]: self.data[p] for p in range(self.ptr[i], self.ptr[i + 1])}

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

    def nnz(self):
        return len(self.ind)


class ZeroPivot(ArithmeticError):
    pass


class ILU:
    """L (unit lower, strict part stored) and U (upper with diagonal) in CSR."""

    def __init__(self, lower, upper):
        self.L, self.U = lower, upper

    def solve(self, r):
        """Return (L U)^{-1} r by a forward and a backward sweep."""
        n = self.L.n
        y = list(r)
        lp, li, ld = self.L.ptr, self.L.ind, self.L.data
        for i in range(n):
            acc = y[i]
            for p in range(lp[i], lp[i + 1]):
                acc -= ld[p] * y[li[p]]
            y[i] = acc
        up, ui, ud = self.U.ptr, self.U.ind, self.U.data
        for i in range(n - 1, -1, -1):
            acc = y[i]
            diag = None
            for p in range(up[i], up[i + 1]):
                j = ui[p]
                if j == i:
                    diag = ud[p]
                else:
                    acc -= ud[p] * y[j]
            y[i] = acc / diag
        return y

    def nnz(self):
        return self.L.nnz() + self.U.nnz()


def ilu(a, p=0):
    """ILU(p) of the CSR matrix a. Raises ZeroPivot on a zero pivot u_kk."""
    n = a.n
    INF = float("inf")
    urows = []  # dict column -> value for row k of U (columns >= k)
    ulev = []  # level of each entry of U
    lrows = []
    for i in range(n):  # @line L1
        w = a.row(i)
        lev = {j: 0 for j in w}
        heap = [j for j in w if j < i]
        heapq.heapify(heap)
        done = set()
        while heap:  # @line L2
            k = heapq.heappop(heap)
            if k in done:
                continue
            done.add(k)
            if lev[k] > p:
                continue  # dropped entry: not used as a multiplier
            ukk = urows[k][k]
            if ukk == 0:
                raise ZeroPivot("zero pivot in row %d" % k)
            w[k] = w[k] / ukk  # @line L3
            lik, levk = w[k], lev[k]
            for j, ukj in urows[k].items():  # @line L4
                if j <= k:
                    continue
                newlev = levk + ulev[k][j] + 1
                if j in w:
                    w[j] -= lik * ukj  # @line L5
                    if newlev < lev[j]:
                        lev[j] = newlev
                elif p > 0:  # @line L6
                    # fill (level >= 1, so never kept by ILU(0)); dropped in L7
                    # if its final level exceeds p
                    w[j] = -lik * ukj
                    lev[j] = newlev
                    if j < i:
                        heapq.heappush(heap, j)
        lrow = {j: v for j, v in w.items() if j < i and lev[j] <= p}  # @line L7
        urow = {j: v for j, v in w.items() if j >= i and lev[j] <= p}
        if i not in urow or urow[i] == 0:
            raise ZeroPivot("zero pivot in row %d" % i)
        lrows.append(lrow)
        urows.append(urow)
        ulev.append({j: lev[j] for j in urow})
    return ILU(CSR.from_rows(n, lrows), CSR.from_rows(n, urows))
