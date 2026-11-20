# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dodgson-rule/. The authors are listed in prov/81D8GC.jsonl.

import random
from collections import deque

from agtprefs import (check_anonymity, check_condorcet_consistency, check_neutrality, check_pareto,
                      condorcet_winner, find_manipulation, pairwise, prefers, random_profile)
from dodgson_rule import dodgson, dodgson_score, dodgson_scores, dodgson_winners, pairwise_counts

A, B, C, D = 0, 1, 2, 3

# The worked example of the page: 7 voters, 4 candidates, no Condorcet winner.
EXAMPLE = ((D, A, B, C), (D, A, B, C), (B, C, D, A), (C, D, B, A), (D, A, C, B), (A, B, C, D),
           (C, D, A, B))


def swap_distance(P, m, c):
    """The Dodgson score by breadth-first search over all profiles one adjacent swap apart."""
    start = tuple(tuple(r) for r in P)
    dist = {start: 0}
    queue = deque([start])
    while queue:
        Q = queue.popleft()
        if condorcet_winner(Q, m) == c:
            return dist[Q]
        for i, r in enumerate(Q):
            for j in range(m - 1):
                s = list(r)
                s[j], s[j + 1] = s[j + 1], s[j]
                R = Q[:i] + (tuple(s),) + Q[i + 1:]
                if R not in dist:
                    dist[R] = dist[Q] + 1
                    queue.append(R)
    return None


def test_example():
    N = pairwise_counts(EXAMPLE, 4)
    assert N == pairwise(EXAMPLE, 4)
    assert N[D][A] == 6 and N[D][B] == 5 and N[C][D] == 4
    assert N[A][B] == 5 and N[A][C] == 4 and N[B][C] == 4
    assert condorcet_winner(EXAMPLE, 4) is None
    assert dodgson_scores(EXAMPLE, 4) == [3, 4, 2, 1]
    assert dodgson_winners(EXAMPLE, 4) == frozenset({D})
    assert dodgson(EXAMPLE, 4) == D


def test_edge_cases():
    assert dodgson_score((), 1, 0) == 0
    assert dodgson_score((), 3, 1) is None
    assert dodgson_winners((), 3) == frozenset({0, 1, 2})
    assert dodgson_scores(((2, 0, 1),), 3) == [1, 2, 0]
    cycle = ((A, B, C), (B, C, A), (C, A, B))
    assert dodgson_scores(cycle, 3) == [1, 1, 1]
    assert dodgson(cycle, 3) == A


def test_matches_breadth_first_search():
    rng = random.Random(1)
    for _ in range(60):
        m = rng.randint(2, 4)
        n = rng.randint(1, 2 if m == 4 else 3)
        P = random_profile(rng, m, n)
        for c in range(m):
            assert dodgson_score(P, m, c) == swap_distance(P, m, c)


def test_condorcet_winner_has_score_zero():
    rng = random.Random(2)
    for _ in range(150):
        m, n = rng.randint(2, 5), rng.randint(1, 9)
        P = random_profile(rng, m, n)
        s = dodgson_scores(P, m)
        w = condorcet_winner(P, m)
        assert (w is not None) == (0 in s)
        if w is not None:
            assert s[w] == 0 and dodgson_winners(P, m) == frozenset({w})


def test_axioms_on_full_domains():
    for m, n in ((2, 3), (3, 1), (3, 2), (3, 3), (4, 1)):
        assert check_anonymity(dodgson_winners, m, n) is None
        assert check_neutrality(dodgson_winners, m, n) is None
        assert check_pareto(dodgson_winners, m, n) is None
        assert check_condorcet_consistency(dodgson_winners, m, n) is None


def test_axioms_on_random_profiles():
    for m, n, seed in ((4, 5, 3), (5, 5, 4)):
        rng = random.Random(seed)
        Ps = [random_profile(rng, m, n) for _ in range(25)]
        assert check_anonymity(dodgson_winners, m, n, Ps) is None
        assert check_neutrality(dodgson_winners, m, n, Ps) is None
        assert check_pareto(dodgson_winners, m, n, Ps) is None
        assert check_condorcet_consistency(dodgson_winners, m, n, Ps) is None


def test_pareto_score_gap():
    rng = random.Random(6)
    for _ in range(300):
        m, n = rng.randint(2, 5), rng.randint(1, 7)
        P = random_profile(rng, m, n)
        s = dodgson_scores(P, m)
        for a in range(m):
            for b in range(m):
                if a != b and all(prefers(r, a, b) for r in P):
                    assert s[a] < s[b]


def test_not_homogeneous():
    P = ((A, D, C, B), (A, D, C, B), (C, D, B, A), (D, B, A, C), (B, A, D, C), (B, A, C, D),
         (C, B, A, D))
    assert dodgson_scores(P, 4) == [2, 2, 3, 2]
    assert dodgson_winners(P, 4) == frozenset({A, B, D})
    assert dodgson_scores(P * 3, 4) == [5, 4, 7, 5]
    assert dodgson_winners(P * 3, 4) == frozenset({B})


def test_resolute_rule_is_not_neutral():
    assert dodgson(((A, B), (B, A)), 2) == A
    assert check_neutrality(dodgson, 2, 2) is not None


def test_manipulation_exists():
    found = find_manipulation(dodgson, 3, 3)
    assert found is not None
    P, i, s = found
    Q = P[:i] + (s,) + P[i + 1:]
    assert prefers(P[i], dodgson(Q, 3), dodgson(P, 3))


def test_larger_input():
    rng = random.Random(7)
    P = random_profile(rng, 6, 15)
    s = dodgson_scores(P, 6)
    assert all(x is not None and x >= 0 for x in s)
    w = dodgson(P, 6)
    assert s[w] == min(s)
    assert s[w] <= 6 * 15
