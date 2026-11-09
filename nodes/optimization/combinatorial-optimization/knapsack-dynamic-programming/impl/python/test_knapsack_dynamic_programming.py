# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knapsack-dynamic-programming/. The authors are listed in prov/2ST7VJ.jsonl.

import random
from itertools import combinations

from knapsack_dynamic_programming import knapsack_dynamic_programming, knapsack_value


def brute_force(weights: list[int], values: list[int], capacity: int) -> int:
    n = len(weights)
    best = 0
    for r in range(n + 1):
        for s in combinations(range(n), r):
            if sum(weights[i] for i in s) <= capacity:
                best = max(best, sum(values[i] for i in s))
    return best


def check(weights: list[int], values: list[int], capacity: int) -> int:
    best, chosen = knapsack_dynamic_programming(weights, values, capacity)
    assert chosen == sorted(set(chosen))
    assert sum(weights[i] for i in chosen) <= capacity
    assert sum(values[i] for i in chosen) == best
    assert knapsack_value(weights, values, capacity) == best
    return best


def test_example() -> None:
    w, v = [5, 4, 6, 3], [10, 40, 30, 50]
    assert knapsack_dynamic_programming(w, v, 10) == (90, [1, 3])
    assert check(w, v, 10) == 90


def test_edges() -> None:
    assert knapsack_dynamic_programming([], [], 0) == (0, [])
    assert knapsack_dynamic_programming([], [], 7) == (0, [])
    assert knapsack_dynamic_programming([3], [5], 0) == (0, [])
    assert knapsack_dynamic_programming([3], [5], 2) == (0, [])
    assert knapsack_dynamic_programming([3], [5], 3) == (5, [0])
    assert check([2, 2, 2, 2], [3, 3, 3, 3], 5) == 6
    assert check([0, 4], [7, 1], 3) == 7


def test_ratio_greedy_trap() -> None:
    # The ratio greedy takes item 0 and loses item 1.
    assert knapsack_dynamic_programming([1, 100], [2, 100], 100) == (100, [1])


def test_one_row_order_matters() -> None:
    # A loop over capacities from low to high would use the item twice.
    assert knapsack_value([2], [3], 4) == 3


def test_large_numbers() -> None:
    big = 2**62
    assert check([1, 2, 3], [big, big, big], 3) == 2 * big


def test_random_against_brute_force() -> None:
    rng = random.Random(4421)
    for _ in range(600):
        n = rng.randint(0, 9)
        weights = [rng.randint(1, 15) for _ in range(n)]
        values = [rng.randint(0, 30) for _ in range(n)]
        capacity = rng.randint(0, 40)
        assert check(weights, values, capacity) == brute_force(weights, values, capacity)
