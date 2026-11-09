# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/permute-by-sorting/. The authors are listed in prov/E5K3WT.jsonl.

import itertools
import math
import random
from fractions import Fraction

from permute_by_sorting import distinct_probability, permute_by_sorting, permute_once


class ScriptedRandom:
    """A fake generator that returns a fixed list of choices, then zeros."""

    def __init__(self, prefix: list[int]) -> None:
        self.prefix = prefix
        self.trace: list[tuple[int, int]] = []

    def randrange(self, start: int, stop: int | None = None) -> int:
        if stop is None:
            start, stop = 0, start
        k = len(self.trace)
        v = self.prefix[k] if k < len(self.prefix) else 0
        assert 0 <= v < stop - start
        self.trace.append((v, stop - start))
        return start + v


def all_runs(run):
    """Yield (output, probability) for every sequence of choices."""
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


def stable_sort_no_redraw(a: list, rng, m: int) -> list:
    """A WRONG variant: keep tied keys and rely on a stable sort."""
    keys = [rng.randrange(m) for _ in range(len(a))]
    order = sorted(range(len(a)), key=keys.__getitem__)
    return [a[i] for i in order]


def conditional_distribution(n: int, m: int) -> tuple[dict, Fraction]:
    dist: dict = {}
    accept = Fraction(0)
    for out, p in all_runs(lambda s: permute_once(list(range(n)), s, m)):
        if out is not None:
            dist[tuple(out)] = dist.get(tuple(out), 0) + p
            accept += p
    return {k: v / accept for k, v in dist.items()}, accept


def test_example() -> None:
    rng = ScriptedRandom([37, 5, 51, 12])
    assert permute_by_sorting(["a", "b", "c", "d"], rng) == ["b", "d", "a", "c"]
    assert [size for _, size in rng.trace] == [64] * 4


def test_redraw_on_tie() -> None:
    rng = ScriptedRandom([3, 3, 1, 2, 0, 1])
    assert permute_by_sorting(["x", "y", "z"], rng) == ["y", "z", "x"]
    assert len(rng.trace) == 6


def test_edges() -> None:
    rng = random.Random(3)
    assert permute_by_sorting([], rng) == []
    assert permute_by_sorting([7], rng) == [7]
    assert sorted(permute_by_sorting([2, 2, 1], rng)) == [1, 2, 2]
    try:
        permute_by_sorting([1, 2, 3], rng, m=2)
    except ValueError:
        pass
    else:
        raise AssertionError("m < n must be rejected")


def test_exact_uniform_given_distinct_keys() -> None:
    cases = [(1, 1), (2, 2), (2, 5), (3, 3), (3, 4), (3, 27), (4, 4), (4, 6), (5, 5), (5, 6)]
    for n, m in cases:
        dist, accept = conditional_distribution(n, m)
        assert len(dist) == math.factorial(n)
        assert set(dist.values()) == {Fraction(1, math.factorial(n))}
        assert accept == Fraction(math.perm(m, n), m**n)


def test_each_order_has_binomial_count() -> None:
    # With distinct keys, each order comes from exactly C(m, n) key vectors.
    n, m = 3, 5
    counts: dict = {}
    for keys in itertools.product(range(m), repeat=n):
        if len(set(keys)) == n:
            order = tuple(sorted(range(n), key=keys.__getitem__))
            counts[order] = counts.get(order, 0) + 1
    assert set(counts.values()) == {math.comb(m, n)}


def test_ties_with_stable_sort_are_biased() -> None:
    expected = {
        2: [4, 1, 1, 1, 1, 0],
        3: [10, 4, 4, 4, 4, 1],
        4: [20, 10, 10, 10, 10, 4],
    }
    perms = list(itertools.permutations(range(3)))
    for m, counts in expected.items():
        dist: dict = {}
        for out, p in all_runs(lambda s: tuple(stable_sort_no_redraw([0, 1, 2], s, m))):
            dist[out] = dist.get(out, 0) + p
        assert [dist.get(q, 0) for q in perms] == [Fraction(c, m**3) for c in counts]


def test_distinct_probability() -> None:
    assert abs(distinct_probability(3, 27) - 650 / 729) < 1e-12
    for n in [2, 3, 10, 100, 1000]:
        assert distinct_probability(n, n**3) >= 1 - 1 / (2 * n)


def test_chi_squared_with_fixed_seed() -> None:
    perms = list(itertools.permutations(range(4)))
    index = {p: k for k, p in enumerate(perms)}
    rng = random.Random(77)
    counts = [0] * 24
    total = 24000
    for _ in range(total):
        counts[index[tuple(permute_by_sorting([0, 1, 2, 3], rng))]] += 1
    e = total / 24
    assert sum((c - e) ** 2 / e for c in counts) < 80


def test_against_oracle() -> None:
    rng = random.Random(12)
    for _ in range(300):
        n = rng.randrange(0, 40)
        a = [rng.randrange(6) for _ in range(n)]
        assert sorted(permute_by_sorting(list(a), rng)) == sorted(a)
