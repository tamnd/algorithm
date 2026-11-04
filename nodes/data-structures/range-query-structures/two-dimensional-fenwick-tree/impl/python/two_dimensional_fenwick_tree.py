# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-dimensional-fenwick-tree/. The authors are listed in prov/RNZB8E.jsonl.

from collections.abc import Sequence


def _low(i: int) -> int:
    """Return the lowest set bit of i > 0, written g(i) on the page."""
    return i & -i


class FenwickTree2D:
    """A two-dimensional Fenwick tree over an n x m integer matrix.

    The table f is 1-indexed with f[0][*] and f[*][0] unused. The cell f[i][j]
    holds the sum of M over the rows (i - g(i), i] and the columns
    (j - g(j), j], in 1-indexed form, where g(i) is the lowest set bit of i.
    Build takes O(nm) time; add, prefix and query take O(log n log m) time.
    Public methods use 0-indexed rows and columns.
    """

    def __init__(self, matrix: Sequence[Sequence[int]]) -> None:
        self.n = len(matrix)
        self.m = len(matrix[0]) if self.n else 0
        n, m = self.n, self.m
        f = [[0] * (m + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):  # @line L1
            row = matrix[i - 1]
            if len(row) != m:
                raise ValueError("all rows must have the same length")
            for j in range(1, m + 1):
                f[i][j] = row[j - 1]
        for i in range(1, n + 1):  # @line L2
            for j in range(1, m + 1):
                p = j + _low(j)
                if p <= m:  # @line L3
                    f[i][p] += f[i][j]
        for i in range(1, n + 1):  # @line L4
            p = i + _low(i)
            if p <= n:  # @line L5
                fp, fi = f[p], f[i]
                for j in range(1, m + 1):
                    fp[j] += fi[j]
        self.f = f

    def add(self, r: int, c: int, delta: int) -> None:
        """Add delta to M[r][c], for 0 <= r < n and 0 <= c < m."""
        if not (0 <= r < self.n and 0 <= c < self.m):
            raise IndexError("cell out of range")
        i = r + 1  # @line L6
        while i <= self.n:  # @line L7
            j = c + 1  # @line L8
            row = self.f[i]
            while j <= self.m:  # @line L9
                row[j] += delta  # @line L10
                j += _low(j)  # @line L11
            i += _low(i)  # @line L12

    def prefix(self, r: int, c: int) -> int:
        """Return the sum of M over the rows 0..r-1 and the columns 0..c-1."""
        if not (0 <= r <= self.n and 0 <= c <= self.m):
            raise IndexError("prefix out of range")
        s = 0  # @line L13
        i = r
        while i > 0:  # @line L14
            j = c  # @line L15
            row = self.f[i]
            while j > 0:  # @line L16
                s += row[j]  # @line L17
                j -= _low(j)  # @line L18
            i -= _low(i)  # @line L19
        return s  # @line L20

    def query(self, r1: int, c1: int, r2: int, c2: int) -> int:
        """Return the sum of M[r][c] for r1 <= r <= r2 and c1 <= c <= c2.

        An empty rectangle (r1 = r2 + 1 or c1 = c2 + 1) gives 0.
        """
        if not (0 <= r1 <= r2 + 1 <= self.n and 0 <= c1 <= c2 + 1 <= self.m):
            raise IndexError("rectangle out of range")
        return (  # @line L21
            self.prefix(r2 + 1, c2 + 1)
            - self.prefix(r1, c2 + 1)
            - self.prefix(r2 + 1, c1)
            + self.prefix(r1, c1)
        )

    def to_matrix(self) -> list[list[int]]:
        """Return the current matrix M, in O(nm log n log m) time."""
        return [
            [self.query(r, c, r, c) for c in range(self.m)] for r in range(self.n)
        ]

    def check_invariant(self) -> None:
        """Assert that each cell holds the sum of its rectangle of M."""
        mat = self.to_matrix()
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                want = sum(
                    mat[a][b]
                    for a in range(i - _low(i), i)
                    for b in range(j - _low(j), j)
                )
                assert self.f[i][j] == want, (i, j)
