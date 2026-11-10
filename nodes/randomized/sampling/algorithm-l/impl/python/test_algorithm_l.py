# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/algorithm-l/. The authors are listed in prov/ZE9C9M.jsonl.

import itertools
import math
import random

from algorithm_l import algorithm_l


def algorithm_r(stream, k, rng):
    """The reference method (Algorithm R), used as the oracle in distribution."""
    r = []
    for t, x in enumerate(stream, 1):
        if t <= k:
            r.append(x)
        else:
            j = rng.randrange(t)
            if j < k:
                r[j] = x
    return r


def frozen_w(stream, k, rng):
    """A known wrong version: W is drawn once and never updated (line L8 left out)."""
    it = iter(stream)
    r = list(itertools.islice(it, k))
    w = math.exp(math.log(1.0 - rng.random()) / k)
    while True:
        skip = math.floor(math.log(1.0 - rng.random()) / math.log1p(-w))
        x = next(itertools.islice(it, skip, None), None)
        if x is None:
            return r
        r[rng.randrange(k)] = x


class Counting:
    """A wrapper of a seeded generator that counts the calls of random and randrange."""

    def __init__(self, seed: int) -> None:
        self.rng = random.Random(seed)
        self.calls = 0

    def random(self) -> float:
        self.calls += 1
        return self.rng.random()

    def randrange(self, stop: int) -> int:
        self.calls += 1
        return self.rng.randrange(stop)


def chi2_threshold(df: int, z: float = 6.0) -> float:
    """Wilson-Hilferty approximation of the chi-squared quantile at about z normal deviations."""
    a = 2.0 / (9.0 * df)
    return df * (1.0 - a + z * math.sqrt(a)) ** 3


def subset_chi2(sampler, n: int, k: int, trials: int, seed: int) -> float:
    rng = random.Random(seed)
    cells = list(itertools.combinations(range(n), k))
    counts = dict.fromkeys(cells, 0)
    for _ in range(trials):
        counts[tuple(sorted(sampler(range(n), k, rng)))] += 1
    e = trials / len(cells)
    return sum((c - e) ** 2 / e for c in counts.values())


def test_edges() -> None:
    rng = random.Random(1)
    assert algorithm_l([], 3, rng) == []
    assert algorithm_l([5, 6], 3, rng) == [5, 6]
    assert algorithm_l([5, 6, 7], 0, rng) == []
    assert sorted(algorithm_l([5, 6, 7], 3, rng)) == [5, 6, 7]
    assert algorithm_l(iter([9, 9, 9, 9, 9]), 2, rng) == [9, 9]


def test_sample_is_a_subset() -> None:
    rng = random.Random(2)
    for _ in range(500):
        n = rng.randrange(0, 60)
        k = rng.randrange(0, 10)
        out = algorithm_l(iter(range(n)), k, rng)
        assert len(out) == min(n, k)
        assert len(set(out)) == len(out)
        assert all(0 <= x < n for x in out)


def test_same_distribution_as_algorithm_r() -> None:
    n, k, trials = 12, 3, 44000
    df = math.comb(n, k) - 1
    assert subset_chi2(algorithm_l, n, k, trials, 3) < chi2_threshold(df)
    assert subset_chi2(algorithm_r, n, k, trials, 4) < chi2_threshold(df)


def test_inclusion_probability_long_stream() -> None:
    n, k, trials = 200, 5, 20000
    rng = random.Random(5)
    counts = [0] * n
    for _ in range(trials):
        for x in algorithm_l(range(n), k, rng):
            counts[x] += 1
    e = trials * k / n
    chi2 = sum((c - e) ** 2 / e for c in counts)
    assert chi2 < chi2_threshold(n - 1)


def test_wrong_version_fails() -> None:
    n, k, trials = 12, 3, 44000
    assert subset_chi2(frozen_w, n, k, trials, 6) > chi2_threshold(math.comb(n, k) - 1)


def test_number_of_random_draws() -> None:
    n, k, runs = 100000, 10, 1000
    harmonic = sum(1.0 / t for t in range(k + 1, n + 1))
    expected = 2 + 3 * k * harmonic  # about 276.8
    total = 0
    for seed in range(runs):
        rng = Counting(seed)
        algorithm_l(range(n), k, rng)  # type: ignore[arg-type]
        total += rng.calls
    mean = total / runs
    # The count is 2 + 3R, where R is a sum of independent Bernoulli
    # variables with mean about 91.6, so the mean of 1000 runs has a
    # standard deviation below 1.
    assert abs(mean - expected) < 6.0
    assert mean < n / 300
