# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/post-randomization-method/. The authors are listed in prov/4VVPMW.jsonl.
"""The post-randomization method (PRAM) of Gouweleeuw, Kooiman, Willenborg and de Wolf.

Categories are the integers 0 .. K-1. A PRAM matrix P is a list of K rows, where
P[k][l] is the probability that a true value k is released as l. Each row sums to 1.
Use Fraction entries for exact results. The rng argument needs only a method
random() that returns a number in [0, 1); random.Random is fine for tests, but a
real release needs a cryptographic source of randomness.
"""

from fractions import Fraction
from typing import Optional, Protocol, Sequence, Union

Number = Union[int, Fraction]
Matrix = Sequence[Sequence[Number]]


class UniformSource(Protocol):
    def random(self) -> float: ...


def check_matrix(P: Matrix) -> None:
    """Raise ValueError unless P is a square matrix of probabilities with rows that sum to 1."""
    size = len(P)
    if size == 0 or any(len(row) != size for row in P):
        raise ValueError("P must be a non-empty square matrix")
    for row in P:
        if any(p < 0 for p in row) or sum(row) != 1:
            raise ValueError("each row of P must be a probability vector")


def pram(values: Sequence[int], P: Matrix, rng: UniformSource) -> list[int]:
    """Release each value k as l with probability P[k][l], independently.

    Precondition: P passes check_matrix and each value is in 0 .. K-1.
    Cost: O(n K) time for n values, O(n) space for the output.
    """
    check_matrix(P)
    out: list[int] = []
    for k in values:  # @line L1
        row = P[k]  # @line L2
        u = rng.random()  # @line L3
        acc: Number = 0
        y = len(row) - 1
        for j, p in enumerate(row):  # @line L4
            acc += p
            if acc > u:
                y = j
                break
        out.append(y)  # @line L5
    return out  # @line L6


def counts(values: Sequence[int], size: int) -> list[int]:
    """The frequency of each category 0 .. size-1. Cost: O(n + size)."""
    t = [0] * size
    for v in values:
        t[v] += 1
    return t


def transpose_times(P: Matrix, t: Sequence[Number]) -> list[Number]:
    """P^T t, the expected released counts for true counts t. Cost: O(K^2)."""
    size = len(P)
    return [sum(P[k][l] * t[k] for k in range(size)) for l in range(size)]


def solve(A: Matrix, b: Sequence[Number]) -> Optional[list[Fraction]]:
    """Solve A z = b exactly by Gaussian elimination; None if A is singular.

    Cost: O(K^3) arithmetic operations on fractions.
    """
    size = len(A)
    m = [[Fraction(A[i][j]) for j in range(size)] + [Fraction(b[i])] for i in range(size)]
    for col in range(size):
        piv = next((r for r in range(col, size) if m[r][col] != 0), None)
        if piv is None:
            return None
        m[col], m[piv] = m[piv], m[col]
        for r in range(size):
            if r != col and m[r][col] != 0:
                f = m[r][col] / m[col][col]
                m[r] = [a - f * c for a, c in zip(m[r], m[col])]
    return [m[i][size] / m[i][i] for i in range(size)]


def estimate(released: Sequence[int], P: Matrix) -> Optional[list[Fraction]]:
    """The unbiased estimate of the true counts: solve P^T T = T* for T.

    Returns None if P is singular. The estimate can have negative entries.
    Precondition: P passes check_matrix. Cost: O(n + K^3).
    """
    check_matrix(P)
    size = len(P)
    t_star = counts(released, size)  # @line L7
    pt = [[P[k][l] for k in range(size)] for l in range(size)]
    t_hat = solve(pt, t_star)  # @line L8
    return t_hat  # @line L9


def invariant_matrix(P: Matrix, t: Sequence[Number]) -> list[list[Fraction]]:
    """R = P Q with Q[l][k] = P[k][l] t[k] / sum_j P[j][l] t[j], so that t^T R = t^T.

    Precondition: P passes check_matrix, t has K entries >= 0, and every category with
    t[k] > 0 has some released value. A column l with no mass gets Q[l] = unit vector l.
    Cost: O(K^3).
    """
    check_matrix(P)
    size = len(P)
    col = [sum(Fraction(P[j][l]) * t[j] for j in range(size)) for l in range(size)]
    q = []
    for l in range(size):
        if col[l] == 0:
            q.append([Fraction(int(k == l)) for k in range(size)])
        else:
            q.append([Fraction(P[k][l]) * t[k] / col[l] for k in range(size)])
    return [[sum(Fraction(P[i][l]) * q[l][j] for l in range(size)) for j in range(size)] for i in range(size)]


def ldp_ratio(P: Matrix) -> Optional[Fraction]:
    """The least c with P[k][l] <= c P[k'][l] for all k, k', l; None if no c exists.

    PRAM with matrix P is epsilon-locally differentially private for epsilon = ln c.
    A column of zeros is a value that is never released and is skipped.
    Cost: O(K^2).
    """
    check_matrix(P)
    worst = Fraction(1)
    for l in range(len(P)):
        column = [Fraction(row[l]) for row in P]
        hi, lo = max(column), min(column)
        if hi == 0:
            continue
        if lo == 0:
            return None
        worst = max(worst, hi / lo)
    return worst
