# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/max-product/. The authors are listed in prov/SMKERH.jsonl.

import random
from fractions import Fraction
from itertools import product

import pytest

from max_product import Factor, max_product, max_sum, to_log


def value_of(factors, x):
    w = Fraction(1)
    for f in factors:
        w *= f.table[tuple(x[v] for v in f.scope)]
    return w


def brute(factors, card, evidence):
    best, mm = None, [[Fraction(0)] * c for c in card]
    for x in product(*(range(c) for c in card)):
        if any(x[v] != val for v, val in evidence.items()):
            continue
        w = value_of(factors, x)
        best = w if best is None or w > best else best
        for v in range(len(card)):
            mm[v][x[v]] = max(mm[v][x[v]], w)
    return best, mm


def random_factor_tree(rng, n):
    card = [rng.choice([2, 2, 3]) for _ in range(n)]

    def table(scope):
        # Small integers give many ties.
        return Factor(scope, {a: Fraction(rng.randint(0, 3)) for a in product(*(range(card[v]) for v in scope))})
    factors = [table((0,))]
    v = 1
    while v < n:
        k = rng.randint(1, min(2, n - v))
        scope = [rng.randrange(v)] + list(range(v, v + k))
        rng.shuffle(scope)
        factors.append(table(tuple(scope)))
        v += k
    for _ in range(rng.randint(0, 2)):
        factors.append(table((rng.randrange(n),)))
    return factors, card


def test_random_factor_trees_against_brute_force():
    rng = random.Random(4)
    for _ in range(400):
        n = rng.randint(1, 8)
        factors, card = random_factor_tree(rng, n)
        ev = {v: rng.randrange(card[v]) for v in rng.sample(range(n), rng.randint(0, min(2, n)))}
        best, mm = brute(factors, card, ev)
        if best == 0:
            with pytest.raises(ValueError):
                max_product(factors, card, ev)
            continue
        res = max_product(factors, card, ev)
        assert res.value == best
        assert all(res.assignment[v] == val for v, val in ev.items())
        assert value_of(factors, res.assignment) == best
        assert res.max_marginals == mm
        assert res.messages == 2 * sum(len(f.scope) for f in factors)
        # Max-sum in log space finds an assignment of the same value.
        ls = max_sum(to_log(factors), card, ev)
        assert value_of(factors, ls.assignment) == best


def test_ties_need_backtracking():
    # f(x, y) = 1 when x != y: both max-marginals are (1, 1), and the
    # argmax of each one alone gives (0, 0), which has value 0.
    f = Factor((0, 1), {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 0})
    res = max_product([f], [2, 2], {})
    assert res.max_marginals == [[1, 1], [1, 1]]
    alone = tuple(max(range(2), key=lambda t: (m[t], -t)) for m in res.max_marginals)
    assert value_of([f], alone) == 0
    assert res.assignment in {(0, 1), (1, 0)} and res.value == 1


def test_chain_is_viterbi():
    # A hidden Markov chain of length 3 with two states; compare with brute force.
    init = Factor((0,), {(0,): Fraction(6, 10), (1,): Fraction(4, 10)})
    trans = {(0, 0): Fraction(7, 10), (0, 1): Fraction(3, 10), (1, 0): Fraction(4, 10), (1, 1): Fraction(6, 10)}
    emit = [{0: Fraction(5, 10), 1: Fraction(1, 10)}, {0: Fraction(4, 10), 1: Fraction(3, 10)},
            {0: Fraction(1, 10), 1: Fraction(6, 10)}]
    factors = [init]
    for t in range(2):
        factors.append(Factor((t, t + 1), {(a, b): trans[a, b] for a in (0, 1) for b in (0, 1)}))
    for t in range(3):
        factors.append(Factor((t,), {(s,): emit[t][s] for s in (0, 1)}))
    res = max_product(factors, [2, 2, 2], {})
    best, _ = brute(factors, [2, 2, 2], {})
    assert res.value == best == value_of(factors, res.assignment)


def test_cycle_rejected():
    tri = [Factor(s, {a: 1 for a in product((0, 1), repeat=2)}) for s in ((0, 1), (1, 2), (0, 2))]
    with pytest.raises(ValueError):
        max_product(tri, [2, 2, 2], {})
