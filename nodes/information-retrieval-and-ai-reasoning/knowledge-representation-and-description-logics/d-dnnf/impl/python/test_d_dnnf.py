# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/d-dnnf/. The authors are listed in prov/FSRAPA.jsonl.
"""Tests of the d-DNNF compiler and queries against brute force over all assignments."""

import itertools
import random

from d_dnnf import FALSE, TRUE, Circuit, compile_cnf


def assignments(variables):
    variables = sorted(variables)
    for bits in itertools.product([False, True], repeat=len(variables)):
        yield dict(zip(variables, bits))


def cnf_holds(cnf, a) -> bool:
    return all(any(a[abs(l)] == (l > 0) for l in c) for c in cnf)


def brute_count(cnf, n: int) -> int:
    return sum(cnf_holds(cnf, a) for a in assignments(range(1, n + 1)))


def random_cnf(rng: random.Random, n: int, m: int, width: int = 3):
    cnf = []
    for _ in range(m):
        k = rng.randint(1, min(width, n))
        vs = rng.sample(range(1, n + 1), k)
        cnf.append(tuple(v if rng.random() < 0.5 else -v for v in vs))
    return cnf


def cases(seed: int, count: int, max_n: int):
    rng = random.Random(seed)
    for _ in range(count):
        n = rng.randint(1, max_n)
        m = rng.randint(0, 3 * n)
        yield n, random_cnf(rng, n, m)


def complete(a, n):
    """The assignment a extended with False on the variables 1 to n that it misses."""
    return {v: a.get(v, False) for v in range(1, n + 1)}


def test_equivalent_to_cnf():
    for n, cnf in cases(1, 300, 7):
        c, root = compile_cnf(cnf)
        for a in assignments(range(1, n + 1)):
            assert c.evaluate(root, a) == cnf_holds(cnf, a)


def test_model_count_matches_brute_force():
    for n, cnf in cases(2, 400, 10):
        c, root = compile_cnf(cnf)
        assert c.model_count(root, n) == brute_count(cnf, n)


def test_every_and_node_is_decomposable():
    for n, cnf in cases(3, 300, 12):
        c, root = compile_cnf(cnf)
        vs = c.variables(root)
        for u in vs:
            key = c.nodes[u]
            if key[0] == "and":
                for a, b in itertools.combinations(key[1], 2):
                    assert not (vs[a] & vs[b])


def test_every_or_node_is_deterministic():
    """Brute force: no assignment of vars(u) satisfies two children of an or-node u."""
    for n, cnf in cases(4, 200, 7):
        c, root = compile_cnf(cnf)
        vs = c.variables(root)
        for u in vs:
            key = c.nodes[u]
            if key[0] != "or":
                continue
            for a in assignments(vs[u]):
                assert sum(c.evaluate(ch, a) for ch in key[1]) <= 1


def test_every_or_node_is_a_decision_node():
    for n, cnf in cases(5, 200, 10):
        c, root = compile_cnf(cnf)
        for u in c.reachable(root):
            key = c.nodes[u]
            if key[0] != "or":
                continue
            assert len(key[1]) == 2
            heads = []
            for ch in key[1]:
                k = c.nodes[ch]
                lits = [k[1]] if k[0] == "lit" else [c.nodes[g][1] for g in k[1] if c.nodes[g][0] == "lit"]
                heads.append(set(lits))
            assert any(-l in heads[1] for l in heads[0])


def test_smoothing_keeps_models_and_properties():
    for n, cnf in cases(6, 200, 7):
        c, root = compile_cnf(cnf)
        s = c.smooth(root, range(1, n + 1))
        assert c.is_smooth(s)
        vs = c.variables(s)
        if s not in (FALSE, TRUE):
            assert vs[s] == frozenset(range(1, n + 1))
        for a in assignments(range(1, n + 1)):
            assert c.evaluate(s, a) == c.evaluate(root, a)
        for u in vs:
            key = c.nodes[u]
            if key[0] == "and":
                for x, y in itertools.combinations(key[1], 2):
                    assert not (vs[x] & vs[y])
            if key[0] == "or":
                for a in assignments(vs[u]):
                    assert sum(c.evaluate(ch, a) for ch in key[1]) <= 1


def test_consistency_matches_brute_force():
    for n, cnf in cases(7, 400, 9):
        c, root = compile_cnf(cnf)
        assert c.consistent(root) == (brute_count(cnf, n) > 0)


def test_clause_entailment_matches_brute_force():
    rng = random.Random(8)
    for n, cnf in cases(9, 200, 8):
        c, root = compile_cnf(cnf)
        for _ in range(10):
            clause = random_cnf(rng, n, 1)[0]
            expect = all(any(a[abs(l)] == (l > 0) for l in clause) for a in assignments(range(1, n + 1)) if cnf_holds(cnf, a))
            assert c.entails_clause(root, clause) == expect


def test_conditioning_is_restriction():
    rng = random.Random(10)
    for n, cnf in cases(11, 150, 7):
        c, root = compile_cnf(cnf)
        k = rng.randint(1, n)
        term = {v if rng.random() < 0.5 else -v for v in rng.sample(range(1, n + 1), k)}
        cond = c.condition(root, term)
        for a in assignments(range(1, n + 1)):
            b = dict(a)
            for l in term:
                b[abs(l)] = l > 0
            assert c.evaluate(cond, complete(a, n)) == c.evaluate(root, b)


def test_worked_example():
    cnf = [(1, 2), (-1, 3), (4, 5), (-4, -5)]
    c, root = compile_cnf(cnf)
    assert c.model_count(root, 5) == brute_count(cnf, 5) == 8
    assert c.entails_clause(root, (2, 3))
    assert not c.entails_clause(root, (2,))


def test_constants():
    c = Circuit()
    assert c.model_count(TRUE, 3) == 8
    assert c.model_count(FALSE, 3) == 0
    c, root = compile_cnf([(1,), (-1,)])
    assert root == FALSE
    c, root = compile_cnf([])
    assert root == TRUE
