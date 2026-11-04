# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knapsack-branch-and-bound/. The authors are listed in prov/0VCNY1.jsonl.

import itertools
import math
import random

from knapsack_branch_and_bound import knapsack_branch_and_bound


def brute(values, weights, capacity):
    best = 0
    for mask in itertools.product([0, 1], repeat=len(values)):
        if sum(w for w, m in zip(weights, mask) if m) <= capacity:
            best = max(best, sum(v for v, m in zip(values, mask) if m))
    return best


def test_example_of_the_page() -> None:
    stats: dict[str, int] = {}
    assert knapsack_branch_and_bound([40, 30, 50, 10], [2, 5, 10, 5], 16, stats) == (90, [0, 2])
    assert stats == {"nodes": 8, "max_stack": 3}


def test_unsorted_input() -> None:
    assert knapsack_branch_and_bound([10, 50, 30, 40], [5, 10, 5, 2], 16) == (90, [1, 3])


def test_edges() -> None:
    assert knapsack_branch_and_bound([], [], 5) == (0, [])
    assert knapsack_branch_and_bound([7], [3], 0) == (0, [])
    assert knapsack_branch_and_bound([7], [3], 3) == (7, [0])
    assert knapsack_branch_and_bound([4, 6], [0, 0], 0) == (10, [0, 1])
    assert knapsack_branch_and_bound([0, 0], [1, 1], 5) == (0, [])


def test_hard_family_of_the_page() -> None:
    for n in (6, 10, 14):
        stats: dict[str, int] = {}
        assert knapsack_branch_and_bound([2] * n, [2] * n, n + 1, stats)[0] == n
        assert stats["nodes"] == math.comb(n + 1, n // 2) - 1


def test_random_against_brute_force() -> None:
    rng = random.Random(1960)
    for _ in range(800):
        n = rng.randint(0, 10)
        values = [rng.randint(0, 40) for _ in range(n)]
        weights = [rng.randint(0, 20) for _ in range(n)]
        capacity = rng.randint(0, 60)
        z, chosen = knapsack_branch_and_bound(values, weights, capacity)
        assert z == brute(values, weights, capacity)
        assert len(set(chosen)) == len(chosen)
        assert sum(weights[i] for i in chosen) <= capacity
        assert sum(values[i] for i in chosen) == z
