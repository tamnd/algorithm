# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gap-preserving-reduction/. The authors are listed in prov/YVSNYR.jsonl.

import random
from fractions import Fraction
from itertools import product

from gap_preserving_reduction import (
    assignment_to_independent_set,
    independent_set_to_assignment,
    independent_sets,
    is_independent,
    max_independent_set_size,
    max_satisfied,
    sat_to_independent_set,
    satisfied_count,
)


def random_3cnf(rng: random.Random, num_vars: int, m: int) -> list[tuple[int, ...]]:
    clauses = []
    for _ in range(m):
        vs = rng.sample(range(1, num_vars + 1), 3)
        clauses.append(tuple(v if rng.random() < 0.5 else -v for v in vs))
    return clauses


ALL_EIGHT = [tuple(s * v for s, v in zip(signs, (1, 2, 3))) for signs in product((1, -1), repeat=3)]


def test_example_all_eight_clauses() -> None:
    labels, edges = sat_to_independent_set(ALL_EIGHT)
    assert len(labels) == 24
    assert max_satisfied(ALL_EIGHT, 3) == 7
    assert max_independent_set_size(len(labels), edges) == 7


def test_size_of_the_graph() -> None:
    rng = random.Random(1)
    for _ in range(50):
        m = rng.randint(1, 6)
        clauses = random_3cnf(rng, 5, m)
        labels, edges = sat_to_independent_set(clauses)
        assert len(labels) == 3 * m
        triangle_edges = 3 * m
        assert len(edges) >= triangle_edges


def test_completeness_and_soundness() -> None:
    rng = random.Random(7)
    sat_seen = unsat_seen = 0
    for _ in range(150):
        num_vars = rng.randint(3, 4)
        m = rng.randint(2, 6)
        clauses = random_3cnf(rng, num_vars, m)
        labels, edges = sat_to_independent_set(clauses)
        alpha = max_independent_set_size(len(labels), edges)
        opt = max_satisfied(clauses, num_vars)
        assert alpha == opt
        c = Fraction(1)
        if opt == m:
            sat_seen += 1
            assert alpha >= c * m
        else:
            unsat_seen += 1
            s = Fraction(opt, m)
            assert alpha <= s * m < c * m
    assert sat_seen > 0


def test_unsatisfiable_instances() -> None:
    rng = random.Random(3)
    for _ in range(10):
        extra = random_3cnf(rng, 3, rng.randint(0, 2))
        clauses = ALL_EIGHT + extra
        labels, edges = sat_to_independent_set(clauses)
        alpha = max_independent_set_size(len(labels), edges)
        opt = max_satisfied(clauses, 3)
        assert opt < len(clauses)
        assert alpha == opt


def test_solution_maps() -> None:
    rng = random.Random(11)
    for _ in range(40):
        num_vars = 4
        m = rng.randint(1, 5)
        clauses = random_3cnf(rng, num_vars, m)
        labels, edges = sat_to_independent_set(clauses)
        for s in independent_sets(len(labels), edges):
            a = independent_set_to_assignment(clauses, num_vars, s)
            assert satisfied_count(clauses, a) >= len(s)
        for bits in product((False, True), repeat=num_vars):
            a = {v + 1: bits[v] for v in range(num_vars)}
            s = assignment_to_independent_set(clauses, a)
            assert is_independent(s, edges)
            assert len(s) == satisfied_count(clauses, a)
