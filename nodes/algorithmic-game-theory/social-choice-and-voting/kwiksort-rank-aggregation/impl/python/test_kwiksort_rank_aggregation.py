# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kwiksort-rank-aggregation/. The authors are listed in prov/BHYQT7.jsonl.

import random
from fractions import Fraction
from itertools import combinations, permutations

from agtprefs import condorcet_winner, kendall_tau, margins, pairwise, random_profile
from kwiksort_rank_aggregation import (best_input_ranking, fas_cost, kemeny_cost, kwiksort,
                                       kwiksort_aggregate, majority_tournament, pairwise_counts,
                                       partition)

A, B, C, D = 0, 1, 2, 3

# The worked example of the page (the same profile as on the Slater rule page).
EXAMPLE = ((D, B, C, A),) * 4 + ((B, A, D, C),) * 6 + ((C, A, D, B),) * 3


def output_distribution(T, V):
    """The exact distribution of the output of KwikSort on the list V."""
    if len(V) <= 1:
        return {tuple(V): Fraction(1)}
    out = {}
    for p in V:
        left, right = partition(T, V, p)
        for a, pa in output_distribution(T, left).items():
            for b, pb in output_distribution(T, right).items():
                k = a + (p,) + b
                out[k] = out.get(k, 0) + pa * pb / len(V)
    return out


def random_tournament(rng, m):
    T = [[False] * m for _ in range(m)]
    for u, v in combinations(range(m), 2):
        if rng.random() < 0.5:
            T[u][v] = True
        else:
            T[v][u] = True
    return T


def test_example():
    N = pairwise_counts(EXAMPLE, 4)
    assert N == pairwise(EXAMPLE, 4)
    T = majority_tournament(EXAMPLE, 4)
    arcs = {(u, v) for u in range(4) for v in range(4) if T[u][v]}
    assert arcs == {(B, A), (B, C), (D, C), (A, D), (C, A), (D, B)}
    dist = output_distribution(T, [A, B, C, D])
    assert dist == {(B, C, A, D): Fraction(1, 4), (D, B, C, A): Fraction(1, 2),
                    (A, D, B, C): Fraction(1, 4)}
    assert [kemeny_cost(N, r) for r in ((B, C, A, D), (D, B, C, A), (A, D, B, C))] == [33, 30, 33]
    assert sum(p * kemeny_cost(N, r) for r, p in dist.items()) == Fraction(63, 2)
    assert min(kemeny_cost(N, r) for r in permutations(range(4))) == 27
    assert best_input_ranking(EXAMPLE, N) == (B, A, D, C)
    assert kwiksort_aggregate(EXAMPLE, 4, seed=1) == (B, A, D, C)
    assert sum(kendall_tau((B, A, D, C), v) for v in EXAMPLE) == 27


def test_edge_cases():
    rng = random.Random(0)
    T = majority_tournament((), 3)
    assert kwiksort(T, [], rng) == ()
    assert kwiksort(T, [2], rng) == (2,)
    assert kwiksort(T, range(3), rng) == (0, 1, 2)
    assert kwiksort_aggregate((), 3) == (0, 1, 2)
    assert kwiksort_aggregate(((2, 0, 1),), 3) == (2, 0, 1)


def test_transitive_tournament_is_sorted():
    rng = random.Random(1)
    for _ in range(100):
        m = rng.randint(1, 12)
        order = list(range(m))
        rng.shuffle(order)
        T = [[False] * m for _ in range(m)]
        for i in range(m):
            for j in range(i + 1, m):
                T[order[i]][order[j]] = True
        assert kwiksort(T, range(m), rng) == tuple(order)
        assert fas_cost(T, order) == 0


def test_output_is_a_ranking_and_seeded():
    rng = random.Random(2)
    for _ in range(100):
        m, n = rng.randint(1, 9), rng.randint(0, 7)
        P = random_profile(rng, m, n)
        r = kwiksort_aggregate(P, m, seed=5)
        assert sorted(r) == list(range(m))
        assert r == kwiksort_aggregate(P, m, seed=5)


def test_condorcet_winner_and_smith_set_on_top():
    rng = random.Random(3)
    for _ in range(150):
        m, n = rng.randint(2, 8), rng.randint(1, 7)
        P = random_profile(rng, m, n)
        T = majority_tournament(P, m)
        M = margins(P, m)
        smith = None
        for size in range(1, m + 1):
            for S in combinations(range(m), size):
                if all(M[a][b] > 0 for a in S for b in range(m) if b not in S):
                    smith = frozenset(S)
                    break
            if smith:
                break
        r = kwiksort(T, range(m), random.Random(rng.random()))
        assert frozenset(r[:len(smith)]) == smith
        w = condorcet_winner(P, m)
        if w is not None:
            assert r[0] == w


def test_ratio_three_for_feedback_arc_set_in_tournaments():
    rng = random.Random(4)
    for _ in range(40):
        m = rng.randint(2, 6)
        T = random_tournament(rng, m)
        opt = min(fas_cost(T, r) for r in permutations(range(m)))
        dist = output_distribution(T, list(range(m)))
        assert sum(dist.values()) == 1
        expected = sum(p * fas_cost(T, r) for r, p in dist.items())
        assert expected <= 3 * opt


def test_ratios_for_rank_aggregation():
    rng = random.Random(5)
    for _ in range(40):
        m, n = rng.randint(2, 5), rng.choice((3, 4, 5, 6, 7))
        P = random_profile(rng, m, n)
        N = pairwise_counts(P, m)
        T = majority_tournament(P, m)
        opt = min(kemeny_cost(N, r) for r in permutations(range(m)))
        dist = output_distribution(T, list(range(m)))
        e_kwik = sum(p * kemeny_cost(N, r) for r, p in dist.items())
        assert e_kwik <= 2 * opt
        pick = [kemeny_cost(N, v) for v in P]
        assert Fraction(sum(pick), n) <= 2 * opt
        e_best = sum(p * min(kemeny_cost(N, r), c) for r, p in dist.items() for c in pick) / n
        assert e_best <= Fraction(11, 7) * opt
        best_ballot = min(pick)
        e_ours = sum(p * min(kemeny_cost(N, r), best_ballot) for r, p in dist.items())
        assert e_ours <= e_best


def test_larger_input():
    rng = random.Random(6)
    m, n = 100, 9
    P = random_profile(rng, m, n)
    N = pairwise_counts(P, m)
    r = kwiksort_aggregate(P, m, seed=2)
    assert sorted(r) == list(range(m))
    assert kemeny_cost(N, r) <= min(kemeny_cost(N, v) for v in P)
