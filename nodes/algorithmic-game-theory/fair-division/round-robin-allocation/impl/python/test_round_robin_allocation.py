# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/round-robin-allocation/. The authors are listed in prov/MZAAJ5.jsonl.

import itertools
import random

import pytest

from round_robin_allocation import round_robin


def value(row, bundle) -> int:
    return sum(row[g] for g in bundle)


def is_ef1(values, bundles) -> bool:
    """EF1 by its definition: try every good of the envied bundle."""
    n = len(values)
    for i in range(n):
        mine = value(values[i], bundles[i])
        for j in range(n):
            if i == j or not bundles[j]:
                continue
            other = value(values[i], bundles[j])
            if not any(mine >= other - values[i][g] for g in bundles[j]):
                return False
    return True


def envies(values, bundles, i, j) -> bool:
    return value(values[i], bundles[j]) > value(values[i], bundles[i])


def pareto_improvement(values, bundles):
    """Brute force over all n^m allocations; returns a dominating one or None."""
    n, m = len(values), len(values[0])
    u = [value(values[i], bundles[i]) for i in range(n)]
    for owner in itertools.product(range(n), repeat=m):
        w = [0] * n
        for g, i in enumerate(owner):
            w[i] += values[i][g]
        if all(w[i] >= u[i] for i in range(n)) and any(w[i] > u[i] for i in range(n)):
            return owner
    return None


def test_worked_example():
    values = [[8, 7, 4, 3, 2, 1], [8, 2, 6, 5, 1, 3], [6, 7, 5, 1, 4, 2]]
    bundles = round_robin(values)
    assert bundles == [[0, 3], [2, 5], [1, 4]]
    assert [value(values[i], bundles[i]) for i in range(3)] == [11, 9, 11]
    assert envies(values, bundles, 1, 0)
    assert value(values[1], [3]) <= 9  # removing good 0 ends the envy
    assert is_ef1(values, bundles)


def test_every_good_is_given_once():
    rng = random.Random(7)
    for _ in range(200):
        n, m = rng.randint(1, 5), rng.randint(0, 9)
        values = [[rng.randint(0, 9) for _ in range(m)] for _ in range(n)]
        bundles = round_robin(values)
        assert sorted(g for b in bundles for g in b) == list(range(m))
        sizes = [len(b) for b in bundles]
        assert max(sizes, default=0) - min(sizes, default=0) <= 1


def test_ef1_random_against_definition():
    rng = random.Random(2024)
    for _ in range(800):
        n, m = rng.randint(2, 4), rng.randint(1, 7)
        values = [[rng.randint(0, 10) for _ in range(m)] for _ in range(n)]
        order = list(range(n))
        rng.shuffle(order)
        bundles = round_robin(values, order)
        assert is_ef1(values, bundles)
        # the first agent to pick envies no one
        first = order[0]
        assert not any(envies(values, bundles, first, j) for j in range(n))


def test_ef1_identical_and_tied_values():
    for n in range(1, 5):
        for m in range(0, 8):
            values = [[1] * m for _ in range(n)]
            assert is_ef1(values, round_robin(values))
            values = [[m - g for g in range(m)] for _ in range(n)]
            assert is_ef1(values, round_robin(values))


def test_not_pareto_optimal():
    values = [[4, 3, 2, 1], [6, 3, 2, 1]]
    bundles = round_robin(values)
    assert bundles == [[0, 2], [1, 3]]
    assert [value(values[i], bundles[i]) for i in range(2)] == [6, 4]
    better = pareto_improvement(values, bundles)
    assert better is not None
    # A takes goods 1, 2, 3 and B takes good 0: (6, 6) dominates (6, 4)
    assert pareto_improvement(values, [[1, 2, 3], [0]]) is None


def greedy_round_robin(vals, m):
    """Round-robin for general valuations: each pick has the largest marginal value."""
    n = len(vals)
    bundles = [frozenset() for _ in range(n)]
    free = set(range(m))
    t = 0
    while free:
        i = t % n
        g = max(sorted(free), key=lambda g: (vals[i](bundles[i] | {g}) - vals[i](bundles[i]), -g))
        bundles[i] = bundles[i] | {g}
        free.remove(g)
        t += 1
    return bundles


def test_fails_for_a_submodular_valuation():
    # Agent B counts colours: red 2, blue 2, green 1. Goods 0..4 are red, blue, green, blue, blue.
    colour = ["red", "blue", "green", "blue", "blue"]
    weight = {"red": 2, "blue": 2, "green": 1}
    a = [5, 1, 4, 2, 3]

    def va(s):
        return sum(a[g] for g in s)

    def vb(s):
        return sum(weight[c] for c in {colour[g] for g in s})

    bundles = greedy_round_robin([va, vb], 5)
    assert bundles == [frozenset({0, 2, 4}), frozenset({1, 3})]
    assert vb(bundles[1]) == 2
    assert all(vb(bundles[0] - {g}) > 2 for g in bundles[0])


def test_bad_input():
    with pytest.raises(ValueError):
        round_robin([])
    with pytest.raises(ValueError):
        round_robin([[1, 2], [3]])
    with pytest.raises(ValueError):
        round_robin([[1, -1]])
    with pytest.raises(ValueError):
        round_robin([[1], [2]], order=[0, 0])
