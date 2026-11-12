# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-separability/. The authors are listed in prov/7A99T5.jsonl.

"""Exact tests of linear separability by Fourier-Motzkin elimination.

A finite labelled set is strictly separable by (w, b) when
y_i (w . x_i + b) > 0 for all i. Scaling (w, b) shows that this holds if and
only if the linear system y_i (w . x_i + b) >= 1 has a solution, so the test is
a linear feasibility problem. All arithmetic uses Fraction, so the answer is
exact, and a yes answer comes with a separator that the caller can check.
"""

from fractions import Fraction
from itertools import combinations, product
from math import comb
from typing import Optional, Sequence

Row = tuple[tuple[Fraction, ...], Fraction]  # a . z >= c


def _eliminate_last(rows: list[Row]) -> list[Row]:
    """Remove the last variable from a system of rows a . z >= c."""
    pos, neg, out = [], [], set()
    for a, c in rows:
        if a[-1] > 0:
            pos.append((a, c))
        elif a[-1] < 0:
            neg.append((a, c))
        else:
            out.add((a[:-1], c))
    for ap, cp in pos:
        for an, cn in neg:
            sp, sn = 1 / ap[-1], 1 / -an[-1]
            a = tuple(sp * u + sn * v for u, v in zip(ap[:-1], an[:-1]))
            out.add((a, sp * cp + sn * cn))
    return list(out)


def fourier_motzkin(rows: list[Row], m: int) -> Optional[list[Fraction]]:
    """Return z in Q^m with a . z >= c for every row, or None if none exists."""
    levels = [rows]
    for _ in range(m):
        levels.append(_eliminate_last(levels[-1]))
    if any(c > 0 for _, c in levels[-1]):  # each row is now 0 >= c
        return None
    z: list[Fraction] = []
    for j in range(m):  # level m - j holds the variables z_0 .. z_j
        lo, hi = None, None
        for a, c in levels[m - j - 1]:
            rest = c - sum(a[t] * z[t] for t in range(j))
            if a[j] > 0:
                v = rest / a[j]
                lo = v if lo is None or v > lo else lo
            elif a[j] < 0:
                v = rest / a[j]
                hi = v if hi is None or v < hi else hi
        if lo is not None and hi is not None:
            z.append((lo + hi) / 2)
        elif lo is not None:
            z.append(lo)
        elif hi is not None:
            z.append(hi)
        else:
            z.append(Fraction(0))
    return z


def separator(
    xs: Sequence[Sequence[int]], ys: Sequence[int], bias: bool = True
) -> Optional[tuple[list[Fraction], Fraction]]:
    """Return (w, b) with y_i (w . x_i + b) >= 1 for all i, or None.

    With bias=False the hyperplane passes through the origin and b = 0.
    """
    if not xs:
        return [], Fraction(0)
    d = len(xs[0])
    rows: list[Row] = []
    for x, y in zip(xs, ys):
        a = [Fraction(y * v) for v in x]
        if bias:
            a.append(Fraction(y))
        rows.append((tuple(a), Fraction(1)))
    z = fourier_motzkin(rows, d + (1 if bias else 0))
    if z is None:
        return None
    return z[:d], (z[d] if bias else Fraction(0))


def is_separable(xs: Sequence[Sequence[int]], ys: Sequence[int], bias: bool = True) -> bool:
    return separator(xs, ys, bias) is not None


def count_separable_dichotomies(xs: Sequence[Sequence[int]], bias: bool) -> int:
    """Count the labelings in {-1, +1}^n that are strictly separable."""
    return sum(1 for ys in product((-1, 1), repeat=len(xs)) if is_separable(xs, ys, bias))


def cover_count(n: int, d: int) -> int:
    """Cover (1965): C(n, d) = 2 * sum_{k=0}^{d-1} binom(n - 1, k)."""
    return 2 * sum(comb(n - 1, k) for k in range(d))


def _det(m: list[list[Fraction]]) -> Fraction:
    m = [row[:] for row in m]
    n, det = len(m), Fraction(1)
    for c in range(n):
        p = next((r for r in range(c, n) if m[r][c] != 0), None)
        if p is None:
            return Fraction(0)
        if p != c:
            m[c], m[p] = m[p], m[c]
            det = -det
        det *= m[c][c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            for k in range(c, n):
                m[r][k] -= f * m[c][k]
    return det


def in_general_position(xs: Sequence[Sequence[int]]) -> bool:
    """Every d of the vectors in R^d are linearly independent.

    Every smaller subset is then independent too.
    """
    d = len(xs[0])
    if len(xs) < d:
        return _rank(xs) == len(xs)
    return all(_det([[Fraction(v) for v in r] for r in s]) != 0 for s in combinations(xs, d))


def _rank(xs: Sequence[Sequence[int]]) -> int:
    m = [[Fraction(v) for v in r] for r in xs]
    rank, cols = 0, len(m[0]) if m else 0
    for c in range(cols):
        p = next((r for r in range(rank, len(m)) if m[r][c] != 0), None)
        if p is None:
            continue
        m[rank], m[p] = m[p], m[rank]
        for r in range(len(m)):
            if r != rank and m[r][c] != 0:
                f = m[r][c] / m[rank][c]
                m[r] = [u - f * v for u, v in zip(m[r], m[rank])]
        rank += 1
    return rank
