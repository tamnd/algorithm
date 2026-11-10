# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knapsack-fptas/. The authors are listed in prov/8ZRYG2.jsonl.

from fractions import Fraction
from typing import Union

Number = Union[int, Fraction, float]


def scale_profits(
    profits: list[int], weights: list[int], capacity: int, eps: Number
) -> tuple[list[int], list[int], Fraction]:
    """Return (kept, scaled, k) for the knapsack FPTAS.

    kept are the 0-based indices of the items that fit alone, scaled[j] is
    the scaled profit floor(p / k) of the item kept[j], and k = eps * P / n,
    where P is the largest kept profit and n = len(kept). The arithmetic is
    exact (fractions). Precondition: positive integer profits and weights,
    capacity >= 0, 0 < eps <= 1.
    """
    e = Fraction(eps)
    if not 0 < e <= 1:
        raise ValueError("eps must be in (0, 1]")
    kept = [i for i in range(len(profits)) if weights[i] <= capacity]  # @line L1
    if not kept:
        return [], [], Fraction(0)
    n = len(kept)
    big_p = max(profits[i] for i in kept)  # @line L3
    k = e * big_p / n  # @line L4
    scaled = [int(Fraction(profits[i]) / k) for i in kept]  # @line L5
    return kept, scaled, k


def knapsack_fptas(
    profits: list[int], weights: list[int], capacity: int, eps: Number
) -> list[int]:
    """Return a feasible set of 0-based item indices, sorted.

    The profit of the set is at least (1 - eps) times the optimum (Ibarra
    and Kim 1975). The table has n + 1 rows and Q + 1 columns, where Q is
    the sum of the scaled profits and Q <= n * floor(n / eps), so the time
    and the space are O(n^3 / eps) for the n items that fit alone.
    """
    kept, scaled, _ = scale_profits(profits, weights, capacity, eps)
    if not kept:  # @line L2
        return []
    n = len(kept)
    total = sum(scaled)
    inf = float("inf")
    table = [[0] + [inf] * total]  # @line L6
    for j in range(1, n + 1):  # @line L7
        prev = table[j - 1]
        pj, wj = scaled[j - 1], weights[kept[j - 1]]
        row = prev[:]  # @line L8 @line L9
        for q in range(pj, total + 1):
            if prev[q - pj] + wj < row[q]:  # @line L10
                row[q] = prev[q - pj] + wj
        table.append(row)
    best = max(q for q in range(total + 1) if table[n][q] <= capacity)  # @line L11
    chosen = []
    q = best
    for j in range(n, 0, -1):  # @line L12
        if table[j][q] != table[j - 1][q]:
            chosen.append(kept[j - 1])
            q -= scaled[j - 1]
    return sorted(chosen)  # @line L13
