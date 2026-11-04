# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/best-first-branch-and-bound/. The authors are listed in prov/0SPYHN.jsonl.

import itertools
import random

from best_first_branch_and_bound import best_first_branch_and_bound, knapsack


def brute_knapsack(values, weights, capacity):
    best = 0
    for mask in itertools.product([0, 1], repeat=len(values)):
        if sum(w for w, m in zip(weights, mask) if m) <= capacity:
            best = max(best, sum(v for v, m in zip(values, mask) if m))
    return best


def test_example_of_the_page() -> None:
    stats: dict[str, int] = {}
    assert knapsack([40, 30, 50, 10], [2, 5, 10, 5], 16, stats) == (90, [0, 2])
    assert stats == {"expanded": 5, "generated": 9, "max_live": 4}


def test_edges() -> None:
    assert knapsack([], [], 10) == (0, [])
    assert knapsack([5], [3], 2) == (0, [])
    assert knapsack([5], [3], 3) == (5, [0])
    assert knapsack([5, 7], [0, 0], 0) == (12, [0, 1])
    # a tree without leaves: the root is a dead end
    assert best_first_branch_and_bound(0, lambda n: [], lambda n: 0, lambda n: False, lambda n: 0) == (float("-inf"), None)
    # the root is the only leaf
    assert best_first_branch_and_bound(0, lambda n: [], lambda n: 3, lambda n: True, lambda n: 3) == (3, 0)


def test_deep_tree() -> None:
    n = 5000
    z, best = best_first_branch_and_bound(
        0, lambda k: [k + 1], lambda k: n, lambda k: k == n, lambda k: k
    )
    assert (z, best) == (n, n)


def test_random_knapsack_against_brute_force() -> None:
    rng = random.Random(20240601)
    for _ in range(600):
        n = rng.randint(0, 9)
        values = [rng.randint(0, 30) for _ in range(n)]
        weights = [rng.randint(0, 15) for _ in range(n)]
        capacity = rng.randint(0, 40)
        z, chosen = knapsack(values, weights, capacity)
        assert z == brute_knapsack(values, weights, capacity)
        assert sum(weights[i] for i in chosen) <= capacity
        assert sum(values[i] for i in chosen) == z


def test_random_trees_against_brute_force() -> None:
    rng = random.Random(7)
    for _ in range(500):
        depth = rng.randint(0, 5)
        # node = tuple of child indices; leaves at full depth get random values
        table: dict[tuple[int, ...], int] = {}

        def kids(node: tuple[int, ...]) -> list[tuple[int, ...]]:
            return [node + (i,) for i in range(rng_kids[node])]

        rng_kids: dict[tuple[int, ...], int] = {}
        stack = [()]
        leaves = []
        while stack:
            node = stack.pop()
            if len(node) == depth:
                table[node] = rng.randint(-20, 20)
                leaves.append(node)
                continue
            rng_kids[node] = rng.randint(0, 3)
            stack.extend(node + (i,) for i in range(rng_kids[node]))

        def ub(node: tuple[int, ...]) -> float:
            below = [table[x] for x in leaves if x[: len(node)] == node]
            return max(below) + rng.randint(0, 3) if below else -100

        z, best = best_first_branch_and_bound((), kids, ub, lambda x: len(x) == depth, lambda x: table[x])
        if leaves:
            assert z == max(table.values())
            assert best is not None and table[best] == z
        else:
            assert (z, best) == (float("-inf"), None)
