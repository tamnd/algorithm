# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lawler-algorithm/. The authors are listed in prov/TBK2E7.jsonl.

from fractions import Fraction
from typing import Callable, Sequence, Union

Number = Union[int, Fraction]
Cost = Callable[[Number], Number]


def lawler_algorithm(
    p: Sequence[Number],
    f: Sequence[Cost],
    prec: Sequence[tuple[int, int]] = (),
) -> tuple[list[int], Number]:
    """Minimize max_j f[j](C_j) on one machine under precedence constraints (1|prec|fmax).

    Job j has processing time p[j] >= 0 and a nondecreasing cost function f[j].
    A pair (a, b) in prec means that a must finish before b starts. The schedule
    is built from the end: among the jobs whose successors are all placed, the
    job with the least cost at the current end time P goes last.
    Returns the order (first job first) and its value max_j f[j](C_j).
    Raises ValueError if prec has a cycle.

    Cost: O(n^2 + e) evaluations and steps, with e = len(prec).
    """
    n = len(p)
    if len(f) != n:
        raise ValueError("p and f must have the same length")
    if any(x < 0 for x in p):
        raise ValueError("processing times must be nonnegative")
    preds: list[list[int]] = [[] for _ in range(n)]
    out = [0] * n
    for a, b in prec:
        preds[b].append(a)
        out[a] += 1
    placed = [False] * n
    big_p: Number = sum(p)  # @line L1
    # out[j] counts the successors of j that are not placed yet  # @line L2
    order = [0] * n
    for k in range(n - 1, -1, -1):  # @line L3
        best = -1
        best_cost: Number = 0
        for j in range(n):  # @line L4
            if not placed[j] and out[j] == 0:
                c = f[j](big_p)
                if best < 0 or c < best_cost:
                    best, best_cost = j, c
        if best < 0:
            raise ValueError("the precedence constraints have a cycle")
        order[k] = best  # @line L5
        placed[best] = True
        big_p = big_p - p[best]
        for i in preds[best]:  # @line L6
            out[i] -= 1
    return order, objective(p, f, order)  # @line L7


def objective(p: Sequence[Number], f: Sequence[Cost], order: Sequence[int]) -> Number:
    """Return max_j f[j](C_j) for the order run back to back from time 0."""
    t: Number = 0
    worst: Number = 0
    for i, j in enumerate(order):
        t = t + p[j]
        c = f[j](t)
        if i == 0 or c > worst:
            worst = c
    return worst
