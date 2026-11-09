# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-fractional-knapsack/. The authors are listed in prov/Q1RH1S.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from greedy_fractional_knapsack import dual_certificate, greedy_fractional_knapsack


def lp_brute_force(weights: list[int], values: list[int], capacity: int) -> Fraction:
    """Optimum of the relaxation over all basic solutions.

    A basic solution takes a set S whole and at most one more item j in part,
    so the maximum over all (S, j) is the optimum of the linear program.
    """
    n = len(weights)
    best = Fraction(0)
    for r in range(n + 1):
        for s in combinations(range(n), r):
            ws = sum(weights[i] for i in s)
            if ws > capacity:
                continue
            vs = Fraction(sum(values[i] for i in s))
            best = max(best, vs)
            for j in range(n):
                if j not in s:
                    part = min(Fraction(1), Fraction(capacity - ws, weights[j]))
                    best = max(best, vs + values[j] * part)
    return best


def check(weights: list[int], values: list[int], capacity: int) -> Fraction:
    total, x = greedy_fractional_knapsack(weights, values, capacity)
    assert all(0 <= xi <= 1 for xi in x)
    assert sum(w * xi for w, xi in zip(weights, x)) <= capacity
    assert sum(v * xi for v, xi in zip(values, x)) == total
    assert sum(1 for xi in x if 0 < xi < 1) <= 1
    lam, mu = dual_certificate(weights, values, capacity)
    assert lam >= 0 and all(m >= 0 for m in mu)
    assert all(lam * w + m >= v for w, v, m in zip(weights, values, mu))
    assert capacity * lam + sum(mu) == total
    return total


def test_example() -> None:
    total, x = greedy_fractional_knapsack([5, 4, 6, 3], [10, 40, 30, 50], 10)
    assert total == 105
    assert x == [0, 1, Fraction(1, 2), 1]
    assert check([5, 4, 6, 3], [10, 40, 30, 50], 10) == 105


def test_edges() -> None:
    assert greedy_fractional_knapsack([], [], 5) == (0, [])
    assert greedy_fractional_knapsack([4], [8], 0) == (0, [0])
    assert greedy_fractional_knapsack([4], [8], 3) == (6, [Fraction(3, 4)])
    assert greedy_fractional_knapsack([4], [8], 9) == (8, [1])
    assert check([2, 2, 2], [6, 6, 6], 5) == 15
    assert check([3, 1], [0, 0], 2) == 0


def test_ratio_ties_and_exact_comparison() -> None:
    # 1/3 and 2/6 tie exactly. The ratios (big + 2) / (big + 1) and
    # (big + 1) / big are equal as floats, but the second is larger, so a
    # float sort that keeps the input order would start with the wrong item.
    big = 2**60
    assert check([3, 6, 5], [1, 2, 1], 7) == Fraction(7, 3)
    assert float(Fraction(big + 2, big + 1)) == float(Fraction(big + 1, big))
    total, x = greedy_fractional_knapsack([big + 1, big], [big + 2, big + 1], big)
    assert x == [0, 1]
    assert total == big + 1
    assert total > Fraction((big + 2) * big, big + 1)


def test_greedy_is_not_optimal_for_0_1() -> None:
    total, x = greedy_fractional_knapsack([1, 100], [2, 100], 100)
    assert total == Fraction(2 + 99)
    assert x == [1, Fraction(99, 100)]


def test_random_against_vertex_enumeration() -> None:
    rng = random.Random(7781)
    for _ in range(600):
        n = rng.randint(0, 7)
        weights = [rng.randint(1, 12) for _ in range(n)]
        values = [rng.randint(0, 20) for _ in range(n)]
        capacity = rng.randint(0, 40)
        assert check(weights, values, capacity) == lp_brute_force(weights, values, capacity)
