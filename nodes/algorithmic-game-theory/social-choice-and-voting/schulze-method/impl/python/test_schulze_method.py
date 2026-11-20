# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schulze-method/. The authors are listed in prov/PFHMFN.jsonl.

import random
from itertools import combinations, permutations

from agtprefs import (check_anonymity, check_condorcet_consistency, check_monotonicity,
                      check_neutrality, check_pareto, condorcet_winner, find_manipulation, margins,
                      pairwise, prefers, random_profile)
from schulze_method import margin_matrix, schulze, schulze_ranking, schulze_winners, strongest_paths

A, B, C, D = 0, 1, 2, 3

# The worked example of the page: 26 voters in four groups.
EXAMPLE = ((A, B, C, D),) * 3 + ((C, D, A, B),) * 6 + ((B, C, D, A),) * 11 + ((C, A, B, D),) * 6


def smith_set(P, m):
    M = margins(P, m)
    for size in range(1, m + 1):
        for S in combinations(range(m), size):
            if all(M[a][b] > 0 for a in S for b in range(m) if b not in S):
                return frozenset(S)
    return frozenset()


def brute_paths(weight, m):
    """Strongest paths by trying every simple path; weight[a][b] is 0 when there is no link."""
    p = [[0] * m for _ in range(m)]
    for a in range(m):
        for b in range(m):
            if a == b:
                continue
            others = [c for c in range(m) if c not in (a, b)]
            for k in range(len(others) + 1):
                for mid in permutations(others, k):
                    path = (a,) + mid + (b,)
                    s = min(weight[path[i]][path[i + 1]] for i in range(len(path) - 1))
                    p[a][b] = max(p[a][b], s)
    return p


def winning_votes_winners(P, m):
    N = pairwise(P, m)
    w = [[N[a][b] if N[a][b] > N[b][a] else 0 for b in range(m)] for a in range(m)]
    p = brute_paths(w, m)
    return frozenset(a for a in range(m) if all(p[a][b] >= p[b][a] for b in range(m) if b != a))


def test_example():
    M = margin_matrix(EXAMPLE, 4)
    assert M[A][B] == 4 and M[C][A] == 20 and M[D][A] == 8
    assert M[B][C] == 2 and M[B][D] == 14 and M[C][D] == 26
    assert condorcet_winner(EXAMPLE, 4) is None
    p = strongest_paths(EXAMPLE, 4)
    assert [p[A][B], p[A][C], p[A][D]] == [4, 2, 4]
    assert [p[B][A], p[B][C], p[B][D]] == [8, 2, 14]
    assert [p[C][A], p[C][B], p[C][D]] == [20, 4, 26]
    assert [p[D][A], p[D][B], p[D][C]] == [8, 4, 2]
    assert schulze_winners(EXAMPLE, 4) == frozenset({C})
    assert schulze(EXAMPLE, 4) == C
    assert schulze_ranking(EXAMPLE, 4) == (C, B, D, A)


def test_edge_cases():
    assert schulze((), 1) == 0
    assert schulze_winners((), 3) == frozenset({0, 1, 2})
    assert schulze(((2, 0, 1),), 3) == 2
    cycle = ((A, B, C), (B, C, A), (C, A, B))
    assert schulze_winners(cycle, 3) == frozenset({A, B, C})
    assert schulze_ranking(cycle, 3) == (A, B, C)


def test_matches_brute_force_paths():
    rng = random.Random(1)
    for _ in range(200):
        m, n = rng.randint(1, 5), rng.randint(0, 9)
        P = random_profile(rng, m, n)
        M = margin_matrix(P, m)
        assert M == margins(P, m)
        d = [[M[a][b] if M[a][b] > 0 else 0 for b in range(m)] for a in range(m)]
        p = strongest_paths(P, m)
        q = brute_paths(d, m)
        assert all(p[a][b] == q[a][b] for a in range(m) for b in range(m) if a != b)
        assert schulze_winners(P, m) == winning_votes_winners(P, m)


def test_relation_is_transitive_and_has_winners():
    rng = random.Random(2)
    for _ in range(400):
        m, n = rng.randint(1, 7), rng.randint(0, 9)
        P = random_profile(rng, m, n)
        p = strongest_paths(P, m)

        def beats(a, b):
            return p[a][b] > p[b][a]

        for a in range(m):
            for b in range(m):
                for c in range(m):
                    if len({a, b, c}) == 3 and beats(a, b) and beats(b, c):
                        assert beats(a, c)
        W = schulze_winners(P, m)
        assert W
        assert W <= smith_set(P, m)
        r = schulze_ranking(P, m)
        assert sorted(r) == list(range(m))
        assert r[0] == schulze(P, m)
        for i in range(m):
            for j in range(i + 1, m):
                assert not beats(r[j], r[i])


def test_axioms_on_full_domains():
    for m, n in ((2, 3), (3, 1), (3, 2), (3, 3), (3, 4), (4, 1), (4, 2)):
        assert check_anonymity(schulze_winners, m, n) is None
        assert check_neutrality(schulze_winners, m, n) is None
        assert check_pareto(schulze_winners, m, n) is None
        assert check_condorcet_consistency(schulze_winners, m, n) is None
        assert check_monotonicity(schulze_winners, m, n) is None
        assert check_monotonicity(schulze, m, n) is None


def test_axioms_on_random_profiles():
    for m, n, seed in ((4, 5, 3), (5, 6, 4), (6, 7, 5)):
        rng = random.Random(seed)
        Ps = [random_profile(rng, m, n) for _ in range(120)]
        assert check_anonymity(schulze_winners, m, n, Ps) is None
        assert check_neutrality(schulze_winners, m, n, Ps) is None
        assert check_pareto(schulze_winners, m, n, Ps) is None
        assert check_condorcet_consistency(schulze_winners, m, n, Ps) is None
        assert check_monotonicity(schulze_winners, m, n, Ps) is None


def test_resolute_rule_is_not_neutral():
    assert schulze(((A, B), (B, A)), 2) == A
    assert check_neutrality(schulze, 2, 2) is not None


def test_manipulation_exists():
    found = find_manipulation(schulze, 3, 3)
    assert found is not None
    P, i, s = found
    Q = P[:i] + (s,) + P[i + 1:]
    assert prefers(P[i], schulze(Q, 3), schulze(P, 3))


def test_large_input():
    rng = random.Random(7)
    P = random_profile(rng, 40, 25)
    p = strongest_paths(P, 40)
    W = schulze_winners(P, 40)
    assert W
    for a in W:
        assert all(p[a][b] >= p[b][a] for b in range(40) if b != a)
    assert schulze_ranking(P, 40)[0] == schulze(P, 40)
