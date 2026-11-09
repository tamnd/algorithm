# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merge-shuffle/. The authors are listed in prov/GCQCHN.jsonl.

import itertools
import math
import random
from fractions import Fraction

from merge_shuffle import merge, merge_shuffle


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


def distribution(run) -> dict:
    d: dict = {}
    for out, p in all_runs(run):
        d[out] = d.get(out, 0) + p
    return d


def fair_coin_merge_sort(a: list, rng) -> list:
    """A WRONG shuffle: merge with fair coins and append the rest."""
    if len(a) <= 1:
        return list(a)
    m = len(a) // 2
    left, right = fair_coin_merge_sort(a[:m], rng), fair_coin_merge_sort(a[m:], rng)
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if rng.randrange(2) == 0:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    return out + left[i:] + right[j:]


def test_example_merge() -> None:
    # Halves [a b c] and [d e f]; coins 1 0 1 0 0 0 (the last coin asks for
    # the empty left half), then f is inserted at position RANDOM(0, 5) = 1.
    t = list("abcdef")
    rng = ScriptedRandom([1, 0, 1, 0, 0, 0, 1])
    merge(t, rng, 0, 3, 3)
    assert "".join(t) == "dfeacb"
    assert [size for _, size in rng.trace] == [2, 2, 2, 2, 2, 2, 6]


def test_edges() -> None:
    rng = random.Random(1)
    assert merge_shuffle([], rng) == []
    assert merge_shuffle([5], rng) == [5]
    assert sorted(merge_shuffle([3, 3, 1, 2], rng)) == [1, 2, 3, 3]


def test_exact_uniform() -> None:
    # The whole algorithm for n <= 4 (n = 5 already has 282240 runs). For
    # larger n, uniformity follows by induction from the merge test below.
    for n in range(0, 5):
        d = distribution(lambda s: tuple(merge_shuffle(list(range(n)), s)))
        assert len(d) == math.factorial(n)
        assert set(d.values()) == {Fraction(1, math.factorial(n))}


def test_merge_of_uniform_halves_is_uniform_for_every_split() -> None:
    # Shuffle each half with all orders equally likely, then merge.
    for n1, n2 in [(1, 1), (1, 2), (2, 1), (1, 3), (2, 2), (3, 1), (2, 3), (1, 4), (3, 3)]:
        d: dict = {}
        orders = list(itertools.product(itertools.permutations(range(n1)),
                                        itertools.permutations(range(n1, n1 + n2))))
        for left, right in orders:
            for out, p in all_runs(lambda s: (merge(t := list(left + right), s, 0, n1, n2), tuple(t))[1]):
                d[out] = d.get(out, 0) + p / len(orders)
        n = n1 + n2
        assert len(d) == math.factorial(n)
        assert set(d.values()) == {Fraction(1, math.factorial(n))}


def test_fair_coin_merge_without_the_fix_is_biased() -> None:
    d = distribution(lambda s: tuple(fair_coin_merge_sort(list(range(3)), s)))
    assert d[(0, 1, 2)] == Fraction(1, 4)
    assert d[(1, 2, 0)] == Fraction(1, 8)
    for n in range(3, 7):
        d = distribution(lambda s: tuple(fair_coin_merge_sort(list(range(n)), s)))
        assert set(d.values()) != {Fraction(1, math.factorial(n))}


def test_chi_squared_with_fixed_seed() -> None:
    perms = list(itertools.permutations(range(4)))
    index = {p: k for k, p in enumerate(perms)}
    rng = random.Random(99)
    counts = [0] * 24
    total = 24000
    for _ in range(total):
        counts[index[tuple(merge_shuffle([0, 1, 2, 3], rng))]] += 1
    e = total / 24
    assert sum((c - e) ** 2 / e for c in counts) < 80


def test_against_oracle() -> None:
    rng = random.Random(6)
    for _ in range(300):
        n = rng.randrange(0, 60)
        a = [rng.randrange(7) for _ in range(n)]
        assert sorted(merge_shuffle(list(a), rng)) == sorted(a)
