# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smawk-algorithm/. The authors are listed in prov/V8AHMD.jsonl.

from typing import Callable, Sequence


def smawk(rows: Sequence[int], cols: Sequence[int], a: Callable[[int, int], float]) -> dict[int, int]:
    """Return a map from each row to the column of its leftmost minimum.

    rows and cols are increasing lists of indices, cols is not empty, and
    a(i, j) returns the entry in row i and column j. The matrix restricted to
    rows and cols must be totally monotone: for i < i2 and j < j2,
    a(i, j) > a(i, j2) implies a(i2, j) > a(i2, j2).
    It reads O(len(rows) + len(cols)) entries and takes the same time.
    """
    if not rows:  # @line L1
        return {}
    c = reduce_columns(rows, cols, a)  # @line L2
    odd = rows[1::2]  # @line L3
    m = smawk(odd, c, a)  # @line L4
    pos = {col: t for t, col in enumerate(c)}
    k = 0  # @line L5
    for i in range(0, len(rows), 2):  # @line L6
        stop = pos[m[rows[i + 1]]] if i + 1 < len(rows) else len(c) - 1  # @line L7
        r = rows[i]
        best, best_val = c[k], a(r, c[k])  # @line L8
        for t in range(k + 1, stop + 1):
            v = a(r, c[t])
            if v < best_val:
                best, best_val = c[t], v
        m[r] = best
        k = stop  # @line L9
    return m  # @line L10


def reduce_columns(rows: Sequence[int], cols: Sequence[int], a: Callable[[int, int], float]) -> list[int]:
    """Drop columns that hold no leftmost row minimum; at most len(rows) columns stay."""
    s: list[int] = []  # @line L11
    for c in cols:  # @line L12
        while s and a(rows[len(s) - 1], s[-1]) > a(rows[len(s) - 1], c):  # @line L13
            s.pop()
        if len(s) < len(rows):  # @line L14
            s.append(c)
    return s  # @line L15


def row_minima(n: int, m: int, a: Callable[[int, int], float]) -> list[int]:
    """Leftmost minimum column of each row of a totally monotone n by m matrix (m >= 1)."""
    res = smawk(list(range(n)), list(range(m)), a)
    return [res[i] for i in range(n)]
