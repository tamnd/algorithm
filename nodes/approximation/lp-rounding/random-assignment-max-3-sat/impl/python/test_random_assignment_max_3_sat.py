# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-assignment-max-3-sat/. The authors are listed in prov/G3HNQ1.jsonl.

import random
from fractions import Fraction
from itertools import product

import pytest

from random_assignment_max_3_sat import (
    count_satisfied,
    derandomized_max_3_sat,
    expected_satisfied,
    random_assignment_max_3_sat,
)


def all_counts(n, clauses):
    return [count_satisfied(clauses, a) for a in product([False, True], repeat=n)]


def random_exact_3cnf(rng, n, m):
    out = []
    for _ in range(m):
        vs = rng.sample(range(1, n + 1), 3)
        out.append([v if rng.random() < 0.5 else -v for v in vs])
    return out


EXAMPLE = [[1, 2, -3], [-1, 3, 4], [-2, -3, -4], [1, -2, 4], [-1, -2, 3], [2, 3, 4]]


def test_example():
    counts = all_counts(4, EXAMPLE)
    assert Fraction(sum(counts), len(counts)) == Fraction(21, 4)
    assert max(counts) == 6
    assert expected_satisfied(EXAMPLE, {}) == Fraction(21, 4)
    assert sorted(counts) == [4] * 2 + [5] * 8 + [6] * 6
    assert expected_satisfied(EXAMPLE, {1: True}) == expected_satisfied(EXAMPLE, {1: False}) == Fraction(21, 4)
    assert expected_satisfied(EXAMPLE, {1: True, 2: True}) == 5
    assert expected_satisfied(EXAMPLE, {1: True, 2: False}) == Fraction(11, 2)
    assert expected_satisfied(EXAMPLE, {1: True, 2: False, 3: True}) == 6
    assert expected_satisfied(EXAMPLE, {1: True, 2: False, 3: False}) == 5
    a, s = derandomized_max_3_sat(4, EXAMPLE)
    assert a == [True, False, True, True] and s == 6


def test_all_eight_sign_patterns_is_tight():
    clauses = [[s1 * 1, s2 * 2, s3 * 3] for s1, s2, s3 in product([1, -1], repeat=3)]
    assert all_counts(3, clauses) == [7] * 8
    assert derandomized_max_3_sat(3, clauses)[1] == 7


def test_edge_cases():
    rng = random.Random(0)
    assert random_assignment_max_3_sat(0, [], rng) == ([], 0)
    assert derandomized_max_3_sat(0, []) == ([], 0)
    with pytest.raises(ValueError):
        random_assignment_max_3_sat(2, [[1, 3]], rng)
    with pytest.raises(ValueError):
        derandomized_max_3_sat(2, [[]])
    # a repeated variable or a complementary pair changes the probability
    assert expected_satisfied([[1, 1, 2]], {}) == Fraction(3, 4)
    assert expected_satisfied([[1, -1, 2]], {}) == 1


def test_random_assignment_matches_its_count():
    rng = random.Random(8)
    clauses = random_exact_3cnf(rng, 6, 20)
    for _ in range(50):
        a, s = random_assignment_max_3_sat(6, clauses, rng)
        assert len(a) == 6 and s == count_satisfied(clauses, a)


def test_exact_expectation_and_derandomization():
    rng = random.Random(1974)
    for _ in range(500):
        n = rng.randint(3, 7)
        m = rng.randint(1, 12)
        clauses = random_exact_3cnf(rng, n, m)
        counts = all_counts(n, clauses)
        # every assignment is equally likely, so this is the exact expectation
        assert Fraction(sum(counts), len(counts)) == Fraction(7 * m, 8)
        assert expected_satisfied(clauses, {}) == Fraction(7 * m, 8)
        opt = max(counts)
        a, s = derandomized_max_3_sat(n, clauses)
        assert s == count_satisfied(clauses, a)
        assert 8 * s >= 7 * m >= 7 * opt


def test_general_clause_lengths():
    rng = random.Random(9)
    for _ in range(200):
        n = rng.randint(1, 6)
        clauses = []
        for _ in range(rng.randint(1, 8)):
            vs = rng.sample(range(1, n + 1), rng.randint(1, n))
            clauses.append([v if rng.random() < 0.5 else -v for v in vs])
        counts = all_counts(n, clauses)
        want = sum(1 - Fraction(1, 2 ** len(cl)) for cl in clauses)
        assert Fraction(sum(counts), len(counts)) == want == expected_satisfied(clauses, {})
        assert derandomized_max_3_sat(n, clauses)[1] >= want
