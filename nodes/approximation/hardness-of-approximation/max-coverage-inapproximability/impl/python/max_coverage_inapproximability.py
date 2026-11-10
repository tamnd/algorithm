# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/max-coverage-inapproximability/. The authors are listed in prov/7DN3DJ.jsonl.
"""Set cover from a maximum coverage algorithm, by covering in rounds of k sets.

Sets are frozensets of elements. An oracle takes (sets, k, remaining) and returns at most k set indices.
For small instances only: the exact oracle tries every choice of k sets.
"""

import math
from itertools import combinations
from typing import Callable

Oracle = Callable[[list[frozenset[int]], int, frozenset[int]], list[int]]


def covered(sets: list[frozenset[int]], chosen: list[int], within: frozenset[int]) -> int:
    return len(within & frozenset().union(*(sets[j] for j in chosen)))


def exact_oracle(sets: list[frozenset[int]], k: int, within: frozenset[int]) -> list[int]:
    best: tuple[int, ...] = ()
    for c in combinations(range(len(sets)), min(k, len(sets))):
        if covered(sets, list(c), within) > covered(sets, list(best), within):
            best = c
    return list(best)


def greedy_oracle(sets: list[frozenset[int]], k: int, within: frozenset[int]) -> list[int]:
    chosen: list[int] = []
    left = set(within)
    for _ in range(k):
        j = max(range(len(sets)), key=lambda i: len(sets[i] & left))
        chosen.append(j)
        left -= sets[j]
    return chosen


def rounds_needed(n: int, alpha: float) -> int:
    """The least t with (1 - alpha)^t n < 1, for 0 < alpha < 1."""
    if n <= 0:
        return 0
    return math.floor(math.log(n) / math.log(1 / (1 - alpha))) + 1


def cover_in_rounds(n: int, sets: list[frozenset[int]], k: int, oracle: Oracle, max_rounds: int) -> list[int] | None:
    """Call the oracle with budget k on the uncovered elements until all are covered, or give up."""
    remaining = frozenset(range(n))
    chosen: list[int] = []
    for _ in range(max_rounds):
        if not remaining:
            break
        picked = oracle(sets, k, remaining)
        chosen += picked
        remaining = remaining - frozenset().union(*(sets[j] for j in picked))
    return chosen if not remaining else None


def min_cover(n: int, sets: list[frozenset[int]]) -> int:
    for size in range(len(sets) + 1):
        for c in combinations(range(len(sets)), size):
            if covered(sets, list(c), frozenset(range(n))) == n:
                return size
    raise ValueError("no cover")
