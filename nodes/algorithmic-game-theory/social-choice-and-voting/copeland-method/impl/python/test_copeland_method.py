# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/copeland-method/. The authors are listed in prov/D4PRR4.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from agtprefs import (all_profiles, check_anonymity, check_condorcet_consistency,
                      check_monotonicity, check_neutrality, check_pareto, condorcet_winner,
                      find_manipulation, margins, pairwise, prefers, random_profile)
from copeland_method import (copeland, copeland_alpha_scores, copeland_ranking, copeland_scores,
                             copeland_winners, pairwise_counts)

A, B, C, D = 0, 1, 2, 3

# The worked example of the page: three voters and the cycle a > b > d > a.
EXAMPLE = ((D, A, B, C), (A, B, C, D), (B, C, D, A))


def smith_set(P, m):
    """The smallest set whose members all beat every outsider, by brute force over subsets."""
    M = margins(P, m)
    for size in range(1, m + 1):
        for S in combinations(range(m), size):
            if all(M[a][b] > 0 for a in S for b in range(m) if b not in S):
                return frozenset(S)
    return frozenset()


def samples(seed, m, n, count):
    rng = random.Random(seed)
    return [random_profile(rng, m, n) for _ in range(count)]


def test_example():
    assert pairwise_counts(EXAMPLE, 4) == [[0, 2, 2, 1], [1, 0, 3, 2], [1, 0, 0, 2], [2, 1, 1, 0]]
    assert copeland_scores(EXAMPLE, 4) == [1, 1, -1, -1]
    assert copeland_winners(EXAMPLE, 4) == frozenset({A, B})
    assert copeland(EXAMPLE, 4) == A
    assert copeland_ranking(EXAMPLE, 4) == (A, B, C, D)
    assert condorcet_winner(EXAMPLE, 4) is None
    assert smith_set(EXAMPLE, 4) == frozenset({A, B, C, D})


def test_condorcet_cycle_ties_everyone():
    cycle = ((A, B, C), (B, C, A), (C, A, B))
    assert copeland_scores(cycle, 3) == [0, 0, 0]
    assert copeland_winners(cycle, 3) == frozenset({A, B, C})
    assert copeland(cycle, 3) == A


def test_edge_cases():
    assert copeland((), 1) == 0
    assert copeland_winners((), 3) == frozenset({0, 1, 2})
    assert copeland(((2, 0, 1),), 3) == 2
    assert copeland(((0, 1), (1, 0)), 2) == 0
    assert copeland_winners(((0, 1), (1, 0)), 2) == frozenset({0, 1})


def test_scores_match_definition():
    rng = random.Random(1)
    for _ in range(300):
        m, n = rng.randint(1, 6), rng.randint(0, 7)
        P = random_profile(rng, m, n)
        assert pairwise_counts(P, m) == pairwise(P, m)
        M = margins(P, m)
        s = copeland_scores(P, m)
        for a in range(m):
            wins = sum(1 for b in range(m) if M[a][b] > 0)
            losses = sum(1 for b in range(m) if M[a][b] < 0)
            assert s[a] == wins - losses
        assert sum(s) == 0
        half = copeland_alpha_scores(P, m, Fraction(1, 2))
        for a in range(m):
            assert 2 * half[a] == m - 1 + s[a]
        r = copeland_ranking(P, m)
        assert sorted(r) == list(range(m))
        assert r[0] == copeland(P, m)
        assert all(s[r[i]] >= s[r[i + 1]] for i in range(m - 1))


def test_smith_members_outscore_outsiders():
    rng = random.Random(2)
    for _ in range(400):
        m, n = rng.randint(2, 6), rng.randint(1, 7)
        P = random_profile(rng, m, n)
        S = smith_set(P, m)
        for alpha in (Fraction(0), Fraction(1, 2), Fraction(1)):
            t = copeland_alpha_scores(P, m, alpha)
            assert all(t[a] > t[b] for a in S for b in range(m) if b not in S)
        assert copeland_winners(P, m) <= S


def test_axioms_on_full_domains():
    for m, n in ((2, 3), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2)):
        assert check_anonymity(copeland_winners, m, n) is None
        assert check_neutrality(copeland_winners, m, n) is None
        assert check_pareto(copeland_winners, m, n) is None
        assert check_condorcet_consistency(copeland_winners, m, n) is None
        assert check_monotonicity(copeland_winners, m, n) is None
        assert check_monotonicity(copeland, m, n) is None


def test_axioms_on_random_profiles():
    for m, n, seed in ((4, 5, 3), (5, 4, 4), (6, 7, 5)):
        Ps = samples(seed, m, n, 150)
        assert check_anonymity(copeland_winners, m, n, Ps) is None
        assert check_neutrality(copeland_winners, m, n, Ps) is None
        assert check_pareto(copeland_winners, m, n, Ps) is None
        assert check_condorcet_consistency(copeland, m, n, Ps) is None
        assert check_monotonicity(copeland_winners, m, n, Ps) is None


def test_resolute_rule_is_not_neutral():
    P = ((A, B), (B, A))
    assert copeland(P, 2) == A
    assert copeland(((B, A), (A, B)), 2) == A
    assert check_neutrality(copeland, 2, 2) is not None


def test_manipulation_exists():
    found = find_manipulation(copeland, 3, 3)
    assert found is not None
    P, i, s = found
    Q = P[:i] + (s,) + P[i + 1:]
    assert prefers(P[i], copeland(Q, 3), copeland(P, 3))


def test_large_input():
    rng = random.Random(6)
    P = random_profile(rng, 40, 31)
    s = copeland_scores(P, 40)
    assert sum(s) == 0
    assert copeland(P, 40) in copeland_winners(P, 40)
    assert sum(1 for _ in all_profiles(2, 2)) == 4
