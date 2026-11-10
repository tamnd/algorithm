# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clique-inapproximability/. The authors are listed in prov/KWSQM6.jsonl.

import random
from fractions import Fraction
from itertools import product

from clique_inapproximability import (
    acceptance_count,
    clause_verifier,
    clique_to_proof,
    fglss_graph,
    max_acceptance,
    max_clique,
    repeat_verifier,
)

XOR_FREE = [(1, 2), (-1, 2), (1, -2), (-1, -2)]  # every assignment of two variables fails one clause


def random_verifier(rng: random.Random, proof_length: int, num_tests: int, q: int):
    tests = []
    for _ in range(num_tests):
        pos = tuple(sorted(rng.sample(range(proof_length), q)))
        acc = frozenset(b for b in product((0, 1), repeat=q) if rng.random() < 0.6)
        tests.append((pos, acc))
    return tests


def check_clique(adj: list[int], clique: list[int]) -> bool:
    return all(adj[u] >> v & 1 for u in clique for v in clique if u != v)


def test_clique_number_equals_best_acceptance() -> None:
    rng = random.Random(1)
    for _ in range(200):
        length = rng.randint(1, 5)
        q = rng.randint(1, min(3, length))
        tests = random_verifier(rng, length, rng.randint(1, 6), q)
        verts, adj = fglss_graph(tests)
        assert len(verts) <= len(tests) * 2 ** q
        clique = max_clique(adj)
        assert check_clique(adj, clique)
        assert len(clique) == max_acceptance(tests, length)
        proof = clique_to_proof(tests, verts, clique, length)
        assert acceptance_count(tests, proof) >= len(clique)


def test_each_proof_gives_a_clique_of_its_accepting_views() -> None:
    rng = random.Random(2)
    for _ in range(60):
        length = rng.randint(1, 4)
        tests = random_verifier(rng, length, rng.randint(1, 5), rng.randint(1, length))
        verts, adj = fglss_graph(tests)
        index = {v: i for i, v in enumerate(verts)}
        for proof in product((0, 1), repeat=length):
            views = []
            for r, (pos, acc) in enumerate(tests):
                a = tuple(proof[i] for i in pos)
                if a in acc:
                    views.append(index[(r, a)])
            assert check_clique(adj, views)
            assert len(views) == acceptance_count(tests, proof)


def test_completeness_and_soundness_of_the_clause_verifier() -> None:
    rng = random.Random(3)
    for _ in range(100):
        num_vars = rng.randint(2, 4)
        m = rng.randint(1, 6)
        clauses = []
        for _ in range(m):
            k = rng.randint(1, min(3, num_vars))
            vs = rng.sample(range(1, num_vars + 1), k)
            clauses.append(tuple(v if rng.random() < 0.5 else -v for v in vs))
        tests = clause_verifier(clauses)
        verts, adj = fglss_graph(tests)
        omega = len(max_clique(adj))
        best = max_acceptance(tests, num_vars)
        assert omega == best
        if best == m:
            assert omega >= 1 * m
        else:
            s = Fraction(best, m)
            assert omega <= s * m < m


def test_example_and_repetition() -> None:
    tests = clause_verifier(XOR_FREE)
    verts, adj = fglss_graph(tests)
    assert len(verts) == 12
    assert len(max_clique(adj)) == 3
    rep = repeat_verifier(tests, 2)
    verts2, adj2 = fglss_graph(rep)
    assert len(rep) == 16 and len(verts2) == 36
    assert len(max_clique(adj2)) == 9


def test_repetition_squares_the_soundness() -> None:
    rng = random.Random(4)
    for _ in range(12):
        m = rng.randint(2, 4)
        clauses = [tuple(v if rng.random() < 0.5 else -v for v in rng.sample(range(1, 4), 2)) for _ in range(m)]
        tests = clause_verifier(clauses)
        best = max_acceptance(tests, 3)
        rep = repeat_verifier(tests, 2)
        _, adj = fglss_graph(rep)
        assert len(max_clique(adj)) == best * best
