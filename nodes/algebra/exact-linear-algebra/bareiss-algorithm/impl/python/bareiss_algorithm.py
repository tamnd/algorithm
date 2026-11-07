# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bareiss-algorithm/. The authors are listed in prov/S667TN.jsonl.

from typing import Sequence


def bareiss(a: Sequence[Sequence[int]]) -> tuple[int, list[list[int]], list[int]]:
    """Return (det, u, perm) for the n by n integer matrix a, by fraction-free elimination.

    Every division is exact. u is the final working matrix: for k <= j, u[k][j] is the minor of
    the row-permuted matrix in rows 0..k and columns 0..k-1, j. perm lists the original row index
    of each row of u. When a is singular, det is 0 and u, perm describe the state at that point.
    Cost: O(n^3) integer operations on numbers of O(n (b + log n)) bits.
    """
    n = len(a)
    u = [list(row) for row in a]
    perm = list(range(n))
    if n == 0:  # @line L1
        return 1, u, perm
    s, prev = 1, 1  # @line L2
    for k in range(n - 1):  # @line L3
        if u[k][k] == 0:  # @line L4
            p = next((i for i in range(k + 1, n) if u[i][k] != 0), None)  # @line L5
            if p is None:  # @line L6
                return 0, u, perm
            u[k], u[p] = u[p], u[k]  # @line L7
            perm[k], perm[p] = perm[p], perm[k]
            s = -s
        pivot, row_k = u[k][k], u[k]
        for i in range(k + 1, n):  # @line L8
            row_i = u[i]
            f = row_i[k]
            for j in range(k + 1, n):  # @line L9
                row_i[j] = (pivot * row_i[j] - f * row_k[j]) // prev  # @line L10
            row_i[k] = 0
        prev = pivot  # @line L11
    return s * u[n - 1][n - 1], u, perm  # @line L12


def bareiss_determinant(a: Sequence[Sequence[int]]) -> int:
    """Return the determinant of the square integer matrix a. Cost: O(n^3) integer operations."""
    return bareiss(a)[0]


def fraction_free_echelon(a: Sequence[Sequence[int]], n: int | None = None) -> tuple[list[list[int]], int, list[int]]:
    """Return (e, r, pivots): an echelon form e of the m by n integer matrix a with integer
    entries, obtained by fraction-free row operations, its rank r and its pivot columns.

    The nonzero rows of e span the row space of a over Q. Every division is exact.
    Cost: O(m n min(m, n)) integer operations.
    """
    e = [list(row) for row in a]
    m = len(e)
    if n is None:
        n = len(e[0]) if m else 0
    r, prev, pivots = 0, 1, []
    for j in range(n):
        if r == m:
            break
        p = next((i for i in range(r, m) if e[i][j] != 0), None)
        if p is None:
            continue
        e[r], e[p] = e[p], e[r]
        pivot, row_r = e[r][j], e[r]
        for i in range(r + 1, m):
            row_i = e[i]
            f = row_i[j]
            for t in range(j + 1, n):
                q, rem = divmod(pivot * row_i[t] - f * row_r[t], prev)
                assert rem == 0, "inexact division"
                row_i[t] = q
            row_i[j] = 0
        prev = pivot
        pivots.append(j)
        r += 1
    return e, r, pivots
