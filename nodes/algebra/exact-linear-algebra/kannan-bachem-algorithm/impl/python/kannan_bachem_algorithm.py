# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kannan-bachem-algorithm/. The authors are listed in prov/XTZT1P.jsonl.

from typing import Sequence


def xgcd(a: int, b: int) -> tuple[int, int, int]:
    """Return (g, x, y) with g = gcd(a, b) >= 0 and x a + y b = g."""
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a - q * b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    if a < 0:
        a, x0, y0 = -a, -x0, -y0
    return a, x0, y0


def _lead(w: Sequence[int], n: int) -> int | None:
    """Index of the first nonzero entry among the first n entries of w, or None."""
    for j in range(n):
        if w[j]:
            return j
    return None


def kannan_bachem(a: Sequence[Sequence[int]]) -> tuple[list[list[int]], list[list[int]]]:
    """Row Hermite normal form H = U a of an m x n integer matrix, with U unimodular.

    The rows are inserted one at a time; after each insertion the stored rows are the
    Hermite normal form of the rows inserted so far, so every stored number is bounded
    by the Hermite bound. H has the nonzero rows first, in echelon form with positive
    pivots and the entries above each pivot in [0, pivot), then zero rows.

    Cost: O(m r (r + 1) (n + m)) integer operations for rank r, on numbers whose
    length is polynomial in m, n and the length of the entries.
    """
    m = len(a)
    n = len(a[0]) if m else 0
    rows: list[list[int]] = []  # @line L1
    piv: list[int] = []
    kernel: list[list[int]] = []
    for t in range(m):  # @line L2
        w = [int(v) for v in a[t]] + [int(j == t) for j in range(m)]  # @line L3
        k = 0
        while k < len(rows):  # @line L4
            c = _lead(w, n)
            if c is None or c < piv[k]:  # @line L5
                break
            if c == piv[k]:  # @line L6
                h = rows[k]
                g, x, y = xgcd(h[c], w[c])  # @line L7
                p, q = h[c] // g, w[c] // g
                rows[k], w = [x * u + y * v for u, v in zip(h, w)], [p * v - q * u for u, v in zip(h, w)]  # @line L8
            k += 1
        c = _lead(w, n)
        if c is None:  # @line L9
            kernel.append(w)
        else:
            if w[c] < 0:  # @line L10
                w = [-v for v in w]
            rows.insert(k, w)
            piv.insert(k, c)
        for l in range(len(rows) - 2, -1, -1):  # @line L11
            for k2 in range(l + 1, len(rows)):  # @line L12
                f = rows[l][piv[k2]] // rows[k2][piv[k2]]
                if f:
                    rows[l] = [u - f * v for u, v in zip(rows[l], rows[k2])]  # @line L13
    h_out = [r[:n] for r in rows] + [[0] * n for _ in kernel]
    u_out = [r[n:] for r in rows] + [r[n:] for r in kernel]
    return h_out, u_out  # @line L14


def hermite_normal_form(a: Sequence[Sequence[int]]) -> list[list[int]]:
    """The row Hermite normal form of a, with the zero rows at the bottom."""
    return kannan_bachem(a)[0]
