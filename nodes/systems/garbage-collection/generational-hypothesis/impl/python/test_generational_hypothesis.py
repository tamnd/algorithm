# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generational-hypothesis/. The authors are listed in prov/GHBQBX.jsonl.

import itertools
import random
from fractions import Fraction

from generational_hypothesis import (
    expected_survivors,
    finite_survival,
    geometric_survival,
    hazard,
    mixture_survival,
    nursery_survivors,
    sample_geometric,
    survivor_fraction,
)


def test_geometric_closed_form() -> None:
    for mean in (1, 2, 5, 10):
        s = geometric_survival(mean)
        q = 1 - Fraction(1, mean)
        for n in range(1, 30):
            assert expected_survivors(s, n) == mean * (1 - q ** n)


def test_page_example_mixture() -> None:
    s = mixture_survival([(Fraction(9, 10), geometric_survival(10, False)), (Fraction(1, 10), geometric_survival(10000, False))])
    f = float(survivor_fraction(s, 1000))
    assert abs(f - 0.1042) < 5e-4
    assert abs(float(survivor_fraction(s, 100)) - 0.1895) < 5e-4
    assert abs(float(survivor_fraction(s, 10000)) - 0.0641) < 5e-4
    one = geometric_survival(10000, False)
    assert abs(float(survivor_fraction(one, 1000)) - 0.9516) < 5e-4


def test_hazard_shapes() -> None:
    s = mixture_survival([(Fraction(9, 10), geometric_survival(10, False)), (Fraction(1, 10), geometric_survival(10000, False))])
    hs = [hazard(s, a) for a in range(0, 200, 10)]
    assert all(x > y for x, y in zip(hs, hs[1:]))
    g = geometric_survival(7)
    assert {hazard(g, a) for a in range(20)} == {Fraction(1, 7)}
    phase = finite_survival({1: Fraction(9, 10), 50: Fraction(1, 10)})
    assert hazard(phase, 0) == Fraction(9, 10)
    assert all(hazard(phase, a) == 0 for a in range(1, 49))
    assert hazard(phase, 49) == 1
    assert survivor_fraction(phase, 50) == Fraction(118, 1000)
    assert survivor_fraction(phase, 100) == Fraction(59, 1000)


def test_expectation_against_brute_force() -> None:
    dist = {1: Fraction(1, 2), 2: Fraction(1, 4), 5: Fraction(1, 8), 9: Fraction(1, 8)}
    s = finite_survival(dist)
    for n in range(1, 5):
        total = Fraction(0)
        for lives in itertools.product(dist, repeat=n):
            p = Fraction(1)
            for life in lives:
                p *= dist[life]
            total += p * nursery_survivors(list(lives), n)[0]
        assert total == expected_survivors(s, n)


def test_simulation_matches_model() -> None:
    rng = random.Random(1983)
    n, mean = 50, 8
    lives = [sample_geometric(rng, mean) for _ in range(n * 400)]
    counts = nursery_survivors(lives, n)
    avg = sum(counts) / len(counts)
    exact = float(expected_survivors(geometric_survival(mean), n))
    assert abs(avg - exact) < 0.3


def test_edges() -> None:
    assert nursery_survivors([], 3) == []
    assert nursery_survivors([1, 1, 1], 3) == [1]
    assert nursery_survivors([10, 10, 10], 3) == [3]
    assert expected_survivors(geometric_survival(1), 5) == 1
