# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ancestral-recombination-graph/. The authors are listed in prov/NNH0F8.jsonl.

import random

import pytest

from ancestral_recombination_graph import (
    ARG,
    COALESCENCE,
    RECOMBINATION,
    covers,
    difference,
    intersect,
    simulate,
    union,
)


def test_interval_algebra_against_a_grid():
    rng = random.Random(1)
    grid = [i / 64 for i in range(64)]
    for _ in range(120):
        def rand():
            cuts = sorted(rng.sample(range(65), 2 * rng.randint(0, 3)))
            return tuple((cuts[i] / 64, cuts[i + 1] / 64) for i in range(0, len(cuts), 2) if cuts[i] < cuts[i + 1])
        a, b = rand(), rand()
        for x in grid:
            assert covers(union(a, b), x) == (covers(a, x) or covers(b, x))
            assert covers(intersect(a, b), x) == (covers(a, x) and covers(b, x))
            assert covers(difference(a, b), x) == (covers(a, x) and not covers(b, x))


def test_hand_built_graph():
    # samples 0, 1, 2. Sample 2 recombines at 0.4: its left part joins 0, its right part joins 1.
    g = ARG()
    s0, s1, s2 = g.add_sample(), g.add_sample(), g.add_sample()
    left, right = g.recombine(s2, 0.4, 0.1)
    a = g.coalesce(s0, left, 0.2)
    b = g.coalesce(s1, right, 0.3)
    g.coalesce(a, b, 0.9)
    assert g.num_recombinations() == 1
    t_left = g.local_tree(0.2)
    t_right = g.local_tree(0.7)
    assert frozenset({0, 2}) in t_left.clusters and frozenset({1, 2}) in t_right.clusters
    assert t_left.tmrca == t_right.tmrca == 0.9
    trees = g.local_trees()
    assert [(l, r) for l, r, _ in trees] == [(0.0, 0.4), (0.4, 1.0)]
    assert g.local_tree_by_material(0.2) == t_left.clusters
    assert g.local_tree_by_material(0.7) == t_right.clusters
    with pytest.raises(ValueError):
        g.coalesce(a, b, 1.0)  # both lineages are already closed


def check_arg(g: ARG, n: int, rng: random.Random):
    """Structural checks, and the two ways of reading a local tree agree."""
    for v, k in enumerate(g.kind):
        for c in g.children[v]:
            assert g.time[c[0]] <= g.time[v]
            assert g.parents[c[0]][c[1]] == v
        if k == COALESCENCE:
            assert len(g.children[v]) == 2
        if k == RECOMBINATION:
            assert len(g.children[v]) == 1 and len(g.parents[v]) == 2
    for x in [rng.random() for _ in range(10)]:
        t = g.local_tree(x)
        assert len(t.clusters) == 2 * n - 1          # a binary tree on n leaves
        assert frozenset(g.samples) in t.clusters
        assert g.local_tree_by_material(x) == t.clusters
        # every cluster pair is nested or disjoint
        for A in t.clusters:
            for B in t.clusters:
                assert A <= B or B <= A or not (A & B)
    trees = g.local_trees()
    assert len(trees) <= g.num_recombinations() + 1
    assert trees[0][0] == 0.0 and trees[-1][1] == 1.0
    for l, r, t in trees:
        assert g.local_tree(l + (r - l) * rng.random()).nodes == t.nodes
    assert len(g.topologies()) <= len(trees)


def test_simulated_graphs_are_valid():
    rng = random.Random(2)
    for _ in range(60):
        n = rng.randint(2, 7)
        rho = rng.choice([0.0, 0.5, 2.0, 6.0])
        g = simulate(n, rho, rng)
        check_arg(g, n, rng)


def test_no_recombination_gives_one_tree():
    rng = random.Random(3)
    for _ in range(50):
        g = simulate(6, 0.0, rng)
        assert g.num_recombinations() == 0
        assert len(g.local_trees()) == 1
        assert len([k for k in g.kind if k == COALESCENCE]) == 5


def test_mean_tmrca_is_kingman_at_every_position():
    # each marginal tree is a Kingman tree, so E[TMRCA] = 2 (1 - 1/n) for any rho
    rng = random.Random(4)
    n, runs = 5, 1000
    for rho in (0.0, 1.5):
        total = sum(simulate(n, rho, rng).local_tree(0.5).tmrca for _ in range(runs))
        mean = total / runs
        expected = 2 * (1 - 1 / n)
        # Var(TMRCA) = sum 4 / (k (k - 1))^2 over k = 2..n, about 1.16 for n = 5
        assert abs(mean - expected) < 4 * (1.2 / runs) ** 0.5


def test_first_event_probability_for_two_samples():
    # two lineages: coalescence at rate 1, recombination at rate 2 * rho / 2 = rho
    rng = random.Random(5)
    rho, runs = 1.5, 4000
    hits = 0
    for _ in range(runs):
        g = simulate(2, rho, rng)
        hits += g.kind[2] == RECOMBINATION   # node 2 is the first event
    p = rho / (1 + rho)
    assert abs(hits / runs - p) < 4 * (p * (1 - p) / runs) ** 0.5


def test_marginal_topology_is_uniform_for_three_samples():
    # for n = 3 each of the three cherries has probability 1/3 at every position
    rng = random.Random(6)
    runs = 1500
    counts = {}
    for _ in range(runs):
        t = simulate(3, 2.0, rng).local_tree(0.3)
        cherry = next(c for c in t.clusters if len(c) == 2)
        counts[cherry] = counts.get(cherry, 0) + 1
    assert len(counts) == 3
    for c in counts.values():
        assert abs(c / runs - 1 / 3) < 4 * ((2 / 9) / runs) ** 0.5


def test_recombinations_on_the_marginal_trees():
    # a recombination whose breakpoint lies in the material of the lineage it splits falls on the
    # marginal tree at that position. Their expected number is (rho / 2) E[tree length] = rho H(n - 1)
    rng = random.Random(7)
    n, rho, runs = 4, 2.0, 1200
    counts = []
    for _ in range(runs):
        g = simulate(n, rho, rng)
        counts.append(sum(
            1 for v, k in enumerate(g.kind)
            if k == RECOMBINATION and covers(g.material[g.children[v][0]], g.breakpoint[v])
        ))
        assert counts[-1] <= g.num_recombinations()
    mean = sum(counts) / runs
    var = sum((c - mean) ** 2 for c in counts) / (runs - 1)
    expected = rho * sum(1 / i for i in range(1, n))
    assert abs(mean - expected) < 4 * (var / runs) ** 0.5


def test_more_recombination_gives_more_trees():
    rng = random.Random(8)
    low = sum(len(simulate(4, 0.5, rng).local_trees()) for _ in range(100))
    high = sum(len(simulate(4, 4.0, rng).local_trees()) for _ in range(100))
    assert low < high
    # two samples always have the same shape, but the coalescence time changes along the sequence
    g = next(g for g in (simulate(2, 3.0, rng) for _ in range(50)) if len(g.local_trees()) > 1)
    assert len(g.topologies()) == 1
