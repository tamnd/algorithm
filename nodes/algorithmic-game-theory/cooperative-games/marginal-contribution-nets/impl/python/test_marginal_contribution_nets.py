# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/marginal-contribution-nets/. The authors are listed in prov/J0TAYV.jsonl.

import random
from fractions import Fraction
from itertools import combinations
from math import factorial

import pytest

from marginal_contribution_nets import banzhaf, from_game, make_rule, shapley, value


def all_sets(n):
    for r in range(n + 1):
        for S in combinations(range(n), r):
            yield frozenset(S)


def brute_shapley(n, v):
    phi = []
    for i in range(n):
        t = Fraction(0)
        for S in all_sets(n):
            if i in S:
                continue
            s = len(S)
            t += Fraction(factorial(s) * factorial(n - 1 - s), factorial(n)) * (v(S | {i}) - v(S))
        phi.append(t)
    return phi


def brute_banzhaf(n, v):
    out = []
    for i in range(n):
        t = sum(v(S | {i}) - v(S) for S in all_sets(n) if i not in S)
        out.append(Fraction(t, 2 ** (n - 1)))
    return out


def random_rules(rng, n, count):
    rules = []
    for _ in range(count):
        players = list(range(n))
        rng.shuffle(players)
        a = rng.randint(1, n)
        b = rng.randint(0, n - a)
        rules.append(make_rule(players[:a], players[a:a + b], rng.randint(-6, 9)))
    return rules


def test_example_game():
    # v(12) = 4, v(13) = 2, v(123) = 6 (players 0, 1, 2 here): two rules.
    rules = [make_rule({0, 1}, (), 4), make_rule({0, 2}, (), 2)]
    assert [value(rules, S) for S in ({0, 1}, {0, 2}, {1, 2}, {0, 1, 2})] == [4, 2, 0, 6]
    assert shapley(rules, 3) == [3, 2, 1]
    assert banzhaf(rules, 3) == [3, 2, 1]


def test_random_nets_against_enumeration():
    rng = random.Random(2005)
    for _ in range(40):
        n = rng.randint(1, 7)
        rules = random_rules(rng, n, rng.randint(0, 6))
        v = lambda S, rules=rules: value(rules, S)
        assert v(frozenset()) == 0
        assert shapley(rules, n) == brute_shapley(n, v)
        assert banzhaf(rules, n) == brute_banzhaf(n, v)
        assert sum(shapley(rules, n)) == v(frozenset(range(n)))


def test_round_trip_from_game():
    rng = random.Random(4)
    for _ in range(15):
        n = rng.randint(1, 6)
        table = {S: (rng.randint(-5, 10) if S else 0) for S in all_sets(n)}
        rules = from_game(n, table.__getitem__)
        assert all(not Q for _, Q, _ in rules)
        for S in all_sets(n):
            assert value(rules, S) == table[S]
        assert shapley(rules, n) == brute_shapley(n, table.__getitem__)


def test_or_game_is_small_with_negations():
    k = 6
    v = lambda S: 1 if S else 0
    # Without negative literals the dividends give 2^k - 1 rules.
    assert len(from_game(k, v)) == 2 ** k - 1
    # With negative literals, k rules: player i counts if no lower player is present.
    rules = [make_rule({i}, range(i), 1) for i in range(k)]
    for S in all_sets(k):
        assert value(rules, S) == v(S)
    assert shapley(rules, k) == [Fraction(1, k)] * k


def test_graph_game():
    # Edge weights; v(S) is the weight of the edges with both ends in S.
    edges = {(0, 1): 3, (1, 2): 5, (0, 3): -2, (2, 3): 4}
    rules = [make_rule(e, (), w) for e, w in edges.items()]
    expect = [Fraction(0)] * 4
    for (a, b), w in edges.items():
        expect[a] += Fraction(w, 2)
        expect[b] += Fraction(w, 2)
    assert shapley(rules, 4) == expect


def test_fraction_values():
    rules = [make_rule({0}, {1}, Fraction(1, 3)), make_rule({1, 2}, (), Fraction(5, 2))]
    v = lambda S: value(rules, S)
    assert shapley(rules, 3) == brute_shapley(3, v)
    assert banzhaf(rules, 3) == brute_banzhaf(3, v)


def test_invalid_rules():
    with pytest.raises(ValueError):
        make_rule((), {0}, 1)
    with pytest.raises(ValueError):
        make_rule({0, 1}, {1}, 1)
