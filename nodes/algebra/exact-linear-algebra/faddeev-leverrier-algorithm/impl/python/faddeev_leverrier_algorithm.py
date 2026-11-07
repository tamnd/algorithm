# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/faddeev-leverrier-algorithm/. The authors are listed in prov/6P3FW5.jsonl.

from fractions import Fraction
from typing import Any, Sequence


def _divide(x: Any, k: int) -> Any:
    """Divide x by the integer k. For an int the quotient must be exact."""
    if isinstance(x, int):
        q, r = divmod(x, k)
        assert r == 0, "inexact division by k"
        return q
    return x / k


def faddeev_leverrier(a: Sequence[Sequence[Any]]) -> tuple[list[Any], list[list[Any]]]:
    """Return (c, m): c lists det(xI - a) highest degree first, and m is the matrix M_n.

    Works over a field of characteristic 0 or greater than n, and over the integers, where
    every division by k is exact. adj(a) = (-1)^(n-1) M_n, and a M_n = -c_0 I.
    Cost: n matrix products, 2n^4 + O(n^3) field operations.
    """
    n = len(a)
    c = [1] + [0] * n  # @line L1
    nm = [[0] * n for _ in range(n)]
    m = nm
    for k in range(1, n + 1):  # @line L2
        m = [[nm[i][j] + (c[k - 1] if i == j else 0) for j in range(n)] for i in range(n)]  # @line L3
        nm = [[sum((a[i][t] * m[t][j] for t in range(1, n)), a[i][0] * m[0][j]) for j in range(n)] for i in range(n)]  # @line L4
        c[k] = -_divide(sum((nm[i][i] for i in range(1, n)), nm[0][0]), k)  # @line L5
    return c, m  # @line L6


def characteristic_polynomial(a: Sequence[Sequence[Any]]) -> list[Any]:
    """Coefficients of det(xI - a), highest degree first."""
    return faddeev_leverrier(a)[0]


def determinant(a: Sequence[Sequence[Any]]) -> Any:
    """det a = (-1)^n c_0."""
    c0 = faddeev_leverrier(a)[0][-1]
    return c0 if len(a) % 2 == 0 else -c0


def adjugate(a: Sequence[Sequence[Any]]) -> list[list[Any]]:
    """adj a = (-1)^(n-1) M_n, the matrix of cofactors transposed."""
    n = len(a)
    if n == 0:
        return []
    m = faddeev_leverrier(a)[1]
    return m if n % 2 == 1 else [[-x for x in row] for row in m]


def inverse(a: Sequence[Sequence[Any]]) -> list[list[Fraction]] | None:
    """Return the inverse of an integer or rational matrix as Fractions, or None if singular."""
    n = len(a)
    q = [[Fraction(x) for x in row] for row in a]
    c, m = faddeev_leverrier(q)
    if c[-1] == 0:
        return None
    return [[-x / c[-1] for x in row] for row in m] if n else []
