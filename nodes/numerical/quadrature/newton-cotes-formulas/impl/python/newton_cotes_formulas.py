# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newton-cotes-formulas/. The authors are listed in prov/BB06D0.jsonl.

import math
from fractions import Fraction
from typing import Callable, Dict, Iterable, List, Tuple, TypeVar, Union

Num = TypeVar("Num", float, Fraction)


def _sum(values: Iterable[Num]) -> Num:
    """Sum floats with math.fsum (one rounding), and Fractions exactly."""
    vals = list(values)
    if any(isinstance(v, Fraction) for v in vals) or not vals:
        return sum(vals)
    return math.fsum(vals)


def reference_nodes(n: int, open_: bool = False) -> List[Fraction]:
    """Equally spaced nodes on [0, 1]: i/(n-1) (closed) or i/(n+1) (open)."""
    if open_:
        if n < 1:
            raise ValueError("an open rule needs n >= 1")
        return [Fraction(i, n + 1) for i in range(1, n + 1)]
    if n < 2:
        raise ValueError("a closed rule needs n >= 2")
    return [Fraction(i, n - 1) for i in range(n)]


def newton_cotes_weights(n: int, open_: bool = False) -> Tuple[List[Fraction], List[Fraction]]:
    """Nodes and exact weights of the n-point Newton-Cotes rule on [0, 1].

    The weights solve the moment equations sum_i W_i t_i^k = 1/(k + 1) for
    k = 0..n-1, by Gauss-Jordan elimination in rational arithmetic.
    Cost: O(n^3) operations on fractions; no evaluation of f.
    """
    t = reference_nodes(n, open_)  # @line L1
    rows = [[ti**k for ti in t] + [Fraction(1, k + 1)] for k in range(n)]  # @line L2
    for c in range(n):
        p = next(r for r in range(c, n) if rows[r][c] != 0)
        rows[c], rows[p] = rows[p], rows[c]
        piv = rows[c][c]
        rows[c] = [v / piv for v in rows[c]]
        for r in range(n):
            if r != c and rows[r][c] != 0:
                fac = rows[r][c]
                rows[r] = [vr - fac * vc for vr, vc in zip(rows[r], rows[c])]
    return t, [rows[i][n] for i in range(n)]


def newton_cotes(
    f: Callable[[Num], Num],
    a: Num,
    b: Num,
    n: int,
    open_: bool = False,
    m: int = 1,
) -> Num:
    """Composite n-point Newton-Cotes rule with m panels for the integral of f on [a, b].

    Precondition: n >= 2 (closed) or n >= 1 (open), m >= 1. With Fraction
    arguments and a Fraction-valued f the result is exact. Closed panels share
    their end nodes, which are evaluated once.
    Cost: m*(n - 1) + 1 evaluations of f (closed) or m*n (open), plus O(n^3)
    rational operations for the weights.
    """
    if m < 1:
        raise ValueError("m must be at least 1")
    t, w = newton_cotes_weights(n, open_)
    exact = isinstance(a, Fraction) or isinstance(b, Fraction)
    weights: List[Union[Fraction, float]] = list(w) if exact else [float(x) for x in w]
    big_h = (b - a) / m  # @line L3
    # Collect the coefficient of each distinct node. A key (j, i) names the
    # node a + (j + t_i) H; for closed rules the right end of panel j is the
    # left end of panel j + 1, so both map to the same key.
    coef: Dict[Tuple[int, int], Union[Fraction, float]] = {}  # @line L4
    for j in range(m):  # @line L5
        for i in range(n):  # @line L6
            key = (j + 1, 0) if (not open_ and i == n - 1 and j < m - 1) else (j, i)
            coef[key] = coef.get(key, 0) + weights[i]
    s = _sum(c * f(a + (j + t[i]) * big_h) for (j, i), c in coef.items())  # @line L7
    return big_h * s  # @line L8


def degree_of_exactness(n: int, open_: bool = False) -> int:
    """The degree d of the n-point rule: n - 1 for even n, n for odd n."""
    return n if n % 2 == 1 else n - 1
