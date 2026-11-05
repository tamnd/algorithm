# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bentley-column-sweep/. The authors are listed in prov/B4PWT1.jsonl.

from typing import Optional, Union

Number = Union[int, float]


def _kadane(c: list[Number]) -> tuple[Number, int, int]:
    """Return (best, e, d): the largest sum of a non-empty subarray of c and its columns."""
    cur = c[0]
    start = 0
    best = c[0]
    be, bd = 0, 0
    for j in range(1, len(c)):
        if cur < 0:
            cur, start = c[j], j
        else:
            cur += c[j]
        if cur > best:
            best, be, bd = cur, start, j
    return best, be, bd


def max_sum_submatrix(m: list[list[Number]]) -> tuple[Number, tuple[int, int, int, int]]:
    """Return (best, (a, b, e, d)): rows a..b and columns e..d of a largest-sum rectangle.

    Indices are 0-based and inclusive. Precondition: m is a non-empty rectangular
    matrix with at least one column (raises ValueError otherwise).
    Cost: Theta(r^2 c) time for r rows and c columns, Theta(c) extra space. The rows
    are swept as given; transpose first if there are more rows than columns.
    """
    if not m or not m[0] or any(len(row) != len(m[0]) for row in m):
        raise ValueError("the matrix must be non-empty and rectangular")
    rows, cols = len(m), len(m[0])
    best: Optional[Number] = None  # @line L1
    rect = (0, 0, 0, 0)
    for a in range(rows):  # @line L2
        c: list[Number] = [0] * cols  # @line L3
        for b in range(a, rows):  # @line L4
            row = m[b]  # @line L5
            for j in range(cols):
                c[j] += row[j]
            s, e, d = _kadane(c)  # @line L6
            if best is None or s > best:  # @line L7
                best, rect = s, (a, b, e, d)
    assert best is not None
    return best, rect  # @line L8


def max_sum_submatrix_auto(m: list[list[Number]]) -> Number:
    """Return the largest rectangle sum, sweeping bands of the shorter side.

    Cost: Theta(min(r, c)^2 max(r, c)) time.
    """
    if not m or not m[0]:
        raise ValueError("the matrix must be non-empty and rectangular")
    if len(m) > len(m[0]):
        m = [list(col) for col in zip(*m)]
    return max_sum_submatrix(m)[0]
