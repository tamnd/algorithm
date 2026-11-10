# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/floyd-sampling/. The authors are listed in prov/H5FM3F.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from floyd_sampling import floyd_sampling


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
    src = ScriptedRandom([3, 3, 8, 0])
    assert floyd_sampling(10, 4, src) == {0, 3, 7, 8}  # type: ignore[arg-type]
    assert [size for _, size in src.calls] == [7, 8, 9, 10]


@pytest.mark.parametrize("n", range(0, 8))
def test_exact_uniform(n: int) -> None:
    for k in range(n + 1):
        dist = exact_distribution(lambda src: frozenset(floyd_sampling(n, k, src)))
        subsets = {frozenset(c) for c in itertools.combinations(range(n), k)}
        assert set(dist) == subsets
        assert all(p == Fraction(1, math.comb(n, k)) for p in dist.values())


def test_exactly_k_draws() -> None:
    for n in range(0, 8):
        for k in range(n + 1):
            def run(src, n=n, k=k):
                floyd_sampling(n, k, src)
                return len(src.calls)

            assert set(exact_distribution(run)) == {k}


def test_wrong_variant_is_not_uniform() -> None:
    # Drawing from {0, ..., j - 1} instead of {0, ..., j} breaks uniformity.
    def wrong(n, k, rng):
        s = set()
        for j in range(n - k, n):
            t = rng.randrange(j) if j > 0 else 0
            s.add(t if t not in s else j)
        return frozenset(s)

    def run(src):
        return wrong(5, 2, src)

    dist = exact_distribution(run)
    assert len(set(dist.values())) > 1


def test_errors_and_random_oracle() -> None:
    rng = random.Random(1)
    with pytest.raises(ValueError):
        floyd_sampling(3, 4, rng)
    with pytest.raises(ValueError):
        floyd_sampling(3, -1, rng)
    for _ in range(500):
        n = rng.randrange(0, 10**9)
        k = rng.randrange(0, min(n, 50) + 1)
        s = floyd_sampling(n, k, rng)
        assert len(s) == k
        assert all(0 <= x < n for x in s)


def test_chi_squared_large_case() -> None:
    rng = random.Random(2)
    n, k, trials = 9, 4, 40000
    counts = {frozenset(c): 0 for c in itertools.combinations(range(n), k)}
    for _ in range(trials):
        counts[frozenset(floyd_sampling(n, k, rng))] += 1
    e = trials / len(counts)
    chi2 = sum((c - e) ** 2 / e for c in counts.values())
    df = len(counts) - 1
    a = 2.0 / (9.0 * df)
    assert chi2 < df * (1.0 - a + 6.0 * math.sqrt(a)) ** 3
