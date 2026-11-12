# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variable-elimination/. The authors are listed in prov/ZJC1JG.jsonl.

import random
from fractions import Fraction
from itertools import product

import pytest

from variable_elimination import (Factor, induced_width, sprinkler_network,
                                  variable_elimination)


def brute_force(factors, card, query, evidence):
    """P(query | evidence) by a sum over all joint assignments."""
    n = len(card)
    acc = {}
    for x in product(*(range(c) for c in card)):
        if any(x[v] != val for v, val in evidence.items()):
            continue
        w = Fraction(1)
        for f in factors:
            w *= f.table[tuple(x[v] for v in f.scope)]
        key = tuple(x[q] for q in query)
        acc[key] = acc.get(key, 0) + w
    total = sum(acc.values())
    out = {}
    for key in product(*(range(card[q]) for q in query)):
        out[key] = acc.get(key, 0) / total
    assert n == len(card)
    return out


def random_bn(rng, n):
    card = [rng.choice([2, 2, 2, 3]) if n <= 6 else 2 for _ in range(n)]
    factors = []
    for v in range(n):
        parents = tuple(u for u in range(v) if rng.random() < 0.4)[:3]
        scope = (v,) + parents
        table = {}
        for pa in product(*(range(card[u]) for u in parents)):
            w = [rng.randint(0, 5) for _ in range(card[v])]
            if sum(w) == 0:
                w[0] = 1
            for x in range(card[v]):
                table[(x,) + pa] = Fraction(w[x], sum(w))
        factors.append(Factor(scope, table))
    return factors, card


def test_sprinkler_example():
    factors, card = sprinkler_network()
    pr = variable_elimination(factors, card, [2], {3: 1}, [0, 1])
    ps = variable_elimination(factors, card, [1], {3: 1}, [0, 2])
    assert pr[(1,)] == Fraction(509, 719)
    assert ps[(1,)] == Fraction(309, 719)
    both = variable_elimination(factors, card, [1], {3: 1, 2: 1}, [0])
    assert both[(1,)] == Fraction(99, 509)
    pw = variable_elimination(factors, card, [3], {}, [0, 1, 2])
    assert pw[(1,)] == Fraction(6471, 10000)


def test_order_does_not_change_answer():
    factors, card = sprinkler_network()
    a = variable_elimination(factors, card, [2], {3: 1}, [0, 1])
    b = variable_elimination(factors, card, [2], {3: 1}, [1, 0])
    assert a == b


def test_no_evidence_and_all_query():
    factors, card = sprinkler_network()
    joint = variable_elimination(factors, card, [0, 1, 2, 3], {}, [])
    assert sum(joint.values()) == 1
    assert joint == brute_force(factors, card, [0, 1, 2, 3], {})


def test_zero_evidence_and_bad_order():
    factors, card = sprinkler_network()
    with pytest.raises(ValueError):
        variable_elimination(factors, card, [3], {}, [0, 1])
    with pytest.raises(ValueError):
        variable_elimination(factors, card, [3], {}, [3, 0, 1, 2])
    with pytest.raises(ValueError):
        variable_elimination(factors, card, [0], {3: 1, 1: 0, 2: 0}, [])  # P(W=1, S=0, R=0) = 0


def test_induced_width():
    # A chain has width 1 along its order; a 4-cycle has width 2.
    assert induced_width([(0, 1), (1, 2), (2, 3)], [0, 1, 2, 3]) == 1
    assert induced_width([(0, 1), (1, 2), (2, 3), (3, 0)], [0, 1, 2, 3]) == 2
    # The star with center 0 has width 4 if the center goes first, 1 if it goes last.
    star = [(0, i) for i in range(1, 5)]
    assert induced_width(star, [0, 1, 2, 3, 4]) == 4
    assert induced_width(star, [1, 2, 3, 4, 0]) == 1


def test_random_networks_against_enumeration():
    rng = random.Random(20240611)
    for _ in range(500):
        n = rng.randint(1, 8)
        factors, card = random_bn(rng, n)
        vars_ = list(range(n))
        rng.shuffle(vars_)
        k = rng.randint(1, min(2, n))
        query = vars_[:k]
        rest = vars_[k:]
        evidence = {v: rng.randrange(card[v]) for v in rest if rng.random() < 0.3}
        order = [v for v in rest if v not in evidence]
        rng.shuffle(order)
        try:
            want = brute_force(factors, card, query, evidence)
        except ZeroDivisionError:
            # The evidence has probability zero: the algorithm must refuse.
            with pytest.raises(ValueError):
                variable_elimination(factors, card, query, evidence, order)
            continue
        assert variable_elimination(factors, card, query, evidence, order) == want


def test_markov_random_field_with_zeros():
    rng = random.Random(7)
    for _ in range(200):
        n = rng.randint(2, 7)
        card = [2] * n
        factors = []
        for _ in range(rng.randint(1, 2 * n)):
            u, v = rng.sample(range(n), 2)
            factors.append(Factor((u, v), {(a, b): Fraction(rng.randint(0, 4))
                                           for a in (0, 1) for b in (0, 1)}))
        q = rng.randrange(n)
        order = [v for v in range(n) if v != q]
        rng.shuffle(order)
        try:
            want = brute_force(factors, card, [q], {})
        except ZeroDivisionError:
            with pytest.raises(ValueError):
                variable_elimination(factors, card, [q], {}, order)
            continue
        assert variable_elimination(factors, card, [q], {}, order) == want
