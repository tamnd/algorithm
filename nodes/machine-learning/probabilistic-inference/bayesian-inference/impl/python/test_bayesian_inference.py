# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayesian-inference/. The authors are listed in prov/CSGT71.jsonl.

import random
from fractions import Fraction as F
from itertools import permutations

from bayesian_inference import (
    batch_update,
    evidence_sequence,
    grid_mean,
    grid_posterior,
    predictive_one,
    sequential_update,
)

DATA = [1, 1, 0, 1, 1, 0, 1, 1]


def test_worked_example() -> None:
    a, b = batch_update(F(2), F(2), DATA)
    assert (a, b) == (8, 4)
    assert predictive_one(a, b) == F(2, 3)
    path = sequential_update(F(2), F(2), DATA)
    assert [predictive_one(*p) for p in path] == [
        F(3, 5), F(2, 3), F(4, 7), F(5, 8), F(2, 3), F(3, 5), F(7, 11), F(2, 3)
    ]


def test_sequential_equals_batch_in_every_order() -> None:
    for a0, b0 in [(F(1), F(1)), (F(1, 2), F(1, 2)), (F(2), F(5))]:
        batch = batch_update(a0, b0, DATA)
        for order in set(permutations(DATA)):
            assert sequential_update(a0, b0, order)[-1] == batch


def test_sequential_equals_batch_random_data() -> None:
    rng = random.Random(42)
    for _ in range(100):
        n = rng.randint(1, 30)
        data = [rng.randint(0, 1) for _ in range(n)]
        a0, b0 = F(rng.randint(1, 9), rng.randint(1, 4)), F(rng.randint(1, 9), rng.randint(1, 4))
        # update on the first half, then use that posterior as the prior for the rest
        k = rng.randint(0, n)
        mid = batch_update(a0, b0, data[:k])
        assert batch_update(*mid, data[k:]) == batch_update(a0, b0, data)


def test_predictive_is_ratio_of_evidences() -> None:
    # Pr(x_{n+1} = 1 | D) = p(D, 1) / p(D)
    for a, b in [(1, 1), (2, 2), (3, 1)]:
        for data in ([1], [0, 0, 1], DATA):
            ratio = evidence_sequence(a, b, list(data) + [1]) / evidence_sequence(a, b, data)
            assert ratio == predictive_one(*batch_update(F(a), F(b), data))


def test_grid_posterior_mean_matches_conjugate() -> None:
    grid, w = grid_posterior(lambda t: t * (1 - t), DATA)  # Beta(2, 2) up to a constant
    assert abs(grid_mean(grid, w) - 2 / 3) < 1e-6


def test_welch_interval_coverage() -> None:
    # X1, X2 uniform on (theta - 1/2, theta + 1/2); interval [min, max]
    rng = random.Random(1939)
    theta, trials, covered = 3.0, 20000, 0
    for _ in range(trials):
        x1 = theta + rng.random() - 0.5
        x2 = theta + rng.random() - 0.5
        lo, hi = min(x1, x2), max(x1, x2)
        hit = lo <= theta <= hi
        covered += hit
        if hi - lo >= 0.5:
            assert hit
    assert abs(covered / trials - 0.5) < 0.015
