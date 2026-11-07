# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/winograd-inner-product-algorithm/. The authors are listed in prov/FZ993N.jsonl.

from typing import Optional

Matrix = list[list[int]]


def winograd_inner_product_algorithm(a: Matrix, b: Matrix, p: Optional[int] = None,
                                     mod: Optional[int] = None) -> Matrix:
    """Return the product a b of an n x m and an m x p matrix over Z, or Z/mod Z.

    The entries must commute (Z and Z/qZ do). Uses (n p + n + p) floor(m/2)
    multiplications, plus n p more when m is odd, and Theta(n m p) operations
    in all. When m = 0 the number of columns p must be given.
    """
    n = len(a)
    m = len(a[0]) if n else len(b)
    if any(len(row) != m for row in a) or len(b) != m:
        raise ValueError("inner dimensions do not match")
    if p is None:
        if m == 0:
            raise ValueError("p is needed when the inner dimension is 0")
        p = len(b[0])
    if any(len(row) != p for row in b):
        raise ValueError("rows of b have different lengths")
    h = m // 2  # @line L1
    xi = [sum(a[i][2 * t] * a[i][2 * t + 1] for t in range(h)) for i in range(n)]  # @line L2
    eta = [sum(b[2 * t][j] * b[2 * t + 1][j] for t in range(h)) for j in range(p)]  # @line L3
    c = [[0] * p for _ in range(n)]
    for i in range(n):  # @line L4
        row = a[i]
        for j in range(p):
            s = -xi[i] - eta[j]  # @line L5
            for t in range(h):  # @line L6
                s += (row[2 * t] + b[2 * t + 1][j]) * (row[2 * t + 1] + b[2 * t][j])
            if m % 2 == 1:  # @line L7
                s += row[m - 1] * b[m - 1][j]
            c[i][j] = s % mod if mod is not None else s  # @line L8
    return c  # @line L9


def multiplication_count(n: int, m: int, p: int) -> int:
    """The number of multiplications that the method makes."""
    return (n * p + n + p) * (m // 2) + n * p * (m % 2)
