# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pool-adjacent-violators/. The authors are listed in prov/9PKVV8.jsonl.

from fractions import Fraction
from numbers import Real
from typing import Sequence


def pool_adjacent_violators(
    y: Sequence[Real], weights: Sequence[Real] | None = None
) -> list[Real]:
    """Return the weighted isotonic (non-decreasing) least squares fit of y.

    The result z minimizes sum(weights[i] * (y[i] - z[i])**2) subject to
    z[0] <= z[1] <= ... <= z[n-1]. Precondition: every weight is positive,
    and len(weights) == len(y). Exact for int and Fraction inputs (the block
    values are Fractions then). Cost: O(n) arithmetic operations and O(n)
    extra memory, because each item is pushed once and merged at most once.
    """
    n = len(y)
    wt = [1] * n if weights is None else list(weights)
    if len(wt) != n:
        raise ValueError("y and weights must have the same length")
    if any(c <= 0 for c in wt):
        raise ValueError("weights must be positive")
    exact = all(isinstance(v, (int, Fraction)) for v in list(y) + wt)
    # Each block is [value, total weight, length].
    stack: list[list] = []  # @line L1
    for i in range(n):  # @line L2
        v = Fraction(y[i]) if exact else y[i]
        stack.append([v, wt[i], 1])  # @line L3
        while len(stack) >= 2 and stack[-2][0] > stack[-1][0]:  # @line L4
            v2, w2, m2 = stack.pop()  # @line L5
            v1, w1, m1 = stack.pop()
            total = w1 + w2
            stack.append([(w1 * v1 + w2 * v2) / total, total, m1 + m2])  # @line L6
    out: list[Real] = []  # @line L7
    for v, _, m in stack:  # @line L8
        out.extend([v] * m)  # @line L9
    return out  # @line L10


def blocks(z: Sequence[Real]) -> list[tuple[int, int]]:
    """Split a fitted sequence into maximal runs of equal values, as (start, end) half-open pairs."""
    out: list[tuple[int, int]] = []
    start = 0
    for i in range(1, len(z) + 1):
        if i == len(z) or z[i] != z[start]:
            out.append((start, i))
            start = i
    return out
