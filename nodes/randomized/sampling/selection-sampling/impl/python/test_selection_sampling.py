# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/selection-sampling/. The authors are listed in prov/2YMG5Q.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from selection_sampling import selection_sampling


class ScriptedRandom:
    """A fake source: randrange(size) returns the next scripted value (0 after the script)."""

    def __init__(self, script: list[int]) -> None:
        self.script = script
        self.calls: list[tuple[int, int]] = []

    def randrange(self, size: int) -> int:
        i = len(self.calls)
        v = self.script[i] if i < len(self.script) else 0
        assert 0 <= v < size
        self.calls.append((v, size))
        return v


def exact_distribution(run) -> dict:
    """Run run(source) over every sequence of random integers; add up exact probabilities."""
    dist: dict = {}
    script: list[int] = []
    while True:
        src = ScriptedRandom(script)
        out = run(src)
        p = Fraction(1)
        for _, size in src.calls:
            p /= size
        dist[out] = dist.get(out, Fraction(0)) + p
        i = len(src.calls) - 1
        while i >= 0 and src.calls[i][0] == src.calls[i][1] - 1:
            i -= 1
        if i < 0:
            return dist
        script = [v for v, _ in src.calls[:i]] + [src.calls[i][0] + 1]


def test_worked_example() -> None:
    # N = 8, n = 3; the integers drawn for items 1..6 are 5, 2, 1, 4, 2, 0.
    items = list("abcdefgh")
    src = ScriptedRandom([5, 2, 1, 4, 2, 0])
    assert selection_sampling(items, 3, src) == ["b", "c", "f"]  # type: ignore[arg-type]
    assert len(src.calls) == 6
    assert [size for _, size in src.calls] == [8, 7, 6, 5, 4, 3]


@pytest.mark.parametrize("big_n", range(0, 8))
def test_exact_uniform_in_order(big_n: int) -> None:
    items = list(range(big_n))
    for n in range(big_n + 1):
        dist = exact_distribution(lambda src: tuple(selection_sampling(items, n, src)))
        subsets = list(itertools.combinations(items, n))
        assert set(dist) == set(subsets)
        assert all(p == Fraction(1, math.comb(big_n, n)) for p in dist.values())


def test_exact_expected_number_of_draws() -> None:
    for big_n in range(1, 8):
        for n in range(1, big_n + 1):
            def run(src, big_n=big_n, n=n):
                selection_sampling(range(big_n), n, src)
                return len(src.calls)

            dist = exact_distribution(run)
            mean = sum(p * draws for draws, p in dist.items())
            assert mean == Fraction(n * (big_n + 1), n + 1)


def test_wrong_fixed_probability_is_not_a_fixed_size_sample() -> None:
    def fixed(items, n, rng):
        return [x for x in items if rng.randrange(len(items)) < n]

    dist = exact_distribution(lambda src: tuple(fixed(list(range(4)), 2, src)))
    assert any(len(s) != 2 for s, p in dist.items() if p > 0)


def test_errors_and_random_oracle() -> None:
    rng = random.Random(1)
    with pytest.raises(ValueError):
        selection_sampling([1, 2], 3, rng)
    with pytest.raises(ValueError):
        selection_sampling([1, 2], -1, rng)
    for _ in range(500):
        big_n = rng.randrange(0, 60)
        n = rng.randrange(0, big_n + 1)
        items = list(range(big_n))
        out = selection_sampling(items, n, rng)
        assert len(out) == n
        assert out == sorted(set(out))


def test_chi_squared_large_case() -> None:
    rng = random.Random(2)
    big_n, n, trials = 9, 4, 40000
    counts = dict.fromkeys(itertools.combinations(range(big_n), n), 0)
    for _ in range(trials):
        counts[tuple(selection_sampling(range(big_n), n, rng))] += 1
    e = trials / len(counts)
    chi2 = sum((c - e) ** 2 / e for c in counts.values())
    df = len(counts) - 1
    a = 2.0 / (9.0 * df)
    assert chi2 < df * (1.0 - a + 6.0 * math.sqrt(a)) ** 3
