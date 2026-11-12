# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/consensus-clustering/. The authors are listed in prov/B4JZZB.jsonl.

import random
from fractions import Fraction
from itertools import combinations, permutations

from consensus_clustering import (
    best_input,
    canonical,
    co_association,
    consensus,
    majority_pivot,
    majority_pivot_order,
    median_partition,
    mirkin_distance,
    mirkin_distance_naive,
    set_partitions,
    total_distance,
    weighted_cost,
)


def random_labels(rng, n):
    k = rng.randint(1, n)
    return [rng.randrange(k) for _ in range(n)]


def random_ensemble(rng, n, m):
    return [random_labels(rng, n) for _ in range(m)]


def exact_pivot_costs(labelings):
    """Total distance of the majority pivot output for every order of the items."""
    n = len(labelings[0])
    W = co_association(labelings)
    return [total_distance(majority_pivot_order(W, o), labelings) for o in permutations(range(n))]


def test_set_partitions_counts_are_bell_numbers():
    assert [sum(1 for _ in set_partitions(n)) for n in range(8)] == [1, 1, 2, 5, 15, 52, 203, 877]


def test_mirkin_distance_by_contingency_table_matches_pair_scan():
    rng = random.Random(1)
    for _ in range(200):
        n = rng.randint(1, 12)
        a, b = random_labels(rng, n), random_labels(rng, n)
        assert mirkin_distance(a, b) == mirkin_distance_naive(a, b)
        assert mirkin_distance(a, a) == 0
        assert mirkin_distance(a, b) == mirkin_distance(b, a)


def test_reduction_to_correlation_clustering_is_exact():
    # sum_i d(P, P_i) = m * (sum of w+ over split pairs + sum of w- over joined pairs)
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randint(1, 9)
        m = rng.randint(1, 6)
        labs = random_ensemble(rng, n, m)
        W = co_association(labs)
        P = random_labels(rng, n)
        assert Fraction(total_distance(P, labs)) == m * weighted_cost(P, W)


def test_median_is_the_correlation_clustering_optimum():
    rng = random.Random(3)
    for _ in range(25):
        n = rng.randint(2, 6)
        m = rng.randint(2, 5)
        labs = random_ensemble(rng, n, m)
        W = co_association(labs)
        opt, arg = median_partition(labs)
        best_cc = min(weighted_cost(P, W) for P in set_partitions(n))
        assert m * best_cc == opt
        assert all(m * weighted_cost(P, W) == opt for P in arg)


def test_weights_satisfy_probability_and_triangle_constraints():
    rng = random.Random(4)
    for _ in range(50):
        n = rng.randint(3, 8)
        labs = random_ensemble(rng, n, rng.randint(1, 6))
        W = co_association(labs)
        for u, v, w in combinations(range(n), 3):
            for a, b, c in ((u, v, w), (u, w, v), (v, w, u)):
                # w- = 1 - w+ is a pseudometric
                assert (1 - W[a][b]) <= (1 - W[a][c]) + (1 - W[c][b])


def test_best_input_is_within_2_minus_2_over_m():
    rng = random.Random(5)
    for _ in range(40):
        n = rng.randint(2, 6)
        m = rng.randint(1, 5)
        labs = random_ensemble(rng, n, m)
        opt, _ = median_partition(labs)
        assert total_distance(best_input(labs), labs) <= Fraction(2 * (m - 1), m) * opt


def test_exact_expected_ratios_of_pivot_and_combined_algorithm():
    # Over all n! orders: E[pivot] <= 2 OPT, and E[min(pivot, best input)] <= 11/7 OPT.
    rng = random.Random(6)
    for _ in range(25):
        n = rng.randint(2, 6)
        m = rng.randint(2, 5)
        labs = random_ensemble(rng, n, m)
        opt, _ = median_partition(labs)
        costs = exact_pivot_costs(labs)
        b = total_distance(best_input(labs), labs)
        expected_pivot = Fraction(sum(costs), len(costs))
        expected_combined = Fraction(sum(min(c, b) for c in costs), len(costs))
        assert expected_pivot <= 2 * opt
        assert expected_combined <= Fraction(11, 7) * opt


def test_worked_example():
    labs = [[0, 0, 0, 1, 1, 1], [0, 0, 1, 1, 2, 2], [0, 0, 0, 0, 1, 1]]
    W = co_association(labs)
    assert W[0][2] == Fraction(2, 3) and W[2][3] == Fraction(2, 3) and W[3][4] == Fraction(1, 3)
    assert median_partition(labs) == (8, [[0, 0, 0, 1, 2, 2]])
    assert [total_distance(lab, labs) for lab in labs] == [10, 9, 9]
    costs = exact_pivot_costs(labs)
    assert Fraction(sum(costs), len(costs)) == Fraction(17, 2)
    assert sorted(set(costs)) == [8, 9] and costs.count(8) == 360
    assert canonical(majority_pivot_order(W, [2, 0, 1, 3, 4, 5])) == [0, 0, 0, 0, 1, 1]
    assert canonical(majority_pivot_order(W, [0, 1, 2, 3, 4, 5])) == [0, 0, 0, 1, 2, 2]


def test_unanimous_inputs_are_returned():
    rng = random.Random(7)
    for _ in range(30):
        n = rng.randint(1, 15)
        P = canonical(random_labels(rng, n))
        assert consensus([P, list(P), list(P)], rng) == P


def test_random_runs_return_partitions_no_worse_than_best_input():
    rng = random.Random(8)
    for _ in range(40):
        n = rng.randint(1, 25)
        labs = random_ensemble(rng, n, rng.randint(1, 7))
        out = consensus(labs, rng)
        assert len(out) == n and out == canonical(out)
        assert total_distance(out, labs) <= total_distance(best_input(labs), labs)
        W = co_association(labs)
        assert len(majority_pivot(W, rng)) == n
