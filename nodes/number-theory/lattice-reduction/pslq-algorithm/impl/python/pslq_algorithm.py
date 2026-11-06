# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pslq-algorithm/. The authors are listed in prov/GH5331.jsonl.

from fractions import Fraction
from math import floor
from typing import Optional, Sequence, Union

Number = Union[int, Fraction]


def _nearest(v: Fraction) -> int:
    """The integer nearest to v; a half is rounded up."""
    return floor(v + Fraction(1, 2))


def pslq_counted(
    x: Sequence[Number], gamma2: Fraction = Fraction(2), max_iterations: int = 100000
) -> tuple[list[int], int, list[Fraction]]:
    """PSLQ in exact rational arithmetic.

    Input: a vector x of n >= 2 rationals, not all zero, and gamma2 = gamma^2 > 4/3.
    Output: (m, iterations, bounds), where m is a nonzero integer vector with
    sum m_i x_i = 0, iterations is the number of swaps, and bounds[t] is
    max_j ||p_j*||^2 before iteration t; every integer relation r of x has
    ||r||^2 >= 1 / bounds[t] for every t.
    The matrix H of the usual description is represented by the Gram-Schmidt data
    of the rows p_i of A P_x: H[j][j]^2 = big_b[j] and H[i][j] / H[j][j] = mu[i][j].
    Raises ValueError for bad input and RuntimeError if max_iterations is exceeded.
    """
    n = len(x)
    if n < 2:
        raise ValueError("need at least two numbers")
    xs = [Fraction(v) for v in x]
    norm2 = sum((v * v for v in xs), Fraction(0))
    if norm2 == 0:
        raise ValueError("x must not be the zero vector")
    if gamma2 <= Fraction(4, 3):
        raise ValueError("gamma^2 must exceed 4/3")
    a = [[int(i == j) for j in range(n)] for i in range(n)]  # @line L1
    bmat = [[int(i == j) for j in range(n)] for i in range(n)]  # B = A^-1, relations are columns
    y = list(xs)  # y = x B
    for j in range(n):
        if y[j] == 0:
            return [bmat[i][j] for i in range(n)], 0, []
    # @line L2: Gram-Schmidt of p_i = e_i - (x_i / <x, x>) x, from the Gram matrix of the p_i
    gram = [[Fraction(int(i == j)) - xs[i] * xs[j] / norm2 for j in range(n)] for i in range(n)]
    mu = [[Fraction(0)] * n for _ in range(n)]
    big_b = [Fraction(0)] * n  # big_b[n-1] is 0 throughout
    for i in range(n):
        for j in range(min(i, n - 1)):
            s = gram[i][j] - sum((mu[j][k] * mu[i][k] * big_b[k] for k in range(j)), Fraction(0))
            mu[i][j] = s / big_b[j]
        if i < n - 1:
            big_b[i] = gram[i][i] - sum((mu[i][k] ** 2 * big_b[k] for k in range(i)), Fraction(0))

    def hermite_reduce() -> None:
        for i in range(1, n):  # @line L10
            for j in range(i - 1, -1, -1):
                t = _nearest(mu[i][j])  # @line L11
                if t == 0:
                    continue
                a[i] = [p - t * q for p, q in zip(a[i], a[j])]
                for k in range(j):
                    mu[i][k] -= t * mu[j][k]
                mu[i][j] -= t
                y[j] += t * y[i]  # @line L12
                for row in bmat:
                    row[j] += t * row[i]

    hermite_reduce()  # @line L3
    bounds: list[Fraction] = []
    iterations = 0
    while True:  # @line L4
        for j in range(n):  # @line L5
            if y[j] == 0:
                return [bmat[i][j] for i in range(n)], iterations, bounds
        if iterations >= max_iterations:
            raise RuntimeError("no relation found within max_iterations")
        bounds.append(max(big_b[: n - 1]))
        r = max(range(n - 1), key=lambda j: (gamma2 ** (j + 1) * big_b[j], -j))  # @line L6
        k = r + 1
        a[r], a[k] = a[k], a[r]  # @line L7
        y[r], y[k] = y[k], y[r]
        for row in bmat:
            row[r], row[k] = row[k], row[r]
        # @line L8: the swap formulas of LLL, with big_b[n-1] = 0
        u = mu[k][r]
        new_r = big_b[k] + u * u * big_b[r]
        mu[k][r] = u * big_b[r] / new_r
        big_b[k] = big_b[r] * big_b[k] / new_r
        big_b[r] = new_r
        for j in range(r):
            mu[r][j], mu[k][j] = mu[k][j], mu[r][j]
        for i in range(k + 1, n):
            t = mu[i][k]
            mu[i][k] = mu[i][r] - u * t
            mu[i][r] = t + mu[k][r] * mu[i][k]
        hermite_reduce()  # @line L9
        iterations += 1


def pslq(x: Sequence[Number], gamma2: Fraction = Fraction(2)) -> list[int]:
    """A nonzero integer vector m with sum m_i x_i = 0, found by PSLQ."""
    return pslq_counted(x, gamma2)[0]
