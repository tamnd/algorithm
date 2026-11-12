# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kingman-coalescent/. The authors are listed in prov/6QE1Y8.jsonl.

import math
import random
from fractions import Fraction

from kingman_coalescent import (
    expected_tmrca,
    expected_total_length,
    harmonic,
    root_split,
    segregating_sites,
    simulate,
    tmrca_and_length,
    var_tmrca,
    var_total_length,
    watterson_estimator,
    wright_fisher_pair_time,
)


def test_closed_forms_exact() -> None:
    for n in range(2, 40):
        assert expected_tmrca(n) == 2 * (1 - Fraction(1, n))
        assert expected_total_length(n) == 2 * harmonic(n - 1)
        b = sum((Fraction(1, i * i) for i in range(1, n)), Fraction(0))
        assert var_total_length(n) == 4 * b


def test_small_values() -> None:
    assert expected_tmrca(2) == 1 and expected_total_length(2) == 2
    assert expected_tmrca(10) == Fraction(9, 5)
    assert expected_total_length(10) == Fraction(7129, 1260)
    assert watterson_estimator(20, 10) == Fraction(20) / Fraction(7129, 2520)


def test_simulated_means_match() -> None:
    # 20000 runs with seed 1; the tolerance is 4 standard errors of the mean.
    rng = random.Random(1)
    n, reps = 10, 20000
    sum_t = sum_l = 0.0
    for _ in range(reps):
        t, length = tmrca_and_length(simulate(n, rng)[0])
        sum_t += t
        sum_l += length
    se_t = math.sqrt(float(var_tmrca(n)) / reps)
    se_l = math.sqrt(float(var_total_length(n)) / reps)
    assert abs(sum_t / reps - float(expected_tmrca(n))) < 4 * se_t
    assert abs(sum_l / reps - float(expected_total_length(n))) < 4 * se_l


def test_tree_has_every_label_once() -> None:
    rng = random.Random(2)
    for n in range(1, 12):
        _, tree = simulate(n, rng)
        stack, seen = [tree], []
        while stack:
            x = stack.pop()
            if isinstance(x, tuple):
                assert len(x) == 2
                stack.extend(x)
            else:
                seen.append(x)
        assert sorted(seen) == list(range(n))


def test_root_split_is_uniform() -> None:
    # Kingman: a side of the root split, taken at random, has j leaves with
    # probability 1/(n-1) for j = 1..n-1. Both sides are counted, so the
    # frequency is a mean of two indicators, with at most the variance of one.
    rng = random.Random(3)
    n, reps = 6, 30000
    counts = [0] * n
    for _ in range(reps):
        _, tree = simulate(n, rng)
        j = root_split(tree)
        counts[j] += 1
        counts[n - j] += 1
    p = 1 / (n - 1)
    se = math.sqrt(p * (1 - p) / reps)
    for j in range(1, n):
        assert abs(counts[j] / (2 * reps) - p) < 4 * se


def test_watterson_is_unbiased() -> None:
    rng = random.Random(4)
    n, theta, reps = 8, 5.0, 20000
    a = float(harmonic(n - 1))
    b = float(sum((Fraction(1, i * i) for i in range(1, n)), Fraction(0)))
    total = sum(segregating_sites(n, theta, rng) for _ in range(reps))
    var_s = theta * a + theta * theta * b
    se = math.sqrt(var_s / reps) / a
    assert abs(total / reps / a - theta) < 4 * se


def test_wright_fisher_pair_time() -> None:
    # Geometric with success probability 1/N: mean N, variance N(N-1).
    rng = random.Random(5)
    pop, reps = 40, 20000
    mean = sum(wright_fisher_pair_time(pop, rng) for _ in range(reps)) / reps
    assert abs(mean - pop) < 4 * math.sqrt(pop * (pop - 1) / reps)
