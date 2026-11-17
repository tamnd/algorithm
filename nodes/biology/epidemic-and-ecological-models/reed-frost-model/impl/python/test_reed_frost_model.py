# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reed-frost-model/. The authors are listed in prov/PA1DQR.jsonl.

import random
from fractions import Fraction as F

from biostoch import chi2_sf
from reed_frost_model import (
    chain_probability,
    chains_by_graphs,
    final_size,
    final_size_distribution,
    infection_probability,
    simulate,
)


def test_household_of_three():
    # One case and two susceptibles, p = 1/5.
    p = F(1, 5)
    assert chain_probability([1, 0], 2, p) == F(16, 25)
    assert chain_probability([1, 1, 0], 2, p) == F(32, 125)
    assert chain_probability([1, 1, 1, 0], 2, p) == F(8, 125)
    assert chain_probability([1, 2, 0], 2, p) == F(1, 25)
    assert final_size_distribution(2, 1, p) == {0: F(16, 25), 1: F(32, 125), 2: F(13, 125)}


def test_chain_law_equals_random_graph_layers():
    for s0, i0, p in ((4, 1, F(1, 3)), (3, 2, F(2, 5)), (5, 1, F(1, 4))):
        by_graph = chains_by_graphs(s0, i0, p)
        assert sum(by_graph.values()) == 1
        for chain, w in by_graph.items():
            assert chain_probability(list(chain), s0, p) == w
        sizes = {}
        for chain, w in by_graph.items():
            k = sum(chain) - i0
            sizes[k] = sizes.get(k, 0) + w
        assert final_size_distribution(s0, i0, p) == dict(sorted(sizes.items()))


def test_greenwood_differs_only_when_two_cases_meet_one_susceptible():
    p = F(1, 5)
    assert infection_probability(p, 2) == F(9, 25)
    assert infection_probability(p, 2, greenwood=True) == p
    rf = final_size_distribution(4, 1, p)
    gw = final_size_distribution(4, 1, p, greenwood=True)
    assert rf[0] == gw[0] == F(256, 625)
    assert rf[1] == gw[1]
    assert rf[4] > gw[4]
    assert sum(rf.values()) == sum(gw.values()) == 1


def test_simulation_matches_exact_final_size_law():
    rng = random.Random(20261118)
    s0, p, n = 10, 0.15, 4000
    exact = final_size_distribution(s0, 1, p)
    counts = [0] * (s0 + 1)
    for _ in range(n):
        counts[final_size(simulate(rng, s0, 1, p))] += 1
    stat = sum((counts[k] - n * exact[k]) ** 2 / (n * exact[k]) for k in range(s0 + 1))
    assert chi2_sf(stat, s0) > 0.001


def test_path_invariants():
    rng = random.Random(5)
    path = simulate(rng, 30, 2, 0.08)
    assert path[0] == (30, 2) and path[-1][1] == 0
    for (s, i), (s2, i2) in zip(path, path[1:]):
        assert s2 == s - i2 and 0 <= i2 <= s


def test_large_population_follows_branching_and_final_size():
    # N = 1000 and p = R0 / N with R0 = 2: about 0.203 of the runs stay
    # minor, and a major outbreak infects about 0.797 of the population.
    rng = random.Random(11)
    N, runs = 1000, 2000
    sizes = [final_size(simulate(rng, N - 1, 1, 2.0 / N)) for _ in range(runs)]
    major = [x for x in sizes if x > 100]
    minor = 1 - len(major) / runs
    assert abs(minor - 0.203) < 0.04
    assert abs(sum(major) / len(major) / N - 0.797) < 0.02
