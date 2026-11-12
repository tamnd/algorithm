# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/factor-graph/. The authors are listed in prov/XJS0S3.jsonl.

import random
from fractions import Fraction as F
from itertools import product

from factor_graph import FactorGraph, from_bayesian_network, from_markov_random_field


def rand_table(rng, cards):
    return {vals: F(rng.randint(1, 9)) for vals in product(*(range(c) for c in cards))}


def test_bayesian_network_conversion_preserves_the_joint() -> None:
    rng = random.Random(2001)
    for _ in range(10):
        names = [f"X{i}" for i in range(4)]
        card = {v: rng.randint(2, 3) for v in names}
        parents = {v: [names[j] for j in range(i) if rng.random() < 0.5] for i, v in enumerate(names)}
        cpt = {}
        for v in names:
            cpt[v] = {}
            for u in product(*(range(card[p]) for p in parents[v])):
                w = [rng.randint(1, 9) for _ in range(card[v])]
                cpt[v][u] = [F(x, sum(w)) for x in w]
        fg = from_bayesian_network(card, parents, cpt)
        assert len(fg.factors) == len(names)
        assert fg.partition_function() == 1
        for x in fg.assignments():
            direct = F(1)
            for v in names:
                direct *= cpt[v][tuple(x[p] for p in parents[v])][x[v]]
            assert fg.value(x) == direct


def test_markov_random_field_conversion_preserves_the_joint() -> None:
    rng = random.Random(5)
    card = {"A": 2, "B": 3, "C": 2, "D": 2}
    pots = [(("A", "B"), None), (("B", "C"), None), (("C", "D"), None), (("D", "A"), None)]
    pots = [(s, rand_table(rng, [card[v] for v in s])) for s, _ in pots]
    fg = from_markov_random_field(card, pots)
    z = F(0)
    direct = {}
    for vals in product(*(range(card[v]) for v in sorted(card))):
        x = dict(zip(sorted(card), vals))
        g = F(1)
        for s, t in pots:
            g *= t[tuple(x[v] for v in s)]
        direct[vals] = g
        z += g
    assert fg.partition_function() == z
    assert fg.joint() == {k: v / z for k, v in direct.items()}
    assert sorted(fg.edges()) == sorted((f"psi{k}", v) for k, (s, _) in enumerate(pots) for v in s)


def test_triangle_two_factor_graphs_one_markov_graph() -> None:
    rng = random.Random(9)
    card = {"a": 2, "b": 2, "c": 2}
    pairwise = from_markov_random_field(card, [(s, rand_table(rng, [2, 2])) for s in (("a", "b"), ("b", "c"), ("a", "c"))])
    triple = from_markov_random_field(card, [(("a", "b", "c"), rand_table(rng, [2, 2, 2]))])
    assert not pairwise.is_tree() and triple.is_tree()
    assert len(pairwise.edges()) == 6 and len(triple.edges()) == 3


def kfl_example(rng) -> FactorGraph:
    fg = FactorGraph()
    for v in ("x1", "x2", "x3", "x4", "x5"):
        fg.add_variable(v, 2)
    for name, scope in [("fA", ["x1"]), ("fB", ["x2"]), ("fC", ["x1", "x2", "x3"]), ("fD", ["x3", "x4"]), ("fE", ["x3", "x5"])]:
        fg.add_factor(name, scope, rand_table(rng, [2] * len(scope)))
    return fg


def random_tree_factor_graph(rng: random.Random, n_factors: int) -> FactorGraph:
    fg = FactorGraph()
    fg.add_variable("v0", rng.randint(2, 3))
    count = 1
    for k in range(n_factors):
        anchor = f"v{rng.randrange(count)}"
        new = []
        for _ in range(rng.randint(0, 2)):
            name = f"v{count}"
            fg.add_variable(name, rng.randint(2, 3))
            new.append(name)
            count += 1
        scope = [anchor] + new
        fg.add_factor(f"f{k}", scope, rand_table(rng, [fg.card[v] for v in scope]))
    return fg


def test_sum_product_is_exact_on_trees() -> None:
    rng = random.Random(47)
    graphs = [kfl_example(rng)] + [random_tree_factor_graph(rng, rng.randint(2, 6)) for _ in range(20)]
    for fg in graphs:
        assert fg.is_tree()
        bp = fg.sum_product_marginals()
        for v in fg.card:
            assert bp[v] == fg.brute_force_marginal(v)


def test_sum_product_refuses_a_cycle() -> None:
    rng = random.Random(1)
    fg = from_markov_random_field({"a": 2, "b": 2, "c": 2}, [(s, rand_table(rng, [2, 2])) for s in (("a", "b"), ("b", "c"), ("a", "c"))])
    try:
        fg.sum_product_marginals()
    except ValueError:
        return
    raise AssertionError("expected ValueError")
