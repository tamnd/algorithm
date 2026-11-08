# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/romberg-integration/. The authors are listed in prov/M6H41M.jsonl.

import math
from fractions import Fraction
from typing import Callable, Iterable, List, Tuple, TypeVar

Num = TypeVar("Num", float, Fraction)


def _sum(values: Iterable[Num]) -> Num:
    """Sum floats with math.fsum (one rounding), and Fractions exactly."""
    vals = list(values)
    if any(isinstance(v, Fraction) for v in vals) or not vals:
        return sum(vals)
    return math.fsum(vals)


def romberg(
    f: Callable[[Num], Num],
    a: Num,
    b: Num,
    tol: float = 1e-12,
    max_level: int = 20,
    min_level: int = 3,
) -> Tuple[Num, Num, List[List[Num]]]:
    """Romberg integration of f on [a, b].

    Builds the triangular table R[i][k], i = 0..K, where R[i][0] is the
    trapezoidal rule with 2^i subintervals and R[i][k] the k-th Richardson
    extrapolation in h^2. Stops at the first level i >= min_level with
    |R[i][i] - R[i-1][i-1]| <= tol, or at i = max_level.
    Returns (R[K][K], |R[K][K] - R[K-1][K-1]|, the table); the second value is
    an asymptotic error estimate, not a bound (0 if K = 0).
    Precondition: max_level >= 0 and f defined at the nodes a + j (b - a)/2^K.
    With Fraction arguments, a Fraction-valued f and tol = 0 the table is
    exact. Cost: 2^K + 1 evaluations of f and O(K^2) further operations.
    """
    if max_level < 0:
        raise ValueError("max_level must be at least 0")
    h = b - a  # @line L1
    table: List[List[Num]] = [[h * (f(a) + f(b)) / 2]]  # @line L2
    for i in range(1, max_level + 1):  # @line L3
        h = h / 2  # @line L4
        new = _sum(f(a + (2 * j - 1) * h) for j in range(1, 2 ** (i - 1) + 1))
        row = [table[i - 1][0] / 2 + h * new]  # @line L5
        for k in range(1, i + 1):  # @line L6
            row.append(row[k - 1] + (row[k - 1] - table[i - 1][k - 1]) / (4**k - 1))  # @line L7
        table.append(row)
        est = abs(row[i] - table[i - 1][i - 1])
        if i >= min_level and est <= tol:  # @line L8
            return row[i], est, table
    k = len(table) - 1
    est = abs(table[k][k] - table[k - 1][k - 1]) if k > 0 else table[0][0] * 0
    return table[k][k], est, table  # @line L9
