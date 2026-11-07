# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/banded-matrix/. The authors are listed in prov/HE5FHC.jsonl.

"""A banded matrix in diagonal storage, with matvec, band LU and band LU with partial pivoting.

Entry a[i][j] with -q <= j - i <= p ... is kept in ab[q + i - j][j], so row d of `ab`
holds one diagonal: d = q is the main diagonal, d < q the superdiagonals, d > q the
subdiagonals. This is the LAPACK general band layout, written with 0-based indices.
Only +, -, * and / are used, so entries may be fractions.Fraction.
"""


class SingularMatrix(ValueError):
    pass


class BandedMatrix:
    """n by n matrix with a_ij = 0 whenever i - j > p or j - i > q."""

    def __init__(self, n, p, q, zero=0):
        if n < 0 or p < 0 or q < 0:
            raise ValueError("n, p and q must be nonnegative")
        self.n, self.p, self.q = n, p, q
        self.zero = zero
        self.ab = [[zero] * n for _ in range(p + q + 1)]

    @staticmethod
    def from_dense(a, p, q):
        n = len(a)
        zero = 0 * a[0][0] if n else 0
        m = BandedMatrix(n, p, q, zero)
        for i in range(n):
            for j in range(n):
                if a[i][j] != 0:
                    m.set(i, j, a[i][j])
        return m

    def in_band(self, i, j):
        return 0 <= i < self.n and 0 <= j < self.n and -self.q <= i - j <= self.p

    def get(self, i, j):
        if not (0 <= i < self.n and 0 <= j < self.n):
            raise IndexError((i, j))
        return self.ab[self.q + i - j][j] if self.in_band(i, j) else self.zero

    def set(self, i, j, v):
        if not self.in_band(i, j):
            if v != 0:
                raise ValueError(f"entry ({i}, {j}) lies outside the band")
            return
        self.ab[self.q + i - j][j] = v

    def to_dense(self):
        return [[self.get(i, j) for j in range(self.n)] for i in range(self.n)]

    def copy(self, q=None):
        """Copy, optionally with a wider upper bandwidth (room for fill from pivoting)."""
        m = BandedMatrix(self.n, self.p, self.q if q is None else q, self.zero)
        for i in range(self.n):
            for j in range(max(0, i - self.p), min(self.n, i + self.q + 1)):
                m.set(i, j, self.get(i, j))
        return m

    def matvec(self, x):
        """y = A x in 2 n (p + q + 1) flops at most."""
        n, p, q = self.n, self.p, self.q
        y = []
        for i in range(n):  # @line M1
            s = 0 * x[0]
            for j in range(max(0, i - p), min(n, i + q + 1)):  # @line M2
                s += self.ab[q + i - j][j] * x[j]  # @line M3
            y.append(s)
        return y

    def lu(self):
        """Band LU without pivoting. Returns a BandLU; raises SingularMatrix on a zero pivot."""
        w = self.copy()
        n, p, q = w.n, w.p, w.q
        for k in range(n):  # @line L1
            piv = w.get(k, k)
            if piv == 0:  # @line L2
                raise SingularMatrix(f"zero pivot at step {k}")
            for i in range(k + 1, min(k + p, n - 1) + 1):  # @line L3
                w.set(i, k, w.get(i, k) / piv)  # @line L4
            for j in range(k + 1, min(k + q, n - 1) + 1):  # @line L5
                ukj = w.get(k, j)
                for i in range(k + 1, min(k + p, n - 1) + 1):  # @line L6
                    w.set(i, j, w.get(i, j) - w.get(i, k) * ukj)  # @line L7
        return BandLU(w, None)  # @line L8

    def lu_pivoted(self):
        """Band LU with partial pivoting: P A = L U, with U of upper bandwidth p + q.

        The interchanges are recorded in piv and applied step by step in solve, as in LINPACK;
        the multipliers of step k stay in column k. Raises SingularMatrix if A is singular.
        """
        n, p, q = self.n, self.p, self.q
        w = self.copy(q=p + q)
        piv = []
        for k in range(n):
            last = min(k + p, n - 1)
            r = max(range(k, last + 1), key=lambda i: abs(w.get(i, k)))
            if w.get(r, k) == 0:
                raise SingularMatrix(f"no nonzero pivot in column {k}")
            piv.append(r)
            right = min(k + p + q, n - 1)
            if r != k:
                for j in range(k, right + 1):
                    a, b = w.get(k, j), w.get(r, j)
                    w.set(k, j, b)
                    w.set(r, j, a)
            for i in range(k + 1, last + 1):
                w.set(i, k, w.get(i, k) / w.get(k, k))
            for j in range(k + 1, right + 1):
                ukj = w.get(k, j)
                if ukj != 0:
                    for i in range(k + 1, last + 1):
                        w.set(i, j, w.get(i, j) - w.get(i, k) * ukj)
        return BandLU(w, piv)

    def check_invariant(self):
        assert len(self.ab) == self.p + self.q + 1
        assert all(len(row) == self.n for row in self.ab)
        # Slots of ab that do not correspond to matrix entries must hold zero.
        for d in range(self.p + self.q + 1):
            for j in range(self.n):
                i = d - self.q + j
                if not 0 <= i < self.n:
                    assert self.ab[d][j] == 0
        return True


class BandLU:
    """Factors stored in band form: multipliers below the diagonal, U on and above it."""

    def __init__(self, w, piv):
        self.w, self.piv = w, piv

    def solve(self, b):
        w, piv = self.w, self.piv
        n, p, q = w.n, w.p, w.q
        y = list(b)
        for k in range(n):  # @line S1
            if piv is not None and piv[k] != k:
                y[k], y[piv[k]] = y[piv[k]], y[k]
            for i in range(k + 1, min(k + p, n - 1) + 1):  # @line S2
                y[i] -= w.get(i, k) * y[k]
        x = [None] * n
        for i in range(n - 1, -1, -1):  # @line S3
            s = y[i]
            for j in range(i + 1, min(i + q, n - 1) + 1):
                s -= w.get(i, j) * x[j]
            x[i] = s / w.get(i, i)  # @line S4
        return x

    def lower(self):
        """Unit lower triangular L (no pivoting only), as a dense list of rows."""
        if self.piv is not None:
            raise ValueError("L is not formed explicitly for the pivoted factorization")
        n = self.w.n
        one = self.w.zero + 1
        return [[one if i == j else (self.w.get(i, j) if j < i else self.w.zero) for j in range(n)] for i in range(n)]

    def upper(self):
        n = self.w.n
        return [[self.w.get(i, j) if j >= i else self.w.zero for j in range(n)] for i in range(n)]
