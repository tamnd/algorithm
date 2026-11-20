# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/power-index-dynamic-programming/. The authors are listed in prov/MQFKCA.jsonl.

import random
from fractions import Fraction
from itertools import combinations, permutations
from math import comb, factorial

import pytest

from power_index_dynamic_programming import player_indices, power_indices, swings_by_size


def wins(weights, q, S):
    return sum(weights[j] for j in S) >= q


def brute_swings(weights, q, i):
    others = [j for j in range(len(weights)) if j != i]
    return sum(
        1
        for r in range(len(others) + 1)
        for S in combinations(others, r)
        if not wins(weights, q, S) and wins(weights, q, S + (i,))
    )


def brute_shapley_shubik(weights, q, i):
    """The subset formula of the Shapley value for the simple game."""
    n = len(weights)
    others = [j for j in range(n) if j != i]
    total = Fraction(0)
    for r in range(n):
        for S in combinations(others, r):
            if not wins(weights, q, S) and wins(weights, q, S + (i,)):
                total += Fraction(factorial(r) * factorial(n - 1 - r), factorial(n))
    return total


def pivot_counts(weights, q):
    """Count, over all n! orders, how often each player is the pivot."""
    n = len(weights)
    count = [0] * n
    for order in permutations(range(n)):
        t = 0
        for j in order:
            t += weights[j]
            if t >= q:
                count[j] += 1
                break
    return count


def test_check_value_51_50_49_1():
    r = power_indices([50, 49, 1], 51)
    assert r["swings"] == [3, 1, 1]
    assert r["banzhaf_raw"] == [Fraction(3, 4), Fraction(1, 4), Fraction(1, 4)]
    assert r["banzhaf_normalized"] == [Fraction(3, 5), Fraction(1, 5), Fraction(1, 5)]
    assert r["shapley_shubik"] == [Fraction(2, 3), Fraction(1, 6), Fraction(1, 6)]


def test_eec_1958_council():
    r = power_indices([4, 4, 4, 2, 2, 1], 12)
    assert r["swings"] == [10, 10, 10, 6, 6, 0]
    assert r["banzhaf_normalized"] == [Fraction(5, 21)] * 3 + [Fraction(1, 7)] * 2 + [Fraction(0)]
    assert r["shapley_shubik"] == [Fraction(7, 30)] * 3 + [Fraction(3, 20)] * 2 + [Fraction(0)]


def test_swings_by_size_small():
    # [51; 50, 49, 1], player 0: the swings are {1} and {2} (size 1) and {1, 2} (size 2).
    assert swings_by_size([50, 49, 1], 51, 0) == [0, 2, 1]


def test_random_against_enumeration():
    rng = random.Random(20251120)
    for _ in range(60):
        n = rng.randint(1, 9)
        weights = [rng.randint(0, 12) for _ in range(n)]
        if sum(weights) == 0:
            weights[0] = 1
        q = rng.randint(1, sum(weights))
        r = power_indices(weights, q)
        for i in range(n):
            assert r["swings"][i] == brute_swings(weights, q, i)
            assert r["banzhaf_raw"][i] == Fraction(brute_swings(weights, q, i), 2 ** (n - 1))
            assert r["shapley_shubik"][i] == brute_shapley_shubik(weights, q, i)
        assert sum(r["shapley_shubik"]) == 1
        assert sum(r["banzhaf_normalized"]) == 1


def test_against_orders():
    rng = random.Random(7)
    for _ in range(15):
        n = rng.randint(2, 6)
        weights = [rng.randint(1, 9) for _ in range(n)]
        q = rng.randint(1, sum(weights))
        counts = pivot_counts(weights, q)
        r = power_indices(weights, q)
        assert r["shapley_shubik"] == [Fraction(c, factorial(n)) for c in counts]


def test_equal_weights_closed_form():
    n, k = 14, 8
    r = power_indices([1] * n, k)
    assert r["shapley_shubik"] == [Fraction(1, n)] * n
    assert r["swings"] == [comb(n - 1, k - 1)] * n


def test_large_weights_one_player_dominates():
    # A player with weight at least q swings in every coalition of weight < q.
    weights = [100, 3, 3, 3]
    swings, beta, phi = player_indices(weights, 100, 0)
    assert swings == 8 and beta == 1 and phi == 1


def test_zero_weight_player_is_dummy():
    r = power_indices([3, 0, 2, 2], 4)
    assert r["swings"][1] == 0 and r["shapley_shubik"][1] == 0


def test_bad_input():
    with pytest.raises(ValueError):
        power_indices([1, 2], 0)
    with pytest.raises(ValueError):
        power_indices([1, 2], 4)
    with pytest.raises(ValueError):
        power_indices([1, -2, 5], 3)
