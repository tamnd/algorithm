# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/round-robin-allocation/. The authors are listed in prov/MZAAJ5.jsonl.

from typing import Optional, Sequence


def round_robin(values: Sequence[Sequence], order: Optional[Sequence[int]] = None) -> list[list[int]]:
    """Round-robin allocation of m indivisible goods to n agents.

    values[i][g] is the nonnegative additive value of agent i for good g,
    with goods 0..m-1. order is the picking order, a permutation of the
    agents (default 0, 1, ..., n-1). The agents pick in this order, again
    and again, and each pick takes the most valuable free good of the agent;
    ties go to the smallest good index. Returns the bundles, each a list of
    goods in the order of the picks.

    Cost: O(n m log m) time for the n sorts, then O(n m) for the picks,
    because each pointer of an agent only moves forward. Extra space O(n m).
    """
    n = len(values)
    if n == 0:
        raise ValueError("at least one agent is needed")
    m = len(values[0])
    if any(len(row) != m for row in values):
        raise ValueError("every agent needs a value for every good")
    if any(x < 0 for row in values for x in row):
        raise ValueError("values must be nonnegative")
    order = list(range(n)) if order is None else list(order)
    if sorted(order) != list(range(n)):
        raise ValueError("order must be a permutation of the agents")
    prefs = [sorted(range(m), key=lambda g, i=i: (-values[i][g], g)) for i in range(n)]  # @line L1
    bundles: list[list[int]] = [[] for _ in range(n)]
    free = [True] * m  # @line L2
    pointer = [0] * n
    t = 0
    left = m
    while left > 0:  # @line L3
        i = order[t % n]  # @line L4
        while not free[prefs[i][pointer[i]]]:  # @line L5
            pointer[i] += 1
        g = prefs[i][pointer[i]]
        bundles[i].append(g)  # @line L6
        free[g] = False
        left -= 1
        t += 1  # @line L7
    return bundles  # @line L8
