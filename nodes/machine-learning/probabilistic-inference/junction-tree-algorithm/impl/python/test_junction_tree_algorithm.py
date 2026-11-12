# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/junction-tree-algorithm/. The authors are listed in prov/RT2GC9.jsonl.

import random
from fractions import Fraction
from itertools import product

import pytest

from junction_tree_algorithm import (Factor, junction_tree_algorithm, project, shafer_shenoy,
                                     sprinkler_network)


def enumerate_joint(factors, card, evidence):
    """The unnormalized joint restricted to the evidence, as a dict."""
    out = {}
    for x in product(*(range(c) for c in card)):
        if any(x[v] != val for v, val in evidence.items()):
            continue
        w = Fraction(1)
        for f in factors:
            w *= f.table[tuple(x[v] for v in f.scope)]
        out[x] = w
    return out


def random_bn(rng, n):
    card = [rng.choice([2, 2, 3]) if n <= 6 else 2 for _ in range(n)]
    factors = []
    for v in range(n):
        parents = tuple(u for u in range(v) if rng.random() < 0.45)[:3]
        table = {}
        for pa in product(*(range(card[u]) for u in parents)):
            w = [rng.randint(0, 4) for _ in range(card[v])]
            if sum(w) == 0:
                w[0] = 1
            for x in range(card[v]):
                table[(x,) + pa] = Fraction(w[x], sum(w))
        factors.append(Factor((v,) + parents, table))
    return factors, card


def random_mrf(rng, n):
    card = [2] * n
    factors = []
    for _ in range(rng.randint(1, 2 * n)):
        scope = tuple(rng.sample(range(n), rng.randint(1, min(3, n))))
        factors.append(Factor(scope, {a: Fraction(rng.randint(0, 3)) for a in product((0, 1), repeat=len(scope))}))
    return factors, card


def check_against_enumeration(res, factors, card, evidence):
    joint = enumerate_joint(factors, card, evidence)
    pe = sum(joint.values())
    assert res.evidence_probability == pe
    for i, c in enumerate(res.cliques):
        want = {}
        for x, w in joint.items():
            key = tuple(x[v] for v in c)
            want[key] = want.get(key, 0) + w
        for a, p in res.potentials[i].items():
            assert p == want.get(a, 0)
    for v in range(len(card)):
        m = res.marginal(v)
        for val in range(card[v]):
            assert m[val] == sum(w for x, w in joint.items() if x[v] == val) / pe


def check_calibrated(res):
    for i, j in res.tree_edges:
        s = tuple(sorted(set(res.cliques[i]) & set(res.cliques[j])))
        assert project(res.cliques[i], res.potentials[i], s) == project(res.cliques[j], res.potentials[j], s)


def check_rip(res):
    nb = {i: set() for i in range(len(res.cliques))}
    for i, j in res.tree_edges:
        nb[i].add(j)
        nb[j].add(i)
    for x in set().union(*map(set, res.cliques)):
        hold = {i for i, c in enumerate(res.cliques) if x in c}
        start = min(hold)
        seen, stack = {start}, [start]
        while stack:
            a = stack.pop()
            for b in nb[a] & hold:
                if b not in seen:
                    seen.add(b)
                    stack.append(b)
        assert seen == hold


def test_sprinkler_example():
    factors, card = sprinkler_network()
    res = junction_tree_algorithm(factors, card, {3: 1}, order=[3, 0, 1, 2])
    assert res.cliques == [(1, 2, 3), (0, 1, 2)]
    assert res.messages == 2
    assert res.evidence_probability == Fraction(6471, 10000)
    assert res.marginal(2)[1] == Fraction(509, 719)
    assert res.marginal(1)[1] == Fraction(309, 719)
    assert res.marginal(0)[1] == Fraction(414, 719)
    check_calibrated(res)
    # Before any evidence, the separator {S, R} holds P(S, R).
    res0 = junction_tree_algorithm(factors, card, {}, order=[3, 0, 1, 2])
    sr = project(res0.cliques[1], res0.potentials[1], (1, 2))
    assert sr == {(0, 0): Fraction(29, 100), (0, 1): Fraction(41, 100),
                  (1, 0): Fraction(21, 100), (1, 1): Fraction(9, 100)}


def test_random_bayesian_networks_against_enumeration():
    rng = random.Random(7)
    for _ in range(250):
        n = rng.randint(1, 8)
        factors, card = random_bn(rng, n)
        evidence = {v: rng.randrange(card[v]) for v in rng.sample(range(n), rng.randint(0, min(2, n)))}
        if sum(enumerate_joint(factors, card, evidence).values()) == 0:
            with pytest.raises(ValueError):
                junction_tree_algorithm(factors, card, evidence)
            continue
        order = list(range(n))
        rng.shuffle(order)
        for o in (None, order):
            res = junction_tree_algorithm(factors, card, evidence, o)
            check_against_enumeration(res, factors, card, evidence)
            check_calibrated(res)
            check_rip(res)
            assert res.messages == 2 * (len(res.cliques) - 1)
            ss = shafer_shenoy(factors, card, evidence, o)
            assert ss.potentials == res.potentials and ss.messages == res.messages


def test_markov_random_fields_with_zeros_and_disconnected_parts():
    rng = random.Random(11)
    for _ in range(250):
        n = rng.randint(1, 7)
        factors, card = random_mrf(rng, n)
        evidence = {v: rng.randrange(2) for v in rng.sample(range(n), rng.randint(0, 1))}
        if sum(enumerate_joint(factors, card, evidence).values()) == 0:
            with pytest.raises(ValueError):
                junction_tree_algorithm(factors, card, evidence)
            continue
        res = junction_tree_algorithm(factors, card, evidence)
        check_against_enumeration(res, factors, card, evidence)
        check_calibrated(res)
        assert shafer_shenoy(factors, card, evidence).potentials == res.potentials


def test_bad_order():
    factors, card = sprinkler_network()
    with pytest.raises(ValueError):
        junction_tree_algorithm(factors, card, {}, order=[0, 1, 2])
