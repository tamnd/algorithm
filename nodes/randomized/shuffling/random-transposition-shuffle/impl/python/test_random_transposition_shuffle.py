# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-transposition-shuffle/. The authors are listed in prov/56XJ14.jsonl.

import itertools
import math
import random
from fractions import Fraction

from random_transposition_shuffle import (
    broder_tail,
    broder_until_uniform,
    class_probability,
    exact_distribution,
    random_transposition_shuffle,
    total_variation_by_cycle_type,
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


def test_example() -> None:
    rng = ScriptedRandom([0, 3, 1, 1, 2, 0])
    assert "".join(random_transposition_shuffle(list("abcd"), 3, rng)) == "cbda"


def test_edges() -> None:
    rng = random.Random(0)
    assert random_transposition_shuffle([], 4, rng) == []
    assert random_transposition_shuffle([7], 4, rng) == [7]
    assert random_transposition_shuffle([1, 2], 0, rng) == [1, 2]


def test_small_distances_exactly() -> None:
    tv4 = [total_variation_to_uniform(exact_distribution(4, t), 4) for t in range(1, 5)]
    assert tv4 == [Fraction(17, 24), Fraction(9, 32), Fraction(65, 384), Fraction(39, 512)]
    tv3 = [total_variation_to_uniform(exact_distribution(3, t), 3) for t in range(1, 4)]
    assert tv3 == [Fraction(1, 3), Fraction(5, 54), Fraction(1, 27)]


def test_cycle_type_chain_matches_brute_force() -> None:
    for n in range(2, 6):
        for t in range(0, 6):
            d = exact_distribution(n, t)
            assert total_variation_to_uniform(d, n) == total_variation_by_cycle_type(n, t)


def test_class_probabilities_sum_to_one() -> None:
    def partitions(n: int, m: int):
        if n == 0:
            yield ()
            return
        for a in range(min(n, m), 0, -1):
            for rest in partitions(n - a, a):
                yield (a,) + rest

    for n in range(1, 9):
        assert sum(class_probability(lam) for lam in partitions(n, n)) == 1


def test_law_is_constant_on_cycle_types() -> None:
    def cycle_type(p: tuple[int, ...]) -> tuple[int, ...]:
        seen, out = set(), []
        for s in range(len(p)):
            if s not in seen:
                k, x = 0, s
                while x not in seen:
                    seen.add(x)
                    x = p[x]
                    k += 1
                out.append(k)
        return tuple(sorted(out, reverse=True))

    for t in range(0, 4):
        d = exact_distribution(4, t)
        by_type: dict = {}
        for p in itertools.permutations(range(4)):
            by_type.setdefault(cycle_type(p), set()).add(d.get(p, Fraction(0)))
        assert all(len(v) == 1 for v in by_type.values())


def test_never_exactly_uniform_at_a_fixed_time() -> None:
    for n in range(3, 6):
        for t in range(0, 8):
            assert total_variation_by_cycle_type(n, t) > 0


def test_distinct_pairs_are_periodic() -> None:
    # Forcing L != R makes every move odd, so the parity is fixed by t.
    for t in range(0, 6):
        d: dict = {(0, 1, 2): Fraction(1)}
        for _ in range(t):
            nd: dict = {}
            for p, w in d.items():
                for i, j in itertools.permutations(range(3), 2):
                    e = list(p)
                    e[i], e[j] = e[j], e[i]
                    nd[tuple(e)] = nd.get(tuple(e), 0) + w / 6
            d = nd
        assert total_variation_to_uniform(d, 3) >= Fraction(1, 2)


def joint_with_broder(n: int, t: int) -> dict:
    """Exact law of (deck, marks by position, all marked) after t moves."""
    start = (tuple(range(n)), tuple([False] * n))
    d = {start: Fraction(1)}
    w = Fraction(1, n * n)
    for _ in range(t):
        nd: dict = {}
        for (deck, marks), p in d.items():
            for i in range(n):
                for j in range(n):
                    m = list(marks)
                    if not m[j] and (m[i] or i == j):
                        m[j] = True
                    e = list(deck)
                    e[i], e[j] = e[j], e[i]
                    m[i], m[j] = m[j], m[i]
                    key = (tuple(e), tuple(m))
                    nd[key] = nd.get(key, 0) + p * w
        d = nd
    return d


def test_broder_time_is_strong_uniform_exactly() -> None:
    for n in range(2, 5):
        for t in range(0, 9):
            d = joint_with_broder(n, t)
            done: dict = {}
            for (deck, marks), p in d.items():
                if all(marks):
                    done[deck] = done.get(deck, 0) + p
            p_stop = 1 - broder_tail(n, t)
            assert sum(done.values()) == p_stop
            for perm in itertools.permutations(range(n)):
                assert done.get(perm, 0) == p_stop / math.factorial(n)


def test_distance_is_below_the_broder_tail() -> None:
    for n in range(2, 6):
        for t in range(1, 16):
            assert total_variation_by_cycle_type(n, t) <= broder_tail(n, t)


def test_broder_expected_time() -> None:
    rng = random.Random(5)
    n, runs = 8, 4000
    mean = sum(broder_until_uniform(list(range(n)), rng)[1] for _ in range(runs)) / runs
    expected = 2 * n * n / (n + 1) * sum(1 / i for i in range(1, n + 1))
    assert abs(mean - expected) < 2.0


def test_broder_stopped_deck_chi_squared() -> None:
    perms = list(itertools.permutations(range(4)))
    index = {p: k for k, p in enumerate(perms)}
    rng = random.Random(17)
    counts = [0] * 24
    total = 24000
    for _ in range(total):
        deck, _ = broder_until_uniform([0, 1, 2, 3], rng)
        counts[index[tuple(deck)]] += 1
    e = total / 24
    assert sum((c - e) ** 2 / e for c in counts) < 80


def test_against_oracle() -> None:
    rng = random.Random(11)
    for _ in range(200):
        n = rng.randrange(0, 20)
        a = [rng.randrange(5) for _ in range(n)]
        assert sorted(random_transposition_shuffle(list(a), rng.randrange(40), rng)) == sorted(a)
