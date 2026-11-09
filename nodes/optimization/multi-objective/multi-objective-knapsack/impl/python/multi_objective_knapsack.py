# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-objective-knapsack/. The authors are listed in prov/V5J5TR.jsonl.

"""The nondominated profit vectors of a multi-objective 0-1 knapsack problem.

On this page all objectives are maximized. Item j has a weight w_j >= 0 and
a profit vector c_j with p >= 1 entries. A subset S is feasible when its
weight is at most W. The answer is the set of profit vectors of feasible
subsets that no other feasible subset beats, with one subset for each.

The method is the dynamic program over the items. A state is a triple
(weight, profit vector, subset as a bit mask). After item j, a state is
removed when another state has a weight that is not larger and a profit
vector that is not smaller; every completion of the removed state is then
matched by the same completion of the other state. Exact arithmetic is
used: integers or fractions.
"""

from typing import List, Sequence, Tuple

State = Tuple[object, Tuple, int]


def _keep_nondominated(states: List[State]) -> List[State]:
    """Keep one state for each (weight, profit) pair that no other state
    beats: weight not larger and profit not smaller, with a difference."""
    states = sorted(states, key=lambda s: (s[0], tuple(-x for x in s[1])))
    kept: List[State] = []
    for w, v, mask in states:
        # Earlier states have weight <= w, so only they can beat this one.
        if any(all(a >= b for a, b in zip(u, v)) for _, u, _ in kept):
            continue
        kept.append((w, v, mask))
    return kept


def knapsack_front(
    weights: Sequence, profits: Sequence[Sequence], capacity
) -> List[Tuple[Tuple, int]]:
    """Return (profit vector, bit mask of a subset) pairs, one for each
    nondominated profit vector, sorted by profit vector."""
    n = len(weights)
    p = len(profits[0]) if n else 0
    states: List[State] = [(0, tuple(0 for _ in range(p)), 0)]  # @line L1
    for j in range(n):  # @line L2
        w, c = weights[j], tuple(profits[j])  # @line L3
        new = [  # @line L3
            (sw + w, tuple(a + b for a, b in zip(sv, c)), mask | (1 << j))  # @line L3
            for sw, sv, mask in states  # @line L3
            if sw + w <= capacity  # @line L3
        ]  # @line L3
        states = _keep_nondominated(states + new)  # @line L4
    best: dict = {}  # @line L5
    for _, v, mask in states:  # @line L5
        best.setdefault(v, mask)  # @line L5
    vs = list(best)  # @line L5
    front = [  # @line L5
        v for v in vs  # @line L5
        if not any(u != v and all(a >= b for a, b in zip(u, v)) for u in vs)  # @line L5
    ]  # @line L5
    return sorted((v, best[v]) for v in front)  # @line L6
