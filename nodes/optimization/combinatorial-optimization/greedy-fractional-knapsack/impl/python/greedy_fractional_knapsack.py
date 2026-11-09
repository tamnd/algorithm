# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-fractional-knapsack/. The authors are listed in prov/Q1RH1S.jsonl.

from fractions import Fraction
from functools import cmp_to_key


def _by_ratio_desc(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    """Compare (index, weight, value) by v/w, larger first, without division."""
    _, wa, va = a
    _, wb, vb = b
    left, right = va * wb, vb * wa
    return -1 if left > right else (1 if left < right else 0)


def greedy_fractional_knapsack(
    weights: list[int], values: list[int], capacity: int
) -> tuple[Fraction, list[Fraction]]:
    """Solve the fractional knapsack problem exactly.

    Precondition: every weight is a positive integer, every value and the
    capacity are non-negative integers.

    Returns (total, x): the optimal value and fractions x[i] in [0, 1], one
    for each item in the input order, with sum(weights[i] * x[i]) <= capacity.
    At most one x[i] is strictly between 0 and 1.

    Cost: O(n log n) time for the sort and O(n) extra space.
    """
    n = len(weights)
    if len(values) != n:
        raise ValueError("weights and values must have the same length")
    if any(w <= 0 for w in weights) or capacity < 0:
        raise ValueError("weights must be positive and capacity non-negative")
    items = sorted(zip(range(n), weights, values), key=cmp_to_key(_by_ratio_desc))  # @line L1
    r = Fraction(capacity)  # @line L2
    x = [Fraction(0)] * n
    total = Fraction(0)
    for i, w, v in items:  # @line L3
        if w <= r:  # @line L4
            x[i] = Fraction(1)  # @line L5
            r -= w
            total += v
        else:  # @line L6
            x[i] = r / w  # @line L7
            total += v * x[i]
            return total, x  # @line L8
    return total, x  # @line L9


def dual_certificate(
    weights: list[int], values: list[int], capacity: int
) -> tuple[Fraction, list[Fraction]]:
    """Return a dual solution (lam, mu) whose value equals the greedy total.

    The dual of the relaxation is: minimize capacity * lam + sum(mu) subject
    to lam * w[i] + mu[i] >= v[i], lam >= 0, mu >= 0.
    """
    n = len(weights)
    _, x = greedy_fractional_knapsack(weights, values, capacity)
    lam = Fraction(0)
    for i in range(n):
        if x[i] < 1:
            lam = max(lam, Fraction(values[i], weights[i]))
    mu = [max(Fraction(0), values[i] - lam * weights[i]) for i in range(n)]
    return lam, mu
