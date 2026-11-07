# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sylvester-matrix/. The authors are listed in prov/NEATH6.jsonl.
"""The Sylvester matrix of two univariate polynomials, stored implicitly.

A polynomial is a list of coefficients from the highest degree down:
f = [a_m, ..., a_0] has formal degree m = len(f) - 1. The leading coefficient
may be zero (a formal degree). Coefficients are elements of an integral
domain with exact division, such as int or Fraction.

Syl(f, g) is the (m + n) x (m + n) matrix whose row i < n holds the
coefficients of x^(n-1-i) f and whose row n + j holds those of x^(m-1-j) g,
from x^(m+n-1) down to x^0.

Cost (ring operations, which over Z means operations on integers whose size
grows with the input, not bit operations): entry O(1), combine O(m n),
determinant O((m + n)^3) by Bareiss elimination with exact divisions, rank
O((m + n)^3). Space: O(m + n) for the matrix itself.
"""

from __future__ import annotations

from typing import Any, Sequence


class SylvesterMatrix:
    """Implicit Sylvester matrix: only the two coefficient vectors are stored."""

    def __init__(self, f: Sequence[Any], g: Sequence[Any]) -> None:
        if len(f) == 0 or len(g) == 0:
            raise ValueError("each polynomial needs a formal degree, at least one coefficient")
        self.f = list(f)
        self.g = list(g)
        self.m = len(self.f) - 1
        self.n = len(self.g) - 1
        self.size = self.m + self.n

    def check_invariant(self) -> None:
        """The dense matrix agrees with entry(), and each row is a shifted coefficient vector."""
        m, n, N = self.m, self.n, self.size
        rows = self.to_dense()
        assert len(rows) == N and all(len(r) == N for r in rows)
        for i in range(n):
            assert rows[i][i:i + m + 1] == self.f
        for j in range(m):
            assert rows[n + j][j:j + n + 1] == self.g

    def entry(self, r: int, c: int) -> Any:
        """Entry in row r, column c. Cost O(1)."""
        if not (0 <= r < self.size and 0 <= c < self.size):  # @line E1
            raise IndexError("index out of range")
        if r < self.n:  # @line E2
            k = c - r  # @line E3
            return self.f[k] if 0 <= k <= self.m else 0 * self.f[0]
        k = c - (r - self.n)  # @line E4
        return self.g[k] if 0 <= k <= self.n else 0 * self.g[0]

    def to_dense(self) -> list[list[Any]]:
        """The full matrix as a list of rows. Cost O((m + n)^2)."""
        return [[self.entry(r, c) for c in range(self.size)] for r in range(self.size)]

    def combine(self, s: Sequence[Any], t: Sequence[Any]) -> list[Any]:
        """Row vector (s, t) times Syl(f, g): the coefficients of s f + t g.

        s has n coefficients (degree < n) and t has m (degree < m), highest first.
        The result has m + n coefficients, highest first. Cost O(m n).
        """
        if len(s) != self.n or len(t) != self.m:  # @line C1
            raise ValueError("s needs n coefficients and t needs m")
        out = [0 * self.f[0]] * self.size  # @line C2
        for i, si in enumerate(s):  # @line C3
            for k, a in enumerate(self.f):
                out[i + k] = out[i + k] + si * a
        for j, tj in enumerate(t):  # @line C4
            for k, b in enumerate(self.g):
                out[j + k] = out[j + k] + tj * b
        return out  # @line C5

    def determinant(self) -> Any:
        """det Syl(f, g), the resultant Res_(m,n)(f, g), by Bareiss elimination.

        Every division is exact in the coefficient domain. Cost O((m + n)^3) ring operations.
        """
        N = self.size
        if N == 0:  # @line L1
            return 1
        A = self.to_dense()  # @line L2
        sign, prev = 1, 1  # @line L3
        for k in range(N - 1):  # @line L4
            p = next((r for r in range(k, N) if A[r][k] != 0), None)  # @line L5
            if p is None:  # @line L6
                return 0 * A[0][0]
            if p != k:  # @line L7
                A[k], A[p] = A[p], A[k]
                sign = -sign
            for i in range(k + 1, N):  # @line L8
                for j in range(k + 1, N):
                    A[i][j] = _exact_div(A[i][j] * A[k][k] - A[i][k] * A[k][j], prev)  # @line L9
                A[i][k] = 0 * A[i][k]
            prev = A[k][k]  # @line L10
        return sign * A[N - 1][N - 1]  # @line L11

    def rank(self) -> int:
        """Rank over the fraction field, by fraction-free elimination. Cost O((m + n)^3)."""
        A = self.to_dense()
        N = self.size
        rank, prev, row = 0, 1, 0
        for col in range(N):
            p = next((r for r in range(row, N) if A[r][col] != 0), None)
            if p is None:
                continue
            A[row], A[p] = A[p], A[row]
            for i in range(row + 1, N):
                for j in range(col + 1, N):
                    A[i][j] = _exact_div(A[i][j] * A[row][col] - A[i][col] * A[row][j], prev)
                A[i][col] = 0 * A[i][col]
            prev = A[row][col]
            row += 1
            rank += 1
        return rank


def _exact_div(a: Any, b: Any) -> Any:
    """a / b where b divides a exactly (int or Fraction)."""
    if isinstance(a, int) and isinstance(b, int):
        q, r = divmod(a, b)
        if r != 0:
            raise ArithmeticError("division is not exact")
        return q
    return a / b
