# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sort-based-shuffle/. The authors are listed in prov/JTAPRN.jsonl.

import itertools
import math
import random
from fractions import Fraction

from sort_based_shuffle import (
    random_comparator_insertion_sort,
    random_comparator_merge_sort,
    random_key_shuffle,
)


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


def distribution(shuffle, n: int) -> dict:
    d: dict = {}
    for out, p in all_runs(lambda s: tuple(shuffle(list(range(n)), s))):
        d[out] = d.get(out, 0) + p
    return d


def is_exactly_uniform(d: dict, n: int) -> bool:
    perms = list(itertools.permutations(range(n)))
    return all(d.get(q, 0) == Fraction(1, math.factorial(n)) for q in perms)


def total_variation(d: dict, n: int) -> Fraction:
    u = Fraction(1, math.factorial(n))
    return sum(abs(d.get(q, 0) - u) for q in itertools.permutations(range(n))) / 2


def fisher_yates(a: list, rng) -> list:
    for i in range(len(a) - 1, 0, -1):
        j = rng.randrange(i + 1)
        a[i], a[j] = a[j], a[i]
    return a


def test_example_trace() -> None:
    # Coins 1; 0, 1; 0, 0, 1 (0 means "x is less, move left").
    rng = ScriptedRandom([1, 0, 1, 0, 0, 1])
    assert random_comparator_insertion_sort(["a", "b", "c", "d"], rng) == ["a", "d", "c", "b"]


def test_fisher_yates_passes_the_exact_test() -> None:
    for n in range(0, 6):
        assert is_exactly_uniform(distribution(fisher_yates, n), n)


def test_insertion_with_coin_n3_exact() -> None:
    d = distribution(random_comparator_insertion_sort, 3)
    assert d == {
        (0, 1, 2): Fraction(1, 4),
        (0, 2, 1): Fraction(1, 8),
        (1, 0, 2): Fraction(1, 4),
        (1, 2, 0): Fraction(1, 8),
        (2, 0, 1): Fraction(1, 8),
        (2, 1, 0): Fraction(1, 8),
    }
    assert total_variation(d, 3) == Fraction(1, 6)


def test_merge_with_coin_n3_exact() -> None:
    d = distribution(random_comparator_merge_sort, 3)
    assert d == {
        (0, 1, 2): Fraction(1, 4),
        (0, 2, 1): Fraction(1, 4),
        (1, 0, 2): Fraction(1, 8),
        (1, 2, 0): Fraction(1, 8),
        (2, 0, 1): Fraction(1, 8),
        (2, 1, 0): Fraction(1, 8),
    }
    assert total_variation(d, 3) == Fraction(1, 6)


def test_random_comparator_fails_exact_test() -> None:
    for n in range(3, 7):
        for shuffle in (random_comparator_insertion_sort, random_comparator_merge_sort):
            d = distribution(shuffle, n)
            assert abs(sum(d.values()) - 1) == 0
            assert not is_exactly_uniform(d, n)
            # Every probability has a power of two as its denominator.
            assert all(p.denominator & (p.denominator - 1) == 0 for p in d.values())


def test_total_variation_n4() -> None:
    assert total_variation(distribution(random_comparator_insertion_sort, 4), 4) == Fraction(7, 24)
    assert total_variation(distribution(random_comparator_merge_sort, 4), 4) == Fraction(1, 6)


def test_identity_probability_of_insertion() -> None:
    for n in range(1, 7):
        d = distribution(random_comparator_insertion_sort, n)
        assert d[tuple(range(n))] == Fraction(1, 2 ** (n - 1))


def test_n2_is_fair() -> None:
    for shuffle in (random_comparator_insertion_sort, random_comparator_merge_sort):
        assert is_exactly_uniform(distribution(shuffle, 2), 2)


def test_chi_squared_with_fixed_seed() -> None:
    perms = list(itertools.permutations(range(4)))
    index = {p: k for k, p in enumerate(perms)}

    def stat(shuffle, seed: int) -> float:
        rng = random.Random(seed)
        counts = [0] * 24
        total = 24000
        for _ in range(total):
            counts[index[tuple(shuffle([0, 1, 2, 3], rng))]] += 1
        e = total / 24
        return sum((c - e) ** 2 / e for c in counts)

    assert stat(random_key_shuffle, 31) < 80
    assert stat(random_comparator_insertion_sort, 31) > 1000
    assert stat(random_comparator_merge_sort, 31) > 1000


def test_key_shuffle_against_oracle() -> None:
    rng = random.Random(4)
    for _ in range(300):
        n = rng.randrange(0, 30)
        a = [rng.randrange(5) for _ in range(n)]
        assert sorted(random_key_shuffle(list(a), rng)) == sorted(a)
        assert sorted(random_comparator_merge_sort(list(a), rng)) == sorted(a)
        assert sorted(random_comparator_insertion_sort(list(a), rng)) == sorted(a)
