# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/systematic-sampling/. The authors are listed in prov/JDXKJ0.jsonl.

import random
from fractions import Fraction

import pytest

from systematic_sampling import estimate_mean, systematic_positions, systematic_sampling


class FixedStart:
    """A fake source whose randrange returns a chosen start."""

    def __init__(self, r: int) -> None:
        self.r = r
        self.sizes: list[int] = []

    def randrange(self, size: int) -> int:
        self.sizes.append(size)
        return self.r


def all_samples(big_n: int, n: int) -> list[list[int]]:
    """The N equally likely position lists, one per start r."""
    out = []
    for r in range(big_n):
        src = FixedStart(r)
        out.append(systematic_positions(big_n, n, src))  # type: ignore[arg-type]
        assert src.sizes == [big_n]
    return out


def test_worked_example_classical_step() -> None:
    # N = 12, n = 3, step k = 4: starts 0..3 give the four possible samples.
    samples = {tuple(p) for p in all_samples(12, 3)}
    assert samples == {(0, 4, 8), (1, 5, 9), (2, 6, 10), (3, 7, 11)}


def test_worked_example_fractional_step() -> None:
    # N = 10, n = 4, step 2.5; start r = 7 gives floor(7/4), floor(17/4), ...
    assert systematic_positions(10, 4, FixedStart(7)) == [1, 4, 6, 9]  # type: ignore[arg-type]


@pytest.mark.parametrize("big_n", range(1, 13))
def test_exact_inclusion_probability(big_n: int) -> None:
    for n in range(1, big_n + 1):
        samples = all_samples(big_n, n)
        for p in samples:
            assert len(p) == n
            assert p == sorted(set(p))
            assert 0 <= p[0] and p[-1] < big_n
        for j in range(big_n):
            hits = sum(j in p for p in samples)
            assert Fraction(hits, big_n) == Fraction(n, big_n)


def exact_mean_and_variance(y: list[int], n: int) -> tuple[Fraction, Fraction]:
    means = [Fraction(sum(y[j] for j in p), n) for p in all_samples(len(y), n)]
    m = sum(means) / len(means)
    v = sum((x - m) ** 2 for x in means) / len(means)
    return m, v


def srs_variance(y: list[int], n: int) -> Fraction:
    big_n = len(y)
    mu = Fraction(sum(y), big_n)
    s2 = sum((Fraction(v) - mu) ** 2 for v in y) / (big_n - 1)
    return (1 - Fraction(n, big_n)) * s2 / n


def test_unbiased_and_trend_and_period() -> None:
    trend = list(range(1, 13))
    m, v = exact_mean_and_variance(trend, 3)
    assert m == Fraction(13, 2)
    assert v == Fraction(5, 4)
    assert srs_variance(trend, 3) == Fraction(13, 4)

    periodic = [10, 0, 0, 0] * 3
    m, v = exact_mean_and_variance(periodic, 3)
    assert m == Fraction(5, 2)
    assert v == Fraction(75, 4)
    assert srs_variance(periodic, 3) == Fraction(225, 44)

    rng = random.Random(1)
    for _ in range(200):
        big_n = rng.randrange(1, 30)
        n = rng.randrange(1, big_n + 1)
        y = [rng.randrange(-5, 20) for _ in range(big_n)]
        m, _ = exact_mean_and_variance(y, n)
        assert m == Fraction(sum(y), big_n)


def test_items_wrapper_and_errors() -> None:
    rng = random.Random(2)
    items = list("abcdefghij")
    out = systematic_sampling(items, 4, rng)
    assert len(out) == 4 and out == sorted(set(out))
    assert estimate_mean([1.0, 2.0, 6.0]) == 3.0
    with pytest.raises(ValueError):
        systematic_positions(5, 0, rng)
    with pytest.raises(ValueError):
        systematic_positions(5, 6, rng)
