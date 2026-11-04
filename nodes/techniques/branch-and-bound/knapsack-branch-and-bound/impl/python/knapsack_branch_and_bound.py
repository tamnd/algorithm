# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knapsack-branch-and-bound/. The authors are listed in prov/0VCNY1.jsonl.

from collections.abc import Sequence
from fractions import Fraction


def knapsack_branch_and_bound(
    values: Sequence[int],
    weights: Sequence[int],
    capacity: int,
    stats: dict[str, int] | None = None,
) -> tuple[int, list[int]]:
    """Solve the 0-1 knapsack problem by depth-first branch and bound.

    Values, weights and the capacity are nonnegative integers. The bound is
    the floor of the fractional (Dantzig) bound, computed in exact integer
    arithmetic. Returns the optimal value and the sorted indices of one
    optimal set of items.
    """
    if stats is None:
        stats = {}
    stats.update(nodes=0, max_stack=0)
    n = len(values)
    # Sort by value per unit weight, nonincreasing; items of weight 0 first.
    order = sorted(range(n), key=lambda i: (weights[i] > 0, -Fraction(values[i], weights[i]) if weights[i] else 0, i))
    v = [values[i] for i in order]
    w = [weights[i] for i in order]

    def bound(k: int, cw: int, cv: int) -> int:
        room = capacity - cw
        for j in range(k, n):
            if w[j] <= room:
                room -= w[j]
                cv += v[j]
            else:
                return cv + v[j] * room // w[j]
        return cv

    z = 0  # @line L1
    best: tuple[int, ...] = ()  # @line L1
    stack: list[tuple[int, int, int, tuple[int, ...]]] = [(0, 0, 0, ())]  # @line L2
    while stack:  # @line L3
        k, cw, cv, chosen = stack.pop()  # @line L4
        stats["nodes"] += 1
        if cv > z:  # @line L5
            z, best = cv, chosen
        if k == n or bound(k, cw, cv) <= z:  # @line L6
            continue
        if bound(k + 1, cw, cv) > z:  # @line L7
            stack.append((k + 1, cw, cv, chosen))  # @line L8
        if cw + w[k] <= capacity:  # @line L9
            stack.append((k + 1, cw + w[k], cv + v[k], chosen + (k,)))  # @line L10
        stats["max_stack"] = max(stats["max_stack"], len(stack))
    return z, sorted(order[j] for j in best)  # @line L11

