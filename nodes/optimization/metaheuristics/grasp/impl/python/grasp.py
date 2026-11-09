# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grasp/. The authors are listed in prov/FPPN86.jsonl.

import random
from fractions import Fraction

Cover = frozenset[int]


def cover_cost(costs: list[int], x: Cover) -> int:
    """The total cost of the chosen sets."""
    return sum(costs[j] for j in x)


def covers(universe: set[int], sets: list[set[int]], x: Cover) -> bool:
    """True if the chosen sets cover the universe."""
    covered: set[int] = set()
    for j in x:
        covered |= sets[j]
    return universe <= covered


def greedy_randomized_construction(
    universe: set[int], sets: list[set[int]], costs: list[int], alpha: Fraction, rng: random.Random
) -> tuple[Cover, list[tuple[list[int], int]]]:
    """Build a cover one set at a time, each time a uniform pick from the restricted candidate list.

    The greedy ratio of set j is costs[j] / (number of uncovered elements in it); the
    list holds the sets with ratio <= r_min + alpha * (r_max - r_min). Returns the
    cover and the steps as (candidate list, chosen set). Needs the sets to cover
    the universe.
    """
    chosen: set[int] = set()
    uncovered = set(universe)
    steps: list[tuple[list[int], int]] = []
    while uncovered:  # @line L4
        ratio = {j: Fraction(costs[j], len(s & uncovered)) for j, s in enumerate(sets) if s & uncovered}  # @line L5
        if not ratio:
            raise ValueError("the sets do not cover the universe")
        lo, hi = min(ratio.values()), max(ratio.values())
        rcl = sorted(j for j, r in ratio.items() if r <= lo + alpha * (hi - lo))  # @line L6
        j = rng.choice(rcl)  # @line L7
        chosen.add(j)
        uncovered -= sets[j]
        steps.append((rcl, j))
    return frozenset(chosen), steps


def drop_and_swap_descent(universe: set[int], sets: list[set[int]], costs: list[int], x: Cover) -> Cover:
    """Best-improvement local search on covers: drop one set, or swap one chosen set for one unchosen set.

    Only moves that keep a cover are allowed. Ends at a cover with no improving drop or swap.
    """
    while True:
        best, best_cost = x, cover_cost(costs, x)
        for j in sorted(x):
            y = x - {j}
            if covers(universe, sets, y) and cover_cost(costs, y) < best_cost:
                best, best_cost = y, cover_cost(costs, y)
            for k in range(len(sets)):
                if k not in x:
                    y = (x - {j}) | {k}
                    if covers(universe, sets, y) and cover_cost(costs, y) < best_cost:
                        best, best_cost = y, cover_cost(costs, y)
        if best == x:
            return x
        x = best


def grasp(
    universe: set[int], sets: list[set[int]], costs: list[int], alpha: Fraction, iterations: int, rng: random.Random
) -> tuple[Cover, int, list[tuple[Cover, int, Cover, int]]]:
    """GRASP for weighted set cover (Feo and Resende).

    Each iteration builds a greedy randomized cover and improves it by local
    search; the best cover is kept. Returns (best, cost, log) with one entry
    (constructed, its cost, improved, its cost) per iteration. Precondition:
    iterations >= 1 and the union of the sets is the universe.
    """
    if iterations < 1:
        raise ValueError("iterations must be at least 1")
    best, best_cost = None, 0  # @line L1
    log: list[tuple[Cover, int, Cover, int]] = []
    for _ in range(iterations):  # @line L2
        x, _ = greedy_randomized_construction(universe, sets, costs, alpha, rng)  # @line L3
        z = drop_and_swap_descent(universe, sets, costs, x)  # @line L8
        log.append((x, cover_cost(costs, x), z, cover_cost(costs, z)))
        if best is None or cover_cost(costs, z) < best_cost:  # @line L9
            best, best_cost = z, cover_cost(costs, z)
    return best, best_cost, log  # @line L10
