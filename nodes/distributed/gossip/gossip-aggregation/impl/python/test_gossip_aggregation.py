# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gossip-aggregation/. The authors are listed in prov/2FN2GA.jsonl.

import math
import random

from gossip_aggregation import aggregate, convergence_factor, count_with_epochs, pairs, run_cycle


def test_pair_selectors():
    rng = random.Random(1)
    n = 100
    pm = pairs("pm", n, rng)
    seen = [0] * n
    for i, j in pm:
        assert i != j
        seen[i] += 1
        seen[j] += 1
    assert seen == [2] * n
    distr = pairs("distr", n, rng)
    assert sorted(i for i, _ in distr) == list(range(n))
    assert all(i != j for i, j in distr)
    assert len(pairs("rand", n, rng)) == n


def test_mean_is_kept():
    rng = random.Random(7)
    x = [rng.uniform(-5, 5) for _ in range(500)]
    total = sum(x)
    for kind in ("pm", "rand", "distr"):
        y = list(x)
        for _ in range(10):
            run_cycle(y, kind, rng)
        assert abs(sum(y) - total) < 1e-9


def test_convergence_factors():
    # Jelasity, Montresor and Babaoglu: E(2^-phi) with phi = 2, Poisson(2)
    # and 1 + Poisson(1) exchanges per node per cycle.
    target = {"pm": 0.25, "rand": math.exp(-1), "distr": 1 / (2 * math.sqrt(math.e))}
    for kind, rho in target.items():
        got = convergence_factor(kind, 4000, 8, 3)
        assert abs(got - rho) < 0.015, (kind, got, rho)


def test_derived_aggregates():
    rng = random.Random(3)
    x = [rng.uniform(1, 10) for _ in range(1000)]
    n = len(x)
    mean = sum(x) / n
    geo = math.exp(sum(math.log(v) for v in x) / n)
    var = sum(v * v for v in x) / n - mean * mean
    assert all(v == max(x) for v in aggregate(x, "max", 30, 1))
    assert all(v == min(x) for v in aggregate(x, "min", 30, 1))
    assert max(abs(v - mean) for v in aggregate(x, "mean", 40, 1)) < 1e-6
    assert max(abs(v - geo) for v in aggregate(x, "geometric", 40, 1)) < 1e-6
    assert max(abs(v - var) for v in aggregate(x, "variance", 40, 1)) < 1e-5


def test_count_without_churn():
    for seed in range(3):
        for start, end, est in count_with_epochs(2000, 2, 40, 0.0, seed):
            assert start == end == 2000
            assert abs(est - 2000) / 2000 < 1e-3


def test_count_with_churn_and_restarts():
    for seed in range(3):
        epochs = count_with_epochs(2000, 3, 30, 0.002, seed)
        for start, end, est in epochs:
            # the estimate lies between the size at the end of the epoch and
            # the size at its start, so a restart keeps it close to the truth
            assert end < start
            assert 0.95 * end <= est <= 1.05 * start
