# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/belief-propagation/. The authors are listed in prov/5AZ02P.jsonl.

import random
from fractions import Fraction
from itertools import product

import pytest

from belief_propagation import Factor, belief_propagation


def enumerate_joint(factors, card, evidence):
    out = {}
    for x in product(*(range(c) for c in card)):
        if any(x[v] != val for v, val in evidence.items()):
            continue
        w = Fraction(1)
        for f in factors:
            w *= f.table[tuple(x[v] for v in f.scope)]
        out[x] = w
    return out


def check(factors, card, evidence):
    joint = enumerate_joint(factors, card, evidence)
    z = sum(joint.values())
    if z == 0:
        with pytest.raises(ValueError):
            belief_propagation(factors, card, evidence)
        return
    res = belief_propagation(factors, card, evidence)
    assert res.partition == z
    for v in range(len(card)):
        for val in range(card[v]):
            assert res.marginals[v][val] == sum(w for x, w in joint.items() if x[v] == val) / z
    for f, bf in zip(factors, res.factor_marginals):
        for a, p in bf.items():
            assert p == sum(w for x, w in joint.items() if tuple(x[v] for v in f.scope) == a) / z
    edges = sum(len(f.scope) for f in factors)
    assert res.messages == 2 * edges


def table(rng, scope, card, zeros=True):
    lo = 0 if zeros else 1
    return Factor(scope, {a: Fraction(rng.randint(lo, 4)) for a in product(*(range(card[v]) for v in scope))})


def random_factor_tree(rng, n):
    """Grow a factor tree: each new factor touches one old variable and some new ones."""
    card = [rng.choice([2, 2, 3]) for _ in range(n)]
    factors = [table(rng, (0,), card)]
    v = 1
    while v < n:
        k = rng.randint(1, min(2, n - v))
        old = rng.randrange(v)
        scope = [old] + list(range(v, v + k))
        rng.shuffle(scope)
        factors.append(table(rng, tuple(scope), card))
        v += k
    for _ in range(rng.randint(0, 3)):
        u = rng.randrange(n)
        factors.append(table(rng, (u,), card))
    return factors, card


def random_polytree(rng, n):
    """A Bayesian network whose skeleton is a tree; its factor graph is a tree."""
    card = [2] * n
    parents = {v: [] for v in range(n)}
    for v in range(1, n):
        u = rng.randrange(v)
        if rng.random() < 0.5:
            parents[v].append(u)
        else:
            parents[u].append(v)
    factors = []
    for v in range(n):
        pa = tuple(parents[v])
        t = {}
        for p in product((0, 1), repeat=len(pa)):
            q = Fraction(rng.randint(0, 10), 10)
            t[(1,) + p] = q
            t[(0,) + p] = 1 - q
        factors.append(Factor((v,) + pa, t))
    return factors, card


def test_chain_by_hand():
    # A chain X0 - X1 with P(X0=1) = 1/4 and P(X1=1 | X0) = 1/2, 9/10.
    f0 = Factor((0,), {(0,): Fraction(3, 4), (1,): Fraction(1, 4)})
    f1 = Factor((1, 0), {(0, 0): Fraction(1, 2), (1, 0): Fraction(1, 2),
                         (0, 1): Fraction(1, 10), (1, 1): Fraction(9, 10)})
    res = belief_propagation([f0, f1], [2, 2], {})
    assert res.marginals[1][1] == Fraction(3, 8) + Fraction(9, 40)
    res = belief_propagation([f0, f1], [2, 2], {1: 1})
    assert res.partition == Fraction(3, 5)
    assert res.marginals[0][1] == Fraction(9, 40) / Fraction(3, 5)
    assert res.messages == 6


def test_random_factor_trees():
    rng = random.Random(5)
    for _ in range(300):
        n = rng.randint(1, 8)
        factors, card = random_factor_tree(rng, n)
        ev = {v: rng.randrange(card[v]) for v in rng.sample(range(n), rng.randint(0, min(2, n)))}
        check(factors, card, ev)


def test_random_polytrees_pearl_setting():
    rng = random.Random(9)
    for _ in range(300):
        n = rng.randint(1, 8)
        factors, card = random_polytree(rng, n)
        ev = {v: rng.randrange(2) for v in rng.sample(range(n), rng.randint(0, min(3, n)))}
        check(factors, card, ev)


def test_forest_and_isolated_variables():
    rng = random.Random(1)
    card = [2, 3, 2, 2, 2]
    factors = [table(rng, (0, 1), card, zeros=False), table(rng, (3, 4), card, zeros=False)]
    check(factors, card, {})
    check(factors, card, {4: 1})


def test_cycles_are_rejected():
    card = [2, 2, 2]
    tri = [Factor(s, {a: 1 for a in product((0, 1), repeat=2)}) for s in ((0, 1), (1, 2), (0, 2))]
    with pytest.raises(ValueError):
        belief_propagation(tri, card, {})
    two = [Factor((0, 1), {a: 1 for a in product((0, 1), repeat=2)})] * 2
    with pytest.raises(ValueError):
        belief_propagation(two, [2, 2], {})
