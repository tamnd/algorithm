# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/top-to-random-shuffle/. The authors are listed in prov/8HFMHV.jsonl.

import itertools
import math
import random
from fractions import Fraction

from top_to_random_shuffle import (
    exact_distribution,
    tail_of_stopping_time,
    top_to_random_shuffle,
    top_to_random_until_uniform,
    total_variation_to_uniform,
)


class ScriptedRandom:
    def __init__(self, values: list[int]) -> None:
        self.values = values
        self.k = 0

    def randrange(self, stop: int) -> int:
        v = self.values[self.k]
        self.k += 1
        assert 0 <= v < stop
        return v


def joint_with_stopping(n: int, t: int) -> dict:
    """Exact law of (deck, stopped by time t), from the identity deck."""
    bottom = n - 1
    d = {(tuple(range(n)), False): Fraction(1)}
    for _ in range(t):
        nd: dict = {}
        for (deck, stopped), p in d.items():
            for q in range(n):
                rest = list(deck[1:])
                rest.insert(q, deck[0])
                key = (tuple(rest), stopped or deck[0] == bottom)
                nd[key] = nd.get(key, 0) + p / n
        d = nd
    return d


def test_example() -> None:
    rng = ScriptedRandom([3, 2, 1, 2])
    deck = top_to_random_shuffle(list("abcd"), 3, rng)
    assert "".join(deck) == "dcba"
    deck = top_to_random_shuffle(deck, 1, rng)
    assert "".join(deck) == "cbda"
    deck, t = top_to_random_until_uniform(list("abcd"), ScriptedRandom([3, 2, 1, 2]))
    assert ("".join(deck), t) == ("cbda", 4)


def test_edges() -> None:
    rng = random.Random(0)
    assert top_to_random_shuffle([], 5, rng) == []
    assert top_to_random_shuffle([1], 5, rng) == [1]
    assert top_to_random_shuffle([1, 2, 3], 0, rng) == [1, 2, 3]


def test_strong_uniform_time_property_exactly() -> None:
    # Pr[X_t = s, T <= t] = Pr[T <= t] / n! for every deck s.
    for n in range(2, 6):
        for t in range(0, 2 * n + 2):
            d = joint_with_stopping(n, t)
            p_stop = 1 - tail_of_stopping_time(n, t)
            assert sum(p for (_, s), p in d.items() if s) == p_stop
            for perm in itertools.permutations(range(n)):
                assert d.get((perm, True), 0) == p_stop / math.factorial(n)


def test_total_variation_is_below_the_tail() -> None:
    for n in range(2, 6):
        for t in range(1, 3 * n + 1):
            tv = total_variation_to_uniform(exact_distribution(n, t), n)
            assert tv <= tail_of_stopping_time(n, t)


def test_small_values() -> None:
    tv = [total_variation_to_uniform(exact_distribution(4, t), 4) for t in range(1, 4)]
    assert tv == [Fraction(5, 6), Fraction(1, 2), Fraction(5, 16)]
    assert [tail_of_stopping_time(4, t) for t in (3, 4)] == [1, Fraction(29, 32)]


def test_never_exactly_uniform_at_a_fixed_time() -> None:
    for n in range(3, 6):
        for t in range(1, 3 * n):
            assert total_variation_to_uniform(exact_distribution(n, t), n) > 0


def test_expected_stopping_time() -> None:
    for n in range(1, 8):
        e = sum(Fraction(n, i) for i in range(1, n + 1))
        assert e == n * sum(Fraction(1, i) for i in range(1, n + 1))
    rng = random.Random(3)
    n, runs = 10, 4000
    mean = sum(top_to_random_until_uniform(list(range(n)), rng)[1] for _ in range(runs)) / runs
    assert abs(mean - 10 * sum(1 / i for i in range(1, 11))) < 1.5


def test_stopped_version_chi_squared() -> None:
    perms = list(itertools.permutations(range(4)))
    index = {p: k for k, p in enumerate(perms)}
    rng = random.Random(21)
    counts = [0] * 24
    total = 24000
    for _ in range(total):
        deck, _ = top_to_random_until_uniform([0, 1, 2, 3], rng)
        counts[index[tuple(deck)]] += 1
    e = total / 24
    assert sum((c - e) ** 2 / e for c in counts) < 80


def test_against_oracle() -> None:
    rng = random.Random(9)
    for _ in range(200):
        n = rng.randrange(0, 20)
        a = [rng.randrange(4) for _ in range(n)]
        assert sorted(top_to_random_shuffle(list(a), rng.randrange(30), rng)) == sorted(a)
