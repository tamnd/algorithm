# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/max-3sat-inapproximability/. The authors are listed in prov/VXQ2G0.jsonl.

import random
from fractions import Fraction
from itertools import product

from max_3sat_inapproximability import (
    clauses_per_test_bound,
    cnf_of_test,
    max_acceptance,
    max_satisfied,
    satisfied_count,
    split_clause,
    verifier_to_3cnf,
)


def random_test(rng: random.Random, proof_length: int, q: int, rejected: int):
    pos = tuple(sorted(rng.sample(range(proof_length), q)))
    all_tuples = list(product((0, 1), repeat=q))
    bad = set(rng.sample(all_tuples, rejected))
    return pos, frozenset(a for a in all_tuples if a not in bad)


def test_cnf_of_a_test_is_false_exactly_on_rejected_views() -> None:
    rng = random.Random(1)
    for _ in range(50):
        q = rng.randint(1, 4)
        t = random_test(rng, 5, q, rng.randint(0, 2 ** q))
        cnf = cnf_of_test(t)
        for bits in product((0, 1), repeat=5):
            value = {i + 1: bits[i] for i in range(5)}
            accepts = tuple(bits[i] for i in t[0]) in t[1]
            assert (satisfied_count(cnf, value) == len(cnf)) == accepts


def test_split_clause_keeps_satisfiability() -> None:
    for w in range(1, 8):
        clause = tuple(range(1, w + 1))
        parts, nxt = split_clause(clause, w + 1)
        assert len(parts) == max(1, w - 2) and all(len(p) <= 3 for p in parts)
        aux = nxt - (w + 1)
        for bits in product((0, 1), repeat=w):
            value = {i + 1: bits[i] for i in range(w)}
            best = 0
            for ybits in product((0, 1), repeat=aux):
                value.update({w + 1 + k: ybits[k] for k in range(aux)})
                best = max(best, satisfied_count(parts, value))
            if any(bits):
                assert best == len(parts)
            else:
                assert best == len(parts) - 1


def test_each_group_loses_exactly_one_clause_when_its_test_rejects() -> None:
    rng = random.Random(2)
    for _ in range(40):
        q = rng.randint(3, 5)
        t = random_test(rng, q, q, rng.randint(0, 2))
        clauses, groups, num_vars = verifier_to_3cnf([t], q)
        assert len(clauses) <= clauses_per_test_bound(q)
        aux = num_vars - q
        for bits in product((0, 1), repeat=q):
            value = {i + 1: bits[i] for i in range(q)}
            best = 0
            for ybits in product((0, 1), repeat=aux):
                value.update({q + 1 + k: ybits[k] for k in range(aux)})
                best = max(best, satisfied_count(clauses, value))
            accepts = tuple(bits[i] for i in t[0]) in t[1]
            assert best == len(clauses) - (0 if accepts else 1)


def test_whole_formula_completeness_and_soundness() -> None:
    rng = random.Random(3)
    for _ in range(25):
        proof_length, q = 4, rng.choice((3, 4))
        tests = [random_test(rng, proof_length, q, rng.randint(0, 2)) for _ in range(3)]
        clauses, _, num_vars = verifier_to_3cnf(tests, proof_length)
        if num_vars > 11:
            continue
        acc = max_acceptance(tests, proof_length)
        opt = max_satisfied(clauses, num_vars)
        m, r = len(clauses), len(tests)
        assert opt == m - (r - acc)
        if acc == r:
            assert opt == m
        else:
            s = Fraction(acc, r)
            assert Fraction(m - opt, m) >= (1 - s) / clauses_per_test_bound(q)
