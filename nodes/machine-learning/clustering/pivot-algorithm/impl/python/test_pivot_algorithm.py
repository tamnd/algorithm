# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pivot-algorithm/. The authors are listed in prov/85NC9H.jsonl.

import random
from fractions import Fraction
from itertools import combinations, permutations

from pivot_algorithm import (
    bad_triangles,
    disagreements,
    expected_cost,
    hit_triangles,
    kwik_cluster,
    kwik_cluster_order,
    optimum,
    set_partitions,
)


def graph(n, edges):
    P = [[False] * n for _ in range(n)]
    for u, v in edges:
        P[u][v] = P[v][u] = True
    return P


def random_instance(rng, n, p=0.5):
    P = [[False] * n for _ in range(n)]
    for u, v in combinations(range(n), 2):
        if rng.random() < p:
            P[u][v] = P[v][u] = True
    return P


def test_set_partitions_counts_are_bell_numbers():
    assert [sum(1 for _ in set_partitions(n)) for n in range(8)] == [1, 1, 2, 5, 15, 52, 203, 877]


def test_exact_expected_cost_is_at_most_three_times_opt():
    rng = random.Random(1)
    for _ in range(60):
        n = rng.randint(2, 6)
        P = random_instance(rng, n, rng.choice([0.3, 0.5, 0.7]))
        opt, _ = optimum(P)
        assert expected_cost(P) <= 3 * opt
        if opt == 0:
            assert expected_cost(P) == 0


def test_cost_equals_number_of_hit_bad_triangles():
    rng = random.Random(2)
    for _ in range(25):
        n = rng.randint(3, 6)
        P = random_instance(rng, n)
        for order in permutations(range(n)):
            clusters = kwik_cluster_order(P, order)
            assert disagreements(P, clusters) == len(hit_triangles(P, order))


def test_fractional_packing_of_bad_triangles():
    # beta_T = Pr[T is hit] / 3 sums to at most 1 over the bad triangles on each pair,
    # and sum_T beta_T equals the expected cost divided by 3.
    rng = random.Random(3)
    for _ in range(12):
        n = rng.randint(3, 6)
        P = random_instance(rng, n)
        bad = bad_triangles(P)
        hits = {t: 0 for t in bad}
        orders = list(permutations(range(n)))
        for order in orders:
            for t in hit_triangles(P, order):
                hits[t] += 1
        beta = {t: Fraction(hits[t], 3 * len(orders)) for t in bad}
        for e in combinations(range(n), 2):
            assert sum(beta[t] for t in bad if set(e) <= set(t)) <= 1
        assert 3 * sum(beta.values()) == expected_cost(P)
        assert sum(beta.values()) <= optimum(P)[0]


def test_worked_example():
    P = graph(5, [(0, 1), (0, 2), (1, 2), (2, 3), (3, 4)])
    assert optimum(P) == (1, [[0, 1, 2], [3, 4]])
    assert expected_cost(P) == Fraction(9, 5)
    assert bad_triangles(P) == [(0, 2, 3), (1, 2, 3), (2, 3, 4)]
    assert kwik_cluster_order(P, [2, 0, 1, 3, 4]) == [[0, 1, 2, 3], [4]]
    assert kwik_cluster_order(P, [0, 1, 2, 3, 4]) == [[0, 1, 2], [3, 4]]
    star = graph(4, [(0, 1), (0, 2), (0, 3)])
    assert optimum(star)[0] == 2 and expected_cost(star) == Fraction(9, 4)


def test_disjoint_cliques_are_recovered():
    rng = random.Random(5)
    blocks = [[0, 1, 2], [3, 4], [5], [6, 7, 8, 9]]
    E = [(u, v) for b in blocks for u, v in combinations(b, 2)]
    P = graph(10, E)
    for _ in range(20):
        clusters = kwik_cluster(P, rng)
        assert sorted(clusters) == blocks
        assert disagreements(P, clusters) == 0


def test_random_runs_give_partitions():
    rng = random.Random(6)
    for _ in range(50):
        n = rng.randint(1, 30)
        P = random_instance(rng, n)
        clusters = kwik_cluster(P, rng)
        assert sorted(v for c in clusters for v in c) == list(range(n))
