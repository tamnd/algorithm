# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gilbert-shannon-reeds-model/. The authors are listed in prov/WYX8N8.jsonl.

import itertools
import math
import random
from fractions import Fraction

from gilbert_shannon_reeds_model import (
    a_shuffle_probability,
    brute_force_distribution,
    brute_force_total_variation,
    eulerian,
    gsr_shuffle,
    inverse_gsr_shuffle,
    inverse_riffle_tail,
    one_shuffle_law,
    rising_sequences,
    separation,
    total_variation,
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
    # cut bits 1,1,0,0 give a cut of 2: packets "ab" and "cd"
    rng = ScriptedRandom([1, 1, 0, 0, 1, 2, 0])
    assert "".join(gsr_shuffle(list("abcd"), rng)) == "acbd"
    assert rng.k == 7


def test_edges() -> None:
    rng = random.Random(0)
    assert gsr_shuffle([], rng) == []
    assert gsr_shuffle([5], rng) == [5]
    assert rising_sequences([]) == 0
    assert rising_sequences([0, 1, 2]) == 1
    assert rising_sequences([2, 1, 0]) == 3
    assert rising_sequences([0, 2, 1, 3]) == 2


def test_one_shuffle_law() -> None:
    for n in range(1, 8):
        law = one_shuffle_law(n)
        assert sum(law.values()) == 1
        assert law[tuple(range(n))] == Fraction(n + 1, 2**n)
        assert len(law) == 2**n - n
        assert all(rising_sequences(p) <= 2 for p in law)


def test_eulerian_numbers() -> None:
    assert eulerian(4) == [0, 1, 11, 11, 1]
    for n in range(0, 9):
        e = eulerian(n)
        assert sum(e) == math.factorial(n)
        counts = [0] * (n + 1)
        if n <= 6:
            for p in itertools.permutations(range(n)):
                counts[rising_sequences(p)] += 1
            if n > 0:
                assert counts == e


def test_formula_matches_brute_force() -> None:
    # The Bayer-Diaconis formula against composing k one-shuffle laws.
    for n in range(2, 7):
        for k in range(1, 5 if n < 6 else 4):
            d = brute_force_distribution(n, k)
            a = 2**k
            for p in itertools.permutations(range(n)):
                assert d.get(p, 0) == a_shuffle_probability(n, a, rising_sequences(p))
            assert brute_force_total_variation(n, k) == total_variation(n, k)


def test_probabilities_sum_to_one() -> None:
    for n in (3, 10, 52):
        e = eulerian(n)
        for k in (1, 3, 7):
            assert sum(e[r] * a_shuffle_probability(n, 2**k, r) for r in range(1, n + 1)) == 1


def test_table_for_52_cards() -> None:
    expected = [1.0, 1.0, 1.0, 1.0, 0.923733, 0.613550, 0.334061, 0.167159, 0.085420, 0.042946, 0.021502, 0.010755]
    got = [round(float(total_variation(52, k)), 6) for k in range(1, 13)]
    assert got == expected


def test_small_tables() -> None:
    def row(n: int, ks: range) -> list[float]:
        return [round(float(total_variation(n, k)), 4) for k in ks]

    assert row(3, range(1, 5)) == [0.3333, 0.1458, 0.0677, 0.0326]
    assert row(4, range(1, 5)) == [0.5, 0.2812, 0.1445, 0.0728]
    assert row(5, range(1, 5)) == [0.775, 0.3629, 0.1657, 0.0781]


def test_identity_after_one_shuffle_of_52() -> None:
    assert a_shuffle_probability(52, 2, 1) == Fraction(53, 2**52)


def test_separation_equals_inverse_riffle_tail() -> None:
    for n in (2, 4, 10, 52):
        for k in range(1, 14):
            assert separation(n, k) == inverse_riffle_tail(n, k)
            assert total_variation(n, k) <= separation(n, k)


def test_monotone_in_rising_sequences() -> None:
    for n in (5, 52):
        for k in (2, 6, 9):
            ps = [a_shuffle_probability(n, 2**k, r) for r in range(1, n + 1)]
            assert all(ps[i] >= ps[i + 1] for i in range(n - 1))


def test_sampler_chi_squared() -> None:
    law = one_shuffle_law(4)
    rng = random.Random(8)
    total = 32000
    counts: dict = {}
    for _ in range(total):
        key = tuple(gsr_shuffle([0, 1, 2, 3], rng))
        counts[key] = counts.get(key, 0) + 1
    assert set(counts) <= set(law)
    chi = sum((counts.get(p, 0) - total * q) ** 2 / (total * q) for p, q in law.items())
    assert chi < 40  # 11 degrees of freedom


def test_inverse_sampler_is_the_inverse_law() -> None:
    law = one_shuffle_law(4)

    def inverse(p: tuple[int, ...]) -> tuple[int, ...]:
        out = [0] * len(p)
        for pos, c in enumerate(p):
            out[c] = pos
        return tuple(out)

    inv_law = {inverse(p): q for p, q in law.items()}
    rng = random.Random(4)
    total = 32000
    counts: dict = {}
    for _ in range(total):
        key = tuple(inverse_gsr_shuffle([0, 1, 2, 3], rng))
        counts[key] = counts.get(key, 0) + 1
    assert set(counts) <= set(inv_law)
    chi = sum((counts.get(p, 0) - total * q) ** 2 / (total * q) for p, q in inv_law.items())
    assert chi < 40


def test_against_oracle() -> None:
    rng = random.Random(2)
    for _ in range(200):
        n = rng.randrange(0, 30)
        a = [rng.randrange(6) for _ in range(n)]
        assert sorted(gsr_shuffle(list(a), rng)) == sorted(a)
        assert sorted(inverse_gsr_shuffle(list(a), rng)) == sorted(a)
