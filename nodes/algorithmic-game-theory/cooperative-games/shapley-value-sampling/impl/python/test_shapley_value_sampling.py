# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shapley-value-sampling/. The authors are listed in prov/SB0VDK.jsonl.

import random
from fractions import Fraction
from itertools import combinations, permutations
from math import factorial

import pytest

from shapley_value_sampling import hoeffding_failure_bound, samples_needed, shapley_sampling


def exact_shapley(n, v):
    """The subset formula, in Fraction."""
    phi = []
    for i in range(n):
        others = [j for j in range(n) if j != i]
        t = Fraction(0)
        for r in range(n):
            w = Fraction(factorial(r) * factorial(n - 1 - r), factorial(n))
            for S in combinations(others, r):
                S = frozenset(S)
                t += w * (v(S | {i}) - v(S))
        phi.append(t)
    return phi


def weighted_voting(q, weights):
    return lambda S: 1 if sum(weights[i] for i in S) >= q else 0


def random_game(rng, n, hi):
    table = {frozenset(): 0}
    for r in range(1, n + 1):
        for S in combinations(range(n), r):
            table[frozenset(S)] = rng.randint(0, hi)
    return table.__getitem__


class AllOrders:
    """A stand-in for random.Random whose shuffle returns each order of range(n) in turn."""

    def __init__(self, n):
        self.orders = list(permutations(range(n)))
        self.k = 0

    def shuffle(self, a):
        a[:] = self.orders[self.k % len(self.orders)]
        self.k += 1


def test_all_orders_gives_the_exact_value():
    # With each of the n! orders once, the estimate is the order formula itself.
    rng = random.Random(1)
    for n in (1, 2, 3, 4):
        v = random_game(rng, n, 9)
        est = shapley_sampling(n, lambda S: Fraction(v(S)), factorial(n), AllOrders(n))
        assert est == exact_shapley(n, v)


def test_check_value_with_hoeffding_sample_size():
    v = weighted_voting(51, [50, 49, 1])
    exact = [2 / 3, 1 / 6, 1 / 6]
    eps, delta = 0.05, 0.01
    m = samples_needed(1, eps, delta, players=3)
    assert m == 1280
    for seed in range(10):
        est = shapley_sampling(3, v, m, random.Random(seed))
        assert max(abs(a - b) for a, b in zip(est, exact)) < eps


def test_efficiency_of_every_estimate():
    rng = random.Random(3)
    for _ in range(20):
        n = rng.randint(1, 6)
        v = random_game(rng, n, 20)
        est = shapley_sampling(n, v, rng.randint(1, 30), rng)
        assert abs(sum(est) - v(frozenset(range(n)))) < 1e-9


def test_failure_rate_is_within_the_hoeffding_bound():
    # Glove game: player 0 holds the left glove, players 1 and 2 hold right gloves.
    v = lambda S: min(len(S & {0}), len(S & {1, 2}))
    exact = [2 / 3, 1 / 6, 1 / 6]
    m, eps, trials = 60, 0.15, 400
    bound = hoeffding_failure_bound(1, eps, m)
    rng = random.Random(11)
    fails = [0, 0, 0]
    for _ in range(trials):
        est = shapley_sampling(3, v, m, rng)
        for i in range(3):
            fails[i] += abs(est[i] - exact[i]) >= eps
    assert bound < 0.15
    for f in fails:
        assert f / trials <= bound


def test_random_games_within_eps():
    rng = random.Random(2009)
    for _ in range(4):
        n = 5
        v = random_game(rng, n, 10)
        exact = [float(x) for x in exact_shapley(n, v)]
        # Values in [0, 10], so each marginal contribution lies in [-10, 10]: r = 20.
        m = samples_needed(20, 1.0, 0.01, players=n)
        est = shapley_sampling(n, v, m, rng)
        assert max(abs(a - b) for a, b in zip(est, exact)) < 1.0


def test_airport_cost_game():
    costs = [1, 3, 6]
    v = lambda S: max((costs[i] for i in S), default=0)
    exact = [1 / 3, 4 / 3, 13 / 3]
    m = samples_needed(6, 0.25, 0.01, players=3)
    est = shapley_sampling(3, v, m, random.Random(5))
    assert max(abs(a - b) for a, b in zip(est, exact)) < 0.25


def test_bad_input():
    with pytest.raises(ValueError):
        shapley_sampling(3, lambda S: 0, 0, random.Random(0))
    with pytest.raises(ValueError):
        samples_needed(1, 0, 0.1)
    with pytest.raises(ValueError):
        samples_needed(1, 0.1, 1.5)
