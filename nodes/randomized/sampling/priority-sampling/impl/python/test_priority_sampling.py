# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/priority-sampling/. The authors are listed in prov/RV0AAH.jsonl.

import math
import random

import pytest

from priority_sampling import priority_sample, subset_sum, variance_estimate


class Scripted:
    """Returns 1 - u for the given u, so that the code sees the uniform u in (0, 1]."""

    def __init__(self, us: list[float]) -> None:
        self.us = list(us)

    def random(self) -> float:
        return 1.0 - self.us.pop(0)


def test_worked_example() -> None:
    stream = [("a", 6.0), ("b", 1.0), ("c", 3.0), ("d", 0.5), ("e", 2.0), ("f", 4.0)]
    us = [0.75, 0.25, 0.6, 0.05, 0.8, 0.45]
    sample, tau = priority_sample(stream, 3, Scripted(us))  # type: ignore[arg-type]
    assert tau == pytest.approx(5.0)
    assert [(x, round(e, 9)) for x, _, e in sample] == [("d", 5.0), ("f", 5.0), ("a", 6.0)]
    assert subset_sum(sample, lambda x: True) == pytest.approx(16.0)
    assert variance_estimate(sample, tau, lambda x: True) == pytest.approx(27.5)


def test_small_streams_are_exact() -> None:
    rng = random.Random(1)
    stream = [("a", 2.0), ("b", 3.5)]
    sample, tau = priority_sample(stream, 2, rng)
    assert tau == 0.0
    assert sorted((x, e) for x, _, e in sample) == [("a", 2.0), ("b", 3.5)]
    assert priority_sample([], 3, rng) == ([], 0.0)
    with pytest.raises(ValueError):
        priority_sample(stream, 0, rng)
    with pytest.raises(ValueError):
        priority_sample([("a", 0.0)], 1, rng)


def test_sample_shape() -> None:
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randrange(0, 30)
        k = rng.randrange(1, 6)
        stream = [(i, rng.uniform(0.01, 5.0)) for i in range(n)]
        sample, tau = priority_sample(stream, k, rng)
        assert len(sample) == min(n, k)
        assert len({x for x, _, _ in sample}) == len(sample)
        for _, w, e in sample:
            assert e == max(w, tau)


WEIGHTS = [1.0, 2.0, 3.0, 5.0, 10.0, 20.0, 0.5, 4.0]


def simulate(k: int, trials: int, seed: int):
    """Per trial: the estimate of each item (0 if not sampled) and its variance estimate."""
    rng = random.Random(seed)
    stream = list(enumerate(WEIGHTS))
    rows = []
    for _ in range(trials):
        sample, tau = priority_sample(stream, k, rng)
        est = [0.0] * len(WEIGHTS)
        var_est = [0.0] * len(WEIGHTS)
        for x, w, e in sample:
            est[x] = e
            var_est[x] = tau * max(0.0, tau - w)
        rows.append((est, var_est))
    return rows


def z_score(values: list[float], target: float) -> float:
    m = sum(values) / len(values)
    var = sum((v - m) ** 2 for v in values) / (len(values) - 1)
    return (m - target) / math.sqrt(var / len(values))


def test_each_estimate_is_unbiased() -> None:
    rows = simulate(3, 40000, 3)
    for i, w in enumerate(WEIGHTS):
        assert abs(z_score([r[0][i] for r in rows], w)) < 5


def test_subset_sums_are_unbiased() -> None:
    rows = simulate(2, 40000, 4)
    for subset in ([0, 6], [1, 2, 3], [5], list(range(8))):
        target = sum(WEIGHTS[i] for i in subset)
        assert abs(z_score([sum(r[0][i] for i in subset) for r in rows], target)) < 5


def test_variance_estimate_is_unbiased() -> None:
    rows = simulate(3, 40000, 5)
    for i, w in enumerate(WEIGHTS):
        # E[estimate^2] - w^2 is the variance; it must equal the mean variance estimate.
        diffs = [r[0][i] ** 2 - w * w - r[1][i] for r in rows]
        assert abs(z_score(diffs, 0.0)) < 5


def test_products_are_unbiased_for_k_at_least_2() -> None:
    rows = simulate(3, 40000, 6)
    for i, j in ((0, 3), (4, 5), (2, 7)):
        assert abs(z_score([r[0][i] * r[0][j] for r in rows], WEIGHTS[i] * WEIGHTS[j])) < 5
    # With k = 1 two items are never sampled together, so the product is always 0.
    rows1 = simulate(1, 2000, 7)
    assert all(r[0][4] * r[0][5] == 0.0 for r in rows1)


def test_wrong_threshold_is_biased() -> None:
    # The wrong rule uses the k-th largest priority, the least one inside the sample.
    rng = random.Random(8)
    totals = []
    for _ in range(40000):
        pr = sorted(((w / (1.0 - rng.random()), w) for w in WEIGHTS), reverse=True)
        kth = pr[2][0]
        totals.append(sum(max(w, kth) for _, w in pr[:3]))
    assert z_score(totals, sum(WEIGHTS)) > 10
