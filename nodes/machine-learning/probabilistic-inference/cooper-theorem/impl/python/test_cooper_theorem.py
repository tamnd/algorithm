# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cooper-theorem/. The authors are listed in prov/RAWF2P.jsonl.

import random
from fractions import Fraction
from itertools import product

import pytest

from cooper_theorem import cooper_network, count_models, probability


def random_3cnf(rng, n, m):
    return [[(v, rng.random() < 0.5) for v in rng.sample(range(n), min(3, n))] for _ in range(m)]


def test_page_example():
    # (x0 or x1 or not x2) and (not x0 or x2 or x3) and (not x1 or not x2 or not x3)
    clauses = [[(0, True), (1, True), (2, False)], [(0, False), (2, True), (3, True)],
               [(1, False), (2, False), (3, False)]]
    nodes, out = cooper_network(4, clauses)
    assert len(nodes) == 4 + 2 * 3
    assert max(len(nd.parents) for nd in nodes) == 3
    assert count_models(4, clauses) == 10
    assert probability(nodes, out, 1) == Fraction(10, 16)


def test_unsatisfiable():
    # All eight clauses on three variables: no assignment satisfies them all.
    clauses = [[(0, a), (1, b), (2, c)] for a, b, c in product((True, False), repeat=3)]
    nodes, out = cooper_network(3, clauses)
    assert probability(nodes, out, 1) == 0
    assert probability(nodes, out, 0) == 1


def test_random_formulas():
    rng = random.Random(12)
    seen_sat = seen_unsat = 0
    for _ in range(200):
        n = rng.randint(3, 6)
        m = rng.randint(1, 4 * n + 4)
        clauses = random_3cnf(rng, n, m)
        nodes, out = cooper_network(n, clauses)
        assert max(len(nd.parents) for nd in nodes) <= 3
        assert len(nodes) == n + 2 * m
        p = probability(nodes, out, 1)
        k = count_models(n, clauses)
        assert p * 2 ** n == k
        assert (p > 0) == (k > 0)
        seen_sat += k > 0
        seen_unsat += k == 0
    assert seen_sat and seen_unsat


def test_bad_input():
    with pytest.raises(ValueError):
        cooper_network(2, [])
    with pytest.raises(ValueError):
        cooper_network(2, [[(0, True), (0, False)]])
