# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-median-inapproximability/. The authors are listed in prov/C8XWBD.jsonl.

import math
import random

from k_median_inapproximability import coverage_to_k_median, is_metric, k_median_opt, max_coverage_opt


def random_system(rng, n, m, p=0.35):
    return [frozenset(e for e in range(n) if rng.random() < p) for _ in range(m)]


def test_example() -> None:
    sets = [frozenset(s) for s in ({0, 1, 2}, {3, 4, 5}, {0, 3}, {1, 4}, {2, 5})]
    d = coverage_to_k_median(6, sets)
    assert is_metric(d)
    fac, cli = list(range(5)), list(range(5, 11))
    assert k_median_opt(d, fac, cli, 2) == 6
    assert k_median_opt(d, fac, cli, 1) == 6 + 2 * 3


def test_cost_identity_and_metric() -> None:
    rng = random.Random(5)
    for _ in range(150):
        n, m = rng.randint(1, 7), rng.randint(1, 6)
        sets = random_system(rng, n, m)
        d = coverage_to_k_median(n, sets)
        assert len(d) == n + m
        assert is_metric(d)
        fac, cli = list(range(m)), list(range(m, m + n))
        for k in range(1, m + 1):
            assert k_median_opt(d, fac, cli, k) == n + 2 * (n - max_coverage_opt(n, sets, k))


def test_gap_numbers() -> None:
    # Yes: k sets cover all n elements, cost n. No: every k sets cover at most (1 - 1/e + eps) n.
    for eps in (0.1, 0.01, 0.001):
        n = 10**6
        no_cost = n + 2 * (n - (1 - 1 / math.e + eps) * n)
        assert abs(no_cost / n - (1 + 2 / math.e - 2 * eps)) < 1e-9
