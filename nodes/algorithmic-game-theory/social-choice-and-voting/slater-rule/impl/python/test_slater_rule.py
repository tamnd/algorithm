# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slater-rule/. The authors are listed in prov/DWARFM.jsonl.

import random
from itertools import combinations, permutations

from agtprefs import (check_anonymity, check_condorcet_consistency, check_monotonicity,
                      check_neutrality, check_pareto, condorcet_winner, find_manipulation,
                      kendall_tau, margins, prefers, random_profile)
from slater_rule import margin_matrix, slater, slater_cost, slater_ranking, slater_winners

A, B, C, D = 0, 1, 2, 3

# The worked example of the page: 13 voters in three groups.
EXAMPLE = ((D, B, C, A),) * 4 + ((B, A, D, C),) * 6 + ((C, A, D, B),) * 3


def kemeny_cost(P, r):
    return sum(kendall_tau(r, v) for v in P)


def test_example():
    M = margin_matrix(EXAMPLE, 4)
    assert [M[B][A], M[C][A], M[A][D], M[B][C], M[D][B], M[D][C]] == [7, 1, 5, 7, 1, 7]
    assert condorcet_winner(EXAMPLE, 4) is None
    assert smith_set(EXAMPLE, 4) == frozenset({A, B, C, D})
    best, opt = brute_force(EXAMPLE, 4)
    assert best == 1 and opt == [(D, B, C, A)]
    assert slater_ranking(EXAMPLE, 4) == (D, B, C, A)
    assert slater_winners(EXAMPLE, 4) == frozenset({D})
    assert slater(EXAMPLE, 4) == D
    first = {v: min(slater_cost(EXAMPLE, 4, r) for r in permutations(range(4)) if r[0] == v)
             for v in range(4)}
    assert first == {A: 2, B: 2, C: 3, D: 1}
    # Kemeny weighs each disagreement by its margin and picks another ranking.
    k = {r: kemeny_cost(EXAMPLE, r) for r in permutations(range(4))}
    kbest = min(k.values())
    assert [r for r in k if k[r] == kbest] == [(B, A, D, C)]
    assert slater_cost(EXAMPLE, 4, (B, A, D, C)) == 2
    assert k[(D, B, C, A)] - kbest == 3


def brute_force(P, m):
    M = margins(P, m)
    costs = {r: sum(1 for i in range(m) for j in range(i + 1, m) if M[r[j]][r[i]] > 0)
             for r in permutations(range(m))}
    best = min(costs.values())
    opt = sorted(r for r in costs if costs[r] == best)
    return best, opt


def smith_set(P, m):
    M = margins(P, m)
    for size in range(1, m + 1):
        for S in combinations(range(m), size):
            if all(M[a][b] > 0 for a in S for b in range(m) if b not in S):
                return frozenset(S)
    return frozenset()


def test_matches_brute_force():
    rng = random.Random(1)
    for _ in range(100):
        m, n = rng.randint(1, 6), rng.randint(0, 7)
        P = random_profile(rng, m, n)
        assert margin_matrix(P, m) == margins(P, m)
        best, opt = brute_force(P, m)
        r = slater_ranking(P, m)
        assert r == opt[0]
        assert slater_cost(P, m, r) == best
        assert slater_winners(P, m) == frozenset(o[0] for o in opt)
        assert slater(P, m) == r[0]


def test_edge_cases():
    assert slater_ranking((), 1) == (0,)
    assert slater_ranking((), 3) == (0, 1, 2)
    assert slater_winners((), 3) == frozenset({0, 1, 2})
    assert slater_ranking(((2, 0, 1),), 3) == (2, 0, 1)
    cycle = ((A, B, C), (B, C, A), (C, A, B))
    assert slater_winners(cycle, 3) == frozenset({A, B, C})
    assert slater_ranking(cycle, 3) == (A, B, C)
    assert slater_cost(cycle, 3, (A, B, C)) == 1


def test_smith_set_on_top():
    rng = random.Random(2)
    for _ in range(100):
        m, n = rng.randint(2, 6), rng.randint(1, 7)
        P = random_profile(rng, m, n)
        S = smith_set(P, m)
        _, opt = brute_force(P, m)
        for r in opt:
            assert frozenset(r[:len(S)]) == S


def test_axioms_on_full_domains():
    for m, n in ((2, 3), (3, 1), (3, 2), (3, 3), (4, 1)):
        assert check_anonymity(slater_winners, m, n) is None
        assert check_neutrality(slater_winners, m, n) is None
        assert check_pareto(slater_winners, m, n) is None
        assert check_condorcet_consistency(slater_winners, m, n) is None
        assert check_monotonicity(slater_winners, m, n) is None


def test_axioms_on_random_profiles():
    for m, n, seed in ((5, 5, 3), (6, 7, 4)):
        rng = random.Random(seed)
        Ps = [random_profile(rng, m, n) for _ in range(15)]
        assert check_anonymity(slater_winners, m, n, Ps) is None
        assert check_neutrality(slater_winners, m, n, Ps) is None
        assert check_pareto(slater_winners, m, n, Ps) is None
        assert check_condorcet_consistency(slater_winners, m, n, Ps) is None
        assert check_monotonicity(slater_winners, m, n, Ps) is None


def test_resolute_rule_is_not_neutral():
    assert slater(((A, B), (B, A)), 2) == A
    assert check_neutrality(slater, 2, 2) is not None


def test_manipulation_exists():
    found = find_manipulation(slater, 3, 3)
    assert found is not None
    P, i, s = found
    Q = P[:i] + (s,) + P[i + 1:]
    assert prefers(P[i], slater(Q, 3), slater(P, 3))


def test_larger_input():
    rng = random.Random(7)
    m = 14
    P = random_profile(rng, m, 9)
    r = slater_ranking(P, m)
    assert sorted(r) == list(range(m))
    c = slater_cost(P, m, r)
    for i in range(m - 1):
        s = r[:i] + (r[i + 1], r[i]) + r[i + 2:]
        assert slater_cost(P, m, s) >= c
    w = condorcet_winner(P, m)
    if w is not None:
        assert r[0] == w
