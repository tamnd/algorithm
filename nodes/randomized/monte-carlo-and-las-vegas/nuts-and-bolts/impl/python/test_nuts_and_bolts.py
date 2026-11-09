# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nuts-and-bolts/. The authors are listed in prov/SA6TXV.jsonl.

import itertools
import math
import random
from fractions import Fraction

from nuts_and_bolts import (
    Counter,
    closed_form,
    exact_expectation,
    expected_comparisons,
    lower_bound,
    match,
)


def test_matches_like_sorting() -> None:
    rng = random.Random(3)
    for _ in range(500):
        n = rng.randint(0, 40)
        sizes = rng.sample(range(1000), n)
        nuts = sizes[:]
        bolts = sizes[:]
        rng.shuffle(nuts)
        rng.shuffle(bolts)
        cmp = Counter()
        match(nuts, bolts, rng, cmp)
        assert nuts == sorted(sizes) and bolts == sorted(sizes)
        # Only nut-bolt pairs are compared, and no pair twice.
        assert len(set(cmp.pairs)) == len(cmp.pairs)
        # Each nut is compared with its own bolt exactly once.
        assert sum(1 for x, y in cmp.pairs if x == y) == n


def test_recurrence_and_closed_form() -> None:
    for n in range(0, 60):
        assert expected_comparisons(n) == closed_form(n)
    assert [expected_comparisons(n) for n in range(1, 6)] == [1, 4, Fraction(25, 3), Fraction(41, 3), Fraction(99, 5)]
    assert expected_comparisons(10) == Fraction(37091, 630)
    assert abs(float(closed_form(100)) - 1395.70) < 0.01


def test_exact_expectation_by_enumeration() -> None:
    for n in range(1, 6):
        sizes = list(range(n))
        for bolts_order in itertools.permutations(sizes):
            exp, least, most = exact_expectation(sizes, list(bolts_order))
            assert exp == expected_comparisons(n)
            assert least >= math.ceil(lower_bound(n) - 1e-9)
            assert most == n * n  # every pivot at an end: each pair compared once


def test_pair_probabilities() -> None:
    # Nut of rank i and bolt of rank j != i are compared with probability 2 / (|i - j| + 1).
    n = 5
    sizes = list(range(n))
    prob = {}
    choices: list[int] = []
    from nuts_and_bolts import Script

    while True:
        script = Script(choices)
        cmp = Counter()
        match(list(sizes), list(sizes), script, cmp)
        w = Fraction(1)
        for m in script.ranges:
            w /= m
        for pair in set(cmp.pairs):
            prob[pair] = prob.get(pair, Fraction(0)) + w
        full = choices + [0] * (len(script.ranges) - len(choices))
        i = len(full) - 1
        while i >= 0 and full[i] == script.ranges[i] - 1:
            i -= 1
        if i < 0:
            break
        choices = full[:i] + [full[i] + 1]
    for i in range(n):
        for j in range(n):
            expect = Fraction(1) if i == j else Fraction(2, abs(i - j) + 1)
            assert prob.get((i, j), Fraction(0)) == expect


def test_average_over_seeds() -> None:
    n = 10
    trials = 4000
    total = 0
    for seed in range(trials):
        rng = random.Random(seed)
        sizes = list(range(n))
        nuts, bolts = sizes[:], sizes[:]
        rng.shuffle(nuts)
        rng.shuffle(bolts)
        total += match(nuts, bolts, rng)
    mean = total / trials
    assert abs(mean - float(expected_comparisons(n))) < 1.0
    assert mean > lower_bound(n)


def test_lower_bound_values() -> None:
    assert abs(lower_bound(10) - 13.75) < 0.01
    assert abs(lower_bound(100) - 331.09) < 0.01
    assert abs(lower_bound(1000) - 5381.45) < 0.01
