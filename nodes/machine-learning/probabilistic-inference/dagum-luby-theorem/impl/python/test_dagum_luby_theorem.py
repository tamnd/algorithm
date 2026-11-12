# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dagum-luby-theorem/. The authors are listed in prov/03QBR6.jsonl.

import random
from fractions import Fraction
from itertools import product

from dagum_luby_theorem import (HALF, absolute_oracle, cooper_network, decide_by_relative, find_assignment,
                                forward_sample, median_oracle, noisy_oracle, posterior, probability_of,
                                repetitions, samples_needed, satisfies)

PAGE = [[(0, True), (1, True), (2, False)], [(0, False), (2, True), (3, True)], [(1, False), (2, False), (3, False)]]


def random_3cnf(rng, n, m):
    return [[(v, rng.random() < 0.5) for v in rng.sample(range(n), 3)] for _ in range(m)]


def count_models(n, clauses):
    return sum(satisfies(q, clauses) for q in product((0, 1), repeat=n))


def test_page_example():
    nodes, y = cooper_network(4, PAGE)
    assert probability_of(nodes, {y: 1}) == Fraction(10, 16)
    assert posterior(nodes, 0, {y: 1}) == HALF
    answers = iter([Fraction(6, 10), Fraction(65, 100), Fraction(2, 10), Fraction(7, 10)])
    assert find_assignment(4, PAGE, lambda p: next(answers)) == [1, 1, 0, 1]


def test_self_reduction_with_absolute_error_below_half():
    rng = random.Random(1993)
    seen = [0, 0]
    for _ in range(150):
        n = rng.randint(3, 5)
        clauses = random_3cnf(rng, n, rng.randint(1, 5 * n))
        sat = count_models(n, clauses) > 0
        seen[sat] += 1
        for eps in (Fraction(0), Fraction(1, 4), Fraction(49, 100)):
            q = find_assignment(n, clauses, absolute_oracle(eps, rng))
            assert (q is not None) == sat
            assert q is None or satisfies(q, clauses)
    assert all(seen)


def test_error_one_half_carries_no_information():
    # 1/2 is within 1/2 of every probability, and with it the reduction can fail.
    assert all(abs(HALF - p) <= HALF for p in (Fraction(0), Fraction(1), Fraction(3, 7)))
    clauses = [[(0, False), (1, True), (2, True)], [(0, False), (1, False), (2, True)],
               [(0, False), (1, True), (2, False)], [(0, False), (1, False), (2, False)]]  # forces q0 = 0
    nodes, y = cooper_network(3, clauses)
    assert posterior(nodes, 0, {y: 1}) == 0
    assert find_assignment(3, clauses, lambda p: HALF) is None
    assert count_models(3, clauses) == 4


def test_randomized_oracle_gives_one_sided_error():
    rng = random.Random(60)
    eps, delta = Fraction(2, 5), 0.1
    for _ in range(25):
        n = rng.randint(3, 4)
        clauses = random_3cnf(rng, n, rng.randint(1, 5 * n))
        sat = count_models(n, clauses) > 0
        k = repetitions(n, delta)
        wins = 0
        for _ in range(8):
            q = find_assignment(n, clauses, median_oracle(noisy_oracle(eps, delta, rng), k))
            assert sat or q is None  # never a false yes
            wins += q is not None
        assert not sat or wins >= 4  # a yes with probability at least 3/4 in theory


def test_relative_approximation_decides_sat():
    rng = random.Random(97)
    for _ in range(150):
        n = rng.randint(3, 5)
        clauses = random_3cnf(rng, n, rng.randint(1, 5 * n))
        eps = Fraction(rng.randint(1, 20), 10)
        est = lambda p: p * rng.choice((1 / (1 + eps), Fraction(1), 1 + eps))
        assert decide_by_relative(n, clauses, est) == (count_models(n, clauses) > 0)


def test_forward_sampling_without_evidence():
    rng = random.Random(7)
    eps, delta = 0.1, 0.001
    s = samples_needed(eps, delta)
    for _ in range(15):
        n = rng.randint(3, 5)
        clauses = random_3cnf(rng, n, rng.randint(1, 2 * n))
        nodes, y = cooper_network(n, clauses)
        exact = probability_of(nodes, {y: 1})
        assert exact * 2 ** n == count_models(n, clauses)
        assert abs(forward_sample(nodes, y, s, rng) - exact) <= eps
