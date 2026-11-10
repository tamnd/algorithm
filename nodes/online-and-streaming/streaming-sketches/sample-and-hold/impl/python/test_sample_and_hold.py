# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sample-and-hold/. The authors are listed in prov/HS0C9K.jsonl.

import math
import random
from collections import Counter
from fractions import Fraction

import pytest

from sample_and_hold import SampleAndHold


class ScriptedCoins:
    """A stand-in for random.Random: the first j calls fail, then all succeed."""

    def __init__(self, j: int) -> None:
        self.left = j

    def random(self) -> float:
        if self.left > 0:
            self.left -= 1
            return 0.999999
        return 0.0


def exact_distribution(p: Fraction, f: int):
    """All outcomes of the implementation on f units of one item, with their
    exact probabilities: j units are missed before the first sampled one."""
    q = 1 - p
    for j in range(f + 1):
        sh = SampleAndHold(p, ScriptedCoins(j))
        sh.extend(["x"] * f)
        prob = q**j * p if j < f else q**f
        yield prob, sh


def test_unbiased_and_variance_exactly() -> None:
    for p in (Fraction(1, 2), Fraction(1, 3), Fraction(1, 10), Fraction(2, 7), Fraction(1)):
        for f in range(0, 25):
            total = mean = second = Fraction(0)
            for prob, sh in exact_distribution(p, f):
                e = Fraction(sh.estimate("x"))
                assert sh.raw("x") <= f
                total += prob
                mean += prob * e
                second += prob * e * e
            assert total == 1
            assert mean == f  # unbiased
            var = second - mean * mean
            assert var <= (1 - p) / p**2
            if f >= 1:
                miss = (1 - p) ** f
                # The raw count is low by (1 - p)/p * (1 - (1 - p)^f) on average.
                raw_mean = sum(prob * sh.raw("x") for prob, sh in exact_distribution(p, f))
                assert raw_mean == f - (1 - p) / p * (1 - miss)


def test_example() -> None:
    # p = 1/2 and the coins fail, fail, succeed on the units of a.
    sh = SampleAndHold(Fraction(1, 2), ScriptedCoins(2))
    sh.extend(["a"] * 6)
    assert sh.raw("a") == 4 and sh.estimate("a") == 5


def test_edges() -> None:
    with pytest.raises(ValueError):
        SampleAndHold(0, random.Random(0))
    sh = SampleAndHold(1, random.Random(0))
    sh.extend("abcab")
    assert sh.count == {"a": 2, "b": 2, "c": 1}
    assert sh.estimate("a") == 2 and sh.estimate("z") == 0


def test_expected_entries_and_misses_seeded() -> None:
    # 20 large flows of 400 units and 6000 flows of 1 to 3 units, mixed.
    rng = random.Random(42)
    stream = [("big", i) for i in range(20) for _ in range(400)]
    stream += [("small", i) for i in range(6000) for _ in range(1 + i % 3)]
    rng.shuffle(stream)
    m = len(stream)
    threshold = 400
    oversampling = 4
    p = oversampling / threshold
    freq = Counter(stream)
    trials = 30
    entries = misses = 0
    big_err = []
    for seed in range(trials):
        sh = SampleAndHold(p, random.Random(seed))
        sh.extend(stream)
        entries += len(sh)
        for i in range(20):
            x = ("big", i)
            misses += x not in sh.count
            big_err.append(sh.estimate(x) - freq[x])
    n_big = 20 * trials
    # The mean number of entries is at most p * m; each run has variance at most p * m.
    assert entries / trials <= p * m + 3 * math.sqrt(p * m / trials)
    # A flow of size >= T is missed with probability <= e^(-O).
    bound = math.exp(-oversampling)
    assert misses / n_big <= bound + 3 * math.sqrt(bound * (1 - bound) / n_big)
    # Unbiased with standard deviation at most sqrt(1 - p)/p = 99.5 per flow.
    sd = math.sqrt(1 - p) / p
    assert abs(sum(big_err) / n_big) <= 3 * sd / math.sqrt(n_big)
    assert math.sqrt(sum(e * e for e in big_err) / n_big) <= 1.2 * sd
