# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reservoir-sampling/. The authors are listed in prov/70ENBG.jsonl.

import itertools
import math
import random
from fractions import Fraction

from reservoir_sampling import reservoir_sampling


class ScriptedRandom:
    """A fake generator: randrange returns the next scripted choice, then 0.

    Each call is recorded as (value, size), so that all_runs can walk
    through every sequence of choices like an odometer.
    """

    def __init__(self, prefix: list[int]) -> None:
        self.prefix = prefix
        self.trace: list[tuple[int, int]] = []

    def randrange(self, stop: int) -> int:
        i = len(self.trace)
        v = self.prefix[i] if i < len(self.prefix) else 0
        assert 0 <= v < stop
        self.trace.append((v, stop))
        return v


def all_runs(run):
    """Yield (output, probability) for every sequence of random choices."""
    prefix: list[int] = []
    while True:
        s = ScriptedRandom(prefix)
        out = run(s)
        p = Fraction(1)
        for _, size in s.trace:
            p /= size
        yield out, p
        tr = s.trace
        i = len(tr) - 1
        while i >= 0 and tr[i][0] == tr[i][1] - 1:
            i -= 1
        if i < 0:
            return
        prefix = [v for v, _ in tr[:i]] + [tr[i][0] + 1]


def exact_distribution(run) -> dict:
    d: dict = {}
    for out, p in all_runs(run):
        d[out] = d.get(out, 0) + p
    return d


def wrong_reservoir(stream, k, rng):
    """A known wrong version: j is drawn from {0, ..., t - 2} instead of {0, ..., t - 1}."""
    r = []
    for t, x in enumerate(stream, 1):
        if t <= k:
            r.append(x)
        else:
            j = rng.randrange(t - 1)
            if j < k:
                r[j] = x
    return r


def chi2_threshold(df: int, z: float = 6.0) -> float:
    """Wilson-Hilferty approximation of the chi-squared quantile at about z normal deviations."""
    a = 2.0 / (9.0 * df)
    return df * (1.0 - a + z * math.sqrt(a)) ** 3


def test_worked_example() -> None:
    # Choices of the page: t = 4, 5, 6, 7, 8 draw j = 2, 5, 1, 6, 3 (1-based).
    rng = ScriptedRandom([1, 4, 0, 5, 2])
    out = reservoir_sampling(["a", "b", "c", "d", "e", "f", "g", "h"], 3, rng)
    assert out == ["f", "d", "h"]
    assert len(rng.trace) == 5


def test_exact_uniform_subsets() -> None:
    for n in range(0, 7):
        for k in range(0, n + 1):
            d = exact_distribution(lambda r: frozenset(reservoir_sampling(range(n), k, r)))
            assert len(d) == math.comb(n, k)
            for s, p in d.items():
                assert len(s) == k
                assert p == Fraction(1, math.comb(n, k))


def test_exact_inclusion_probability() -> None:
    n, k = 6, 2
    d = exact_distribution(lambda r: frozenset(reservoir_sampling(range(n), k, r)))
    for i in range(n):
        assert sum(p for s, p in d.items() if i in s) == Fraction(k, n)


def test_wrong_version_is_not_uniform() -> None:
    d = exact_distribution(lambda r: frozenset(wrong_reservoir(range(5), 2, r)))
    assert any(p != Fraction(1, 10) for p in d.values())


def test_edges() -> None:
    rng = random.Random(1)
    assert reservoir_sampling([], 3, rng) == []
    assert reservoir_sampling([7, 8], 3, rng) == [7, 8]
    assert reservoir_sampling([7, 8, 9], 0, rng) == []
    assert reservoir_sampling([4, 4, 4, 4], 2, rng) == [4, 4]
    assert sorted(reservoir_sampling(range(5), 5, rng)) == [0, 1, 2, 3, 4]


def test_number_of_draws() -> None:
    class Counting(random.Random):
        calls = 0

        def randrange(self, *a, **kw):  # type: ignore[override]
            Counting.calls += 1
            return super().randrange(*a, **kw)

    rng = Counting(5)
    out = reservoir_sampling(iter(range(1000)), 10, rng)
    assert Counting.calls == 990
    assert len(set(out)) == 10


def test_against_oracle_random_inputs() -> None:
    rng = random.Random(2)
    for _ in range(500):
        n = rng.randrange(0, 30)
        k = rng.randrange(0, 8)
        items = [rng.randrange(1000) for _ in range(n)]
        out = reservoir_sampling(items, k, rng)
        assert len(out) == min(n, k)
        rest = list(items)
        for x in out:
            rest.remove(x)


def test_chi_squared_on_subsets() -> None:
    n, k, trials = 8, 3, 28000
    rng = random.Random(3)
    cells = list(itertools.combinations(range(n), k))
    counts = dict.fromkeys(cells, 0)
    for _ in range(trials):
        counts[tuple(sorted(reservoir_sampling(range(n), k, rng)))] += 1
    e = trials / len(cells)
    chi2 = sum((c - e) ** 2 / e for c in counts.values())
    assert chi2 < chi2_threshold(len(cells) - 1)
